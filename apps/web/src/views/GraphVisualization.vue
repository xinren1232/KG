<template>
  <div class="graph-visualization">
    <!-- 控制面板 -->
    <el-card class="control-panel">
      <template #header>
        <div class="panel-header">
          <span>🔍 硬件质量知识图谱</span>
          <div class="controls">
            <el-button type="primary" @click="loadGraphData" :loading="loading">
              <el-icon><Refresh /></el-icon>
              刷新数据
            </el-button>
            <el-button @click="resetView">
              <el-icon><FullScreen /></el-icon>
              重置视图
            </el-button>
            <el-button @click="exportGraph">
              <el-icon><Download /></el-icon>
              导出图片
            </el-button>
          </div>
        </div>
      </template>

      <!-- 统计信息 -->
      <el-row :gutter="20" class="stats-row">
        <el-col :span="6">
          <div class="stat-item">
            <el-icon color="#409EFF"><Document /></el-icon>
            <div class="stat-content">
              <div class="stat-value">{{ graphData.stats.totalNodes }}</div>
              <div class="stat-label">词典条目</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-item">
            <el-icon color="#67C23A"><Share /></el-icon>
            <div class="stat-content">
              <div class="stat-value">{{ graphData.stats.totalRelations }}</div>
              <div class="stat-label">关系数量</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-item">
            <el-icon color="#E6A23C"><Grid /></el-icon>
            <div class="stat-content">
              <div class="stat-value">{{ graphData.stats.totalCategories }}</div>
              <div class="stat-label">分类数量</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-item">
            <el-icon color="#F56C6C"><Collection /></el-icon>
            <div class="stat-content">
              <div class="stat-value">{{ graphData.stats.totalTags }}</div>
              <div class="stat-label">标签数量</div>
            </div>
          </div>
        </el-col>
      </el-row>

      <!-- 过滤器 -->
      <el-row :gutter="20" class="filter-row">
        <el-col :span="8">
          <el-select v-model="selectedCategory" placeholder="选择分类" clearable @change="filterNodes">
            <el-option label="全部分类" value="" />
            <el-option 
              v-for="cat in graphData.categories" 
              :key="cat.name"
              :label="`${cat.name} (${cat.count})`"
              :value="cat.name"
            />
          </el-select>
        </el-col>
        <el-col :span="8">
          <el-select v-model="selectedTag" placeholder="选择标签" clearable @change="filterNodes">
            <el-option label="全部标签" value="" />
            <el-option 
              v-for="tag in graphData.tags.slice(0, 10)" 
              :key="tag.name"
              :label="`${tag.name} (${tag.count})`"
              :value="tag.name"
            />
          </el-select>
        </el-col>
        <el-col :span="8">
          <el-input 
            v-model="searchTerm" 
            placeholder="搜索节点..." 
            clearable
            @input="searchNodes"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-col>
      </el-row>
    </el-card>

    <!-- 图谱容器 -->
    <el-card class="graph-container">
      <div ref="graphCanvas" class="graph-canvas" v-loading="loading"></div>
      
      <!-- 图例 -->
      <div class="legend">
        <h4>节点类型</h4>
        <div class="legend-items">
          <div v-for="cat in graphData.categories" :key="cat.name" class="legend-item">
            <div 
              class="legend-color" 
              :style="{ backgroundColor: getCategoryColor(cat.name) }"
            ></div>
            <span>{{ cat.name }} ({{ cat.count }})</span>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 节点详情面板 -->
    <el-drawer
      v-model="showNodeDetail"
      title="节点详情"
      direction="rtl"
      size="400px"
    >
      <div v-if="selectedNode" class="node-detail">
        <h3>{{ selectedNode.name }}</h3>
        <el-tag :type="getCategoryType(selectedNode.category)">
          {{ selectedNode.category }}
        </el-tag>
        <p class="description">{{ selectedNode.description }}</p>
        
        <h4>相关信息</h4>
        <div class="node-info">
          <div class="info-item">
            <strong>ID:</strong> {{ selectedNode.id }}
          </div>
          <div class="info-item">
            <strong>分类:</strong> {{ selectedNode.category }}
          </div>
          <div class="info-item">
            <strong>连接数:</strong> {{ getNodeConnections(selectedNode.id) }}
          </div>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import {
  Refresh,
  FullScreen,
  Download,
  Document,
  Share,
  Grid,
  Collection,
  Search
} from '@element-plus/icons-vue'

