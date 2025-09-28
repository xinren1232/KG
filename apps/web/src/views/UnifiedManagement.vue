<template>
  <div class="unified-management">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">
          <el-icon><Setting /></el-icon>
          系统管理中心
        </h1>
        <p class="page-description">统一管理系统版本、规则、Prompt、场景和图谱规则</p>
      </div>
      <div class="header-actions">
        <el-button type="primary" @click="refreshAllData">
          <el-icon><Refresh /></el-icon>
          刷新数据
        </el-button>
        <el-button @click="exportAllConfig">
          <el-icon><Download /></el-icon>
          导出配置
        </el-button>
        <el-button @click="showVersionDialog">
          <el-icon><Clock /></el-icon>
          版本发布
        </el-button>
      </div>
    </div>

    <!-- 系统概览 -->
    <div class="system-overview">
      <el-row :gutter="20">
        <el-col :span="4">
          <el-card class="overview-card">
            <div class="overview-content">
              <div class="overview-icon">
                <el-icon><Clock /></el-icon>
              </div>
              <div class="overview-info">
                <div class="overview-number">{{ systemStats.currentVersion }}</div>
                <div class="overview-label">当前版本</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="4">
          <el-card class="overview-card">
            <div class="overview-content">
              <div class="overview-icon">
                <el-icon><DocumentChecked /></el-icon>
              </div>
              <div class="overview-info">
                <div class="overview-number">{{ systemStats.totalRules }}</div>
                <div class="overview-label">业务规则</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="4">
          <el-card class="overview-card">
            <div class="overview-content">
              <div class="overview-icon">
                <el-icon><ChatDotRound /></el-icon>
              </div>
              <div class="overview-info">
                <div class="overview-number">{{ systemStats.totalPrompts }}</div>
                <div class="overview-label">Prompt模板</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="4">
          <el-card class="overview-card">
            <div class="overview-content">
              <div class="overview-icon">
                <el-icon><Operation /></el-icon>
              </div>
              <div class="overview-info">
                <div class="overview-number">{{ systemStats.totalScenarios }}</div>
                <div class="overview-label">应用场景</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="4">
          <el-card class="overview-card">
            <div class="overview-content">
              <div class="overview-icon">
                <el-icon><Share /></el-icon>
              </div>
              <div class="overview-info">
                <div class="overview-number">{{ systemStats.totalGraphRules }}</div>
                <div class="overview-label">图谱规则</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="4">
          <el-card class="overview-card">
            <div class="overview-content">
              <div class="overview-icon">
                <el-icon><PriceTag /></el-icon>
              </div>
              <div class="overview-info">
                <div class="overview-number">{{ systemStats.totalTags }}</div>
                <div class="overview-label">标签数量</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 功能模块导航 -->
    <div class="module-navigation">
      <el-tabs v-model="activeTab" type="card" @tab-change="handleTabChange">
        <el-tab-pane label="版本管理" name="versions">
          <template #label>
            <span class="tab-label">
              <el-icon><Clock /></el-icon>
              版本管理
            </span>
          </template>
        </el-tab-pane>
        
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
        
        <el-tab-pane label="图谱规则" name="graph-rules">
          <template #label>
            <span class="tab-label">
              <el-icon><Share /></el-icon>
              图谱规则
            </span>
          </template>
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- 内容区域 -->
    <div class="content-area">
      <!-- 版本管理 -->
      <div v-show="activeTab === 'versions'" class="module-content">
        <VersionManagement ref="versionsRef" />
      </div>

      <!-- 规则管理 -->
      <div v-show="activeTab === 'rules'" class="module-content">
        <BusinessRulesManagement ref="rulesRef" />
      </div>

      <!-- Prompt管理 -->
      <div v-show="activeTab === 'prompts'" class="module-content">
        <ScenarioPromptsManagement ref="promptsRef" />
      </div>

      <!-- 场景管理 -->
      <div v-show="activeTab === 'scenarios'" class="module-content">
        <BusinessScenariosManagement ref="scenariosRef" />
      </div>

      <!-- 图谱规则 -->
      <div v-show="activeTab === 'graph-rules'" class="module-content">
        <GraphSchemaManagement ref="graphRulesRef" />
      </div>
    </div>

    <!-- 版本发布对话框 -->
    <el-dialog v-model="versionDialogVisible" title="发布新版本" width="600px">
      <el-form :model="versionForm" :rules="versionRules" ref="versionFormRef" label-width="100px">
        <el-form-item label="版本号" prop="version">
          <el-input v-model="versionForm.version" placeholder="如: v1.3.0" />
        </el-form-item>
        <el-form-item label="版本类型" prop="type">
          <el-select v-model="versionForm.type" placeholder="请选择版本类型">
            <el-option label="主要版本 (Major)" value="major" />
            <el-option label="次要版本 (Minor)" value="minor" />
            <el-option label="补丁版本 (Patch)" value="patch" />
            <el-option label="热修复 (Hotfix)" value="hotfix" />
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
          <div class="changes-editor">
            <div
              v-for="(change, index) in versionForm.changes"
              :key="index"
              class="change-item"
            >
              <el-select
                v-model="change.type"
                placeholder="类型"
                style="width: 100px; margin-right: 8px;"
              >
                <el-option label="新增" value="add" />
                <el-option label="修改" value="modify" />
                <el-option label="删除" value="remove" />
                <el-option label="修复" value="fix" />
              </el-select>
              <el-input
                v-model="change.description"
                placeholder="变更描述"
                style="flex: 1; margin-right: 8px;"
              />
              <el-button size="small" type="danger" @click="removeChange(index)">删除</el-button>
            </div>
            <el-button size="small" @click="addChange">添加变更</el-button>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="versionDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="publishVersion" :loading="publishing">发布版本</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import {
  Setting,
  Refresh,
  Download,
  Clock,
  DocumentChecked,
  ChatDotRound,
  Operation,
  Share,
  PriceTag
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import api from '@/api'

