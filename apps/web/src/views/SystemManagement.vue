<template>
  <div class="system-management">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">
          <el-icon><Setting /></el-icon>
          系统管理中心
        </h1>
        <p class="page-description">统一管理系统版本、规则、Prompt、场景和配置信息</p>
      </div>
      <div class="header-actions">
        <el-button type="primary" @click="refreshAllData">
          <el-icon><Refresh /></el-icon>
          刷新数据
        </el-button>
        <el-button @click="exportConfig">
          <el-icon><Download /></el-icon>
          导出配置
        </el-button>
        <el-button type="success" @click="showVersionDialog">
          <el-icon><Clock /></el-icon>
          版本发布
        </el-button>
      </div>
    </div>

    <!-- 系统概览仪表板 -->
    <div class="dashboard-overview">
      <el-row :gutter="20">
        <el-col :span="4">
          <div class="stat-card">
            <div class="stat-icon version">
              <el-icon><Clock /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ systemStatus.currentVersion }}</div>
              <div class="stat-label">当前版本</div>
            </div>
          </div>
        </el-col>
        <el-col :span="4">
          <div class="stat-card">
            <div class="stat-icon rules">
              <el-icon><Collection /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ systemStatus.totalNodes || 0 }}</div>
              <div class="stat-label">图谱节点</div>
            </div>
          </div>
        </el-col>
        <el-col :span="4">
          <div class="stat-card">
            <div class="stat-icon prompts">
              <el-icon><Share /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ systemStatus.totalRelations || 0 }}</div>
              <div class="stat-label">图谱关系</div>
            </div>
          </div>
        </el-col>
        <el-col :span="4">
          <div class="stat-card">
            <div class="stat-icon scenarios">
              <el-icon><DocumentChecked /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ systemStatus.totalTerms || 0 }}</div>
              <div class="stat-label">术语总数</div>
            </div>
          </div>
        </el-col>
        <el-col :span="4">
          <div class="stat-card">
            <div class="stat-icon datasources">
              <el-icon><FolderOpened /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ systemStatus.totalCategories || 0 }}</div>
              <div class="stat-label">分类数量</div>
            </div>
          </div>
        </el-col>
        <el-col :span="4">
          <div class="stat-card">
            <div class="stat-icon monitoring">
              <el-icon><Monitor /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ systemStatus.systemHealth }}%</div>
              <div class="stat-label">系统健康度</div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 功能模块导航 -->
    <div class="module-navigation">
      <el-tabs v-model="activeTab" type="card" @tab-change="handleTabChange">
        <el-tab-pane label="规则管理" name="rules">
          <template #label>
            <span class="tab-label">
              <el-icon><DocumentChecked /></el-icon>
              规则管理
            </span>
          </template>
        </el-tab-pane>
        
        <el-tab-pane label="Prompt管理" name="prompts">
          <template #label>
            <span class="tab-label">
              <el-icon><ChatDotRound /></el-icon>
              Prompt管理
            </span>
          </template>
        </el-tab-pane>
        
        <el-tab-pane label="场景管理" name="scenarios">
          <template #label>
            <span class="tab-label">
              <el-icon><Operation /></el-icon>
              场景管理
            </span>
          </template>
        </el-tab-pane>
        
        <el-tab-pane label="版本管理" name="versions">
          <template #label>
            <span class="tab-label">
              <el-icon><FolderOpened /></el-icon>
              版本管理
            </span>
          </template>
        </el-tab-pane>
        
        <el-tab-pane label="文档抽取" name="extraction">
          <template #label>
            <span class="tab-label">
              <el-icon><Document /></el-icon>
              文档抽取逻辑
            </span>
          </template>
        </el-tab-pane>
        
        <el-tab-pane label="Agent设计" name="agents">
          <template #label>
            <span class="tab-label">
              <el-icon><Avatar /></el-icon>
              Agent设计
            </span>
          </template>
        </el-tab-pane>

        <el-tab-pane label="数据源管理" name="datasources">
          <template #label>
            <span class="tab-label">
              <el-icon><Coin /></el-icon>
              数据源管理
            </span>
          </template>
        </el-tab-pane>

        <el-tab-pane label="监控告警" name="monitoring">
          <template #label>
            <span class="tab-label">
              <el-icon><Monitor /></el-icon>
              监控告警
            </span>
          </template>
        </el-tab-pane>

        <el-tab-pane label="词典Schema" name="dictionary-schema">
          <template #label>
            <span class="tab-label">
              <el-icon><Collection /></el-icon>
              词典Schema
            </span>
          </template>
        </el-tab-pane>

        <el-tab-pane label="图谱Schema" name="graph-schema">
          <template #label>
            <span class="tab-label">
              <el-icon><Share /></el-icon>
              图谱Schema
            </span>
          </template>
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- 内容区域 -->
    <div class="content-area">
      <!-- 规则管理 -->
      <div v-show="activeTab === 'rules'" class="module-content">
        <RulesManagement ref="rulesRef" />
      </div>

      <!-- Prompt管理 -->
      <div v-show="activeTab === 'prompts'" class="module-content">
        <PromptsManagement ref="promptsRef" />
      </div>

      <!-- 场景管理 -->
      <div v-show="activeTab === 'scenarios'" class="module-content">
        <ScenariosManagement ref="scenariosRef" />
      </div>

      <!-- 版本管理 -->
      <div v-show="activeTab === 'versions'" class="module-content">
        <VersionsManagement ref="versionsRef" />
      </div>

      <!-- 文档抽取逻辑 -->
      <div v-show="activeTab === 'extraction'" class="module-content">
        <ExtractionManagement ref="extractionRef" />
      </div>

      <!-- Agent设计管理 -->
      <div v-show="activeTab === 'agents'" class="module-content">
        <AgentsManagement ref="agentsRef" />
      </div>

      <!-- 数据源管理 -->
      <div v-show="activeTab === 'datasources'" class="module-content">
        <DataSourceManagement ref="dataSourceRef" />
      </div>

      <!-- 监控告警 -->
      <div v-show="activeTab === 'monitoring'" class="module-content">
        <MonitoringManagement ref="monitoringRef" />
      </div>

      <!-- 词典Schema -->
      <div v-show="activeTab === 'dictionary-schema'" class="module-content">
        <DictionarySchema ref="dictionarySchemaRef" />
      </div>

      <!-- 图谱Schema -->
      <div v-show="activeTab === 'graph-schema'" class="module-content">
        <GraphSchema ref="graphSchemaRef" />
      </div>
    </div>

    <!-- 版本发布对话框 -->
    <el-dialog
      v-model="versionDialogVisible"
      title="版本发布"
      width="600px"
      @close="resetVersionForm"
    >
      <el-form :model="versionForm" :rules="versionRules" ref="versionFormRef" label-width="100px">
        <el-form-item label="版本号" prop="version">
          <el-input v-model="versionForm.version" placeholder="如: v1.3.0" />
        </el-form-item>
        <el-form-item label="版本类型" prop="type">
          <el-select v-model="versionForm.type" placeholder="请选择版本类型">
            <el-option label="主版本 (Major)" value="major" />
            <el-option label="次版本 (Minor)" value="minor" />
            <el-option label="补丁版本 (Patch)" value="patch" />
          </el-select>
        </el-form-item>
        <el-form-item label="版本描述" prop="description">
          <el-input
            v-model="versionForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入版本描述"
          />
        </el-form-item>
        <el-form-item label="变更内容">
          <div class="changes-list">
            <div v-for="(change, index) in versionForm.changes" :key="index" class="change-item">
              <el-input v-model="change.description" placeholder="变更描述" />
              <el-select v-model="change.type" placeholder="类型" style="width: 120px; margin-left: 10px;">
                <el-option label="新功能" value="feature" />
                <el-option label="修复" value="fix" />
                <el-option label="优化" value="improvement" />
                <el-option label="重构" value="refactor" />
              </el-select>
              <el-button type="danger" size="small" @click="removeChange(index)" style="margin-left: 10px;">
                删除
              </el-button>
            </div>
            <el-button type="primary" size="small" @click="addChange">添加变更</el-button>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="versionDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="publishVersion" :loading="publishing">
            发布版本
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted, nextTick } from 'vue'
import {
  Setting,
  Refresh,
  Download,
  DocumentChecked,
  ChatDotRound,
  Operation,
  FolderOpened,
  Document,
  Avatar,
  Clock,
  Coin,
  Monitor,
  Collection,
  Share
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import api from '@/api'

// 导入子组件
import RulesManagement from '@/components/system/RulesManagement.vue'
import PromptsManagement from '@/components/system/PromptsManagement.vue'
import ScenariosManagement from '@/components/system/ScenariosManagement.vue'
import VersionsManagement from '@/components/system/VersionsManagement.vue'
import ExtractionManagement from '@/components/system/ExtractionManagement.vue'
import AgentsManagement from '@/components/system/AgentsManagement.vue'
import DataSourceManagement from '@/components/system/DataSourceManagement.vue'
import MonitoringManagement from '@/components/system/MonitoringManagement.vue'
import DictionarySchema from '@/components/system/DictionarySchema.vue'
import GraphSchema from '@/components/system/GraphSchema.vue'

export default {
  name: 'SystemManagement',
  components: {
    Setting,
    Refresh,
    Download,
    DocumentChecked,
    ChatDotRound,
    Operation,
    FolderOpened,
    Document,
    Avatar,
    Clock,
    Coin,
    Monitor,
    Collection,
    Share,
    RulesManagement,
    PromptsManagement,
    ScenariosManagement,
    VersionsManagement,
    ExtractionManagement,
    AgentsManagement,
    DataSourceManagement,
    MonitoringManagement,
    DictionarySchema,
    GraphSchema
  },
  setup() {
    // 响应式数据
    const activeTab = ref('versions')
    const loading = ref(false)
    const versionDialogVisible = ref(false)
    const publishing = ref(false)

    // 系统状态
    const systemStatus = reactive({
      currentVersion: 'v1.2.0',
      totalRules: 12,
      totalPrompts: 8,
      totalScenarios: 6,
      totalVersions: 5,
      totalExtractionLogics: 4,
      totalAgents: 3,
      totalDataSources: 7,
      systemHealth: 95
    })

    // 版本表单
    const versionForm = reactive({
      version: '',
      type: 'minor',
      description: '',
      changes: []
    })

    const versionRules = {
      version: [{ required: true, message: '请输入版本号', trigger: 'blur' }],
      type: [{ required: true, message: '请选择版本类型', trigger: 'change' }],
      description: [{ required: true, message: '请输入版本描述', trigger: 'blur' }]
    }

    // 组件引用
    const rulesRef = ref(null)
    const promptsRef = ref(null)
    const scenariosRef = ref(null)
    const versionsRef = ref(null)
    const extractionRef = ref(null)
    const agentsRef = ref(null)
    const dataSourceRef = ref(null)
    const monitoringRef = ref(null)
    const dictionarySchemaRef = ref(null)
    const graphSchemaRef = ref(null)
    const versionFormRef = ref(null)

    // 方法
    const handleTabChange = async (tabName) => {
      console.log('切换到标签页:', tabName)

      // 当切换到词典Schema或图谱Schema标签页时，延迟渲染图表
      // 使用 nextTick 确保 DOM 已经显示
      await nextTick()

      if (tabName === 'dictionary-schema' && dictionarySchemaRef.value?.renderCharts) {
        setTimeout(() => {
          dictionarySchemaRef.value.renderCharts()
        }, 100)
      } else if (tabName === 'graph-schema' && graphSchemaRef.value?.renderSchemaChart) {
        setTimeout(() => {
          graphSchemaRef.value.renderSchemaChart()
        }, 100)
      }
    }

    const refreshAllData = async () => {
      loading.value = true
      try {
        // 刷新所有模块的数据
        const promises = []

        if (rulesRef.value?.refreshData) {
          promises.push(rulesRef.value.refreshData())
        }
        if (promptsRef.value?.refreshData) {
          promises.push(promptsRef.value.refreshData())
        }
        if (scenariosRef.value?.refreshData) {
          promises.push(scenariosRef.value.refreshData())
        }
        if (versionsRef.value?.refreshData) {
          promises.push(versionsRef.value.refreshData())
        }
        if (extractionRef.value?.refreshData) {
          promises.push(extractionRef.value.refreshData())
        }
        if (agentsRef.value?.refreshData) {
          promises.push(agentsRef.value.refreshData())
        }
        if (dataSourceRef.value?.refreshData) {
          promises.push(dataSourceRef.value.refreshData())
        }
        if (monitoringRef.value?.refreshData) {
          promises.push(monitoringRef.value.refreshData())
        }
        if (dictionarySchemaRef.value?.refreshData) {
          promises.push(dictionarySchemaRef.value.refreshData())
        }
        if (graphSchemaRef.value?.refreshData) {
          promises.push(graphSchemaRef.value.refreshData())
        }

        await Promise.all(promises)

        ElMessage.success('数据刷新成功')
      } catch (error) {
        console.error('刷新数据失败:', error)
        ElMessage.error('数据刷新失败')
      } finally {
        loading.value = false
      }
    }

    // 版本管理相关方法
    const showVersionDialog = () => {
      versionDialogVisible.value = true
      resetVersionForm()
    }

    const resetVersionForm = () => {
      Object.assign(versionForm, {
        version: '',
        type: 'minor',
        description: '',
        changes: []
      })
      versionFormRef.value?.resetFields()
    }

    const addChange = () => {
      versionForm.changes.push({
        type: 'feature',
        description: ''
      })
    }

    const removeChange = (index) => {
      versionForm.changes.splice(index, 1)
    }

    const publishVersion = async () => {
      if (!versionFormRef.value) return

      try {
        await versionFormRef.value?.validate()
        publishing.value = true

        const response = await api.publishVersion(versionForm)
        if (response.success) {
          ElMessage.success('版本发布成功')
          versionDialogVisible.value = false
          systemStatus.currentVersion = versionForm.version
          await refreshAllData()
        } else {
          ElMessage.error(response.message || '版本发布失败')
        }
      } catch (error) {
        console.error('版本发布失败:', error)
        ElMessage.error('版本发布失败')
      } finally {
        publishing.value = false
      }
    }

    const exportConfig = () => {
      try {
        const configData = {
          systemStatus: systemStatus,
          rules: rules.value,
          prompts: prompts.value,
          scenarios: scenarios.value,
          versions: versions.value,
          extraction: extraction.value,
          agents: agents.value,
          dataSource: dataSource.value,
          monitoring: monitoring.value,
          exportTime: new Date().toISOString()
        }

        const dataStr = JSON.stringify(configData, null, 2)
        const dataBlob = new Blob([dataStr], { type: 'application/json' })
        const url = URL.createObjectURL(dataBlob)

        const link = document.createElement('a')
        link.href = url
        link.download = `system-config-${new Date().toISOString().slice(0, 10)}.json`
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        URL.revokeObjectURL(url)

        ElMessage.success('配置导出成功')
      } catch (error) {
        console.error('导出配置失败:', error)
        ElMessage.error('导出配置失败')
      }
    }

    const loadSystemStatus = async () => {
      try {
        const response = await api.getSystemStatus()
        console.log('系统状态响应:', response)
        // axios 拦截器返回完整的 response 对象，需要访问 response.data
        if (response.data && response.data.success && response.data.data) {
          Object.assign(systemStatus, response.data.data)
          console.log('系统状态已更新:', systemStatus)
        }
      } catch (error) {
        console.error('加载系统状态失败:', error)
      }
    }

    // 生命周期
    onMounted(() => {
      loadSystemStatus()
    })

    return {
      activeTab,
      loading,
      versionDialogVisible,
      publishing,
      systemStatus,
      versionForm,
      versionRules,
      rulesRef,
      promptsRef,
      scenariosRef,
      versionsRef,
      extractionRef,
      agentsRef,
      dataSourceRef,
      monitoringRef,
      dictionarySchemaRef,
      graphSchemaRef,
      versionFormRef,
      handleTabChange,
      refreshAllData,
      exportConfig,
      showVersionDialog,
      resetVersionForm,
      addChange,
      removeChange,
      publishVersion
    }
  }
}
</script>

<style scoped>
.system-management {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.header-content {
  flex: 1;
}

.page-title {
  display: flex;
  align-items: center;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 8px 0;
}

.page-title .el-icon {
  margin-right: 12px;
  color: #409EFF;
}

.page-description {
  color: #606266;
  margin: 0;
  font-size: 14px;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.dashboard-overview {
  margin-bottom: 24px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  font-size: 20px;
  color: white;
}

.stat-icon.version {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-icon.rules {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.stat-icon.prompts {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.stat-icon.scenarios {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.stat-icon.datasources {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
}

.stat-icon.monitoring {
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.module-navigation {
  margin-bottom: 24px;
}

.tab-label {
  display: flex;
  align-items: center;
  gap: 6px;
}

.content-area {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  min-height: 600px;
}

.module-content {
  padding: 24px;
}

/* 标签页样式优化 */
:deep(.el-tabs__header) {
  margin: 0;
  background: white;
  border-radius: 8px 8px 0 0;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

:deep(.el-tabs__nav) {
  border: none;
}

:deep(.el-tabs__item) {
  border: none;
  color: #606266;
  font-weight: 500;
}

:deep(.el-tabs__item.is-active) {
  color: #409EFF;
  background-color: #f0f9ff;
}

:deep(.el-tabs__content) {
  padding: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .system-management {
    padding: 12px;
  }
  
  .page-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  
  .header-actions {
    width: 100%;
    justify-content: flex-end;
  }
  
  .module-content {
    padding: 16px;
  }
}

/* 版本发布对话框样式 */
.changes-list {
  max-height: 300px;
  overflow-y: auto;
}

.change-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.change-item:last-child {
  margin-bottom: 0;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
