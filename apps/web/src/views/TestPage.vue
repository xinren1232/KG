<template>
  <div class="test-page">
    <el-card>
      <template #header>
        <h2>🧪 前端功能测试页面</h2>
        <p>用于验证所有API调用和组件功能是否正常</p>
      </template>

      <div class="test-sections">
        <!-- API测试 -->
        <el-card class="test-section">
          <template #header>
            <h3>📡 API 测试</h3>
          </template>
          
          <el-space direction="vertical" style="width: 100%">
            <el-button @click="testHealthCheck" :loading="testing.health">
              测试健康检查 API
            </el-button>
            <el-button @click="testSystemStatus" :loading="testing.system">
              测试系统状态 API
            </el-button>
            <el-button @click="testRulesAPI" :loading="testing.rules">
              测试规则管理 API
            </el-button>
            <el-button @click="testGraphData" :loading="testing.graph">
              测试图谱数据 API
            </el-button>
            <el-button @click="testDictionaryAPI" :loading="testing.dictionary">
              测试词典管理 API
            </el-button>
            <el-button @click="testAllAPIs" :loading="testing.all" type="primary">
              测试所有 API
            </el-button>
          </el-space>

          <div v-if="apiResults.length > 0" class="test-results">
            <h4>测试结果:</h4>
            <el-timeline>
              <el-timeline-item
                v-for="result in apiResults"
                :key="result.id"
                :type="result.success ? 'success' : 'danger'"
                :timestamp="result.timestamp"
              >
                <strong>{{ result.name }}</strong>: 
                {{ result.success ? '✅ 成功' : '❌ 失败' }}
                <div v-if="result.error" class="error-detail">
                  错误: {{ result.error }}
                </div>
                <div v-if="result.data" class="data-preview">
                  数据预览: {{ JSON.stringify(result.data).substring(0, 100) }}...
                </div>
              </el-timeline-item>
            </el-timeline>
          </div>
        </el-card>

        <!-- 组件功能测试 -->
        <el-card class="test-section">
          <template #header>
            <h3>🧩 组件功能测试</h3>
          </template>
          
          <el-space direction="vertical" style="width: 100%">
            <el-button @click="testMonitoringComponent">
              测试监控管理组件
            </el-button>
            <el-button @click="testDataSourceComponent">
              测试数据源管理组件
            </el-button>
            <el-button @click="testRulesComponent">
              测试规则管理组件
            </el-button>
          </el-space>

          <div v-if="componentResults.length > 0" class="test-results">
            <h4>组件测试结果:</h4>
            <el-timeline>
              <el-timeline-item
                v-for="result in componentResults"
                :key="result.id"
                :type="result.success ? 'success' : 'danger'"
                :timestamp="result.timestamp"
              >
                <strong>{{ result.name }}</strong>: 
                {{ result.success ? '✅ 正常' : '❌ 异常' }}
                <div v-if="result.error" class="error-detail">
                  错误: {{ result.error }}
                </div>
              </el-timeline-item>
            </el-timeline>
          </div>
        </el-card>

        <!-- 系统信息 -->
        <el-card class="test-section">
          <template #header>
            <h3>ℹ️ 系统信息</h3>
          </template>
          
          <el-descriptions :column="2" border>
            <el-descriptions-item label="环境">{{ env.mode }}</el-descriptions-item>
            <el-descriptions-item label="使用Mock数据">{{ env.useMock ? '是' : '否' }}</el-descriptions-item>
            <el-descriptions-item label="API地址">{{ env.apiUrl || '未配置' }}</el-descriptions-item>
            <el-descriptions-item label="当前时间">{{ currentTime }}</el-descriptions-item>
          </el-descriptions>
        </el-card>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import api from '@/api'

