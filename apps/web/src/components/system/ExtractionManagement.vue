<template>
  <div class="extraction-management">
    <div class="action-bar">
      <div class="action-left">
        <h3>文档抽取逻辑</h3>
        <span class="logic-count">共 {{ extractionLogics.length }} 个抽取逻辑</span>
      </div>
      <div class="action-right">
        <el-button type="primary" @click="showAddDialog">
          <el-icon><Plus /></el-icon>
          新增逻辑
        </el-button>
        <el-button @click="refreshData">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>
    </div>

    <div class="extraction-grid">
      <div
        v-for="logic in extractionLogics"
        :key="logic.id"
        class="logic-card"
      >
        <div class="card-header">
          <div class="logic-info">
            <h4>{{ logic.name }}</h4>
            <el-tag :type="getTypeColor(logic.document_type)">
              {{ logic.document_type }}
            </el-tag>
          </div>
          <div class="card-actions">
            <el-dropdown trigger="click">
              <el-button size="small" text>
                <el-icon><MoreFilled /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="editLogic(logic)">编辑</el-dropdown-item>
                  <el-dropdown-item @click="testLogic(logic)">测试</el-dropdown-item>
                  <el-dropdown-item @click="exportLogic(logic)">导出</el-dropdown-item>
                  <el-dropdown-item @click="deleteLogic(logic)" divided>删除</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
        
        <div class="card-content">
          <p class="logic-description">{{ logic.description }}</p>
          <div class="logic-rules">
            <h5>抽取规则:</h5>
            <ul>
              <li v-for="rule in logic.rules.slice(0, 3)" :key="rule">{{ rule }}</li>
              <li v-if="logic.rules.length > 3">...</li>
            </ul>
          </div>
        </div>
        
        <div class="card-footer">
          <div class="logic-meta">
            <span class="accuracy">准确率: {{ logic.accuracy }}%</span>
            <span class="usage">使用: {{ logic.usage_count }} 次</span>
          </div>
          <div class="logic-status">
            <el-switch
              v-model="logic.status"
              active-value="active"
              inactive-value="inactive"
              @change="updateStatus(logic)"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑抽取逻辑' : '新增抽取逻辑'"
      width="800px"
      @close="resetForm"
    >
      <el-form :model="logicForm" :rules="formRules" ref="formRef" label-width="120px">
        <el-form-item label="逻辑名称" prop="name">
          <el-input v-model="logicForm.name" placeholder="请输入抽取逻辑名称" />
        </el-form-item>
        <el-form-item label="文档类型" prop="document_type">
          <el-select v-model="logicForm.document_type" placeholder="请选择文档类型">
            <el-option label="Excel" value="excel" />
            <el-option label="PDF" value="pdf" />
            <el-option label="Word" value="word" />
            <el-option label="Text" value="text" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="logicForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入抽取逻辑描述"
          />
        </el-form-item>
        <el-form-item label="抽取规则" prop="rules_config">
          <el-input
            v-model="logicForm.rules_config"
            type="textarea"
            :rows="8"
            placeholder="请输入抽取规则配置（JSON格式）"
          />
        </el-form-item>
        <el-form-item label="字段映射" prop="field_mapping">
          <el-input
            v-model="logicForm.field_mapping"
            type="textarea"
            :rows="6"
            placeholder="请输入字段映射配置（JSON格式）"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveLogic" :loading="saving">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { Plus, Refresh, MoreFilled } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  name: 'ExtractionManagement',
  components: { Plus, Refresh, MoreFilled },
  setup() {
    const loading = ref(false)
    const saving = ref(false)
    const dialogVisible = ref(false)
    const isEdit = ref(false)
    const extractionLogics = ref([])
    const formRef = ref(null)

    const logicForm = reactive({
      id: '',
      name: '',
      document_type: '',
      description: '',
      rules_config: '',
      field_mapping: '',
      status: 'active'
    })

    const formRules = {
      name: [{ required: true, message: '请输入逻辑名称', trigger: 'blur' }],
      document_type: [{ required: true, message: '请选择文档类型', trigger: 'change' }],
      description: [{ required: true, message: '请输入描述', trigger: 'blur' }]
    }

    const refreshData = async () => {
      loading.value = true
      try {
        extractionLogics.value = [
          {
            id: 'e001',
            name: 'Excel质量数据抽取',
            document_type: 'excel',
            description: '从Excel文件中抽取质量相关的实体和关系数据',
            rules: [
              '识别症状描述列',
              '提取组件信息',
              '解析异常分类',
              '抽取时间信息'
            ],
            accuracy: 95,
            usage_count: 128,
            status: 'active'
          },
          {
            id: 'e002',
            name: 'PDF技术文档抽取',
            document_type: 'pdf',
            description: '从PDF技术文档中抽取工艺流程和规范信息',
            rules: [
              '识别章节标题',
              '提取工艺步骤',
              '解析参数表格'
            ],
            accuracy: 87,
            usage_count: 45,
            status: 'active'
          }
        ]
      } finally {
        loading.value = false
      }
    }

    const showAddDialog = () => {
      isEdit.value = false
      dialogVisible.value = true
      resetForm()
    }

    const editLogic = (logic) => {
      isEdit.value = true
      Object.assign(logicForm, {
        ...logic,
        rules_config: JSON.stringify(logic.rules || [], null, 2),
        field_mapping: JSON.stringify({
          term: 'A',
          category: 'B',
          description: 'C'
        }, null, 2)
      })
      dialogVisible.value = true
    }

    const resetForm = () => {
      Object.assign(logicForm, {
        id: '',
        name: '',
        document_type: '',
        description: '',
        rules_config: '',
        field_mapping: '',
        status: 'active'
      })
      if (formRef.value) {
        formRef.value.resetFields()
      }
    }

    const saveLogic = async () => {
      if (!formRef.value) return
      
      try {
        await formRef.value.validate()
        saving.value = true
        
        ElMessage.success(isEdit.value ? '抽取逻辑更新成功' : '抽取逻辑创建成功')
        dialogVisible.value = false
        refreshData()
      } catch (error) {
        console.error('保存抽取逻辑失败:', error)
        ElMessage.error('保存抽取逻辑失败')
      } finally {
        saving.value = false
      }
    }

    const updateStatus = async (logic) => {
      try {
        ElMessage.success('状态更新成功')
      } catch (error) {
        console.error('更新状态失败:', error)
        ElMessage.error('更新状态失败')
        logic.status = logic.status === 'active' ? 'inactive' : 'active'
      }
    }

    const testLogic = (logic) => {
      ElMessage.info(`测试抽取逻辑: ${logic.name}`)
    }

    const exportLogic = (logic) => {
      ElMessage.info(`导出抽取逻辑: ${logic.name}`)
    }

    const deleteLogic = async (logic) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除抽取逻辑 "${logic.name}" 吗？`,
          '确认删除',
          { type: 'warning' }
        )
        
        ElMessage.success('抽取逻辑删除成功')
        refreshData()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除抽取逻辑失败')
        }
      }
    }

    const getTypeColor = (type) => {
      const colors = {
        excel: 'success',
        pdf: 'warning',
        word: 'primary',
        text: 'info'
      }
      return colors[type] || 'info'
    }

    onMounted(() => {
      refreshData()
    })

    return {
      loading,
      saving,
      dialogVisible,
      isEdit,
      extractionLogics,
      formRef,
      logicForm,
      formRules,
      refreshData,
      showAddDialog,
      editLogic,
      resetForm,
      saveLogic,
      updateStatus,
      testLogic,
      exportLogic,
      deleteLogic,
      getTypeColor
    }
  }
}
</script>

<style scoped>
.extraction-management {
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

.logic-count {
  color: #909399;
  font-size: 14px;
}

.action-right {
  display: flex;
  gap: 12px;
}

.extraction-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 20px;
}

.logic-card {
  background: white;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  padding: 16px;
  transition: all 0.3s;
}

.logic-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #409EFF;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.logic-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.logic-info h4 {
  margin: 0;
  color: #303133;
}

.card-content {
  margin-bottom: 16px;
}

.logic-description {
  color: #606266;
  margin: 0 0 12px 0;
  line-height: 1.4;
}

.logic-rules h5 {
  margin: 0 0 8px 0;
  color: #303133;
  font-size: 14px;
}

.logic-rules ul {
  margin: 0;
  padding-left: 16px;
  color: #606266;
  font-size: 13px;
}

.logic-rules li {
  margin-bottom: 4px;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid #f0f2f5;
}

.logic-meta {
  display: flex;
  gap: 16px;
  color: #909399;
  font-size: 12px;
}

.accuracy {
  color: #67C23A;
}
</style>
