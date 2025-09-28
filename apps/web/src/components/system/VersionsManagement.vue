<template>
  <div class="versions-management">
    <div class="action-bar">
      <div class="action-left">
        <h3>版本管理</h3>
        <span class="version-count">共 {{ versions.length }} 个版本</span>
      </div>
      <div class="action-right">
        <el-button type="primary" @click="createVersion">
          <el-icon><Plus /></el-icon>
          创建版本
        </el-button>
        <el-button @click="showCompareDialog">
          <el-icon><Operation /></el-icon>
          版本对比
        </el-button>
        <el-button @click="exportVersions">
          <el-icon><Download /></el-icon>
          导出历史
        </el-button>
        <el-button @click="refreshData">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>
    </div>

    <div class="versions-timeline">
      <el-timeline>
        <el-timeline-item
          v-for="version in versions"
          :key="version.id"
          :timestamp="version.created_at"
          :type="getVersionType(version.type)"
        >
          <el-card class="version-card">
            <div class="version-header">
              <div class="version-info">
                <h4>{{ version.name }}</h4>
                <el-tag :type="getVersionType(version.type)">{{ version.type }}</el-tag>
                <el-tag v-if="version.is_current" type="success">当前版本</el-tag>
              </div>
              <div class="version-actions">
                <el-button size="small" @click="viewChanges(version)">
                  <el-icon><View /></el-icon>
                  查看变更
                </el-button>
                <el-button size="small" @click="compareVersion(version)">
                  <el-icon><Operation /></el-icon>
                  对比
                </el-button>
                <el-button size="small" type="warning" @click="rollback(version)" v-if="!version.is_current">
                  <el-icon><RefreshLeft /></el-icon>
                  回滚
                </el-button>
                <el-button size="small" type="danger" @click="deleteVersion(version)">
                  <el-icon><Delete /></el-icon>
                  删除
                </el-button>
              </div>
            </div>
            <p class="version-description">{{ version.description }}</p>
            <div class="version-meta">
              <span>作者: {{ version.author }}</span>
              <span>文件数: {{ version.file_count }}</span>
              <span>大小: {{ version.size }}</span>
            </div>
          </el-card>
        </el-timeline-item>
      </el-timeline>
    </div>

    <!-- 版本对比对话框 -->
    <el-dialog
      v-model="compareDialogVisible"
      title="版本对比"
      width="80%"
      @close="resetCompare"
    >
      <div class="compare-selector">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="基准版本">
              <el-select v-model="compareForm.baseVersion" placeholder="选择基准版本" style="width: 100%">
                <el-option
                  v-for="version in versions"
                  :key="version.id"
                  :label="version.name"
                  :value="version.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="对比版本">
              <el-select v-model="compareForm.targetVersion" placeholder="选择对比版本" style="width: 100%">
                <el-option
                  v-for="version in versions"
                  :key="version.id"
                  :label="version.name"
                  :value="version.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-button type="primary" @click="performCompare" :disabled="!canCompare">
          开始对比
        </el-button>
      </div>

      <div v-if="compareResult" class="compare-result">
        <el-tabs v-model="compareTab">
          <el-tab-pane label="文件变更" name="files">
            <div class="file-changes">
              <div v-for="change in compareResult.fileChanges" :key="change.file" class="file-change-item">
                <div class="file-header">
                  <span class="file-name">{{ change.file }}</span>
                  <el-tag :type="getChangeTypeColor(change.type)">{{ getChangeTypeText(change.type) }}</el-tag>
                </div>
                <div v-if="change.diff" class="file-diff">
                  <pre>{{ change.diff }}</pre>
                </div>
              </div>
            </div>
          </el-tab-pane>
          <el-tab-pane label="配置变更" name="config">
            <div class="config-changes">
              <el-table :data="compareResult.configChanges" stripe>
                <el-table-column prop="key" label="配置项" />
                <el-table-column prop="oldValue" label="旧值" />
                <el-table-column prop="newValue" label="新值" />
                <el-table-column prop="type" label="变更类型">
                  <template #default="{ row }">
                    <el-tag :type="getChangeTypeColor(row.type)">{{ getChangeTypeText(row.type) }}</el-tag>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </el-tab-pane>
          <el-tab-pane label="统计信息" name="stats">
            <div class="compare-stats">
              <el-row :gutter="20">
                <el-col :span="6">
                  <div class="stat-card">
                    <div class="stat-number">{{ compareResult.stats.added }}</div>
                    <div class="stat-label">新增文件</div>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div class="stat-card">
                    <div class="stat-number">{{ compareResult.stats.modified }}</div>
                    <div class="stat-label">修改文件</div>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div class="stat-card">
                    <div class="stat-number">{{ compareResult.stats.deleted }}</div>
                    <div class="stat-label">删除文件</div>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div class="stat-card">
                    <div class="stat-number">{{ compareResult.stats.total }}</div>
                    <div class="stat-label">总变更数</div>
                  </div>
                </el-col>
              </el-row>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-dialog>

    <!-- 变更详情对话框 -->
    <el-dialog
      v-model="changesDialogVisible"
      title="版本变更详情"
      width="70%"
    >
      <div v-if="selectedVersion" class="changes-detail">
        <div class="version-summary">
          <h4>{{ selectedVersion.name }}</h4>
          <p>{{ selectedVersion.description }}</p>
          <div class="version-meta">
            <el-tag>{{ selectedVersion.type }}</el-tag>
            <span>{{ selectedVersion.created_at }}</span>
            <span>作者: {{ selectedVersion.author }}</span>
          </div>
        </div>

        <el-divider />

        <div class="changes-list">
          <h5>变更内容</h5>
          <div v-for="change in selectedVersion.changes" :key="change.id" class="change-item">
            <div class="change-header">
              <el-tag :type="getChangeTypeColor(change.type)">{{ getChangeTypeText(change.type) }}</el-tag>
              <span class="change-title">{{ change.title }}</span>
            </div>
            <p class="change-description">{{ change.description }}</p>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import {
  Plus,
  Refresh,
  Operation,
  Download,
  View,
  RefreshLeft,
  Delete
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  name: 'VersionsManagement',
  components: {
    Plus,
    Refresh,
    Operation,
    Download,
    View,
    RefreshLeft,
    Delete
  },
  setup() {
    const loading = ref(false)
    const versions = ref([])
    const compareDialogVisible = ref(false)
    const changesDialogVisible = ref(false)
    const selectedVersion = ref(null)
    const compareTab = ref('files')

    // 版本对比表单
    const compareForm = reactive({
      baseVersion: '',
      targetVersion: ''
    })

    const compareResult = ref(null)

    // 计算属性
    const canCompare = computed(() => {
      return compareForm.baseVersion && compareForm.targetVersion &&
             compareForm.baseVersion !== compareForm.targetVersion
    })

    const refreshData = async () => {
      loading.value = true
      try {
        versions.value = [
          {
            id: 'v1.2.0',
            name: 'v1.2.0 - 系统管理功能',
            type: 'feature',
            description: '新增系统管理页面，包含规则管理、Prompt管理等功能模块',
            author: 'System',
            file_count: 15,
            size: '2.3MB',
            is_current: true,
            created_at: '2024-01-20 15:30:00'
          },
          {
            id: 'v1.1.0',
            name: 'v1.1.0 - 图谱可视化优化',
            type: 'enhancement',
            description: '优化图谱可视化性能，新增节点过滤功能',
            author: 'System',
            file_count: 8,
            size: '1.8MB',
            is_current: false,
            created_at: '2024-01-18 10:20:00'
          }
        ]
      } finally {
        loading.value = false
      }
    }

    const createVersion = () => {
      ElMessage.info('版本创建功能开发中...')
    }

    const viewChanges = (version) => {
      selectedVersion.value = version
      changesDialogVisible.value = true
    }

    const compareVersion = (version) => {
      compareForm.baseVersion = version.id
      compareDialogVisible.value = true
    }

    const showCompareDialog = () => {
      compareDialogVisible.value = true
    }

    const resetCompare = () => {
      compareForm.baseVersion = ''
      compareForm.targetVersion = ''
      compareResult.value = null
      compareTab.value = 'files'
    }

    const performCompare = async () => {
      try {
        // 模拟版本对比结果
        compareResult.value = {
          fileChanges: [
            {
              file: 'src/components/SystemManagement.vue',
              type: 'modified',
              diff: '+ 新增数据源管理功能\n- 删除旧的配置项\n~ 修改样式定义'
            },
            {
              file: 'src/components/DataSourceManagement.vue',
              type: 'added',
              diff: '+ 新增文件：数据源管理组件'
            }
          ],
          configChanges: [
            {
              key: 'database.maxConnections',
              oldValue: '50',
              newValue: '100',
              type: 'modified'
            },
            {
              key: 'monitoring.enabled',
              oldValue: null,
              newValue: 'true',
              type: 'added'
            }
          ],
          stats: {
            added: 5,
            modified: 8,
            deleted: 2,
            total: 15
          }
        }
        ElMessage.success('版本对比完成')
      } catch (error) {
        ElMessage.error('版本对比失败')
      }
    }

    const exportVersions = () => {
      try {
        const data = JSON.stringify(versions.value, null, 2)
        const blob = new Blob([data], { type: 'application/json' })
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `version_history_${new Date().toISOString().slice(0, 10)}.json`
        link.click()
        window.URL.revokeObjectURL(url)
        ElMessage.success('版本历史导出成功')
      } catch (error) {
        ElMessage.error('版本历史导出失败')
      }
    }

    const getChangeTypeColor = (type) => {
      const colors = {
        added: 'success',
        modified: 'warning',
        deleted: 'danger',
        feature: 'primary',
        improvement: 'success',
        fix: 'warning'
      }
      return colors[type] || 'info'
    }

    const getChangeTypeText = (type) => {
      const texts = {
        added: '新增',
        modified: '修改',
        deleted: '删除',
        feature: '新功能',
        improvement: '改进',
        fix: '修复'
      }
      return texts[type] || type
    }

    const rollback = async (version) => {
      try {
        await ElMessageBox.confirm(
          `确定要回滚到版本 ${version.name} 吗？`,
          '确认回滚',
          { type: 'warning' }
        )
        ElMessage.success('版本回滚成功')
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('版本回滚失败')
        }
      }
    }

    const deleteVersion = async (version) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除版本 ${version.name} 吗？`,
          '确认删除',
          { type: 'warning' }
        )
        ElMessage.success('版本删除成功')
        refreshData()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('版本删除失败')
        }
      }
    }

    const getVersionType = (type) => {
      const types = {
        feature: 'primary',
        enhancement: 'success',
        bugfix: 'warning',
        hotfix: 'danger'
      }
      return types[type] || 'info'
    }

    onMounted(() => {
      refreshData()
    })

    return {
      loading,
      versions,
      compareDialogVisible,
      changesDialogVisible,
      selectedVersion,
      compareTab,
      compareForm,
      compareResult,
      canCompare,
      refreshData,
      createVersion,
      viewChanges,
      compareVersion,
      showCompareDialog,
      resetCompare,
      performCompare,
      exportVersions,
      rollback,
      deleteVersion,
      getVersionType,
      getChangeTypeColor,
      getChangeTypeText
    }
  }
}
</script>

<style scoped>
.versions-management {
  height: 100%;
}

.action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #ebeef5;
}

.action-left h3 {
  margin: 0 0 4px 0;
  color: #303133;
}

.version-count {
  color: #909399;
  font-size: 14px;
}

.action-right {
  display: flex;
  gap: 12px;
}

.versions-timeline {
  max-height: 600px;
  overflow-y: auto;
}

.version-card {
  margin-bottom: 16px;
}

.version-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.version-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.version-info h4 {
  margin: 0;
  color: #303133;
}

.version-actions {
  display: flex;
  gap: 8px;
}

.version-description {
  color: #606266;
  margin: 0 0 12px 0;
  line-height: 1.4;
}

.version-meta {
  display: flex;
  gap: 16px;
  color: #909399;
  font-size: 12px;
}

/* 版本对比样式 */
.compare-selector {
  margin-bottom: 24px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
}

.compare-result {
  margin-top: 24px;
}

.file-changes {
  max-height: 400px;
  overflow-y: auto;
}

.file-change-item {
  margin-bottom: 16px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  overflow: hidden;
}

.file-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #f5f7fa;
  border-bottom: 1px solid #e4e7ed;
}

.file-name {
  font-weight: 500;
  color: #303133;
}

.file-diff {
  padding: 16px;
  background: #fafafa;
  font-family: 'Courier New', monospace;
  font-size: 12px;
  line-height: 1.5;
}

.file-diff pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.config-changes {
  max-height: 400px;
  overflow-y: auto;
}

.compare-stats {
  padding: 16px;
}

.stat-card {
  text-align: center;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #409eff;
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

/* 变更详情样式 */
.changes-detail {
  max-height: 500px;
  overflow-y: auto;
}

.version-summary h4 {
  margin: 0 0 8px 0;
  color: #303133;
}

.version-summary p {
  margin: 0 0 12px 0;
  color: #606266;
}

.version-summary .version-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.changes-list h5 {
  margin: 0 0 16px 0;
  color: #303133;
}

.change-item {
  margin-bottom: 16px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
}

.change-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.change-title {
  font-weight: 500;
  color: #303133;
}

.change-description {
  margin: 0;
  color: #606266;
  font-size: 14px;
}
</style>