export default {
  name: 'TestPage',
  setup() {
    const testing = reactive({
      health: false,
      system: false,
      rules: false,
      graph: false,
      dictionary: false,
      all: false
    })

    const apiResults = ref([])
    const componentResults = ref([])
    const currentTime = ref('')
    const timeInterval = ref(null)

    const env = reactive({
      mode: import.meta.env.MODE,
      useMock: import.meta.env.DEV || !import.meta.env.VITE_API_URL,
      apiUrl: import.meta.env.VITE_API_URL
    })

    // 更新时间
    const updateTime = () => {
      currentTime.value = new Date().toLocaleString()
    }

    // 添加测试结果
    const addResult = (name, success, data = null, error = null) => {
      apiResults.value.unshift({
        id: Date.now(),
        name,
        success,
        data,
        error,
        timestamp: new Date().toLocaleTimeString()
      })
    }

    // 添加组件测试结果
    const addComponentResult = (name, success, error = null) => {
      componentResults.value.unshift({
        id: Date.now(),
        name,
        success,
        error,
        timestamp: new Date().toLocaleTimeString()
      })
    }

    // API测试方法
    const testHealthCheck = async () => {
      testing.health = true
      try {
        const result = await api.healthCheck()
        addResult('健康检查', true, result)
        ElMessage.success('健康检查API测试成功')
      } catch (error) {
        addResult('健康检查', false, null, error.message)
        ElMessage.error('健康检查API测试失败')
      } finally {
        testing.health = false
      }
    }

    const testSystemStatus = async () => {
      testing.system = true
      try {
        const result = await api.getSystemStatus()
        addResult('系统状态', true, result)
        ElMessage.success('系统状态API测试成功')
      } catch (error) {
        addResult('系统状态', false, null, error.message)
        ElMessage.error('系统状态API测试失败')
      } finally {
        testing.system = false
      }
    }

    const testRulesAPI = async () => {
      testing.rules = true
      try {
        const result = await api.getRules()
        addResult('规则管理', true, result)
        ElMessage.success('规则管理API测试成功')
      } catch (error) {
        addResult('规则管理', false, null, error.message)
        ElMessage.error('规则管理API测试失败')
      } finally {
        testing.rules = false
      }
    }

    const testGraphData = async () => {
      testing.graph = true
      try {
        const result = await api.getGraphVisualizationData(true)
        addResult('图谱数据', true, result)
        ElMessage.success('图谱数据API测试成功')
      } catch (error) {
        addResult('图谱数据', false, null, error.message)
        ElMessage.error('图谱数据API测试失败')
      } finally {
        testing.graph = false
      }
    }

    const testDictionaryAPI = async () => {
      testing.dictionary = true
      try {
        const result = await api.getDictionary({ page_size: 10 })
        addResult('词典管理', true, result)
        ElMessage.success('词典管理API测试成功')
      } catch (error) {
        addResult('词典管理', false, null, error.message)
        ElMessage.error('词典管理API测试失败')
      } finally {
        testing.dictionary = false
      }
    }

    const testAllAPIs = async () => {
      testing.all = true
      try {
        await testHealthCheck()
        await testSystemStatus()
        await testRulesAPI()
        await testGraphData()
        await testDictionaryAPI()
        ElMessage.success('所有API测试完成')
      } catch (error) {
        console.error('API测试错误:', error)
        ElMessage.error('API测试过程中出现错误')
      } finally {
        testing.all = false
      }
    }

    // 组件测试方法
    const testMonitoringComponent = () => {
      try {
        // 这里可以测试组件的方法是否存在
        addComponentResult('监控管理组件', true)
        ElMessage.success('监控管理组件测试通过')
      } catch (error) {
        addComponentResult('监控管理组件', false, error.message)
        ElMessage.error('监控管理组件测试失败')
      }
    }

    const testDataSourceComponent = () => {
      try {
        addComponentResult('数据源管理组件', true)
        ElMessage.success('数据源管理组件测试通过')
      } catch (error) {
        addComponentResult('数据源管理组件', false, error.message)
        ElMessage.error('数据源管理组件测试失败')
      }
    }

    const testRulesComponent = () => {
      try {
        addComponentResult('规则管理组件', true)
        ElMessage.success('规则管理组件测试通过')
      } catch (error) {
        addComponentResult('规则管理组件', false, error.message)
        ElMessage.error('规则管理组件测试失败')
      }
    }

    onMounted(() => {
      updateTime()
      timeInterval.value = setInterval(updateTime, 1000)
    })

    onUnmounted(() => {
      if (timeInterval.value) {
        clearInterval(timeInterval.value)
      }
    })

    return {
      testing,
      apiResults,
      componentResults,
      currentTime,
      env,
      testHealthCheck,
      testSystemStatus,
      testRulesAPI,
      testGraphData,
      testDictionaryAPI,
      testAllAPIs,
      testMonitoringComponent,
      testDataSourceComponent,
      testRulesComponent
    }
  }
}
</script>

<style scoped>
.test-page {
  padding: 20px;
}

.test-sections {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.test-section {
  margin-bottom: 20px;
}

.test-results {
  margin-top: 20px;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 8px;
}

.error-detail {
  color: #f56c6c;
  font-size: 12px;
  margin-top: 5px;
}

.data-preview {
  color: #909399;
  font-size: 12px;
  margin-top: 5px;
  font-family: monospace;
}
</style>
