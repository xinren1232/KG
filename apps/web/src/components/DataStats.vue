<template>
  <el-card class="stats-card">
    <template #header>
      <div class="stats-header">
        <span>📊 数据统计</span>
        <el-button type="text" size="small" @click="refreshStats" :loading="loading">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>
    </template>

    <el-row :gutter="20">
      <el-col :span="6" v-for="stat in stats" :key="stat.key">
        <div class="stat-item" :class="stat.type">
          <div class="stat-icon">
            <el-icon :size="24" :color="stat.color">
              <component :is="stat.icon" />
            </el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stat.value }}</div>
            <div class="stat-label">{{ stat.label }}</div>
            <div class="stat-change" v-if="stat.change">
              <el-icon :size="12" :color="stat.change > 0 ? '#67C23A' : '#F56C6C'">
                <ArrowUp v-if="stat.change > 0" />
                <ArrowDown v-else />
              </el-icon>
              <span :style="{ color: stat.change > 0 ? '#67C23A' : '#F56C6C' }">
                {{ Math.abs(stat.change) }}%
              </span>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- 趋势图表 -->
    <div class="trend-section" v-if="showTrend">
      <h4>数据趋势</h4>
      <div class="trend-chart">
        <canvas ref="trendCanvas" width="400" height="200"></canvas>
      </div>
    </div>
  </el-card>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { 
  Refresh, 
  ArrowUp, 
  ArrowDown,
  Document,
  Warning,
  List,
  Share
} from '@element-plus/icons-vue'
import { kgApi } from '../api'

export default {
  name: 'DataStats',
  components: {
    Refresh,
    ArrowUp,
    ArrowDown,
    Document,
    Warning,
    List,
    Share
  },
  props: {
    showTrend: {
      type: Boolean,
      default: false
    }
  },
  setup() {
    const loading = ref(false)
    const trendCanvas = ref(null)
    
    const rawStats = ref({
      products: 2,
      components: 4,
      testCases: 5,
      anomalies: 3,
      nodes: 15,
      edges: 8
    })

    const stats = computed(() => [
      {
        key: 'products',
        label: '产品数量',
        value: rawStats.value.products,
        icon: 'Document',
        color: '#409EFF',
        type: 'primary',
        change: 0
      },
      {
        key: 'testCases',
        label: '测试用例',
        value: rawStats.value.testCases,
        icon: 'List',
        color: '#67C23A',
        type: 'success',
        change: 12
      },
      {
        key: 'anomalies',
        label: '异常记录',
        value: rawStats.value.anomalies,
        icon: 'Warning',
        color: '#F56C6C',
        type: 'danger',
        change: -8
      },
      {
        key: 'nodes',
        label: '知识节点',
        value: rawStats.value.nodes,
        icon: 'Share',
        color: '#E6A23C',
        type: 'warning',
        change: 25
      }
    ])

    const refreshStats = async () => {
      loading.value = true
      
      try {
        // 获取产品数据
        const productsRes = await kgApi.getProducts()
        if (productsRes.success) {
          rawStats.value.products = productsRes.data.length
        }

        // 获取图谱数据
        const graphRes = await kgApi.getGraphData(100)
        if (graphRes.success) {
          rawStats.value.nodes = graphRes.data.nodes.length
          rawStats.value.edges = graphRes.data.edges.length
        }

        ElMessage.success('统计数据已更新')
      } catch (error) {
        ElMessage.error('获取统计数据失败: ' + error.message)
      } finally {
        loading.value = false
      }
    }

    const drawTrendChart = () => {
      if (!trendCanvas.value) return

      const ctx = trendCanvas.value.getContext('2d')
      const width = trendCanvas.value.width
      const height = trendCanvas.value.height

      // 清空画布
      ctx.clearRect(0, 0, width, height)

      // 模拟趋势数据
      const data = [10, 15, 12, 18, 20, 25, 22, 28, 30, 35]
      const maxValue = Math.max(...data)
      const stepX = width / (data.length - 1)
      const stepY = height / maxValue

      // 绘制网格
      ctx.strokeStyle = '#E4E7ED'
      ctx.lineWidth = 1
      for (let i = 0; i <= 5; i++) {
        const y = (height / 5) * i
        ctx.beginPath()
        ctx.moveTo(0, y)
        ctx.lineTo(width, y)
        ctx.stroke()
      }

      // 绘制趋势线
      ctx.strokeStyle = '#409EFF'
      ctx.lineWidth = 2
      ctx.beginPath()
      
      data.forEach((value, index) => {
        const x = index * stepX
        const y = height - (value * stepY)
        
        if (index === 0) {
          ctx.moveTo(x, y)
        } else {
          ctx.lineTo(x, y)
        }
      })
      
      ctx.stroke()

      // 绘制数据点
      ctx.fillStyle = '#409EFF'
      data.forEach((value, index) => {
        const x = index * stepX
        const y = height - (value * stepY)
        
        ctx.beginPath()
        ctx.arc(x, y, 3, 0, 2 * Math.PI)
        ctx.fill()
      })
    }

    onMounted(() => {
      refreshStats()
      if (trendCanvas.value) {
        setTimeout(drawTrendChart, 100)
      }
    })

    return {
      loading,
      trendCanvas,
      stats,
      refreshStats
    }
  }
}
</script>

<style scoped>
.stats-card {
  margin-bottom: 20px;
}

.stats-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-item {
  display: flex;
  align-items: center;
  padding: 15px;
  border-radius: 8px;
  background: #f8f9fa;
  transition: all 0.3s ease;
}

.stat-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-item.primary {
  background: linear-gradient(135deg, #409EFF 0%, #66B3FF 100%);
  color: white;
}

.stat-item.success {
  background: linear-gradient(135deg, #67C23A 0%, #85CE61 100%);
  color: white;
}

.stat-item.danger {
  background: linear-gradient(135deg, #F56C6C 0%, #F78989 100%);
  color: white;
}

.stat-item.warning {
  background: linear-gradient(135deg, #E6A23C 0%, #EEBE77 100%);
  color: white;
}

.stat-icon {
  margin-right: 12px;
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
  font-size: 12px;
  opacity: 0.8;
  margin-bottom: 4px;
}

.stat-change {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
}

.trend-section {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #E4E7ED;
}

.trend-section h4 {
  margin: 0 0 15px 0;
  color: #303133;
}

.trend-chart {
  display: flex;
  justify-content: center;
}

.trend-chart canvas {
  border: 1px solid #E4E7ED;
  border-radius: 4px;
}
</style>
