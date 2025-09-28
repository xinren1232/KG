<template>
  <div class="monitoring-management">
    <!-- 页面头部 -->
    <div class="management-header">
      <div class="header-left">
        <h2 class="module-title">
          <el-icon><Monitor /></el-icon>
          监控告警管理
        </h2>
        <p class="module-description">配置系统监控指标和告警规则</p>
      </div>
      <div class="header-actions">
        <el-button type="primary" @click="showAddDialog">
          <el-icon><Plus /></el-icon>
          新增告警规则
        </el-button>
        <el-button @click="refreshData">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
        <el-button @click="testAllRules">
          <el-icon><Bell /></el-icon>
          测试告警
        </el-button>
      </div>
    </div>

    <!-- 系统健康状态 -->
    <div class="health-overview">
      <el-row :gutter="16">
        <el-col :span="6">
          <div class="health-card">
            <div class="health-icon cpu">
              <el-icon><Cpu /></el-icon>
            </div>
            <div class="health-content">
              <div class="health-value">{{ systemHealth.cpu }}%</div>
              <div class="health-label">CPU使用率</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="health-card">
            <div class="health-icon memory">
              <el-icon><Memo /></el-icon>
            </div>
            <div class="health-content">
              <div class="health-value">{{ systemHealth.memory }}%</div>
              <div class="health-label">内存使用率</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="health-card">
            <div class="health-icon disk">
              <el-icon><FolderOpened /></el-icon>
            </div>
            <div class="health-content">
              <div class="health-value">{{ systemHealth.disk }}%</div>
              <div class="health-label">磁盘使用率</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="health-card">
            <div class="health-icon network">
              <el-icon><Connection /></el-icon>
            </div>
            <div class="health-content">
              <div class="health-value">{{ systemHealth.network }}</div>
              <div class="health-label">网络状态</div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 告警规则列表 -->
    <div class="rules-section">
      <h3 class="section-title">告警规则</h3>
      <el-table :data="alertRules" v-loading="loading" stripe>
        <el-table-column prop="name" label="规则名称" min-width="150" />
        <el-table-column prop="metric" label="监控指标" width="120" />
        <el-table-column prop="condition" label="触发条件" min-width="150" />
        <el-table-column prop="threshold" label="阈值" width="100" />
        <el-table-column prop="severity" label="严重程度" width="100">
          <template #default="{ row }">
            <el-tag :type="getSeverityColor(row.severity)">
              {{ getSeverityText(row.severity) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-switch
              v-model="row.status"
              active-value="enabled"
              inactive-value="disabled"
              @change="updateRuleStatus(row)"
            />
          </template>
        </el-table-column>
        <el-table-column prop="lastTriggered" label="最后触发" width="160" />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="testRule(row)">
              <el-icon><Bell /></el-icon>
              测试
            </el-button>
            <el-button size="small" type="primary" @click="editRule(row)">
              编辑
            </el-button>
            <el-button size="small" type="danger" @click="deleteRule(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 最近告警 -->
    <div class="alerts-section">
      <h3 class="section-title">最近告警</h3>
      <el-table :data="recentAlerts" stripe>
        <el-table-column prop="time" label="时间" width="160" />
        <el-table-column prop="rule" label="规则" min-width="150" />
        <el-table-column prop="message" label="告警信息" min-width="200" />
        <el-table-column prop="severity" label="严重程度" width="100">
          <template #default="{ row }">
            <el-tag :type="getSeverityColor(row.severity)">
              {{ getSeverityText(row.severity) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getAlertStatusColor(row.status)">
              {{ getAlertStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button size="small" @click="acknowledgeAlert(row)" v-if="row.status === 'active'">
              确认
            </el-button>
            <el-button size="small" @click="resolveAlert(row)" v-if="row.status === 'acknowledged'">
              解决
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 新增/编辑告警规则对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑告警规则' : '新增告警规则'"
      width="600px"
      @close="resetForm"
    >
      <el-form :model="ruleForm" :rules="formRules" ref="formRef" label-width="100px">
        <el-form-item label="规则名称" prop="name">
          <el-input v-model="ruleForm.name" placeholder="请输入规则名称" />
        </el-form-item>
        <el-form-item label="监控指标" prop="metric">
          <el-select v-model="ruleForm.metric" placeholder="请选择监控指标">
            <el-option label="CPU使用率" value="cpu_usage" />
            <el-option label="内存使用率" value="memory_usage" />
            <el-option label="磁盘使用率" value="disk_usage" />
            <el-option label="网络延迟" value="network_latency" />
            <el-option label="API响应时间" value="api_response_time" />
            <el-option label="错误率" value="error_rate" />
            <el-option label="并发用户数" value="concurrent_users" />
          </el-select>
        </el-form-item>
        <el-form-item label="触发条件" prop="condition">
          <el-select v-model="ruleForm.condition" placeholder="请选择触发条件">
            <el-option label="大于" value="gt" />
            <el-option label="大于等于" value="gte" />
            <el-option label="小于" value="lt" />
            <el-option label="小于等于" value="lte" />
            <el-option label="等于" value="eq" />
            <el-option label="不等于" value="ne" />
          </el-select>
        </el-form-item>
        <el-form-item label="阈值" prop="threshold">
          <el-input-number v-model="ruleForm.threshold" :min="0" :max="100" />
        </el-form-item>
        <el-form-item label="严重程度" prop="severity">
          <el-select v-model="ruleForm.severity" placeholder="请选择严重程度">
            <el-option label="低" value="low" />
            <el-option label="中" value="medium" />
            <el-option label="高" value="high" />
            <el-option label="紧急" value="critical" />
          </el-select>
        </el-form-item>
        <el-form-item label="通知方式">
          <el-checkbox-group v-model="ruleForm.notifications">
            <el-checkbox label="email">邮件</el-checkbox>
            <el-checkbox label="sms">短信</el-checkbox>
            <el-checkbox label="webhook">Webhook</el-checkbox>
            <el-checkbox label="slack">Slack</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="ruleForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入规则描述"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveRule" :loading="saving">
            {{ isEdit ? '更新' : '创建' }}
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import {
  Monitor,
  Plus,
  Refresh,
  Bell,
  Cpu,
  Memo,
  FolderOpened,
  Connection
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'MonitoringManagement',
  components: {
    Monitor,
    Plus,
    Refresh,
    Bell,
    Cpu,
    Memo,
    FolderOpened,
    Connection
  },
  setup() {
    // 响应式数据
    const loading = ref(false)
    const dialogVisible = ref(false)
    const isEdit = ref(false)
    const saving = ref(false)
    const alertRules = ref([])
    const recentAlerts = ref([])
    
    // 系统健康状态
    const systemHealth = reactive({
      cpu: 45,
      memory: 68,
      disk: 32,
      network: '正常'
    })

    // 表单数据
    const ruleForm = reactive({
      id: '',
      name: '',
      metric: '',
      condition: '',
      threshold: 80,
      severity: 'medium',
      notifications: ['email'],
      description: ''
    })

    // 表单验证规则
    const formRules = {
      name: [{ required: true, message: '请输入规则名称', trigger: 'blur' }],
      metric: [{ required: true, message: '请选择监控指标', trigger: 'change' }],
      condition: [{ required: true, message: '请选择触发条件', trigger: 'change' }],
      threshold: [{ required: true, message: '请输入阈值', trigger: 'blur' }],
      severity: [{ required: true, message: '请选择严重程度', trigger: 'change' }]
    }

    // 组件引用
    const formRef = ref(null)

    // 方法
    const refreshData = async () => {
      loading.value = true
      try {
        // 模拟数据
        alertRules.value = [
          {
            id: 'rule001',
            name: 'CPU使用率过高',
            metric: 'cpu_usage',
            condition: 'gt',
            threshold: 80,
            severity: 'high',
            status: 'enabled',
            lastTriggered: '2024-01-20 14:30:00'
          },
          {
            id: 'rule002',
            name: '内存使用率告警',
            metric: 'memory_usage',
            condition: 'gt',
            threshold: 85,
            severity: 'medium',
            status: 'enabled',
            lastTriggered: '从未触发'
          }
        ]

        recentAlerts.value = [
          {
            id: 'alert001',
            time: '2024-01-20 14:30:00',
            rule: 'CPU使用率过高',
            message: 'CPU使用率达到85%，超过阈值80%',
            severity: 'high',
            status: 'resolved'
          },
          {
            id: 'alert002',
            time: '2024-01-20 13:15:00',
            rule: 'API响应时间过长',
            message: 'API平均响应时间2.5秒，超过阈值2秒',
            severity: 'medium',
            status: 'acknowledged'
          }
        ]
        
      } catch (error) {
        console.error('获取监控数据失败:', error)
        ElMessage.error('获取监控数据失败')
      } finally {
        loading.value = false
      }
    }

    const getSeverityColor = (severity) => {
      const colors = {
        low: 'info',
        medium: 'warning',
        high: 'danger',
        critical: 'danger'
      }
      return colors[severity] || 'info'
    }

    const getSeverityText = (severity) => {
      const texts = {
        low: '低',
        medium: '中',
        high: '高',
        critical: '紧急'
      }
      return texts[severity] || severity
    }

    const getAlertStatusColor = (status) => {
      const colors = {
        active: 'danger',
        acknowledged: 'warning',
        resolved: 'success'
      }
      return colors[status] || 'info'
    }

    const getAlertStatusText = (status) => {
      const texts = {
        active: '活跃',
        acknowledged: '已确认',
        resolved: '已解决'
      }
      return texts[status] || status
    }

    // 测试所有告警规则
    const testAllRules = async () => {
      try {
        ElMessage.info('正在测试所有告警规则...')
        // 这里应该调用后端API测试告警规则
        // await api.testAllAlertRules()

        // 模拟测试结果
        setTimeout(() => {
          ElMessage.success('告警规则测试完成')
        }, 1000)
      } catch (error) {
        console.error('测试告警规则失败:', error)
        ElMessage.error('测试告警规则失败')
      }
    }

    // 显示新增对话框
    const showAddDialog = () => {
      isEdit.value = false
      dialogVisible.value = true
      resetForm()
    }

    // 重置表单
    const resetForm = () => {
      formRef.value?.resetFields()
      ruleForm.value = {
        name: '',
        metric: '',
        condition: 'gt',
        threshold: '',
        severity: 'medium',
        status: 'enabled'
      }
      isEdit.value = false
    }

    // 生命周期
    onMounted(() => {
      refreshData()
    })

    return {
      loading,
      dialogVisible,
      isEdit,
      saving,
      alertRules,
      recentAlerts,
      systemHealth,
      ruleForm,
      formRules,
      formRef,
      refreshData,
      showAddDialog,
      getSeverityColor,
      getSeverityText,
      getAlertStatusColor,
      getAlertStatusText,
      testAllRules,
      resetForm
    }
  }
}
</script>

<style scoped>
.monitoring-management {
  padding: 0;
}

.management-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}

.header-left {
  flex: 1;
}

.module-title {
  display: flex;
  align-items: center;
  font-size: 20px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 8px 0;
}

.module-title .el-icon {
  margin-right: 8px;
  color: #409EFF;
}

.module-description {
  color: #606266;
  margin: 0;
  font-size: 14px;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.health-overview {
  margin-bottom: 24px;
}

.health-card {
  display: flex;
  align-items: center;
  padding: 16px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.health-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
  font-size: 18px;
  color: white;
}

.health-icon.cpu {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.health-icon.memory {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.health-icon.disk {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.health-icon.network {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.health-content {
  flex: 1;
}

.health-value {
  font-size: 20px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 4px;
}

.health-label {
  font-size: 14px;
  color: #909399;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 16px 0;
}

.rules-section,
.alerts-section {
  margin-bottom: 24px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