// 导入子组件
import VersionManagement from '@/components/unified/VersionManagement.vue'
import BusinessRulesManagement from '@/components/unified/BusinessRulesManagement.vue'
import ScenarioPromptsManagement from '@/components/unified/ScenarioPromptsManagement.vue'
import BusinessScenariosManagement from '@/components/unified/BusinessScenariosManagement.vue'
import GraphSchemaManagement from '@/components/unified/GraphSchemaManagement.vue'

export default {
  name: 'UnifiedManagement',
  components: {
    Setting,
    Refresh,
    Download,
    Clock,
    DocumentChecked,
    ChatDotRound,
    Operation,
    Share,
    PriceTag,
    VersionManagement,
    BusinessRulesManagement,
    ScenarioPromptsManagement,
    BusinessScenariosManagement,
    GraphSchemaManagement
  },
  setup() {
    // 响应式数据
    const activeTab = ref('versions')
    const loading = ref(false)
    const versionDialogVisible = ref(false)
    const publishing = ref(false)
    
    // 系统统计
    const systemStats = reactive({
      currentVersion: 'v1.2.0',
      totalRules: 12,
      totalPrompts: 8,
      totalScenarios: 6,
      totalGraphRules: 15,
      totalTags: 79
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
    const versionsRef = ref(null)
    const rulesRef = ref(null)
    const promptsRef = ref(null)
    const scenariosRef = ref(null)
    const graphRulesRef = ref(null)
    const versionFormRef = ref(null)

    // 方法
    const handleTabChange = (tabName) => {
      console.log('切换到标签页:', tabName)
    }

    const refreshAllData = async () => {
      loading.value = true
      try {
        // 刷新所有模块的数据
        const promises = []
        
        if (versionsRef.value?.refreshData) {
          promises.push(versionsRef.value.refreshData())
        }
        if (rulesRef.value?.refreshData) {
          promises.push(rulesRef.value.refreshData())
        }
        if (promptsRef.value?.refreshData) {
          promises.push(promptsRef.value.refreshData())
        }
        if (scenariosRef.value?.refreshData) {
          promises.push(scenariosRef.value.refreshData())
        }
        if (graphRulesRef.value?.refreshData) {
          promises.push(graphRulesRef.value.refreshData())
        }

        await Promise.all(promises)
        
        // 刷新系统统计
        await loadSystemStats()
        
        ElMessage.success('数据刷新成功')
      } catch (error) {
        console.error('刷新数据失败:', error)
        ElMessage.error('数据刷新失败')
      } finally {
        loading.value = false
      }
    }

    const exportAllConfig = async () => {
      try {
        const response = await api.exportUnifiedConfig()
        
        if (response.success) {
          // 创建下载链接
          const blob = new Blob([JSON.stringify(response.data, null, 2)], {
            type: 'application/json'
          })
          const url = window.URL.createObjectURL(blob)
          const link = document.createElement('a')
          link.href = url
          link.download = `unified_config_${new Date().toISOString().slice(0, 10)}.json`
          link.click()
          window.URL.revokeObjectURL(url)
          
          ElMessage.success('配置导出成功')
        } else {
          ElMessage.error('配置导出失败')
        }
      } catch (error) {
        console.error('导出配置失败:', error)
        ElMessage.error('配置导出失败')
      }
    }

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
      if (versionFormRef.value) {
        versionFormRef.value.resetFields()
      }
    }

    const addChange = () => {
      versionForm.changes.push({
        type: 'add',
        description: ''
      })
    }

    const removeChange = (index) => {
      versionForm.changes.splice(index, 1)
    }

    const publishVersion = async () => {
      if (!versionFormRef.value) return
      
      try {
        await versionFormRef.value.validate()
        publishing.value = true
        
        const response = await api.publishVersion(versionForm)
        
        if (response.success) {
          ElMessage.success('版本发布成功')
          versionDialogVisible.value = false
          systemStats.currentVersion = versionForm.version
          
          // 刷新版本管理数据
          if (versionsRef.value?.refreshData) {
            versionsRef.value.refreshData()
          }
        } else {
          ElMessage.error('版本发布失败')
        }
      } catch (error) {
        console.error('发布版本失败:', error)
        ElMessage.error('发布版本失败')
      } finally {
        publishing.value = false
      }
    }

    const loadSystemStats = async () => {
      try {
        const response = await api.getUnifiedSystemStats()
        if (response.success && response.data) {
          Object.assign(systemStats, response.data)
        }
      } catch (error) {
        console.error('加载系统统计失败:', error)
      }
    }

    // 生命周期
    onMounted(() => {
      loadSystemStats()
    })

    return {
      activeTab,
      loading,
      versionDialogVisible,
      publishing,
      systemStats,
      versionForm,
      versionRules,
      versionsRef,
      rulesRef,
      promptsRef,
      scenariosRef,
      graphRulesRef,
      versionFormRef,
      handleTabChange,
      refreshAllData,
      exportAllConfig,
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
.unified-management {
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

.system-overview {
  margin-bottom: 24px;
}

.overview-card {
  cursor: pointer;
  transition: all 0.3s;
}

.overview-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.overview-content {
  display: flex;
  align-items: center;
  padding: 16px;
}

.overview-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #409EFF, #67C23A);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
}

.overview-icon .el-icon {
  font-size: 24px;
  color: white;
}

.overview-info {
  flex: 1;
}

.overview-number {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 4px;
}

.overview-label {
  color: #606266;
  font-size: 14px;
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

.changes-editor {
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 12px;
  background: #fafafa;
}

.change-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
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
  .unified-management {
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
</style>
