<template>
  <div class="entity-management">
    <el-card class="filter-card">
      <template #header>
        <div class="card-header">
          <span>🏷️ 实体管理</span>
          <div class="header-actions">
            <el-select 
              v-model="selectedEntityType" 
              placeholder="选择实体类型" 
              style="width: 200px; margin-right: 10px"
              @change="loadEntities"
            >
              <el-option label="全部类型" value="" />
              <el-option label="产品 (Product)" value="product" />
              <el-option label="组件 (Component)" value="component" />
              <el-option label="测试用例 (TestCase)" value="test_case" />
              <el-option label="异常 (Anomaly)" value="anomaly" />
              <el-option label="症状 (Symptom)" value="symptom" />
              <el-option label="根因 (RootCause)" value="root_cause" />
              <el-option label="对策 (Countermeasure)" value="countermeasure" />
            </el-select>
            <el-button type="primary" @click="loadEntities" :loading="loading">
              刷新数据
            </el-button>
          </div>
        </div>
      </template>

      <!-- 统计信息 -->
      <el-row :gutter="20" class="stats-row">
        <el-col :span="6">
          <el-statistic title="总实体数" :value="totalEntities" />
        </el-col>
        <el-col :span="6">
          <el-statistic title="当前显示" :value="entities.length" />
        </el-col>
        <el-col :span="6">
          <el-statistic title="实体类型" :value="Object.keys(entityTypeStats).length" />
        </el-col>
        <el-col :span="6">
          <el-statistic title="数据源文件" :value="sourceFiles.size" />
        </el-col>
      </el-row>
    </el-card>

    <!-- 实体类型统计 -->
    <el-card class="stats-card" v-if="Object.keys(entityTypeStats).length > 0">
      <template #header>
        <span>📊 实体类型分布</span>
      </template>
      <el-row :gutter="20">
        <el-col :span="4" v-for="(count, type) in entityTypeStats" :key="type">
          <div class="type-stat">
            <div class="type-name">{{ formatEntityType(type) }}</div>
            <div class="type-count">{{ count }}</div>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <!-- 实体列表 -->
    <el-card class="entity-list-card">
      <template #header>
        <span>📋 实体列表</span>
      </template>

      <el-table 
        :data="entities" 
        v-loading="loading" 
        style="width: 100%"
        :default-sort="{prop: 'name', order: 'ascending'}"
      >
        <el-table-column prop="name" label="实体名称" min-width="200" sortable>
          <template #default="scope">
            <div class="entity-name">
              <el-icon style="margin-right: 8px" :color="getEntityTypeColor(scope.row.type)">
                <component :is="getEntityTypeIcon(scope.row.type)" />
              </el-icon>
              {{ scope.row.name }}
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="type" label="类型" width="150" sortable>
          <template #default="scope">
            <el-tag :type="getEntityTypeTagType(scope.row.type)">
              {{ formatEntityType(scope.row.type) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="source_file" label="数据源" min-width="200" sortable>
          <template #default="scope">
            <el-tooltip :content="scope.row.source_file" placement="top">
              <span class="source-file">
                {{ getFileName(scope.row.source_file) }}
              </span>
            </el-tooltip>
          </template>
        </el-table-column>
        
        <el-table-column label="属性数量" width="100">
          <template #default="scope">
            <el-tag size="small">
              {{ Object.keys(scope.row.properties || {}).length }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button 
              type="primary" 
              size="small" 
              @click="viewEntityDetails(scope.row)"
            >
              查看详情
            </el-button>
            <el-button 
              type="info" 
              size="small" 
              @click="viewEntityRelations(scope.row)"
            >
              查看关系
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[20, 50, 100, 200]"
          :total="totalEntities"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 实体详情对话框 -->
    <el-dialog 
      v-model="detailDialogVisible" 
      title="实体详情" 
      width="70%"
      :close-on-click-modal="false"
    >
      <div v-if="selectedEntity">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="实体ID">
            {{ selectedEntity.id }}
          </el-descriptions-item>
          <el-descriptions-item label="实体名称">
            {{ selectedEntity.name }}
          </el-descriptions-item>
          <el-descriptions-item label="实体类型">
            <el-tag :type="getEntityTypeTagType(selectedEntity.type)">
              {{ formatEntityType(selectedEntity.type) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="数据源文件">
            {{ selectedEntity.source_file }}
          </el-descriptions-item>
        </el-descriptions>

        <el-divider>实体属性</el-divider>
        <el-descriptions :column="1" border v-if="selectedEntity.properties">
          <el-descriptions-item 
            v-for="(value, key) in selectedEntity.properties" 
            :key="key" 
            :label="key"
          >
            <div class="property-value">
              {{ formatPropertyValue(value) }}
            </div>
          </el-descriptions-item>
        </el-descriptions>
        <el-empty v-else description="暂无属性信息" />
      </div>
    </el-dialog>

    <!-- 实体关系对话框 -->
    <el-dialog 
      v-model="relationDialogVisible" 
      title="实体关系" 
      width="80%"
      :close-on-click-modal="false"
    >
      <div v-if="selectedEntity">
        <el-tabs v-model="activeRelationTab">
          <el-tab-pane label="出度关系" name="outgoing">
            <el-table :data="outgoingRelations" style="width: 100%">
              <el-table-column prop="target_entity" label="目标实体" />
              <el-table-column prop="relation_type" label="关系类型">
                <template #default="scope">
                  <el-tag>{{ scope.row.relation_type }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="confidence" label="置信度" width="100">
                <template #default="scope">
                  <el-progress 
                    :percentage="Math.round(scope.row.confidence * 100)" 
                    :stroke-width="6"
                    :show-text="false"
                  />
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
          
          <el-tab-pane label="入度关系" name="incoming">
            <el-table :data="incomingRelations" style="width: 100%">
              <el-table-column prop="source_entity" label="源实体" />
              <el-table-column prop="relation_type" label="关系类型">
                <template #default="scope">
                  <el-tag>{{ scope.row.relation_type }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="confidence" label="置信度" width="100">
                <template #default="scope">
                  <el-progress 
                    :percentage="Math.round(scope.row.confidence * 100)" 
                    :stroke-width="6"
                    :show-text="false"
                  />
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { 
  List, 
  Document, 
  Warning, 
  Setting, 
  Tools,
  Connection
} from '@element-plus/icons-vue'
import { kgApi } from '../api'

export default {
  name: 'EntityManagement',
  components: {
    List,
    Document,
    Warning,
    Setting,
    Tools,
    Connection
  },
  setup() {
    const entities = ref([])
    const loading = ref(false)
    const selectedEntityType = ref('')
    const currentPage = ref(1)
    const pageSize = ref(50)
    const totalEntities = ref(0)
    
    const detailDialogVisible = ref(false)
    const relationDialogVisible = ref(false)
    const selectedEntity = ref(null)
    const activeRelationTab = ref('outgoing')
    
    const outgoingRelations = ref([])
    const incomingRelations = ref([])
    
    // 统计信息
    const entityTypeStats = ref({})
    const sourceFiles = computed(() => {
      const files = new Set()
      entities.value.forEach(entity => {
        if (entity.source_file) {
          files.add(entity.source_file)
        }
      })
      return files
    })

    // 加载实体数据
    const loadEntities = async () => {
      loading.value = true
      try {
        const limit = pageSize.value * 10 // 加载更多数据用于统计
        const entityType = selectedEntityType.value || null

        const response = await kgApi.getEntities(entityType, limit)
        entities.value = response.entities || []
        totalEntities.value = response.count || 0

        // 计算类型统计
        calculateTypeStats()

      } catch (error) {
        ElMessage.error('加载实体数据失败: ' + error.message)
      } finally {
        loading.value = false
      }
    }

    // 计算类型统计
    const calculateTypeStats = () => {
      const stats = {}
      entities.value.forEach(entity => {
        stats[entity.type] = (stats[entity.type] || 0) + 1
      })
      entityTypeStats.value = stats
    }

    // 查看实体详情
    const viewEntityDetails = (entity) => {
      selectedEntity.value = entity
      detailDialogVisible.value = true
    }

    // 查看实体关系
    const viewEntityRelations = async (entity) => {
      selectedEntity.value = entity
      
      try {
        // 获取出度关系
        const outgoingResponse = await kgApi.queryGraph(`
          MATCH (source:Entity {id: $entity_id})-[r]->(target:Entity)
          RETURN target.id as target_entity, type(r) as relation_type,
                 r.confidence as confidence, target.name as target_name
        `, { entity_id: entity.id })
        outgoingRelations.value = outgoingResponse.results || []

        // 获取入度关系
        const incomingResponse = await kgApi.queryGraph(`
          MATCH (source:Entity)-[r]->(target:Entity {id: $entity_id})
          RETURN source.id as source_entity, type(r) as relation_type,
                 r.confidence as confidence, source.name as source_name
        `, { entity_id: entity.id })
        incomingRelations.value = incomingResponse.results || []

        relationDialogVisible.value = true

      } catch (error) {
        ElMessage.error('获取实体关系失败: ' + error.message)
      }
    }

    // 分页处理
    const handleSizeChange = (val) => {
      pageSize.value = val
      loadEntities()
    }

    const handleCurrentChange = (val) => {
      currentPage.value = val
      loadEntities()
    }

    // 工具函数
    const formatEntityType = (type) => {
      const typeMap = {
        'product': '产品',
        'component': '组件',
        'test_case': '测试用例',
        'anomaly': '异常',
        'symptom': '症状',
        'root_cause': '根因',
        'countermeasure': '对策'
      }
      return typeMap[type] || type
    }

    const getEntityTypeColor = (type) => {
      const colorMap = {
        'product': '#409EFF',
        'component': '#67C23A',
        'test_case': '#E6A23C',
        'anomaly': '#F56C6C',
        'symptom': '#909399',
        'root_cause': '#F56C6C',
        'countermeasure': '#67C23A'
      }
      return colorMap[type] || '#909399'
    }

    const getEntityTypeTagType = (type) => {
      const tagMap = {
        'product': 'primary',
        'component': 'success',
        'test_case': 'warning',
        'anomaly': 'danger',
        'symptom': 'info',
        'root_cause': 'danger',
        'countermeasure': 'success'
      }
      return tagMap[type] || ''
    }

    const getEntityTypeIcon = (type) => {
      const iconMap = {
        'product': 'List',
        'component': 'Setting',
        'test_case': 'Document',
        'anomaly': 'Warning',
        'symptom': 'Warning',
        'root_cause': 'Warning',
        'countermeasure': 'Tools'
      }
      return iconMap[type] || 'Document'
    }

    const getFileName = (filePath) => {
      if (!filePath) return ''
      return filePath.split('/').pop() || filePath
    }

    const formatPropertyValue = (value) => {
      if (Array.isArray(value)) {
        return value.join(', ')
      }
      if (typeof value === 'object') {
        return JSON.stringify(value, null, 2)
      }
      return String(value)
    }

    onMounted(() => {
      loadEntities()
    })

    return {
      entities,
      loading,
      selectedEntityType,
      currentPage,
      pageSize,
      totalEntities,
      detailDialogVisible,
      relationDialogVisible,
      selectedEntity,
      activeRelationTab,
      outgoingRelations,
      incomingRelations,
      entityTypeStats,
      sourceFiles,
      loadEntities,
      viewEntityDetails,
      viewEntityRelations,
      handleSizeChange,
      handleCurrentChange,
      formatEntityType,
      getEntityTypeColor,
      getEntityTypeTagType,
      getEntityTypeIcon,
      getFileName,
      formatPropertyValue
    }
  }
}
</script>

<style scoped>
.entity-management {
  padding: 20px;
}

.filter-card, .stats-card, .entity-list-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  align-items: center;
}

.stats-row {
  margin-top: 20px;
}

.type-stat {
  text-align: center;
  padding: 10px;
  border: 1px solid #EBEEF5;
  border-radius: 4px;
}

.type-name {
  font-size: 12px;
  color: #909399;
  margin-bottom: 5px;
}

.type-count {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.entity-name {
  display: flex;
  align-items: center;
}

.source-file {
  color: #606266;
  font-size: 12px;
  cursor: pointer;
}

.pagination-wrapper {
  margin-top: 20px;
  text-align: center;
}

.property-value {
  max-width: 400px;
  word-break: break-all;
  white-space: pre-wrap;
}
</style>
