<template>
  <div class="scenarios-management">
    <!-- 操作栏 -->
    <div class="action-bar">
      <div class="action-left">
        <h3>场景管理</h3>
        <span class="scenario-count">共 {{ scenarios.length }} 个应用场景</span>
      </div>
      <div class="action-right">
        <el-button type="primary" @click="showAddDialog">
          <el-icon><Plus /></el-icon>
          新增场景
        </el-button>
        <el-button @click="refreshData">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>
    </div>

    <!-- 场景列表 -->
    <div class="scenarios-list">
      <el-table :data="scenarios" v-loading="loading" stripe>
        <el-table-column prop="name" label="场景名称" min-width="200" />
        <el-table-column prop="type" label="场景类型" width="120">
          <template #default="{ row }">
            <el-tag :type="getTypeColor(row.type)">
              {{ getTypeText(row.type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-switch
              v-model="row.status"
              active-value="active"
              inactive-value="inactive"
              @change="updateStatus(row)"
            />
          </template>
        </el-table-column>
        <el-table-column prop="usage_count" label="使用次数" width="100" />
        <el-table-column prop="updated_at" label="更新时间" width="160" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="editScenario(row)">编辑</el-button>
            <el-button size="small" @click="testScenario(row)">测试</el-button>
            <el-button size="small" type="danger" @click="deleteScenario(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 新增/编辑场景对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑场景' : '新增场景'"
      width="700px"
      @close="resetForm"
    >
      <el-form :model="scenarioForm" :rules="formRules" ref="formRef" label-width="100px">
        <el-form-item label="场景名称" prop="name">
          <el-input v-model="scenarioForm.name" placeholder="请输入场景名称" />
        </el-form-item>
        <el-form-item label="场景类型" prop="type">
          <el-select v-model="scenarioForm.type" placeholder="请选择场景类型">
            <el-option label="异常分析" value="anomaly_analysis" />
            <el-option label="质量检测" value="quality_check" />
            <el-option label="流程优化" value="process_optimization" />
            <el-option label="知识查询" value="knowledge_query" />
          </el-select>
        </el-form-item>
        <el-form-item label="场景描述" prop="description">
          <el-input
            v-model="scenarioForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入场景描述"
          />
        </el-form-item>
        <el-form-item label="触发条件" prop="trigger_conditions">
          <el-input
            v-model="scenarioForm.trigger_conditions"
            type="textarea"
            :rows="4"
            placeholder="请输入触发条件（JSON格式）"
          />
        </el-form-item>
        <el-form-item label="处理流程" prop="workflow">
          <el-input
            v-model="scenarioForm.workflow"
            type="textarea"
            :rows="6"
            placeholder="请输入处理流程配置"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveScenario" :loading="saving">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { Plus, Refresh } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  name: 'ScenariosManagement',
  components: {
    Plus,
    Refresh
  },
  setup() {
    const loading = ref(false)
    const saving = ref(false)
    const dialogVisible = ref(false)
    const isEdit = ref(false)
    const scenarios = ref([])
    const formRef = ref(null)

    const scenarioForm = reactive({
      id: '',
      name: '',
      type: '',
      description: '',
      trigger_conditions: '',
      workflow: '',
      status: 'active'
    })

    const formRules = {
      name: [{ required: true, message: '请输入场景名称', trigger: 'blur' }],
      type: [{ required: true, message: '请选择场景类型', trigger: 'change' }],
      description: [{ required: true, message: '请输入场景描述', trigger: 'blur' }]
    }

    const refreshData = async () => {
      loading.value = true
      try {
        // 模拟数据
        scenarios.value = [
          {
            id: 's001',
            name: 'SMT焊接异常分析',
            type: 'anomaly_analysis',
            description: '分析SMT焊接过程中出现的各种异常情况',
            status: 'active',
            usage_count: 45,
            updated_at: '2024-01-20 14:30:00'
          },
          {
            id: 's002',
            name: '元器件质量检测',
            type: 'quality_check',
            description: '对进料元器件进行质量检测和评估',
            status: 'active',
            usage_count: 32,
            updated_at: '2024-01-19 16:20:00'
          }
        ]
      } catch (error) {
        console.error('获取场景列表失败:', error)
        ElMessage.error('获取场景列表失败')
      } finally {
        loading.value = false
      }
    }

    const showAddDialog = () => {
      isEdit.value = false
      dialogVisible.value = true
      resetForm()
    }

    const editScenario = (scenario) => {
      isEdit.value = true
      Object.assign(scenarioForm, scenario)
      dialogVisible.value = true
    }

    const resetForm = () => {
      Object.assign(scenarioForm, {
        id: '',
        name: '',
        type: '',
        description: '',
        trigger_conditions: '',
        workflow: '',
        status: 'active'
      })
      if (formRef.value) {
        formRef.value.resetFields()
      }
    }

    const saveScenario = async () => {
      if (!formRef.value) return
      
      try {
        await formRef.value.validate()
        saving.value = true
        
        ElMessage.success(isEdit.value ? '场景更新成功' : '场景创建成功')
        dialogVisible.value = false
        refreshData()
      } catch (error) {
        console.error('保存场景失败:', error)
        ElMessage.error('保存场景失败')
      } finally {
        saving.value = false
      }
    }

    const updateStatus = async (scenario) => {
      try {
        ElMessage.success('状态更新成功')
      } catch (error) {
        console.error('更新状态失败:', error)
        ElMessage.error('更新状态失败')
        scenario.status = scenario.status === 'active' ? 'inactive' : 'active'
      }
    }

    const deleteScenario = async (scenario) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除场景 "${scenario.name}" 吗？`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        ElMessage.success('场景删除成功')
        refreshData()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除场景失败:', error)
          ElMessage.error('删除场景失败')
        }
      }
    }

    const testScenario = (scenario) => {
      ElMessage.info('场景测试功能开发中...')
    }

    const getTypeColor = (type) => {
      const colors = {
        anomaly_analysis: 'danger',
        quality_check: 'success',
        process_optimization: 'warning',
        knowledge_query: 'info'
      }
      return colors[type] || 'info'
    }

    const getTypeText = (type) => {
      const texts = {
        anomaly_analysis: '异常分析',
        quality_check: '质量检测',
        process_optimization: '流程优化',
        knowledge_query: '知识查询'
      }
      return texts[type] || type
    }

    onMounted(() => {
      refreshData()
    })

    return {
      loading,
      saving,
      dialogVisible,
      isEdit,
      scenarios,
      formRef,
      scenarioForm,
      formRules,
      refreshData,
      showAddDialog,
      editScenario,
      resetForm,
      saveScenario,
      updateStatus,
      deleteScenario,
      testScenario,
      getTypeColor,
      getTypeText
    }
  }
}
</script>

<style scoped>
.scenarios-management {
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

.scenario-count {
  color: #909399;
  font-size: 14px;
}

.action-right {
  display: flex;
  gap: 12px;
}

.scenarios-list {
  background: white;
  border-radius: 4px;
}
</style>
