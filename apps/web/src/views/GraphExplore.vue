<template>
  <div class="graph-explore">
    <!-- 控制面板 -->
    <el-card class="control-panel">
      <el-row :gutter="20" align="middle">
        <el-col :span="6">
          <el-button type="primary" @click="loadGraphData" :loading="loading">
            <el-icon><Refresh /></el-icon>
            刷新图谱
          </el-button>
        </el-col>
        <el-col :span="6">
          <el-input-number
            v-model="nodeLimit"
            :min="10"
            :max="500"
            :step="10"
            controls-position="right"
            style="width: 100%"
          />
          <div class="input-label">节点数量限制</div>
        </el-col>
        <el-col :span="6">
          <el-select v-model="layoutType" @change="changeLayout" style="width: 100%">
            <el-option label="网格布局" value="grid" />
            <el-option label="圆形布局" value="circle" />
            <el-option label="随机布局" value="random" />
            <el-option label="层次布局" value="breadthfirst" />
          </el-select>
          <div class="input-label">布局类型</div>
        </el-col>
        <el-col :span="6">
          <div class="stats">
            <span>节点: {{ graphStats.nodes }}</span>
            <span>关系: {{ graphStats.edges }}</span>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <!-- 图谱容器 -->
    <el-card class="graph-container">
      <div id="cy" ref="cyContainer"></div>
      
      <!-- 图例 -->
      <div class="legend">
        <h4>图例</h4>
        <div class="legend-item">
          <div class="node-sample product"></div>
          <span>产品</span>
        </div>
        <div class="legend-item">
          <div class="node-sample component"></div>
          <span>组件</span>
        </div>
        <div class="legend-item">
          <div class="node-sample anomaly"></div>
          <span>异常</span>
        </div>
        <div class="legend-item">
          <div class="node-sample testcase"></div>
          <span>测试用例</span>
        </div>
      </div>
    </el-card>

    <!-- 节点详情面板 -->
    <el-drawer
      v-model="detailVisible"
      title="节点详情"
      direction="rtl"
      size="400px"
    >
      <div v-if="selectedNode">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="ID">{{ selectedNode.id }}</el-descriptions-item>
          <el-descriptions-item label="类型">{{ selectedNode.label }}</el-descriptions-item>
          <el-descriptions-item label="名称">{{ selectedNode.name }}</el-descriptions-item>
        </el-descriptions>

        <div class="node-properties">
          <h4>属性</h4>
          <el-table :data="nodePropertiesArray" size="small">
            <el-table-column prop="key" label="属性" width="120" />
            <el-table-column prop="value" label="值" show-overflow-tooltip />
          </el-table>
        </div>

        <div class="node-connections">
          <h4>连接关系</h4>
          <el-tag
            v-for="connection in nodeConnections"
            :key="connection"
            size="small"
            class="connection-tag"
          >
            {{ connection }}
          </el-tag>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import { kgApi } from '../api'

