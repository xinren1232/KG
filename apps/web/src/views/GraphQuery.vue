<template>
  <div class="graph-query">
    <el-card class="query-card">
      <template #header>
        <div class="card-header">
          <span>🔍 知识图谱查询</span>
          <div class="header-actions">
            <el-button type="info" @click="showExamples = !showExamples">
              {{ showExamples ? '隐藏' : '显示' }}示例
            </el-button>
            <el-button type="primary" @click="executeQuery" :loading="loading">
              执行查询
            </el-button>
          </div>
        </div>
      </template>

      <!-- 查询示例 -->
      <el-collapse v-model="activeExamples" v-show="showExamples" class="examples-section">
        <el-collapse-item title="📚 常用查询示例" name="examples">
          <el-row :gutter="20">
            <el-col :span="12" v-for="(example, index) in queryExamples" :key="index">
              <el-card class="example-card" @click="useExample(example)">
                <div class="example-title">{{ example.title }}</div>
                <div class="example-description">{{ example.description }}</div>
                <pre class="example-query">{{ example.query }}</pre>
              </el-card>
            </el-col>
          </el-row>
        </el-collapse-item>
      </el-collapse>

      <!-- 查询编辑器 -->
      <div class="query-editor">
        <el-input
          v-model="cypherQuery"
          type="textarea"
          :rows="8"
          placeholder="请输入Cypher查询语句..."
          class="query-textarea"
        />
        
        <!-- 参数输入 -->
        <el-divider>查询参数</el-divider>
        <div class="parameters-section">
          <el-button type="text" @click="addParameter" icon="Plus">添加参数</el-button>
          <div v-for="(param, index) in parameters" :key="index" class="parameter-item">
            <el-input
              v-model="param.key"
              placeholder="参数名"
              style="width: 200px; margin-right: 10px"
            />
            <el-input
              v-model="param.value"
              placeholder="参数值"
              style="width: 200px; margin-right: 10px"
            />
            <el-button type="danger" @click="removeParameter(index)" icon="Delete" />
          </div>
        </div>
      </div>
    </el-card>

    <!-- 查询结果 -->
    <el-card class="result-card" v-if="queryResult">
      <template #header>
        <div class="result-header">
          <span>📊 查询结果</span>
          <div class="result-stats">
            <el-tag>{{ queryResult.count }} 条记录</el-tag>
            <el-tag type="info">{{ executionTime }}ms</el-tag>
          </div>
        </div>
      </template>

      <!-- 结果表格 -->
      <el-table 
        :data="queryResult.results" 
        style="width: 100%"
        max-height="400"
        v-if="queryResult.results.length > 0"
      >
        <el-table-column 
          v-for="column in resultColumns" 
          :key="column"
          :prop="column"
          :label="column"
          min-width="150"
        >
          <template #default="scope">
            <div class="result-cell">
              {{ formatCellValue(scope.row[column]) }}
            </div>
          </template>
        </el-table-column>
      </el-table>

      <el-empty v-else description="查询无结果" />
    </el-card>

    <!-- 图谱统计 -->
    <el-card class="stats-card">
      <template #header>
        <div class="stats-header">
          <span>📈 图谱统计</span>
          <el-button type="primary" size="small" @click="loadStats" :loading="statsLoading">
            刷新统计
          </el-button>
        </div>
      </template>

      <el-row :gutter="20" v-if="graphStats">
        <el-col :span="6">
          <el-statistic title="总节点数" :value="graphStats.total_nodes" />
        </el-col>
        <el-col :span="6">
          <el-statistic title="总关系数" :value="graphStats.total_relationships" />
        </el-col>
        <el-col :span="6">
          <el-statistic title="节点类型" :value="Object.keys(graphStats.node_types).length" />
        </el-col>
        <el-col :span="6">
          <el-statistic title="关系类型" :value="Object.keys(graphStats.relationship_types).length" />
        </el-col>
      </el-row>

      <el-divider>节点类型分布</el-divider>
      <el-row :gutter="20">
        <el-col :span="4" v-for="(count, type) in graphStats?.node_types" :key="type">
          <div class="type-stat">
            <div class="type-name">{{ formatEntityType(type) }}</div>
            <div class="type-count">{{ count }}</div>
          </div>
        </el-col>
      </el-row>

      <el-divider>关系类型分布</el-divider>
      <el-row :gutter="20">
        <el-col :span="4" v-for="(count, type) in graphStats?.relationship_types" :key="type">
          <div class="type-stat">
            <div class="type-name">{{ type }}</div>
            <div class="type-count">{{ count }}</div>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Delete } from '@element-plus/icons-vue'
import { kgApi } from '../api'

