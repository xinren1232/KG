<template>
  <div class="data-visualization">
    <!-- 统计概览 -->
    <el-row :gutter="20" class="stats-overview">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">{{ stats.totalNodes }}</div>
            <div class="stat-label">图谱节点</div>
          </div>
          <el-icon class="stat-icon" color="#409EFF"><DataAnalysis /></el-icon>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">{{ stats.totalRelations }}</div>
            <div class="stat-label">关系连接</div>
          </div>
          <el-icon class="stat-icon" color="#67C23A"><Share /></el-icon>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">{{ stats.totalAnomalies }}</div>
            <div class="stat-label">异常记录</div>
          </div>
          <el-icon class="stat-icon" color="#F56C6C"><Warning /></el-icon>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">{{ stats.totalComponents }}</div>
            <div class="stat-label">组件类型</div>
          </div>
          <el-icon class="stat-icon" color="#E6A23C"><Grid /></el-icon>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" class="charts-section">
      <!-- 实体类型分布饼图 -->
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <span>实体类型分布</span>
          </template>
          <div ref="entityPieChart" class="chart-container"></div>
        </el-card>
      </el-col>

      <!-- 异常严重程度分布 -->
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <span>异常严重程度分布</span>
          </template>
          <div ref="severityBarChart" class="chart-container"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="charts-section">
      <!-- 时间趋势图 -->
      <el-col :span="24">
        <el-card class="chart-card">
          <template #header>
            <div class="chart-header">
              <span>异常发现趋势</span>
              <el-button-group>
                <el-button size="small" @click="changeTimeRange('7d')">7天</el-button>
                <el-button size="small" @click="changeTimeRange('30d')">30天</el-button>
                <el-button size="small" @click="changeTimeRange('90d')">90天</el-button>
              </el-button-group>
            </div>
          </template>
          <div ref="trendLineChart" class="chart-container-large"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 网络图谱 -->
    <el-row :gutter="20" class="charts-section">
      <el-col :span="24">
        <el-card class="chart-card">
          <template #header>
            <div class="chart-header">
              <span>知识图谱网络</span>
              <div class="chart-controls">
                <el-button size="small" @click="resetNetworkView">重置视图</el-button>
                <el-button size="small" @click="exportNetwork">导出图片</el-button>
              </div>
            </div>
          </template>
          <div ref="networkGraph" class="chart-container-network"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { 
  DataAnalysis, 
  Share, 
  Warning, 
  Grid 
} from '@element-plus/icons-vue'

