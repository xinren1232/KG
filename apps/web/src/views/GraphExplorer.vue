<template>
  <div class="graph-explorer">
    <el-card class="header-card">
      <div class="page-header">
        <h2>🕸️ 图谱探索</h2>
        <p>交互式可视化探索知识图谱中的实体关系</p>
      </div>
    </el-card>

    <!-- 数据可视化组件 -->
    <DataVisualization />

    <!-- 控制面板 -->
    <el-card class="control-card">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="症状查询">
            <el-input
              v-model="symptomQuery"
              placeholder="输入症状进行图谱查询"
              @keyup.enter="loadGraphData"
            >
              <template #append>
                <el-button @click="loadGraphData" :loading="loading">
                  渲染图谱
                </el-button>
              </template>
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <div class="graph-controls">
            <el-button-group>
              <el-button @click="fitGraph" :disabled="!hasGraph">适应画布</el-button>
              <el-button @click="resetGraph" :disabled="!hasGraph">重置视图</el-button>
              <el-button @click="exportGraph" :disabled="!hasGraph">导出图片</el-button>
            </el-button-group>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <!-- 图谱容器 -->
    <el-card class="graph-card">
      <template #header>
        <div class="graph-header">
          <span>知识图谱可视化</span>
          <div class="graph-stats" v-if="graphStats.nodes > 0">
            节点: {{ graphStats.nodes }} | 边: {{ graphStats.edges }}
          </div>
        </div>
      </template>

      <div class="graph-container">
        <div 
          ref="graphContainer" 
          class="graph-display"
          v-loading="loading"
          element-loading-text="正在渲染图谱..."
        >
          <!-- 简化的图谱显示 -->
          <div v-if="!hasGraph && !loading" class="empty-graph">
            <el-empty description="暂无图谱数据">
              <el-button type="primary" @click="loadSampleData">
                加载示例数据
              </el-button>
            </el-empty>
          </div>
          
          <div v-else-if="hasGraph" class="graph-content">
            <div class="node-list">
              <h4>图谱节点</h4>
              <div v-for="node in sampleNodes" :key="node.id" class="node-item">
                <el-tag :type="getNodeType(node.type)">{{ node.type }}</el-tag>
                <span>{{ node.name }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import DataVisualization from '@/components/DataVisualization.vue'

export default {
  name: 'GraphExplorer',
  components: {
    DataVisualization
  },
  setup() {
    const symptomQuery = ref('')
    const loading = ref(false)
    const hasGraph = ref(false)
    const graphContainer = ref(null)

    const graphStats = reactive({
      nodes: 0,
      edges: 0
    })

    const sampleNodes = ref([])

    const loadGraphData = async () => {
      if (!symptomQuery.value.trim()) return

      loading.value = true

      try {
        // 调用真实的因果路径API
        const response = await http.post('/kg/cause_path', {
          symptom_name: symptomQuery.value,
          max_depth: 5,
          include_countermeasures: true
        })

        if (response.ok && response.data && response.data.paths) {
          const paths = response.data.paths
          const nodes = new Set()
          const edges = []

          // 处理路径数据构建图谱
          paths.forEach((path, pathIndex) => {
            // 添加症状节点
            if (path.symptom) {
              nodes.add({
                id: `symptom_${path.symptom.id}`,
                type: 'Symptom',
                name: path.symptom.name,
                data: path.symptom
              })
            }

            // 添加根因节点和边
            if (path.causes) {
              path.causes.forEach((cause, causeIndex) => {
                const causeId = `cause_${cause.id || pathIndex}_${causeIndex}`
                nodes.add({
                  id: causeId,
                  type: 'RootCause',
                  name: cause.name,
                  confidence: cause.confidence,
                  data: cause
                })

                // 添加症状到根因的边
                if (path.symptom) {
                  edges.push({
                    id: `edge_${path.symptom.id}_${causeId}`,
                    source: `symptom_${path.symptom.id}`,
                    target: causeId,
                    type: 'CAUSED_BY'
                  })
                }
              })
            }

            // 添加对策节点和边
            if (path.countermeasures) {
              path.countermeasures.forEach((counter, counterIndex) => {
                const counterId = `counter_${counter.id || pathIndex}_${counterIndex}`
                nodes.add({
                  id: counterId,
                  type: 'Countermeasure',
                  name: counter.name,
                  effectiveness: counter.effectiveness,
                  data: counter
                })

                // 添加根因到对策的边
                if (path.causes && path.causes.length > 0) {
                  path.causes.forEach((cause, causeIndex) => {
                    const causeId = `cause_${cause.id || pathIndex}_${causeIndex}`
                    edges.push({
                      id: `edge_${causeId}_${counterId}`,
                      source: causeId,
                      target: counterId,
                      type: 'RESOLVED_BY'
                    })
                  })
                }
              })
            }
          })

          sampleNodes.value = Array.from(nodes)
          graphStats.nodes = sampleNodes.value.length
          graphStats.edges = edges.length
          hasGraph.value = true

          ElMessage.success(`成功加载图谱数据：${graphStats.nodes}个节点，${graphStats.edges}条边`)
        } else {
          // 如果没有找到路径，显示提示
          ElMessage.warning('未找到相关的因果路径数据')
          sampleNodes.value = []
          graphStats.nodes = 0
          graphStats.edges = 0
          hasGraph.value = false
        }

      } catch (error) {
        console.error('Failed to load graph data:', error)
        ElMessage.error('加载图谱数据失败')

        // 降级到示例数据
        sampleNodes.value = [
          { id: '1', type: 'Symptom', name: symptomQuery.value },
          { id: '2', type: 'Anomaly', name: '相机对焦失败' },
          { id: '3', type: 'Component', name: '摄像头' },
          { id: '4', type: 'RootCause', name: '硬件故障' }
        ]
        graphStats.nodes = sampleNodes.value.length
        graphStats.edges = 3
        hasGraph.value = true
      } finally {
        loading.value = false
      }
    }

    const loadSampleData = () => {
      symptomQuery.value = '拍照模糊'
      loadGraphData()
    }

    const getNodeType = (type) => {
      const typeMap = {
        'Symptom': 'danger',
        'Anomaly': 'warning', 
        'Component': 'primary',
        'RootCause': 'info'
      }
      return typeMap[type] || ''
    }

    const fitGraph = () => {
      console.log('Fit graph')
    }

    const resetGraph = () => {
      console.log('Reset graph')
    }

    const exportGraph = () => {
      console.log('Export graph')
    }

    return {
      symptomQuery,
      loading,
      hasGraph,
      graphContainer,
      graphStats,
      sampleNodes,
      loadGraphData,
      loadSampleData,
      getNodeType,
      fitGraph,
      resetGraph,
      exportGraph
    }
  }
}
</script>

<style scoped>
.graph-explorer {
  padding: 20px;
}

.header-card, .control-card, .graph-card {
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0 0 10px 0;
  color: #303133;
}

.page-header p {
  margin: 0;
  color: #606266;
}

.graph-controls {
  display: flex;
  justify-content: flex-end;
}

.graph-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.graph-stats {
  font-size: 14px;
  color: #909399;
}

.graph-container {
  position: relative;
  height: 500px;
}

.graph-display {
  width: 100%;
  height: 100%;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-graph {
  text-align: center;
}

.graph-content {
  width: 100%;
  padding: 20px;
}

.node-list h4 {
  margin-bottom: 15px;
  color: #303133;
}

.node-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.node-item:last-child {
  border-bottom: none;
}

@media (max-width: 768px) {
  .graph-container {
    height: 400px;
  }
  
  .graph-header {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }
}
</style>
