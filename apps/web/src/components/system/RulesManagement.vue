<template>
  <div class="rules-management">
    <!-- 操作栏 -->
    <div class="action-bar">
      <div class="action-left">
        <h3>规则管理</h3>
        <span class="rule-count">共 {{ filteredRules.length }} 条规则</span>
      </div>
      <div class="action-right">
        <el-button type="primary" @click="showAddDialog">
          <el-icon><Plus /></el-icon>
          新增规则
        </el-button>
        <el-button @click="showTestDialog">
          <el-icon><Operation /></el-icon>
          规则测试
        </el-button>
        <el-button @click="exportRules">
          <el-icon><Download /></el-icon>
          导出规则
        </el-button>
        <el-button @click="refreshData">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>
    </div>

    <!-- 规则分类标签页 -->
    <div class="rules-categories">
      <el-tabs v-model="activeCategory" @tab-change="handleCategoryChange">
        <el-tab-pane label="全部规则" name="all">
          <template #label>
            <span class="tab-label">
              <el-icon><List /></el-icon>
              全部规则 ({{ rules.length }})
            </span>
          </template>
        </el-tab-pane>
        <el-tab-pane label="文档解析" name="document_parsing">
          <template #label>
            <span class="tab-label">
              <el-icon><Document /></el-icon>
              文档解析 ({{ getRuleCountByType('document_parsing') }})
            </span>
          </template>
        </el-tab-pane>
        <el-tab-pane label="信息归一" name="data_normalization">
          <template #label>
            <span class="tab-label">
              <el-icon><Operation /></el-icon>
              信息归一 ({{ getRuleCountByType('data_normalization') }})
            </span>
          </template>
        </el-tab-pane>
        <el-tab-pane label="质量检查" name="quality_check">
          <template #label>
            <span class="tab-label">
              <el-icon><CircleCheck /></el-icon>
              质量检查 ({{ getRuleCountByType('quality_check') }})
            </span>
          </template>
        </el-tab-pane>
        <el-tab-pane label="图谱构建" name="graph_construction">
          <template #label>
            <span class="tab-label">
              <el-icon><Share /></el-icon>
              图谱构建 ({{ getRuleCountByType('graph_construction') }})
            </span>
          </template>
        </el-tab-pane>

      </el-tabs>
    </div>

    <!-- 规则列表 -->
    <div class="rules-list">
      <el-table :data="filteredRules" v-loading="loading" stripe>
        <el-table-column prop="rule_id" label="规则ID" width="120" />
        <el-table-column prop="name" label="规则名称" min-width="200" />
        <el-table-column prop="type" label="类型" width="120">
          <template #default="{ row }">
            <el-tag :type="getRuleTypeColor(row.type)">
              {{ getRuleTypeText(row.type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-switch
              v-model="row.status"
              active-value="active"
              inactive-value="inactive"
              @change="updateRuleStatus(row)"
            />
          </template>
        </el-table-column>
        <el-table-column prop="priority" label="优先级" width="100">
          <template #default="{ row }">
            <el-tag :type="getPriorityColor(row.priority)">
              {{ row.priority }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="last_check" label="最后检查" width="160" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="editRule(row)">编辑</el-button>
            <el-button size="small" @click="testRule(row)">测试</el-button>
            <el-button size="small" type="danger" @click="deleteRule(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 新增/编辑规则对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑规则' : '新增规则'"
      width="600px"
      @close="resetForm"
    >
      <el-form :model="ruleForm" :rules="formRules" ref="formRef" label-width="100px">
        <el-form-item label="规则ID" prop="rule_id">
          <el-input v-model="ruleForm.rule_id" :disabled="isEdit" placeholder="请输入规则ID" />
        </el-form-item>
        <el-form-item label="规则名称" prop="name">
          <el-input v-model="ruleForm.name" placeholder="请输入规则名称" />
        </el-form-item>
        <el-form-item label="规则类型" prop="type">
          <el-select v-model="ruleForm.type" placeholder="请选择规则类型">
            <el-option label="验证规则" value="validation" />
            <el-option label="标准化规则" value="standardization" />
            <el-option label="质量规则" value="quality" />
            <el-option label="业务规则" value="business" />
          </el-select>
        </el-form-item>
        <el-form-item label="优先级" prop="priority">
          <el-select v-model="ruleForm.priority" placeholder="请选择优先级">
            <el-option label="高" value="high" />
            <el-option label="中" value="medium" />
            <el-option label="低" value="low" />
          </el-select>
        </el-form-item>
        <el-form-item label="规则描述" prop="description">
          <el-input
            v-model="ruleForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入规则描述"
          />
        </el-form-item>
        <el-form-item label="规则逻辑" prop="logic">
          <el-input
            v-model="ruleForm.logic"
            type="textarea"
            :rows="5"
            placeholder="请输入规则逻辑（支持JavaScript表达式）"
          />
        </el-form-item>
        <el-form-item label="错误消息" prop="error_message">
          <el-input v-model="ruleForm.error_message" placeholder="规则验证失败时的错误消息" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveRule" :loading="saving">保存</el-button>
      </template>
    </el-dialog>

    <!-- 规则测试对话框 -->
    <el-dialog v-model="testDialogVisible" title="规则测试" width="800px">
      <div class="test-content">
        <el-form :model="testForm" label-width="100px">
          <el-form-item label="测试数据">
            <el-input
              v-model="testForm.testData"
              type="textarea"
              :rows="8"
              placeholder="请输入测试数据（JSON格式）"
            />
          </el-form-item>
        </el-form>
        <div class="test-result" v-if="testResult">
          <h4>测试结果：</h4>
          <el-alert
            :type="testResult.success ? 'success' : 'error'"
            :title="testResult.message"
            show-icon
            :closable="false"
          />
          <div v-if="testResult.details" class="result-details">
            <pre>{{ JSON.stringify(testResult.details, null, 2) }}</pre>
          </div>
        </div>
      </div>
      <template #footer>
        <el-button @click="testDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="runTest" :loading="testing">运行测试</el-button>
      </template>
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
  List,
  Document,
  CircleCheck,
  Share
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '@/api'

export default {
  name: 'RulesManagement',
  components: {
    Plus,
    Refresh,
    Operation,
    Download,
    List,
    Document,
    CircleCheck,
    Share
  },
  setup() {
    // 响应式数据
    const loading = ref(false)
    const saving = ref(false)
    const testing = ref(false)
    const dialogVisible = ref(false)
    const testDialogVisible = ref(false)
    const isEdit = ref(false)
    const rules = ref([])
    const formRef = ref(null)
    const activeCategory = ref('all')

    // 计算属性
    const filteredRules = computed(() => {
      if (activeCategory.value === 'all') {
        return rules.value
      }
      return rules.value.filter(rule => rule.type === activeCategory.value)
    })

    // 表单数据
    const ruleForm = reactive({
      rule_id: '',
      name: '',
      type: '',
      priority: 'medium',
      description: '',
      logic: '',
      error_message: '',
      status: 'active'
    })

    // 测试表单
    const testForm = reactive({
      testData: ''
    })

    const testResult = ref(null)

    // 表单验证规则
    const formRules = {
      rule_id: [
        { required: true, message: '请输入规则ID', trigger: 'blur' }
      ],
      name: [
        { required: true, message: '请输入规则名称', trigger: 'blur' }
      ],
      type: [
        { required: true, message: '请选择规则类型', trigger: 'change' }
      ],
      description: [
        { required: true, message: '请输入规则描述', trigger: 'blur' }
      ],
      logic: [
        { required: true, message: '请输入规则逻辑', trigger: 'blur' }
      ]
    }

    // 方法
    const refreshData = async () => {
      loading.value = true
      try {
        const response = await api.getRules()
        if (response.success) {
          rules.value = response.data || []
        }
      } catch (error) {
        console.error('获取规则列表失败:', error)
        ElMessage.error('获取规则列表失败')
      } finally {
        loading.value = false
      }
    }

    const showAddDialog = () => {
      isEdit.value = false
      dialogVisible.value = true
      resetForm()
    }

    const editRule = (rule) => {
      isEdit.value = true
      Object.assign(ruleForm, rule)
      dialogVisible.value = true
    }

    const resetForm = () => {
      Object.assign(ruleForm, {
        rule_id: '',
        name: '',
        type: '',
        priority: 'medium',
        description: '',
        logic: '',
        error_message: '',
        status: 'active'
      })
      formRef.value?.resetFields()
    }

    const saveRule = async () => {
      if (!formRef.value) return
      
      try {
        await formRef.value?.validate()
        saving.value = true
        
        const response = isEdit.value 
          ? await api.updateRule(ruleForm.rule_id, ruleForm)
          : await api.createRule(ruleForm)
        
        if (response.success) {
          ElMessage.success(isEdit.value ? '规则更新成功' : '规则创建成功')
          dialogVisible.value = false
          refreshData()
        } else {
          ElMessage.error(response.message || '操作失败')
        }
      } catch (error) {
        console.error('保存规则失败:', error)
        ElMessage.error('保存规则失败')
      } finally {
        saving.value = false
      }
    }

    const updateRuleStatus = async (rule) => {
      try {
        const response = await api.updateRuleStatus(rule.rule_id, rule.status)
        if (response.success) {
          ElMessage.success('状态更新成功')
        } else {
          ElMessage.error('状态更新失败')
          // 回滚状态
          rule.status = rule.status === 'active' ? 'inactive' : 'active'
        }
      } catch (error) {
        console.error('更新规则状态失败:', error)
        ElMessage.error('更新规则状态失败')
        // 回滚状态
        rule.status = rule.status === 'active' ? 'inactive' : 'active'
      }
    }

    const deleteRule = async (rule) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除规则 "${rule.name}" 吗？`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        const response = await api.deleteRule(rule.rule_id)
        if (response.success) {
          ElMessage.success('规则删除成功')
          refreshData()
        } else {
          ElMessage.error('规则删除失败')
        }
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除规则失败:', error)
          ElMessage.error('删除规则失败')
        }
      }
    }

    const testRule = (rule) => {
      testForm.testData = JSON.stringify({
        term: "示例术语",
        category: "Component",
        description: "这是一个示例描述"
      }, null, 2)
      testResult.value = null
      testDialogVisible.value = true
    }

    const runTest = async () => {
      try {
        testing.value = true
        const testData = JSON.parse(testForm.testData)

        // 模拟规则测试
        testResult.value = {
          success: true,
          message: '规则测试通过',
          details: {
            input: testData,
            result: '验证成功',
            execution_time: '12ms'
          }
        }
      } catch (error) {
        console.error('规则测试失败:', error)
        testResult.value = {
          success: false,
          message: '测试失败: ' + error.message
        }
      } finally {
        testing.value = false
      }
    }

    // 辅助方法
    const getRuleTypeColor = (type) => {
      const colors = {
        validation: 'primary',
        standardization: 'success',
        quality: 'warning',
        business: 'info'
      }
      return colors[type] || 'info'
    }

    const getRuleTypeText = (type) => {
      const texts = {
        validation: '验证',
        standardization: '标准化',
        quality: '质量',
        business: '业务',
        document_parsing: '文档解析',
        data_normalization: '信息归一',
        quality_check: '质量检查',
        graph_construction: '图谱构建'
      }
      return texts[type] || type
    }

    const getPriorityColor = (priority) => {
      const colors = {
        high: 'danger',
        medium: 'warning',
        low: 'info'
      }
      return colors[priority] || 'info'
    }

    // 新增方法
    const handleCategoryChange = (category) => {
      activeCategory.value = category
    }

    const getRuleCountByType = (type) => {
      return rules.value.filter(rule => rule.type === type).length
    }

    const showTestDialog = () => {
      testDialogVisible.value = true
    }

    const exportRules = () => {
      try {
        const data = JSON.stringify(filteredRules.value, null, 2)
        const blob = new Blob([data], { type: 'application/json' })
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `rules_${activeCategory.value}_${new Date().toISOString().slice(0, 10)}.json`
        link.click()
        window.URL.revokeObjectURL(url)
        ElMessage.success('规则导出成功')
      } catch (error) {
        ElMessage.error('规则导出失败')
      }
    }

    // 生命周期
    onMounted(() => {
      refreshData()
    })

    // 暴露方法给父组件
    const expose = {
      refreshData
    }

    return {
      loading,
      saving,
      testing,
      dialogVisible,
      testDialogVisible,
      isEdit,
      rules,
      formRef,
      activeCategory,
      filteredRules,
      ruleForm,
      testForm,
      testResult,
      formRules,
      refreshData,
      showAddDialog,
      editRule,
      resetForm,
      saveRule,
      updateRuleStatus,
      deleteRule,
      testRule,
      runTest,
      handleCategoryChange,
      getRuleCountByType,
      showTestDialog,
      exportRules,
      getRuleTypeColor,
      getRuleTypeText,
      getPriorityColor,
      ...expose
    }
  }
}
</script>

<style scoped>
.rules-management {
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

.rule-count {
  color: #909399;
  font-size: 14px;
}

.action-right {
  display: flex;
  gap: 12px;
}

.rules-list {
  background: white;
  border-radius: 4px;
}

.test-content {
  max-height: 500px;
  overflow-y: auto;
}

.test-result {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #ebeef5;
}

.result-details {
  margin-top: 12px;
  padding: 12px;
  background: #f5f7fa;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 12px;
  max-height: 200px;
  overflow-y: auto;
}

.result-details pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
}

/* 规则分类样式 */
.rules-categories {
  margin-bottom: 24px;
}

.tab-label {
  display: flex;
  align-items: center;
  gap: 6px;
}

.tab-label .el-icon {
  font-size: 14px;
}

/* 分类标签页样式优化 */
:deep(.el-tabs__header) {
  margin: 0 0 16px 0;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 0 16px;
}

:deep(.el-tabs__nav) {
  border: none;
}

:deep(.el-tabs__item) {
  border: none;
  color: #606266;
  font-weight: 500;
  padding: 0 20px;
  height: 48px;
  line-height: 48px;
}

:deep(.el-tabs__item.is-active) {
  color: #409EFF;
  background-color: #f0f9ff;
  border-radius: 6px;
}

:deep(.el-tabs__active-bar) {
  display: none;
}
</style>
