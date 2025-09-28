<template>
  <div class="business-rules-management">
    <!-- 操作栏 -->
    <div class="action-bar">
      <div class="action-left">
        <h3>业务规则管理</h3>
        <span class="rule-count">共 {{ allRules.length }} 条规则</span>
      </div>
      <div class="action-right">
        <el-button type="primary" @click="showAddDialog">
          <el-icon><Plus /></el-icon>
          新增规则
        </el-button>
        <el-button @click="refreshData">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
        <el-button @click="validateAllRules">
          <el-icon><DocumentChecked /></el-icon>
          批量验证
        </el-button>
      </div>
    </div>

    <!-- 规则分类导航 -->
    <div class="rules-categories">
      <el-tabs v-model="activeCategory" @tab-change="handleCategoryChange">
        <el-tab-pane label="抽取规则" name="extraction">
          <template #label>
            <span class="category-label">
              <el-icon><DocumentCopy /></el-icon>
              抽取规则 ({{ getCategoryCount('extraction') }})
            </span>
          </template>
        </el-tab-pane>
        <el-tab-pane label="归一规则" name="normalization">
          <template #label>
            <span class="category-label">
              <el-icon><MagicStick /></el-icon>
              归一规则 ({{ getCategoryCount('normalization') }})
            </span>
          </template>
        </el-tab-pane>
        <el-tab-pane label="验证规则" name="validation">
          <template #label>
            <span class="category-label">
              <el-icon><DocumentChecked /></el-icon>
              验证规则 ({{ getCategoryCount('validation') }})
            </span>
          </template>
        </el-tab-pane>
        <el-tab-pane label="分类规则" name="classification">
          <template #label>
            <span class="category-label">
              <el-icon><FolderOpened /></el-icon>
              分类规则 ({{ getCategoryCount('classification') }})
            </span>
          </template>
        </el-tab-pane>
        <el-tab-pane label="关联规则" name="association">
          <template #label>
            <span class="category-label">
              <el-icon><Connection /></el-icon>
              关联规则 ({{ getCategoryCount('association') }})
            </span>
          </template>
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- 规则列表 -->
    <div class="rules-content">
      <div class="category-description">
        <el-alert
          :title="getCategoryDescription(activeCategory)"
          type="info"
          :closable="false"
          show-icon
        />
      </div>

      <div class="rules-grid">
        <div
          v-for="rule in filteredRules"
          :key="rule.id"
          class="rule-card"
          :class="{ 'inactive': rule.status === 'inactive' }"
        >
          <div class="card-header">
            <div class="rule-info">
              <h4 class="rule-name">{{ rule.name }}</h4>
              <el-tag :type="getPriorityColor(rule.priority)" size="small">
                {{ rule.priority }}
              </el-tag>
            </div>
            <div class="card-actions">
              <el-dropdown trigger="click">
                <el-button size="small" text>
                  <el-icon><MoreFilled /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item @click="editRule(rule)">编辑</el-dropdown-item>
                    <el-dropdown-item @click="testRule(rule)">测试</el-dropdown-item>
                    <el-dropdown-item @click="duplicateRule(rule)">复制</el-dropdown-item>
                    <el-dropdown-item @click="deleteRule(rule)" divided>删除</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </div>
          
          <div class="card-content">
            <p class="rule-description">{{ rule.description }}</p>
            <div class="rule-details">
              <div class="detail-item">
                <span class="detail-label">适用阶段:</span>
                <el-tag size="small" type="info">{{ rule.stage }}</el-tag>
              </div>
              <div class="detail-item">
                <span class="detail-label">触发条件:</span>
                <code class="condition-code">{{ truncateText(rule.condition, 50) }}</code>
              </div>
              <div class="detail-item" v-if="rule.parameters && rule.parameters.length">
                <span class="detail-label">参数:</span>
                <el-tag
                  v-for="param in rule.parameters.slice(0, 3)"
                  :key="param.name"
                  size="small"
                  style="margin-right: 4px;"
                >
                  {{ param.name }}
                </el-tag>
                <span v-if="rule.parameters.length > 3">+{{ rule.parameters.length - 3 }}</span>
              </div>
            </div>
          </div>
          
          <div class="card-footer">
            <div class="rule-stats">
              <span class="execution-count">执行: {{ rule.execution_count || 0 }} 次</span>
              <span class="success-rate">成功率: {{ rule.success_rate || 0 }}%</span>
              <span class="last-run">{{ formatDate(rule.last_run) }}</span>
            </div>
            <div class="rule-status">
              <el-switch
                v-model="rule.status"
                active-value="active"
                inactive-value="inactive"
                @change="updateRuleStatus(rule)"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 新增/编辑规则对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑业务规则' : '新增业务规则'"
      width="800px"
      @close="resetForm"
    >
      <el-form :model="ruleForm" :rules="formRules" ref="formRef" label-width="120px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="规则名称" prop="name">
              <el-input v-model="ruleForm.name" placeholder="请输入规则名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="规则分类" prop="category">
              <el-select v-model="ruleForm.category" placeholder="请选择分类">
                <el-option label="抽取规则" value="extraction" />
                <el-option label="归一规则" value="normalization" />
                <el-option label="验证规则" value="validation" />
                <el-option label="分类规则" value="classification" />
                <el-option label="关联规则" value="association" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="规则描述" prop="description">
          <el-input
            v-model="ruleForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入规则描述"
          />
        </el-form-item>
        
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="优先级" prop="priority">
              <el-select v-model="ruleForm.priority" placeholder="请选择优先级">
                <el-option label="高" value="high" />
                <el-option label="中" value="medium" />
                <el-option label="低" value="low" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="适用阶段" prop="stage">
              <el-select v-model="ruleForm.stage" placeholder="请选择阶段">
                <el-option label="数据输入" value="input" />
                <el-option label="数据处理" value="processing" />
                <el-option label="数据输出" value="output" />
                <el-option label="数据存储" value="storage" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="执行模式" prop="execution_mode">
              <el-select v-model="ruleForm.execution_mode" placeholder="请选择模式">
                <el-option label="同步" value="sync" />
                <el-option label="异步" value="async" />
                <el-option label="批处理" value="batch" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="触发条件" prop="condition">
          <el-input
            v-model="ruleForm.condition"
            type="textarea"
            :rows="4"
            placeholder="请输入触发条件（支持JavaScript表达式）"
          />
        </el-form-item>
        
        <el-form-item label="执行逻辑" prop="logic">
          <el-input
            v-model="ruleForm.logic"
            type="textarea"
            :rows="6"
            placeholder="请输入执行逻辑（JavaScript代码）"
          />
        </el-form-item>
        
        <el-form-item label="规则参数">
          <div class="parameters-editor">
            <div
              v-for="(param, index) in ruleForm.parameters"
              :key="index"
              class="parameter-item"
            >
              <el-input
                v-model="param.name"
                placeholder="参数名"
                style="width: 150px; margin-right: 8px;"
              />
              <el-select
                v-model="param.type"
                placeholder="类型"
                style="width: 100px; margin-right: 8px;"
              >
                <el-option label="字符串" value="string" />
                <el-option label="数字" value="number" />
                <el-option label="布尔" value="boolean" />
                <el-option label="数组" value="array" />
                <el-option label="对象" value="object" />
              </el-select>
              <el-input
                v-model="param.default_value"
                placeholder="默认值"
                style="width: 120px; margin-right: 8px;"
              />
              <el-input
                v-model="param.description"
                placeholder="描述"
                style="flex: 1; margin-right: 8px;"
              />
              <el-button size="small" type="danger" @click="removeParameter(index)">删除</el-button>
            </div>
            <el-button size="small" @click="addParameter">添加参数</el-button>
          </div>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button @click="testRuleForm">测试规则</el-button>
        <el-button type="primary" @click="saveRule" :loading="saving">保存</el-button>
      </template>
    </el-dialog>

    <!-- 规则测试对话框 -->
    <el-dialog v-model="testDialogVisible" title="规则测试结果" width="700px">
      <div class="test-result">
        <div class="test-header">
          <h4>{{ currentTestRule?.name }}</h4>
          <el-tag :type="testResult.success ? 'success' : 'danger'">
            {{ testResult.success ? '测试通过' : '测试失败' }}
          </el-tag>
        </div>
        
        <div class="test-details">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="执行时间">{{ testResult.execution_time }}ms</el-descriptions-item>
            <el-descriptions-item label="处理记录">{{ testResult.processed_records }}</el-descriptions-item>
            <el-descriptions-item label="成功记录">{{ testResult.success_records }}</el-descriptions-item>
            <el-descriptions-item label="失败记录">{{ testResult.failed_records }}</el-descriptions-item>
            <el-descriptions-item label="错误信息" :span="2">
              <span v-if="testResult.error" class="error-text">{{ testResult.error }}</span>
              <span v-else class="success-text">无错误</span>
            </el-descriptions-item>
          </el-descriptions>
        </div>
        
        <div class="test-output" v-if="testResult.output">
          <h5>执行输出:</h5>
          <pre class="output-content">{{ testResult.output }}</pre>
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
  DocumentChecked,
  DocumentCopy,
  MagicStick,
  FolderOpened,
  Connection,
  MoreFilled
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  name: 'BusinessRulesManagement',
  components: {
    Plus,
    Refresh,
    DocumentChecked,
    DocumentCopy,
    MagicStick,
    FolderOpened,
    Connection,
    MoreFilled
  },
  setup() {
    const loading = ref(false)
    const saving = ref(false)
    const dialogVisible = ref(false)
    const testDialogVisible = ref(false)
    const isEdit = ref(false)
    const activeCategory = ref('extraction')
    const allRules = ref([])
    const formRef = ref(null)
    const currentTestRule = ref(null)

    const ruleForm = reactive({
      id: '',
      name: '',
      category: 'extraction',
      description: '',
      priority: 'medium',
      stage: 'processing',
      execution_mode: 'sync',
      condition: '',
      logic: '',
      parameters: [],
      status: 'active'
    })

    const testResult = reactive({
      success: false,
      execution_time: 0,
      processed_records: 0,
      success_records: 0,
      failed_records: 0,
      error: '',
      output: ''
    })

    const formRules = {
      name: [{ required: true, message: '请输入规则名称', trigger: 'blur' }],
      category: [{ required: true, message: '请选择规则分类', trigger: 'change' }],
      description: [{ required: true, message: '请输入规则描述', trigger: 'blur' }],
      condition: [{ required: true, message: '请输入触发条件', trigger: 'blur' }],
      logic: [{ required: true, message: '请输入执行逻辑', trigger: 'blur' }]
    }

    // 计算属性
    const filteredRules = computed(() => {
      return allRules.value.filter(rule => rule.category === activeCategory.value)
    })

    // 方法
    const getCategoryCount = (category) => {
      return allRules.value.filter(rule => rule.category === category).length
    }

    const getCategoryDescription = (category) => {
      const descriptions = {
        extraction: '数据抽取规则：定义如何从各种数据源中提取和解析结构化信息',
        normalization: '数据归一规则：统一数据格式、标准化术语和消除重复信息',
        validation: '数据验证规则：确保数据质量和完整性的检查规则',
        classification: '数据分类规则：自动分类和标记数据的业务规则',
        association: '关联建立规则：定义实体间关系和知识图谱构建规则'
      }
      return descriptions[category] || ''
    }

    const refreshData = async () => {
      loading.value = true
      try {
        // 模拟业务规则数据
        allRules.value = [
          // 抽取规则
          {
            id: 'br001',
            name: 'Excel术语抽取',
            category: 'extraction',
            description: '从Excel文件中抽取硬件质量术语和描述信息',
            priority: 'high',
            stage: 'input',
            execution_mode: 'sync',
            condition: 'file.type === "xlsx" && file.sheets.includes("术语表")',
            logic: 'extractTermsFromExcel(file, config)',
            parameters: [
              { name: 'sheet_name', type: 'string', default_value: '术语表', description: '工作表名称' },
              { name: 'term_column', type: 'string', default_value: 'A', description: '术语列' },
              { name: 'desc_column', type: 'string', default_value: 'C', description: '描述列' }
            ],
            execution_count: 156,
            success_rate: 95,
            last_run: '2024-01-20 14:30:00',
            status: 'active'
          },
          {
            id: 'br002',
            name: 'PDF文档解析',
            category: 'extraction',
            description: '从PDF技术文档中抽取工艺流程和技术规范',
            priority: 'medium',
            stage: 'input',
            execution_mode: 'async',
            condition: 'file.type === "pdf" && file.pages > 5',
            logic: 'extractFromPDF(file, patterns)',
            parameters: [
              { name: 'patterns', type: 'array', default_value: '["工艺", "流程", "规范"]', description: '抽取模式' }
            ],
            execution_count: 89,
            success_rate: 87,
            last_run: '2024-01-19 16:20:00',
            status: 'active'
          },
          // 归一规则
          {
            id: 'br003',
            name: '术语标准化',
            category: 'normalization',
            description: '统一术语命名规范，消除同义词和缩写差异',
            priority: 'high',
            stage: 'processing',
            execution_mode: 'sync',
            condition: 'entity.type === "term" && entity.aliases.length > 0',
            logic: 'normalizeTerms(entity, standardDict)',
            parameters: [
              { name: 'case_sensitive', type: 'boolean', default_value: 'false', description: '大小写敏感' }
            ],
            execution_count: 234,
            success_rate: 98,
            last_run: '2024-01-20 15:10:00',
            status: 'active'
          },
          // 验证规则
          {
            id: 'br004',
            name: '数据完整性检查',
            category: 'validation',
            description: '检查必填字段和数据格式的完整性',
            priority: 'high',
            stage: 'processing',
            execution_mode: 'sync',
            condition: 'entity.term && entity.category',
            logic: 'validateCompleteness(entity, rules)',
            parameters: [
              { name: 'required_fields', type: 'array', default_value: '["term", "category"]', description: '必填字段' }
            ],
            execution_count: 1124,
            success_rate: 96,
            last_run: '2024-01-20 15:30:00',
            status: 'active'
          },
          // 分类规则
          {
            id: 'br005',
            name: '自动分类识别',
            category: 'classification',
            description: '基于关键词和上下文自动识别术语分类',
            priority: 'medium',
            stage: 'processing',
            execution_mode: 'sync',
            condition: 'entity.category === null || entity.category === ""',
            logic: 'classifyEntity(entity, classificationModel)',
            parameters: [
              { name: 'confidence_threshold', type: 'number', default_value: '0.8', description: '置信度阈值' }
            ],
            execution_count: 567,
            success_rate: 89,
            last_run: '2024-01-20 14:45:00',
            status: 'active'
          },
          // 关联规则
          {
            id: 'br006',
            name: '语义关联发现',
            category: 'association',
            description: '基于语义相似度发现术语间的关联关系',
            priority: 'medium',
            stage: 'processing',
            execution_mode: 'batch',
            condition: 'entities.length > 1',
            logic: 'findSemanticAssociations(entities, threshold)',
            parameters: [
              { name: 'similarity_threshold', type: 'number', default_value: '0.7', description: '相似度阈值' }
            ],
            execution_count: 345,
            success_rate: 82,
            last_run: '2024-01-20 13:20:00',
            status: 'active'
          }
        ]
      } finally {
        loading.value = false
      }
    }

    const handleCategoryChange = (category) => {
      console.log('切换规则分类:', category)
    }

    const showAddDialog = () => {
      isEdit.value = false
      ruleForm.category = activeCategory.value
      dialogVisible.value = true
      resetForm()
    }

    const editRule = (rule) => {
      isEdit.value = true
      Object.assign(ruleForm, {
        ...rule,
        parameters: [...rule.parameters]
      })
      dialogVisible.value = true
    }

    const resetForm = () => {
      Object.assign(ruleForm, {
        id: '',
        name: '',
        category: activeCategory.value,
        description: '',
        priority: 'medium',
        stage: 'processing',
        execution_mode: 'sync',
        condition: '',
        logic: '',
        parameters: [],
        status: 'active'
      })
      if (formRef.value) {
        formRef.value.resetFields()
      }
    }

    const saveRule = async () => {
      if (!formRef.value) return
      
      try {
        await formRef.value.validate()
        saving.value = true
        
        ElMessage.success(isEdit.value ? '规则更新成功' : '规则创建成功')
        dialogVisible.value = false
        refreshData()
      } catch (error) {
        console.error('保存规则失败:', error)
        ElMessage.error('保存规则失败')
      } finally {
        saving.value = false
      }
    }

    const updateRuleStatus = async (rule) => {
      try {
        ElMessage.success('状态更新成功')
      } catch (error) {
        console.error('更新状态失败:', error)
        ElMessage.error('更新状态失败')
        rule.status = rule.status === 'active' ? 'inactive' : 'active'
      }
    }

    const deleteRule = async (rule) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除规则 "${rule.name}" 吗？`,
          '确认删除',
          { type: 'warning' }
        )
        
        ElMessage.success('规则删除成功')
        refreshData()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除规则失败')
        }
      }
    }

    const testRule = (rule) => {
      currentTestRule.value = rule
      
      // 模拟测试结果
      const processed = Math.floor(Math.random() * 1000) + 100
      const failed = Math.floor(Math.random() * 50)
      const success = processed - failed
      
      Object.assign(testResult, {
        success: failed < 10,
        execution_time: Math.floor(Math.random() * 500) + 50,
        processed_records: processed,
        success_records: success,
        failed_records: failed,
        error: failed > 10 ? '部分记录处理失败' : '',
        output: `规则 "${rule.name}" 执行完成\n处理了 ${processed} 条记录\n成功 ${success} 条，失败 ${failed} 条`
      })
      
      testDialogVisible.value = true
    }

    const testRuleForm = () => {
      if (!ruleForm.name) {
        ElMessage.warning('请先填写规则信息')
        return
      }
      testRule(ruleForm)
    }

    const duplicateRule = (rule) => {
      const newRule = {
        ...rule,
        id: '',
        name: rule.name + ' (副本)',
        parameters: [...rule.parameters]
      }
      Object.assign(ruleForm, newRule)
      isEdit.value = false
      dialogVisible.value = true
    }

    const validateAllRules = () => {
      ElMessage.info('批量验证功能开发中...')
    }

    // 参数管理
    const addParameter = () => {
      ruleForm.parameters.push({
        name: '',
        type: 'string',
        default_value: '',
        description: ''
      })
    }

    const removeParameter = (index) => {
      ruleForm.parameters.splice(index, 1)
    }

    // 辅助方法
    const getPriorityColor = (priority) => {
      const colors = {
        'high': 'danger',
        'medium': 'warning',
        'low': 'info'
      }
      return colors[priority] || 'info'
    }

    const truncateText = (text, length) => {
      return text && text.length > length ? text.substring(0, length) + '...' : text
    }

    const formatDate = (date) => {
      return date ? new Date(date).toLocaleString() : ''
    }

    onMounted(() => {
      refreshData()
    })

    return {
      loading,
      saving,
      dialogVisible,
      testDialogVisible,
      isEdit,
      activeCategory,
      allRules,
      formRef,
      currentTestRule,
      ruleForm,
      testResult,
      formRules,
      filteredRules,
      getCategoryCount,
      getCategoryDescription,
      refreshData,
      handleCategoryChange,
      showAddDialog,
      editRule,
      resetForm,
      saveRule,
      updateRuleStatus,
      deleteRule,
      testRule,
      testRuleForm,
      duplicateRule,
      validateAllRules,
      addParameter,
      removeParameter,
      getPriorityColor,
      truncateText,
      formatDate
    }
  }
}
</script>

<style scoped>
.business-rules-management {
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
  align-items: center;
  gap: 12px;
}

.rules-categories {
  margin-bottom: 20px;
}

.category-label {
  display: flex;
  align-items: center;
  gap: 6px;
}

.rules-content {
  background: white;
  border-radius: 8px;
  padding: 20px;
}

.category-description {
  margin-bottom: 20px;
}

.rules-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 20px;
}

.rule-card {
  background: white;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  padding: 16px;
  transition: all 0.3s;
}

.rule-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #409EFF;
}

.rule-card.inactive {
  opacity: 0.6;
  background: #f5f7fa;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.rule-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.rule-name {
  margin: 0;
  color: #303133;
  font-size: 16px;
}

.card-content {
  margin-bottom: 16px;
}

.rule-description {
  color: #606266;
  margin: 0 0 12px 0;
  line-height: 1.4;
}

.rule-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.detail-label {
  color: #909399;
  font-size: 12px;
  min-width: 60px;
}

.condition-code {
  font-family: 'Courier New', monospace;
  font-size: 12px;
  color: #606266;
  background: #f5f7fa;
  padding: 2px 4px;
  border-radius: 2px;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid #f0f2f5;
}

.rule-stats {
  display: flex;
  flex-direction: column;
  gap: 4px;
  color: #909399;
  font-size: 12px;
}

.parameters-editor {
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 12px;
  background: #fafafa;
}

.parameter-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.test-result {
  padding: 16px;
}

.test-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.test-header h4 {
  margin: 0;
  color: #303133;
}

.test-details {
  margin-bottom: 16px;
}

.test-output h5 {
  margin: 0 0 8px 0;
  color: #303133;
}

.output-content {
  background: #f5f7fa;
  padding: 12px;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 12px;
  line-height: 1.4;
  color: #606266;
  white-space: pre-wrap;
  max-height: 200px;
  overflow-y: auto;
}

.error-text {
  color: #F56C6C;
}

.success-text {
  color: #67C23A;
}
</style>