export default {
  name: 'GraphQuery',
  components: {
    Plus,
    Delete
  },
  setup() {
    const cypherQuery = ref('')
    const parameters = ref([])
    const loading = ref(false)
    const queryResult = ref(null)
    const executionTime = ref(0)
    const showExamples = ref(false)
    const activeExamples = ref(['examples'])
    
    const graphStats = ref(null)
    const statsLoading = ref(false)

    // 查询示例
    const queryExamples = ref([
      {
        title: '查看所有实体类型',
        description: '获取图谱中所有实体的类型统计',
        query: 'MATCH (n:Entity)\nRETURN n.type as entity_type, count(n) as count\nORDER BY count DESC'
      },
      {
        title: '查找特定产品的组件',
        description: '查找与特定产品相关的所有组件',
        query: 'MATCH (p:Entity {type: "product"})-[r]-(c:Entity {type: "component"})\nWHERE p.name CONTAINS $product_name\nRETURN p.name as product, c.name as component, type(r) as relation'
      },
      {
        title: '查找异常及其解决方案',
        description: '查找异常问题及其对应的解决方案',
        query: 'MATCH (a:Entity {type: "anomaly"})-[r]-(s:Entity {type: "countermeasure"})\nRETURN a.name as anomaly, s.name as solution, r.confidence as confidence\nORDER BY r.confidence DESC'
      },
      {
        title: '查找节点的邻居',
        description: '查找指定节点的所有直接邻居',
        query: 'MATCH (center:Entity {id: $node_id})-[r]-(neighbor:Entity)\nRETURN center.name as center_node, neighbor.name as neighbor, neighbor.type as neighbor_type, type(r) as relation'
      },
      {
        title: '查找路径',
        description: '查找两个节点之间的最短路径',
        query: 'MATCH path = shortestPath((start:Entity {id: $start_id})-[*]-(end:Entity {id: $end_id}))\nRETURN path'
      },
      {
        title: '查找高度连接的节点',
        description: '查找连接度最高的节点',
        query: 'MATCH (n:Entity)-[r]-()\nRETURN n.name as node_name, n.type as node_type, count(r) as degree\nORDER BY degree DESC\nLIMIT 10'
      }
    ])

    // 计算结果列名
    const resultColumns = computed(() => {
      if (!queryResult.value || !queryResult.value.results.length) return []
      return Object.keys(queryResult.value.results[0])
    })

    // 添加参数
    const addParameter = () => {
      parameters.value.push({ key: '', value: '' })
    }

    // 删除参数
    const removeParameter = (index) => {
      parameters.value.splice(index, 1)
    }

    // 使用示例查询
    const useExample = (example) => {
      cypherQuery.value = example.query
      // 根据查询自动添加参数
      const paramMatches = example.query.match(/\$\w+/g)
      if (paramMatches) {
        parameters.value = paramMatches.map(param => ({
          key: param.substring(1),
          value: ''
        }))
      }
    }

    // 执行查询
    const executeQuery = async () => {
      if (!cypherQuery.value.trim()) {
        ElMessage.warning('请输入查询语句')
        return
      }

      loading.value = true
      const startTime = Date.now()

      try {
        // 构建参数对象
        const queryParams = {}
        parameters.value.forEach(param => {
          if (param.key && param.value) {
            // 尝试解析为数字或保持字符串
            const value = isNaN(param.value) ? param.value : Number(param.value)
            queryParams[param.key] = value
          }
        })

        const response = await kgApi.queryGraph(cypherQuery.value, queryParams)

        queryResult.value = response
        executionTime.value = Date.now() - startTime

        ElMessage.success(`查询完成，返回 ${response.count} 条记录`)

      } catch (error) {
        ElMessage.error('查询失败: ' + error.message)
        queryResult.value = null
      } finally {
        loading.value = false
      }
    }

    // 加载图谱统计
    const loadStats = async () => {
      statsLoading.value = true
      try {
        const response = await kgApi.getGraphStats()
        graphStats.value = response
      } catch (error) {
        ElMessage.error('加载统计信息失败: ' + error.message)
      } finally {
        statsLoading.value = false
      }
    }

    // 格式化单元格值
    const formatCellValue = (value) => {
      if (value === null || value === undefined) {
        return 'null'
      }
      if (typeof value === 'object') {
        return JSON.stringify(value, null, 2)
      }
      return String(value)
    }

    // 格式化实体类型
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

    onMounted(() => {
      loadStats()
    })

    return {
      cypherQuery,
      parameters,
      loading,
      queryResult,
      executionTime,
      showExamples,
      activeExamples,
      queryExamples,
      resultColumns,
      graphStats,
      statsLoading,
      addParameter,
      removeParameter,
      useExample,
      executeQuery,
      loadStats,
      formatCellValue,
      formatEntityType
    }
  }
}
</script>

<style scoped>
.graph-query {
  padding: 20px;
}

.query-card, .result-card, .stats-card {
  margin-bottom: 20px;
}

.card-header, .result-header, .stats-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.examples-section {
  margin-bottom: 20px;
}

.example-card {
  cursor: pointer;
  margin-bottom: 10px;
  transition: all 0.3s;
}

.example-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.example-title {
  font-weight: bold;
  margin-bottom: 5px;
  color: #409EFF;
}

.example-description {
  font-size: 12px;
  color: #666;
  margin-bottom: 10px;
}

.example-query {
  background: #f5f5f5;
  padding: 10px;
  border-radius: 4px;
  font-size: 12px;
  margin: 0;
  white-space: pre-wrap;
}

.query-editor {
  margin-top: 20px;
}

.query-textarea {
  font-family: 'Courier New', monospace;
}

.parameters-section {
  margin-top: 10px;
}

.parameter-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.result-stats {
  display: flex;
  gap: 10px;
}

.result-cell {
  max-width: 300px;
  word-break: break-all;
  white-space: pre-wrap;
}

.type-stat {
  text-align: center;
  padding: 10px;
  border: 1px solid #EBEEF5;
  border-radius: 4px;
  margin-bottom: 10px;
}

.type-name {
  font-size: 12px;
  color: #909399;
  margin-bottom: 5px;
}

.type-count {
  font-size: 20px;
  font-weight: bold;
  color: #303133;
}
</style>
