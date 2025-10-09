<template>
  <div class="graph-schema">
    <div class="schema-header">
      <div>
        <h2>🕸️ 知识图谱Schema设计</h2>
        <p class="description">展示图谱的节点类型、关系类型和设计逻辑</p>
      </div>
      <el-button type="primary" @click="refreshData" :loading="loading">
        <el-icon><Refresh /></el-icon>
        刷新数据
      </el-button>
    </div>

    <!-- 统计概览 -->
    <el-row :gutter="20" class="stats-overview">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="stat-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
              <el-icon><Connection /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ stats.totalNodes }}</div>
              <div class="stat-label">节点总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="stat-icon" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
              <el-icon><Share /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ stats.totalRelationships }}</div>
              <div class="stat-label">关系总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="stat-icon" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
              <el-icon><Grid /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ nodeTypes.length }}</div>
              <div class="stat-label">节点类型</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="stat-icon" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
              <el-icon><Link /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ relationshipTypes.length }}</div>
              <div class="stat-label">关系类型</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 节点类型 -->
    <el-card class="node-types-card" shadow="hover">
      <template #header>
        <span><el-icon><Grid /></el-icon> 节点类型 (Node Types)</span>
      </template>
      <el-table :data="nodeTypes" style="width: 100%" v-loading="loading">
        <el-table-column type="index" label="#" width="60" />
        <el-table-column prop="label" label="节点类型" min-width="150">
          <template #default="{ row }">
            <el-tag :type="getNodeTypeColor(row.label)" effect="dark" size="large">
              {{ row.label }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="count" label="数量" width="120" sortable>
          <template #default="{ row }">
            <el-badge :value="row.count" :max="9999" class="item">
              <el-button size="small">节点</el-button>
            </el-badge>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" min-width="200" />
        <el-table-column prop="properties" label="主要属性" min-width="200">
          <template #default="{ row }">
            <el-tag
              v-for="prop in row.properties"
              :key="prop"
              size="small"
              class="property-tag"
            >
              {{ prop }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button size="small" type="primary" @click="viewNodeDetails(row)">
              查看详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 关系类型 -->
    <el-card class="relationship-types-card" shadow="hover">
      <template #header>
        <span><el-icon><Share /></el-icon> 关系类型 (Relationship Types)</span>
      </template>
      <el-table :data="relationshipTypes" style="width: 100%" v-loading="loading">
        <el-table-column type="index" label="#" width="60" />
        <el-table-column prop="type" label="关系类型" min-width="180">
          <template #default="{ row }">
            <el-tag :type="getRelationshipTypeColor(row.type)" effect="plain" size="large">
              {{ row.type }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="count" label="数量" width="120" sortable>
          <template #default="{ row }">
            <span class="count-badge">{{ row.count }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="pattern" label="关系模式" min-width="250">
          <template #default="{ row }">
            <code class="relationship-pattern">{{ row.pattern }}</code>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="语义描述" min-width="200" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button size="small" type="primary" @click="viewRelationshipDetails(row)">
              查看详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- Schema可视化 -->
    <el-card class="schema-visualization" shadow="hover">
      <template #header>
        <span><el-icon><PieChart /></el-icon> Schema可视化</span>
      </template>
      <div ref="schemaChartRef" style="height: 500px;"></div>
    </el-card>

    <!-- 设计说明 -->
    <el-card class="design-notes" shadow="hover">
      <template #header>
        <span><el-icon><Document /></el-icon> 图谱Schema设计说明</span>
      </template>
      <el-descriptions :column="1" border>
        <el-descriptions-item label="设计目的">
          构建质量知识图谱，支持产品、组件、异常、测试用例等实体的关联分析和知识推理
        </el-descriptions-item>
        <el-descriptions-item label="核心节点类型">
          <div class="node-type-list">
            <el-tag type="success" class="entity-tag">Term (术语)</el-tag>
            <el-tag type="warning" class="entity-tag">Category (分类)</el-tag>
            <el-tag type="danger" class="entity-tag">Tag (标签)</el-tag>
            <el-tag type="info" class="entity-tag">Alias (别名)</el-tag>
            <el-tag type="primary" class="entity-tag">Component (组件)</el-tag>
            <el-tag class="entity-tag">Symptom (症状)</el-tag>
            <el-tag class="entity-tag">Tool (工具)</el-tag>
            <el-tag class="entity-tag">Process (流程)</el-tag>
          </div>
        </el-descriptions-item>
        <el-descriptions-item label="核心关系类型">
          <div class="relationship-type-list">
            <div class="rel-item">
              <code>HAS_TAG</code>
              <span>术语具有标签</span>
              <el-tag size="small">{{ getRelationshipCount('HAS_TAG') }}</el-tag>
            </div>
            <div class="rel-item">
              <code>ALIAS_OF</code>
              <span>别名指向术语</span>
              <el-tag size="small">{{ getRelationshipCount('ALIAS_OF') }}</el-tag>
            </div>
            <div class="rel-item">
              <code>BELONGS_TO</code>
              <span>术语归属分类</span>
              <el-tag size="small">{{ getRelationshipCount('BELONGS_TO') }}</el-tag>
            </div>
            <div class="rel-item">
              <code>AFFECTS</code>
              <span>影响关系</span>
              <el-tag size="small">{{ getRelationshipCount('AFFECTS') }}</el-tag>
            </div>
            <div class="rel-item">
              <code>USED_IN</code>
              <span>使用关系</span>
              <el-tag size="small">{{ getRelationshipCount('USED_IN') }}</el-tag>
            </div>
          </div>
        </el-descriptions-item>
        <el-descriptions-item label="图谱特点">
          <ul class="feature-list">
            <li>✅ 多类型节点支持复杂业务场景</li>
            <li>✅ 丰富的关系类型支持知识推理</li>
            <li>✅ 别名机制提升查询覆盖率</li>
            <li>✅ 标签体系支持多维度分类</li>
            <li>✅ 可扩展的Schema设计</li>
          </ul>
        </el-descriptions-item>
        <el-descriptions-item label="应用场景">
          <el-tag type="success" class="scenario-tag">知识检索</el-tag>
          <el-tag type="warning" class="scenario-tag">关联分析</el-tag>
          <el-tag type="danger" class="scenario-tag">根因分析</el-tag>
          <el-tag type="info" class="scenario-tag">智能问答</el-tag>
          <el-tag type="primary" class="scenario-tag">知识推理</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="扩展性">
          支持动态添加新节点类型、新关系类型，支持属性扩展和索引优化
        </el-descriptions-item>
      </el-descriptions>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Refresh,
  Connection,
  Share,
  Grid,
  Link,
  Document,
  PieChart
} from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import { httpClient as api } from '@/api'

// 响应式数据
const loading = ref(false)
const schemaChartRef = ref(null)

const stats = reactive({
  totalNodes: 0,
  totalRelationships: 0
})

const nodeTypes = ref([
  {
    label: 'Term',
    count: 0,
    description: '质量术语节点',
    properties: ['name', 'category', 'description', 'created_at']
  },
  {
    label: 'Category',
    count: 0,
    description: '分类节点',
    properties: ['name', 'description']
  },
  {
    label: 'Tag',
    count: 0,
    description: '标签节点',
    properties: ['name']
  },
  {
    label: 'Alias',
    count: 0,
    description: '别名节点',
    properties: ['name', 'original_term']
  },
  {
    label: 'Component',
    count: 0,
    description: '组件节点',
    properties: ['name', 'type', 'specification']
  },
  {
    label: 'Symptom',
    count: 0,
    description: '症状/异常节点',
    properties: ['name', 'severity', 'description']
  },
  {
    label: 'Tool',
    count: 0,
    description: '工具节点',
    properties: ['name', 'version', 'purpose']
  },
  {
    label: 'Process',
    count: 0,
    description: '流程节点',
    properties: ['name', 'steps', 'duration']
  }
])

const relationshipTypes = ref([
  {
    type: 'HAS_TAG',
    count: 0,
    pattern: '(Term)-[HAS_TAG]->(Tag)',
    description: '术语具有标签，用于多维度分类'
  },
  {
    type: 'ALIAS_OF',
    count: 0,
    pattern: '(Alias)-[ALIAS_OF]->(Term)',
    description: '别名指向术语，提升查询覆盖率'
  },
  {
    type: 'BELONGS_TO',
    count: 0,
    pattern: '(Term)-[BELONGS_TO]->(Category)',
    description: '术语归属于分类'
  },
  {
    type: 'AFFECTS',
    count: 0,
    pattern: '(Symptom)-[AFFECTS]->(Component)',
    description: '症状影响组件'
  },
  {
    type: 'USED_IN',
    count: 0,
    pattern: '(Tool)-[USED_IN]->(Process)',
    description: '工具用于流程'
  },
  {
    type: 'TESTS',
    count: 0,
    pattern: '(TestCase)-[TESTS]->(Component)',
    description: '测试用例测试组件'
  },
  {
    type: 'PRODUCES',
    count: 0,
    pattern: '(Process)-[PRODUCES]->(Component)',
    description: '流程产生组件'
  },
  {
    type: 'RELATED_TO',
    count: 0,
    pattern: '(Term)-[RELATED_TO]->(Term)',
    description: '术语之间的关联关系'
  }
])

// 方法
const refreshData = async () => {
  loading.value = true
  try {
    // 获取图谱统计数据
    const statsRes = await api.get('/kg/stats')
    if (statsRes.data.ok && statsRes.data.data) {
      stats.totalNodes = statsRes.data.data.total_nodes || 0
      stats.totalRelationships = statsRes.data.data.total_relationships || 0
    }

    // 获取实体和关系统计
    const entitiesRes = await api.get('/kg/entities')
    if (entitiesRes.data.ok) {
      const entities = entitiesRes.data.data
      nodeTypes.value.forEach(nodeType => {
        const entity = entities.find(e => e.label === nodeType.label)
        if (entity) {
          nodeType.count = entity.count
        }
      })
    }

    const relationsRes = await api.get('/kg/relations')
    if (relationsRes.data.ok) {
      const relations = relationsRes.data.data
      relationshipTypes.value.forEach(relType => {
        const relation = relations.find(r => r.type === relType.type)
        if (relation) {
          relType.count = relation.count
        }
      })
    }

    // 渲染图表
    await nextTick()
    renderSchemaChart()

    ElMessage.success('数据刷新成功')
  } catch (error) {
    console.error('刷新数据失败:', error)
    ElMessage.error('数据刷新失败')
  } finally {
    loading.value = false
  }
}

const getNodeTypeColor = (label) => {
  const colorMap = {
    'Term': 'success',
    'Category': 'warning',
    'Tag': 'danger',
    'Alias': 'info',
    'Component': 'primary',
    'Symptom': 'success',
    'Tool': 'warning',
    'Process': 'info'
  }
  return colorMap[label] || 'info'  // 默认返回 'info' 而不是空字符串
}

const getRelationshipTypeColor = (type) => {
  const colorMap = {
    'HAS_TAG': 'success',
    'ALIAS_OF': 'warning',
    'BELONGS_TO': 'danger',
    'AFFECTS': 'info',
    'USED_IN': 'primary'
  }
  return colorMap[type] || 'info'  // 默认返回 'info' 而不是空字符串
}

const getRelationshipCount = (type) => {
  const rel = relationshipTypes.value.find(r => r.type === type)
  return rel ? rel.count : 0
}

const viewNodeDetails = (row) => {
  ElMessage.info(`查看节点详情: ${row.label}`)
}

const viewRelationshipDetails = (row) => {
  ElMessage.info(`查看关系详情: ${row.type}`)
}

let schemaRenderRetryCount = 0
const MAX_SCHEMA_RETRY = 10

const renderSchemaChart = () => {
  if (!schemaChartRef.value) return

  // 确保容器有尺寸
  if (!schemaChartRef.value.clientWidth || !schemaChartRef.value.clientHeight) {
    if (schemaRenderRetryCount < MAX_SCHEMA_RETRY) {
      schemaRenderRetryCount++
      setTimeout(renderSchemaChart, 100)
    } else {
      console.error('Schema图表容器尺寸始终为0，无法渲染')
    }
    return
  }

  schemaRenderRetryCount = 0  // 重置重试计数

  const chart = echarts.init(schemaChartRef.value)
  
  // 构建节点数据
  const nodes = nodeTypes.value.map((node, index) => ({
    id: node.label,
    name: `${node.label}\n(${node.count})`,
    symbolSize: Math.max(30, Math.min(100, node.count / 10)),
    category: index,
    value: node.count
  }))

  // 构建边数据
  const links = relationshipTypes.value
    .filter(rel => rel.count > 0)
    .map(rel => {
      const match = rel.pattern.match(/\((\w+)\)-\[.*\]->\((\w+)\)/)
      if (match) {
        return {
          source: match[1],
          target: match[2],
          name: rel.type,
          value: rel.count
        }
      }
      return null
    })
    .filter(link => link !== null)

  chart.setOption({
    tooltip: {
      formatter: (params) => {
        if (params.dataType === 'edge') {
          return `${params.data.name}: ${params.data.value}`
        }
        return `${params.data.id}: ${params.data.value} 个节点`
      }
    },
    legend: {
      data: nodeTypes.value.map(n => n.label),
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        type: 'graph',
        layout: 'force',
        data: nodes,
        links: links,
        categories: nodeTypes.value.map(n => ({ name: n.label })),
        roam: true,
        label: {
          show: true,
          position: 'inside',
          formatter: '{b}'
        },
        force: {
          repulsion: 200,
          edgeLength: 150
        },
        emphasis: {
          focus: 'adjacency',
          lineStyle: {
            width: 3
          }
        }
      }
    ]
  })
}

// 生命周期
onMounted(() => {
  refreshData()
})

// 暴露方法给父组件
defineExpose({
  refreshData,
  renderSchemaChart  // 暴露 renderSchemaChart 方法，供父组件在标签页切换时调用
})
</script>

<style scoped>
.graph-schema {
  padding: 20px;
}

.schema-header {
  margin-bottom: 24px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.schema-header h2 {
  margin: 0;
  font-size: 24px;
  color: #303133;
}

.description {
  color: #909399;
  margin: 8px 0 0 0;
  font-size: 14px;
}

.stats-overview {
  margin-bottom: 24px;
}

.stat-item {
  display: flex;
  align-items: center;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  font-size: 20px;
  color: white;
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}

.node-types-card,
.relationship-types-card,
.schema-visualization,
.design-notes {
  margin-bottom: 24px;
}

.property-tag {
  margin-right: 4px;
  margin-bottom: 4px;
}

.count-badge {
  display: inline-block;
  padding: 4px 12px;
  background: #f0f9ff;
  color: #409eff;
  border-radius: 12px;
  font-weight: 500;
}

.relationship-pattern {
  background: #f5f7fa;
  padding: 4px 8px;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  color: #e6a23c;
  font-size: 13px;
}

.node-type-list,
.relationship-type-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.entity-tag,
.scenario-tag {
  margin-right: 8px;
  margin-bottom: 8px;
}

.rel-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
  border-bottom: 1px solid #ebeef5;
}

.rel-item:last-child {
  border-bottom: none;
}

.rel-item code {
  background: #f5f7fa;
  padding: 4px 8px;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  color: #e6a23c;
  min-width: 120px;
}

.rel-item span {
  flex: 1;
  color: #606266;
}

.feature-list {
  margin: 0;
  padding-left: 20px;
  color: #606266;
}

.feature-list li {
  margin-bottom: 8px;
}
</style>

