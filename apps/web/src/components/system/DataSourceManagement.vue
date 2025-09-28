<template>
  <div class="datasource-management">
    <!-- 页面头部 -->
    <div class="management-header">
      <div class="header-left">
        <h2 class="module-title">
          <el-icon><Coin /></el-icon>
          数据源管理
        </h2>
        <p class="module-description">管理系统中的各种数据源配置和连接状态</p>
      </div>
      <div class="header-actions">
        <el-button type="primary" @click="showAddDialog">
          <el-icon><Plus /></el-icon>
          新增数据源
        </el-button>
        <el-button @click="refreshData">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
        <el-button @click="testAllConnections">
          <el-icon><Connection /></el-icon>
          测试连接
        </el-button>
      </div>
    </div>

    <!-- 数据源统计 -->
    <div class="stats-overview">
      <el-row :gutter="16">
        <el-col :span="6">
          <div class="stat-item">
            <div class="stat-value">{{ stats.total }}</div>
            <div class="stat-label">总数据源</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-item active">
            <div class="stat-value">{{ stats.active }}</div>
            <div class="stat-label">活跃连接</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-item error">
            <div class="stat-value">{{ stats.error }}</div>
            <div class="stat-label">连接异常</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-item">
            <div class="stat-value">{{ stats.lastSync }}</div>
            <div class="stat-label">最后同步</div>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 数据源列表 -->
    <div class="datasource-list">
      <el-table :data="dataSources" v-loading="loading" stripe>
        <el-table-column prop="name" label="数据源名称" min-width="150" />
        <el-table-column prop="type" label="类型" width="120">
          <template #default="{ row }">
            <el-tag :type="getTypeColor(row.type)">
              {{ getTypeText(row.type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="host" label="主机地址" min-width="200" />
        <el-table-column prop="status" label="连接状态" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusColor(row.status)">
              <el-icon><CircleCheck v-if="row.status === 'connected'" /><CircleClose v-else /></el-icon>
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="lastSync" label="最后同步" width="160" />
        <el-table-column prop="dataCount" label="数据量" width="100" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="testConnection(row)">
              <el-icon><Connection /></el-icon>
              测试
            </el-button>
            <el-button size="small" type="primary" @click="editDataSource(row)">
              编辑
            </el-button>
            <el-button size="small" type="danger" @click="deleteDataSource(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 新增/编辑数据源对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑数据源' : '新增数据源'"
      width="600px"
      @close="resetForm"
    >
      <el-form :model="dataSourceForm" :rules="formRules" ref="formRef" label-width="100px">
        <el-form-item label="数据源名称" prop="name">
          <el-input v-model="dataSourceForm.name" placeholder="请输入数据源名称" />
        </el-form-item>
        <el-form-item label="数据源类型" prop="type">
          <el-select v-model="dataSourceForm.type" placeholder="请选择数据源类型">
            <el-option label="MySQL" value="mysql" />
            <el-option label="PostgreSQL" value="postgresql" />
            <el-option label="MongoDB" value="mongodb" />
            <el-option label="Redis" value="redis" />
            <el-option label="Elasticsearch" value="elasticsearch" />
            <el-option label="Neo4j" value="neo4j" />
            <el-option label="API接口" value="api" />
            <el-option label="文件系统" value="filesystem" />
          </el-select>
        </el-form-item>
        <el-form-item label="主机地址" prop="host">
          <el-input v-model="dataSourceForm.host" placeholder="如: localhost:3306" />
        </el-form-item>
        <el-form-item label="数据库名" prop="database" v-if="needsDatabase">
          <el-input v-model="dataSourceForm.database" placeholder="请输入数据库名" />
        </el-form-item>
        <el-form-item label="用户名" prop="username" v-if="needsAuth">
          <el-input v-model="dataSourceForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="needsAuth">
          <el-input v-model="dataSourceForm.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
        <el-form-item label="连接配置" prop="config">
          <el-input
            v-model="dataSourceForm.config"
            type="textarea"
            :rows="4"
            placeholder="JSON格式的额外配置参数"
          />
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="dataSourceForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入数据源描述"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveDataSource" :loading="saving">
            {{ isEdit ? '更新' : '创建' }}
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import {
  Coin,
  Plus,
  Refresh,
  Connection,
  CircleCheck,
  CircleClose
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'DataSourceManagement',
  components: {
    Coin,
    Plus,
    Refresh,
    Connection,
    CircleCheck,
    CircleClose
  },
  setup() {
    // 响应式数据
    const loading = ref(false)
    const dialogVisible = ref(false)
    const isEdit = ref(false)
    const saving = ref(false)
    const dataSources = ref([])
    
    // 统计数据
    const stats = reactive({
      total: 0,
      active: 0,
      error: 0,
      lastSync: '2小时前'
    })

    // 表单数据
    const dataSourceForm = reactive({
      id: '',
      name: '',
      type: '',
      host: '',
      database: '',
      username: '',
      password: '',
      config: '',
      description: ''
    })

    // 表单验证规则
    const formRules = {
      name: [{ required: true, message: '请输入数据源名称', trigger: 'blur' }],
      type: [{ required: true, message: '请选择数据源类型', trigger: 'change' }],
      host: [{ required: true, message: '请输入主机地址', trigger: 'blur' }]
    }

    // 组件引用
    const formRef = ref(null)

    // 计算属性
    const needsDatabase = computed(() => {
      return ['mysql', 'postgresql', 'mongodb'].includes(dataSourceForm.type)
    })

    const needsAuth = computed(() => {
      return !['filesystem'].includes(dataSourceForm.type)
    })

    // 方法
    const refreshData = async () => {
      loading.value = true
      try {
        // 模拟数据
        dataSources.value = [
          {
            id: 'ds001',
            name: '主数据库',
            type: 'mysql',
            host: 'localhost:3306',
            database: 'quality_kg',
            status: 'connected',
            lastSync: '2024-01-20 15:30:00',
            dataCount: '1.2M'
          },
          {
            id: 'ds002',
            name: '文档存储',
            type: 'mongodb',
            host: 'localhost:27017',
            database: 'documents',
            status: 'connected',
            lastSync: '2024-01-20 15:25:00',
            dataCount: '856K'
          },
          {
            id: 'ds003',
            name: '图数据库',
            type: 'neo4j',
            host: 'localhost:7687',
            database: 'neo4j',
            status: 'error',
            lastSync: '2024-01-20 14:20:00',
            dataCount: '324K'
          }
        ]
        
        // 更新统计
        stats.total = dataSources.value.length
        stats.active = dataSources.value.filter(ds => ds.status === 'connected').length
        stats.error = dataSources.value.filter(ds => ds.status === 'error').length
        
      } catch (error) {
        console.error('获取数据源列表失败:', error)
        ElMessage.error('获取数据源列表失败')
      } finally {
        loading.value = false
      }
    }

    const getTypeColor = (type) => {
      const colors = {
        mysql: 'primary',
        postgresql: 'success',
        mongodb: 'warning',
        redis: 'danger',
        elasticsearch: 'info',
        neo4j: 'primary',
        api: 'success',
        filesystem: 'warning'
      }
      return colors[type] || ''
    }

    const getTypeText = (type) => {
      const texts = {
        mysql: 'MySQL',
        postgresql: 'PostgreSQL',
        mongodb: 'MongoDB',
        redis: 'Redis',
        elasticsearch: 'Elasticsearch',
        neo4j: 'Neo4j',
        api: 'API接口',
        filesystem: '文件系统'
      }
      return texts[type] || type
    }

    const getStatusColor = (status) => {
      return status === 'connected' ? 'success' : 'danger'
    }

    const getStatusText = (status) => {
      return status === 'connected' ? '已连接' : '连接异常'
    }

    // 显示新增对话框
    const showAddDialog = () => {
      isEdit.value = false
      dialogVisible.value = true
      // 重置表单
      Object.assign(dataSourceForm, {
        id: '',
        name: '',
        type: '',
        host: '',
        database: '',
        username: '',
        password: '',
        config: '',
        description: ''
      })
    }

    // 测试所有连接
    const testAllConnections = async () => {
      loading.value = true
      try {
        // 模拟测试所有连接
        for (let i = 0; i < dataSources.value.length; i++) {
          const source = dataSources.value[i]
          // 模拟连接测试
          await new Promise(resolve => setTimeout(resolve, 500))
          source.status = Math.random() > 0.2 ? 'connected' : 'error'
        }
        ElMessage.success('连接测试完成')
      } catch (error) {
        ElMessage.error('连接测试失败')
      } finally {
        loading.value = false
      }
    }

    // 重置表单
    const resetForm = () => {
      formRef.value?.resetFields()
      Object.assign(dataSourceForm, {
        id: '',
        name: '',
        type: 'mysql',
        host: '',
        port: 3306,
        database: '',
        username: '',
        password: '',
        description: ''
      })
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
      dataSources,
      stats,
      dataSourceForm,
      formRules,
      formRef,
      needsDatabase,
      needsAuth,
      refreshData,
      testAllConnections,
      resetForm,
      getTypeColor,
      getTypeText,
      getStatusColor,
      getStatusText,
      showAddDialog
    }
  }
}
</script>

<style scoped>
.datasource-management {
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

.stats-overview {
  margin-bottom: 24px;
}

.stat-item {
  text-align: center;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #e9ecef;
}

.stat-item.active {
  border-left-color: #67c23a;
}

.stat-item.error {
  border-left-color: #f56c6c;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.datasource-list {
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