export default {
  name: 'GraphVisualization',
  components: {
    Refresh,
    FullScreen,
    Download,
    Document,
    Share,
    Grid,
    Collection,
    Search
  },
  setup() {
    const loading = ref(false)
    const graphCanvas = ref(null)
    const showNodeDetail = ref(false)
    const selectedNode = ref(null)
    const selectedCategory = ref('')
    const selectedTag = ref('')
    const searchTerm = ref('')

    // 图谱数据
    const graphData = reactive({
      stats: {
        totalNodes: 1124,
        totalRelations: 7581,
        totalCategories: 8,
        totalTags: 79
      },
      categories: [],
      tags: [],
      nodes: [],
      relations: [],
      sampleNodes: [],
      sampleRelations: []
    })

    // 图谱实例
    let graphInstance = null

    // 分类颜色映射
    const categoryColors = {
      'Symptom': '#F56C6C',
      'Component': '#409EFF', 
      'Tool': '#67C23A',
      'Process': '#E6A23C',
      'TestCase': '#909399',
      'Metric': '#9C27B0',
      'Role': '#FF9800',
      'Material': '#795548'
    }

    // 获取分类颜色
    const getCategoryColor = (category) => {
      return categoryColors[category] || '#606266'
    }

    // 获取分类类型
    const getCategoryType = (category) => {
      const typeMap = {
        'Symptom': 'danger',
        'Component': 'primary',
        'Tool': 'success',
        'Process': 'warning',
        'TestCase': 'info',
        'Metric': '',
        'Role': 'warning',
        'Material': 'info'
      }
      return typeMap[category] || ''
    }

    // 加载图谱数据
    const loadGraphData = async () => {
      loading.value = true
      try {
        // 从API获取数据
        const { kgApi } = await import('../api')
        const response = await kgApi.getGraphVisualizationData(true)

        if (response && response.data) {
          // 只更新从API获取的数据，保持响应式
          graphData.stats = response.data.stats || graphData.stats
          graphData.categories = response.data.categories || graphData.categories
          graphData.tags = response.data.tags || graphData.tags
          graphData.nodes = response.data.nodes || graphData.nodes
          graphData.relations = response.data.relations || graphData.relations
          graphData.sampleNodes = response.data.sampleNodes || graphData.sampleNodes
          graphData.sampleRelations = response.data.sampleRelations || graphData.sampleRelations
        } else {
          // 备用：从配置文件加载数据
          const configResponse = await fetch('/config/graph_visualization_data.json')
          const data = await configResponse.json()
          Object.assign(graphData, data)
        }

        // 初始化图谱
        await nextTick()
        initGraph()

        ElMessage.success('图谱数据加载成功')
      } catch (error) {
        console.error('加载图谱数据失败:', error)
        console.error('错误详情:', error.response?.data || error.message)
        const errorMsg = error.response?.data?.detail || error.message || '加载图谱数据失败'
        ElMessage.error(`加载图谱数据失败: ${errorMsg}`)
      } finally {
        loading.value = false
      }
    }

    // 初始化图谱
    const initGraph = async () => {
      if (!graphCanvas.value) return

      try {
        graphInstance = echarts.init(graphCanvas.value)
        
        const option = {
          title: {
            text: '硬件质量知识图谱',
            subtext: `${graphData.stats.totalNodes}个节点，${graphData.stats.totalRelations}条关系`,
            left: 'center'
          },
          tooltip: {
            trigger: 'item',
            formatter: function(params) {
              if (params.dataType === 'node') {
                return `
                  <strong>${params.data.name}</strong><br/>
                  分类: ${params.data.category}<br/>
                  ${params.data.description ? params.data.description.substring(0, 100) + '...' : ''}
                `
              } else {
                return `${params.data.source} → ${params.data.target}<br/>关系: ${params.data.type}`
              }
            }
          },
          series: [{
            type: 'graph',
            layout: 'force',
            data: (graphData.nodes || graphData.sampleNodes || []).map(node => ({
              id: node.id,
              name: node.name,
              category: node.category,
              description: node.description || node.properties?.description,
              symbolSize: node.symbolSize || 30,
              itemStyle: {
                color: getCategoryColor(node.category)
              },
              label: {
                show: true,
                fontSize: 12
              }
            })),
            links: (graphData.relations || graphData.sampleRelations || graphData.links || []).map(rel => ({
              source: rel.source,
              target: rel.target,
              type: rel.type || rel.relation,
              lineStyle: {
                color: '#999',
                width: 2
              }
            })),
            roam: true,
            force: {
              repulsion: 1000,
              edgeLength: 100
            },
            emphasis: {
              focus: 'adjacency'
            }
          }]
        }
        
        graphInstance.setOption(option)
        
        // 添加点击事件
        graphInstance.on('click', (params) => {
          if (params.dataType === 'node') {
            selectedNode.value = params.data
            showNodeDetail.value = true
          }
        })
        
      } catch (error) {
        console.error('初始化图谱失败:', error)
        ElMessage.error('图谱初始化失败')
      }
    }

    // 过滤节点
    const filterNodes = () => {
      // 实现过滤逻辑
      console.log('过滤条件:', selectedCategory.value, selectedTag.value)
    }

    // 搜索节点
    const searchNodes = () => {
      // 实现搜索逻辑
      console.log('搜索词:', searchTerm.value)
    }

    // 重置视图
    const resetView = () => {
      if (graphInstance) {
        graphInstance.resize()
      }
    }

    // 导出图片
    const exportGraph = () => {
      if (graphInstance) {
        const url = graphInstance.getDataURL({
          type: 'png',
          backgroundColor: '#fff'
        })
        const link = document.createElement('a')
        link.download = '知识图谱.png'
        link.href = url
        link.click()
      }
    }

    // 获取节点连接数
    const getNodeConnections = (nodeId) => {
      return graphData.sampleRelations.filter(rel => 
        rel.source === nodeId || rel.target === nodeId
      ).length
    }

    onMounted(() => {
      loadGraphData()
    })

    return {
      loading,
      graphCanvas,
      showNodeDetail,
      selectedNode,
      selectedCategory,
      selectedTag,
      searchTerm,
      graphData,
      loadGraphData,
      filterNodes,
      searchNodes,
      resetView,
      exportGraph,
      getCategoryColor,
      getCategoryType,
      getNodeConnections
    }
  }
}
</script>

<style scoped>
.graph-visualization {
  padding: 20px;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.control-panel {
  margin-bottom: 20px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-item {
  display: flex;
  align-items: center;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
  gap: 12px;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 4px;
}

.stat-label {
  color: #666;
  font-size: 14px;
}

.filter-row {
  margin-top: 15px;
}

.graph-container {
  flex: 1;
  position: relative;
}

.graph-canvas {
  width: 100%;
  height: 600px;
}

.legend {
  position: absolute;
  top: 20px;
  right: 20px;
  background: rgba(255, 255, 255, 0.9);
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.legend h4 {
  margin: 0 0 10px 0;
  font-size: 14px;
}

.legend-items {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.node-detail {
  padding: 20px;
}

.node-detail h3 {
  margin: 0 0 10px 0;
}

.description {
  margin: 15px 0;
  line-height: 1.6;
  color: #666;
}

.node-info {
  margin-top: 20px;
}

.info-item {
  margin-bottom: 10px;
  padding: 8px;
  background: #f5f5f5;
  border-radius: 4px;
}
</style>
