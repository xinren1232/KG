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

    // 分类颜色映射 - 高对比度配色方案
    const categoryColors = {
      'Symptom': '#E74C3C',      // 深红色 - 症状/问题
      'Component': '#3498DB',    // 蓝色 - 组件
      'Tool': '#2ECC71',         // 绿色 - 工具
      'Process': '#F39C12',      // 橙色 - 流程
      'TestCase': '#9B59B6',     // 紫色 - 测试用例
      'Metric': '#1ABC9C',       // 青绿色 - 指标
      'Role': '#E67E22',         // 深橙色 - 角色
      'Material': '#34495E',     // 深灰蓝 - 材料
      'Product': '#E91E63',      // 粉红色 - 产品
      'Anomaly': '#C0392B',      // 暗红色 - 异常
      'Term': '#3498DB',         // 蓝色 - 术语（映射为组件色）
      'Tag': '#1ABC9C',          // 青色 - 标签（映射为指标色）
      'Category': '#F39C12'      // 橙色 - 分类（映射为流程色）
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

        console.log('图谱API完整响应:', response)
        console.log('响应数据:', response.data)

        // axios拦截器返回完整的response对象，需要访问response.data
        const result = response.data

        if (result && result.ok && result.data) {
          // 只更新从API获取的数据，保持响应式
          graphData.stats = result.data.stats || graphData.stats
          graphData.categories = result.data.categories || graphData.categories
          graphData.tags = result.data.tags || graphData.tags
          graphData.nodes = result.data.nodes || graphData.nodes
          graphData.relations = result.data.relations || graphData.relations
          graphData.sampleNodes = result.data.sampleNodes || graphData.sampleNodes
          graphData.sampleRelations = result.data.sampleRelations || graphData.sampleRelations
        } else {
          // 备用：从配置文件加载数据
          console.warn('API数据格式不正确，使用配置文件:', result)
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

    // 计算节点大小（基于连接数）
    const calculateNodeSize = (nodeId) => {
      const connections = getNodeConnections(nodeId)
      // 更明显的节点大小差异，形成视觉层次
      return Math.min(Math.max(15 + connections * 2, 15), 60)
    }

    // 初始化图谱
    const initGraph = async () => {
      if (!graphCanvas.value) return

      try {
        graphInstance = echarts.init(graphCanvas.value)

        // 准备节点数据 - 优先使用有数据的字段
        const nodes = graphData.sampleNodes || graphData.nodes || []
        const relations = graphData.sampleRelations || graphData.relations || graphData.links || []

        console.log('图谱数据调试:', {
          sampleNodes: graphData.sampleNodes?.length || 0,
          nodes: graphData.nodes?.length || 0,
          sampleRelations: graphData.sampleRelations?.length || 0,
          relations: graphData.relations?.length || 0,
          firstNode: nodes[0]
        })

        // 获取所有分类用于图例
        const categories = [...new Set(nodes.map(n => n.category))].map(cat => ({
          name: cat,
          itemStyle: {
            color: getCategoryColor(cat)
          }
        }))

        const option = {
          title: {
            text: '硬件质量知识图谱',
            subtext: `${nodes.length}个词条，${relations.length}条关系`,
            left: 'center',
            textStyle: {
              fontSize: 24,
              fontWeight: 'bold'
            },
            subtextStyle: {
              fontSize: 14,
              color: '#666'
            }
          },
          legend: [{
            data: categories.map(c => c.name),
            orient: 'vertical',
            left: 10,
            top: 80,
            textStyle: {
              fontSize: 12
            }
          }],
          tooltip: {
            trigger: 'item',
            backgroundColor: 'rgba(255, 255, 255, 0.98)',
            borderColor: '#ddd',
            borderWidth: 1,
            borderRadius: 8,
            padding: 12,
            textStyle: {
              color: '#333',
              fontSize: 13
            },
            extraCssText: 'box-shadow: 0 4px 12px rgba(0,0,0,0.15);',
            formatter: function(params) {
              if (params.dataType === 'node') {
                const connections = getNodeConnections(params.data.id)
                const description = params.data.description || ''
                const truncatedDesc = description.length > 120
                  ? description.substring(0, 120) + '...'
                  : description
                return `
                  <div style="max-width: 320px;">
                    <div style="font-size: 16px; font-weight: bold; margin-bottom: 8px; color: #2c3e50;">
                      ${params.data.name}
                    </div>
                    <div style="margin-bottom: 6px;">
                      <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: ${getCategoryColor(params.data.category)}; margin-right: 6px;"></span>
                      <span style="color: #666; font-weight: 500;">${params.data.category}</span>
                    </div>
                    <div style="color: #666; margin-bottom: 6px;">
                      连接数: <strong style="color: #409EFF;">${connections}</strong>
                    </div>
                    ${truncatedDesc ? '<div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid #eee; color: #555; line-height: 1.4;">' + truncatedDesc + '</div>' : ''}
                  </div>
                `
              } else {
                return `
                  <div style="padding: 4px;">
                    <div style="font-weight: bold; margin-bottom: 4px;">
                      <span style="color: #2c3e50;">${params.data.source}</span>
                      <span style="color: #999; margin: 0 6px;">→</span>
                      <span style="color: #2c3e50;">${params.data.target}</span>
                    </div>
                    <div style="color: #666;">
                      关系: <span style="color: #409EFF; font-weight: 500;">${params.data.type}</span>
                    </div>
                  </div>
                `
              }
            }
          },
          series: [{
            type: 'graph',
            layout: 'force',
            categories: categories,
            data: nodes.map(node => ({
              id: node.id,
              name: node.name,
              category: categories.findIndex(c => c.name === node.category),
              description: node.description || node.properties?.description,
              symbolSize: calculateNodeSize(node.id),
              // 保存原始分类名称用于颜色映射
              originalCategory: node.category,
              itemStyle: {
                color: getCategoryColor(node.category),
                borderColor: '#fff',
                borderWidth: 3,
                shadowBlur: 15,
                shadowColor: 'rgba(0, 0, 0, 0.4)'
              },
              label: {
                show: true,
                fontSize: 9,
                fontWeight: 'normal',
                color: '#333',
                formatter: function(params) {
                  // 显示更多节点标签，形成丰富的视觉效果
                  const connections = getNodeConnections(params.data.id)
                  if (connections > 1 || params.data.symbolSize > 20) {
                    return params.data.name.length > 8
                      ? params.data.name.substring(0, 8) + '...'
                      : params.data.name
                  }
                  return ''
                }
              },
              emphasis: {
                label: {
                  show: true,
                  fontSize: 14,
                  fontWeight: 'bold'
                },
                itemStyle: {
                  shadowBlur: 25,
                  shadowColor: 'rgba(0, 0, 0, 0.6)'
                }
              }
            })),
            links: relations.map(rel => ({
              source: rel.source,
              target: rel.target,
              type: rel.type || rel.relation,
              lineStyle: {
                color: '#ccc',
                width: 1,
                curveness: 0.1,
                opacity: 0.5
              },
              emphasis: {
                lineStyle: {
                  width: 3,
                  opacity: 1,
                  color: '#409EFF'
                }
              }
            })),
            roam: true,
            draggable: true,
            force: {
              repulsion: 300,        // 适中斥力，形成聚类
              gravity: 0.1,          // 适中重力，保持整体结构
              edgeLength: [30, 100], // 适中边长，形成紧密聚类
              layoutAnimation: true,
              friction: 0.6,         // 增加摩擦力，稳定布局
              initLayout: 'none'     // 不使用初始布局，让力导向自然形成
            },
            emphasis: {
              focus: 'adjacency',
              lineStyle: {
                width: 3
              }
            },
            lineStyle: {
              color: 'source',
              curveness: 0.1
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
      const relations = graphData.sampleRelations || graphData.relations || []
      return relations.filter(rel =>
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
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border: 1px solid #e9ecef;
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
