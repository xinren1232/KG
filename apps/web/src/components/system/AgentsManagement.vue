<template>
  <div class="agents-management">
    <div class="action-bar">
      <div class="action-left">
        <h3>Agent设计管理</h3>
        <span class="agent-count">共 {{ agents.length }} 个Agent</span>
      </div>
      <div class="action-right">
        <el-button type="primary" @click="showAddDialog">
          <el-icon><Plus /></el-icon>
          新增Agent
        </el-button>
        <el-button @click="refreshData">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>
    </div>

    <div class="agents-grid">
      <div
        v-for="agent in agents"
        :key="agent.id"
        class="agent-card"
      >
        <div class="card-header">
          <div class="agent-avatar">
            <el-avatar :size="50" :src="agent.avatar">
              <el-icon><Avatar /></el-icon>
            </el-avatar>
          </div>
          <div class="agent-info">
            <h4>{{ agent.name }}</h4>
            <p class="agent-role">{{ agent.role }}</p>
            <el-tag :type="getStatusColor(agent.status)" size="small">
              {{ getStatusText(agent.status) }}
            </el-tag>
          </div>
          <div class="card-actions">
            <el-dropdown trigger="click">
              <el-button size="small" text>
                <el-icon><MoreFilled /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="editAgent(agent)">编辑</el-dropdown-item>
                  <el-dropdown-item @click="testAgent(agent)">测试</el-dropdown-item>
                  <el-dropdown-item @click="deployAgent(agent)">部署</el-dropdown-item>
                  <el-dropdown-item @click="deleteAgent(agent)" divided>删除</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
        
        <div class="card-content">
          <p class="agent-description">{{ agent.description }}</p>
          <div class="agent-capabilities">
            <h5>核心能力:</h5>
            <div class="capabilities-list">
              <el-tag
                v-for="capability in agent.capabilities"
                :key="capability"
                size="small"
                style="margin: 2px 4px 2px 0;"
              >
                {{ capability }}
              </el-tag>
            </div>
          </div>
        </div>
        
        <div class="card-footer">
          <div class="agent-stats">
            <span>调用: {{ agent.call_count }} 次</span>
            <span>成功率: {{ agent.success_rate }}%</span>
          </div>
          <div class="agent-actions">
            <el-button size="small" @click="viewLogs(agent)">日志</el-button>
            <el-button size="small" @click="viewMetrics(agent)">指标</el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 新增/编辑Agent对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑Agent' : '新增Agent'"
      width="800px"
      @close="resetForm"
    >
      <el-form :model="agentForm" :rules="formRules" ref="formRef" label-width="120px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Agent名称" prop="name">
              <el-input v-model="agentForm.name" placeholder="请输入Agent名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="角色定位" prop="role">
              <el-input v-model="agentForm.role" placeholder="请输入角色定位" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="agentForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入Agent描述"
          />
        </el-form-item>
        
        <el-form-item label="系统提示" prop="system_prompt">
          <el-input
            v-model="agentForm.system_prompt"
            type="textarea"
            :rows="5"
            placeholder="请输入系统提示词"
          />
        </el-form-item>
        
        <el-form-item label="核心能力">
          <div class="capabilities-editor">
            <el-tag
              v-for="capability in agentForm.capabilities"
              :key="capability"
              closable
              @close="removeCapability(capability)"
              style="margin-right: 8px; margin-bottom: 8px;"
            >
              {{ capability }}
            </el-tag>
            <el-input
              v-if="capabilityInputVisible"
              ref="capabilityInputRef"
              v-model="capabilityInputValue"
              size="small"
              style="width: 120px;"
              @keyup.enter="handleCapabilityInputConfirm"
              @blur="handleCapabilityInputConfirm"
            />
            <el-button v-else size="small" @click="showCapabilityInput">+ 新能力</el-button>
          </div>
        </el-form-item>
        
        <el-form-item label="工具配置" prop="tools_config">
          <el-input
            v-model="agentForm.tools_config"
            type="textarea"
            :rows="6"
            placeholder="请输入工具配置（JSON格式）"
          />
        </el-form-item>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="模型配置" prop="model_config">
              <el-select v-model="agentForm.model_config" placeholder="请选择模型">
                <el-option label="GPT-4" value="gpt-4" />
                <el-option label="GPT-3.5" value="gpt-3.5-turbo" />
                <el-option label="Claude-3" value="claude-3" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="温度参数" prop="temperature">
              <el-slider
                v-model="agentForm.temperature"
                :min="0"
                :max="1"
                :step="0.1"
                show-input
              />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveAgent" :loading="saving">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { Plus, Refresh, MoreFilled, Avatar } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  name: 'AgentsManagement',
  components: { Plus, Refresh, MoreFilled, Avatar },
  setup() {
    const loading = ref(false)
    const saving = ref(false)
    const dialogVisible = ref(false)
    const isEdit = ref(false)
    const agents = ref([])
    const formRef = ref(null)
    const capabilityInputRef = ref(null)
    const capabilityInputVisible = ref(false)
    const capabilityInputValue = ref('')

    const agentForm = reactive({
      id: '',
      name: '',
      role: '',
      description: '',
      system_prompt: '',
      capabilities: [],
      tools_config: '',
      model_config: 'gpt-4',
      temperature: 0.7,
      status: 'active'
    })

    const formRules = {
      name: [{ required: true, message: '请输入Agent名称', trigger: 'blur' }],
      role: [{ required: true, message: '请输入角色定位', trigger: 'blur' }],
      description: [{ required: true, message: '请输入描述', trigger: 'blur' }],
      system_prompt: [{ required: true, message: '请输入系统提示', trigger: 'blur' }]
    }

    const refreshData = async () => {
      loading.value = true
      try {
        agents.value = [
          {
            id: 'a001',
            name: '质量分析师',
            role: '硬件质量专家',
            description: '专门分析硬件质量问题，提供专业的解决方案和建议',
            capabilities: ['异常分析', '根因追溯', '解决方案推荐', '质量评估'],
            status: 'active',
            call_count: 156,
            success_rate: 94,
            avatar: null
          },
          {
            id: 'a002',
            name: '工艺优化师',
            role: '制造工艺专家',
            description: '专注于制造工艺的优化和改进，提高生产效率和质量',
            capabilities: ['工艺分析', '参数优化', '流程改进', '效率提升'],
            status: 'active',
            call_count: 89,
            success_rate: 91,
            avatar: null
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

    const editAgent = (agent) => {
      isEdit.value = true
      Object.assign(agentForm, {
        ...agent,
        capabilities: [...(agent.capabilities || [])],
        tools_config: JSON.stringify({
          knowledge_search: { enabled: true },
          anomaly_analysis: { enabled: true },
          quality_metrics: { enabled: true }
        }, null, 2)
      })
      dialogVisible.value = true
    }

    const resetForm = () => {
      Object.assign(agentForm, {
        id: '',
        name: '',
        role: '',
        description: '',
        system_prompt: '',
        capabilities: [],
        tools_config: '',
        model_config: 'gpt-4',
        temperature: 0.7,
        status: 'active'
      })
      if (formRef.value) {
        formRef.value.resetFields()
      }
    }

    const saveAgent = async () => {
      if (!formRef.value) return
      
      try {
        await formRef.value.validate()
        saving.value = true
        
        ElMessage.success(isEdit.value ? 'Agent更新成功' : 'Agent创建成功')
        dialogVisible.value = false
        refreshData()
      } catch (error) {
        console.error('保存Agent失败:', error)
        ElMessage.error('保存Agent失败')
      } finally {
        saving.value = false
      }
    }

    const deleteAgent = async (agent) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除Agent "${agent.name}" 吗？`,
          '确认删除',
          { type: 'warning' }
        )
        
        ElMessage.success('Agent删除成功')
        refreshData()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除Agent失败')
        }
      }
    }

    const testAgent = (agent) => {
      ElMessage.info(`测试Agent: ${agent.name}`)
    }

    const deployAgent = (agent) => {
      ElMessage.info(`部署Agent: ${agent.name}`)
    }

    const viewLogs = (agent) => {
      ElMessage.info(`查看Agent日志: ${agent.name}`)
    }

    const viewMetrics = (agent) => {
      ElMessage.info(`查看Agent指标: ${agent.name}`)
    }

    // 能力管理
    const removeCapability = (capability) => {
      const index = agentForm.capabilities.indexOf(capability)
      if (index > -1) {
        agentForm.capabilities.splice(index, 1)
      }
    }

    const showCapabilityInput = () => {
      capabilityInputVisible.value = true
      nextTick(() => {
        capabilityInputRef.value?.focus()
      })
    }

    const handleCapabilityInputConfirm = () => {
      if (capabilityInputValue.value && !agentForm.capabilities.includes(capabilityInputValue.value)) {
        agentForm.capabilities.push(capabilityInputValue.value)
      }
      capabilityInputVisible.value = false
      capabilityInputValue.value = ''
    }

    const getStatusColor = (status) => {
      const colors = {
        active: 'success',
        inactive: 'info',
        error: 'danger',
        deploying: 'warning'
      }
      return colors[status] || 'info'
    }

    const getStatusText = (status) => {
      const texts = {
        active: '运行中',
        inactive: '已停止',
        error: '错误',
        deploying: '部署中'
      }
      return texts[status] || status
    }

    onMounted(() => {
      refreshData()
    })

    return {
      loading,
      saving,
      dialogVisible,
      isEdit,
      agents,
      formRef,
      capabilityInputRef,
      capabilityInputVisible,
      capabilityInputValue,
      agentForm,
      formRules,
      refreshData,
      showAddDialog,
      editAgent,
      resetForm,
      saveAgent,
      deleteAgent,
      testAgent,
      deployAgent,
      viewLogs,
      viewMetrics,
      removeCapability,
      showCapabilityInput,
      handleCapabilityInputConfirm,
      getStatusColor,
      getStatusText
    }
  }
}
</script>

<style scoped>
.agents-management {
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

.agent-count {
  color: #909399;
  font-size: 14px;
}

.action-right {
  display: flex;
  gap: 12px;
}

.agents-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 20px;
}

.agent-card {
  background: white;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  padding: 16px;
  transition: all 0.3s;
}

.agent-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #409EFF;
}

.card-header {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 16px;
}

.agent-info {
  flex: 1;
}

.agent-info h4 {
  margin: 0 0 4px 0;
  color: #303133;
}

.agent-role {
  margin: 0 0 8px 0;
  color: #606266;
  font-size: 14px;
}

.card-content {
  margin-bottom: 16px;
}

.agent-description {
  color: #606266;
  margin: 0 0 12px 0;
  line-height: 1.4;
}

.agent-capabilities h5 {
  margin: 0 0 8px 0;
  color: #303133;
  font-size: 14px;
}

.capabilities-list {
  line-height: 1.6;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid #f0f2f5;
}

.agent-stats {
  display: flex;
  gap: 16px;
  color: #909399;
  font-size: 12px;
}

.agent-actions {
  display: flex;
  gap: 8px;
}

.capabilities-editor {
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 12px;
  background: #fafafa;
  min-height: 60px;
}
</style>