export default {
  name: 'GraphExplore',
  components: {
    Refresh
  },
  setup() {
    const loading = ref(false)
    const detailVisible = ref(false)
    const nodeLimit = ref(100)
    const layoutType = ref('grid')
    
    const cyContainer = ref(null)
    const selectedNode = ref(null)
    const graphData = ref({ nodes: [], edges: [] })
    
    let cy = null

    const graphStats = computed(() => ({
      nodes: graphData.value.nodes.length,
      edges: graphData.value.edges.length
    }))

    const nodePropertiesArray = computed(() => {
      if (!selectedNode.value || !selectedNode.value.properties) return []
      return Object.entries(selectedNode.value.properties).map(([key, value]) => ({
        key,
        value: String(value)
      }))
    })

    const nodeConnections = computed(() => {
      if (!selectedNode.value || !cy) return []
      const nodeId = selectedNode.value.id
      const connections = []
      
      cy.edges().forEach(edge => {
        const source = edge.source().id()
        const target = edge.target().id()
        const relationship = edge.data('relationship')
        
        if (source == nodeId) {
          connections.push(`${relationship} → ${cy.getElementById(target).data('name')}`)
        } else if (target == nodeId) {
          connections.push(`${cy.getElementById(source).data('name')} → ${relationship}`)
        }
      })
      
      return connections
    })

    // 初始化Cytoscape
    const initCytoscape = async () => {
      // 动态导入cytoscape
      const cytoscape = (await import('cytoscape')).default
      
      cy = cytoscape({
        container: cyContainer.value,
        style: [
          {
            selector: 'node',
            style: {
              'background-color': '#666',
              'label': 'data(name)',
              'text-valign': 'center',
              'text-halign': 'center',
              'font-size': '12px',
              'width': '60px',
              'height': '60px'
            }
          },
          {
            selector: 'node[label="Product"]',
            style: {
              'background-color': '#409EFF',
              'shape': 'round-rectangle'
            }
          },
          {
            selector: 'node[label="Component"]',
            style: {
              'background-color': '#67C23A',
              'shape': 'ellipse'
            }
          },
          {
            selector: 'node[label="Anomaly"]',
            style: {
              'background-color': '#F56C6C',
              'shape': 'triangle'
            }
          },
          {
            selector: 'node[label="TestCase"]',
            style: {
              'background-color': '#E6A23C',
              'shape': 'diamond'
            }
          },
          {
            selector: 'edge',
            style: {
              'width': 2,
              'line-color': '#ccc',
              'target-arrow-color': '#ccc',
              'target-arrow-shape': 'triangle',
              'curve-style': 'bezier',
              'label': 'data(relationship)',
              'font-size': '10px',
              'text-rotation': 'autorotate'
            }
          },
          {
            selector: 'node:selected',
            style: {
              'border-width': 3,
              'border-color': '#409EFF'
            }
          }
        ],
        layout: {
          name: layoutType.value
        }
      })

      // 添加点击事件
      cy.on('tap', 'node', (evt) => {
        const node = evt.target
        selectedNode.value = {
          id: node.id(),
          label: node.data('label'),
          name: node.data('name'),
          properties: node.data('properties') || {}
        }
        detailVisible.value = true
      })
    }

    // 加载图谱数据
    const loadGraphData = async () => {
      loading.value = true
      
      try {
        const response = await kgApi.getGraphData(nodeLimit.value, true)
        graphData.value = {
          nodes: response.nodes || [],
          edges: response.edges || []
        }
        updateGraph()
        ElMessage.success(`加载了 ${response.nodes?.length || 0} 个节点和 ${response.edges?.length || 0} 个关系`)
      } catch (error) {
        ElMessage.error('加载图谱数据失败: ' + error.message)
      } finally {
        loading.value = false
      }
    }

    // 更新图谱
    const updateGraph = () => {
      if (!cy) return

      // 清空现有数据
      cy.elements().remove()

      // 添加节点
      const nodes = graphData.value.nodes.map(node => ({
        data: {
          id: node.data.id,
          label: node.data.label,
          name: node.data.label,
          type: node.data.type,
          properties: node.data.properties
        }
      }))

      // 添加边
      const edges = graphData.value.edges.map(edge => ({
        data: {
          id: edge.data.id,
          source: edge.data.source,
          target: edge.data.target,
          relationship: edge.data.type,
          confidence: edge.data.confidence
        }
      }))

      cy.add([...nodes, ...edges])
      
      // 应用布局
      cy.layout({ name: layoutType.value }).run()
    }

    // 改变布局
    const changeLayout = () => {
      if (cy) {
        cy.layout({ name: layoutType.value }).run()
      }
    }

    onMounted(async () => {
      await initCytoscape()
      await loadGraphData()
    })

    onUnmounted(() => {
      if (cy) {
        cy.destroy()
      }
    })

    return {
      loading,
      detailVisible,
      nodeLimit,
      layoutType,
      cyContainer,
      selectedNode,
      graphStats,
      nodePropertiesArray,
      nodeConnections,
      loadGraphData,
      changeLayout
    }
  }
}
</script>

<style scoped>
.graph-explore {
  height: calc(100vh - 140px);
  display: flex;
  flex-direction: column;
}

.control-panel {
  margin-bottom: 20px;
  flex-shrink: 0;
}

.input-label {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
  text-align: center;
}

.stats {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 14px;
  color: #606266;
}

.graph-container {
  flex: 1;
  position: relative;
  min-height: 500px;
}

#cy {
  width: 100%;
  height: 100%;
  min-height: 500px;
}

.legend {
  position: absolute;
  top: 20px;
  right: 20px;
  background: rgba(255, 255, 255, 0.9);
  padding: 15px;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.legend h4 {
  margin: 0 0 10px 0;
  font-size: 14px;
  color: #303133;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  font-size: 12px;
}

.node-sample {
  width: 16px;
  height: 16px;
  border-radius: 50%;
}

.node-sample.product {
  background-color: #409EFF;
}

.node-sample.component {
  background-color: #67C23A;
}

.node-sample.anomaly {
  background-color: #F56C6C;
}

.node-sample.testcase {
  background-color: #E6A23C;
}

.node-properties {
  margin-top: 20px;
}

.node-properties h4 {
  margin: 0 0 10px 0;
  color: #303133;
}

.node-connections {
  margin-top: 20px;
}

.node-connections h4 {
  margin: 0 0 10px 0;
  color: #303133;
}

.connection-tag {
  margin: 0 8px 8px 0;
}
</style>