export default {
  name: 'DataVisualization',
  components: {
    DataAnalysis,
    Share,
    Warning,
    Grid
  },
  setup() {
    // 响应式数据 - 使用真实的Neo4j数据
    const stats = reactive({
      totalNodes: 1124,
      totalRelations: 7581,
      totalCategories: 8,
      totalTags: 79
    })

    // 图表引用
    const entityPieChart = ref(null)
    const severityBarChart = ref(null)
    const trendLineChart = ref(null)
    const networkGraph = ref(null)

    // 图表实例
    let pieChartInstance = null
    let barChartInstance = null
    let lineChartInstance = null
    let networkInstance = null

    // 初始化图表
    const initCharts = async () => {
      await nextTick()
      
      // 动态导入ECharts
      try {
        const echarts = await import('echarts')
        
        // 初始化饼图
        if (entityPieChart.value) {
          pieChartInstance = echarts.init(entityPieChart.value)
          const pieOption = {
            title: {
              text: '实体分布',
              left: 'center'
            },
            tooltip: {
              trigger: 'item',
              formatter: '{a} <br/>{b}: {c} ({d}%)'
            },
            series: [{
              name: '实体类型',
              type: 'pie',
              radius: '60%',
              data: [
                { value: 45, name: '异常' },
                { value: 32, name: '组件' },
                { value: 28, name: '产品' },
                { value: 25, name: '症状' },
                { value: 15, name: '供应商' },
                { value: 11, name: '测试用例' }
              ],
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              }
            }]
          }
          pieChartInstance.setOption(pieOption)
        }

        // 初始化柱状图
        if (severityBarChart.value) {
          barChartInstance = echarts.init(severityBarChart.value)
          const barOption = {
            title: {
              text: '严重程度',
              left: 'center'
            },
            tooltip: {
              trigger: 'axis'
            },
            xAxis: {
              type: 'category',
              data: ['S1', 'S2', 'S3', 'S4']
            },
            yAxis: {
              type: 'value'
            },
            series: [{
              name: '异常数量',
              type: 'bar',
              data: [15, 18, 8, 4],
              itemStyle: {
                color: function(params) {
                  const colors = ['#F56C6C', '#E6A23C', '#409EFF', '#67C23A']
                  return colors[params.dataIndex]
                }
              }
            }]
          }
          barChartInstance.setOption(barOption)
        }

        // 初始化趋势图
        if (trendLineChart.value) {
          lineChartInstance = echarts.init(trendLineChart.value)
          const lineOption = {
            title: {
              text: '异常趋势',
              left: 'center'
            },
            tooltip: {
              trigger: 'axis'
            },
            xAxis: {
              type: 'category',
              data: ['12-01', '12-02', '12-03', '12-04', '12-05', '12-06', '12-07']
            },
            yAxis: {
              type: 'value'
            },
            series: [{
              name: '新增异常',
              type: 'line',
              data: [2, 3, 1, 4, 2, 1, 3],
              smooth: true,
              itemStyle: {
                color: '#409EFF'
              }
            }]
          }
          lineChartInstance.setOption(lineOption)
        }

        // 初始化网络图
        initNetworkGraph()

      } catch (error) {
        console.error('图表初始化失败:', error)
      }
    }

    const initNetworkGraph = () => {
      if (!networkGraph.value) return

      // 简化的网络图实现
      const container = networkGraph.value
      container.innerHTML = `
        <div style="display: flex; align-items: center; justify-content: center; height: 100%; color: #909399;">
          <div style="text-align: center;">
            <div style="font-size: 48px; margin-bottom: 10px;">🕸️</div>
            <div>网络图谱</div>
            <div style="font-size: 12px; margin-top: 5px;">节点: ${stats.totalNodes} | 边: ${stats.totalRelations}</div>
          </div>
        </div>
      `
    }

    const changeTimeRange = (range) => {
      console.log('切换时间范围:', range)
      // 这里可以重新加载数据并更新图表
    }

    const resetNetworkView = () => {
      console.log('重置网络视图')
      initNetworkGraph()
    }

    const exportNetwork = () => {
      console.log('导出网络图片')
    }

    // 响应式处理
    const handleResize = () => {
      if (pieChartInstance) pieChartInstance.resize()
      if (barChartInstance) barChartInstance.resize()
      if (lineChartInstance) lineChartInstance.resize()
    }

    onMounted(() => {
      initCharts()
      window.addEventListener('resize', handleResize)
    })

    return {
      stats,
      entityPieChart,
      severityBarChart,
      trendLineChart,
      networkGraph,
      changeTimeRange,
      resetNetworkView,
      exportNetwork
    }
  }
}
</script>

<style scoped>
.data-visualization {
  padding: 20px;
}

.stats-overview {
  margin-bottom: 20px;
}

.stat-card {
  position: relative;
  overflow: hidden;
}

.stat-content {
  position: relative;
  z-index: 2;
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #606266;
}

.stat-icon {
  position: absolute;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 48px;
  opacity: 0.1;
}

.charts-section {
  margin-bottom: 20px;
}

.chart-card {
  height: 100%;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-controls {
  display: flex;
  gap: 10px;
}

.chart-container {
  height: 300px;
  width: 100%;
}

.chart-container-large {
  height: 400px;
  width: 100%;
}

.chart-container-network {
  height: 500px;
  width: 100%;
  border: 1px solid #ebeef5;
  border-radius: 4px;
}

@media (max-width: 768px) {
  .stats-overview .el-col {
    margin-bottom: 15px;
  }
  
  .chart-header {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }
}
</style>
