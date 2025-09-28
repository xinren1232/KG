<template>
  <div class="real-data-visualization">
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-section">
      <el-col :span="6" v-for="stat in mainStats" :key="stat.key">
        <el-card class="stat-card" :class="stat.type">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon :size="32" :color="stat.color">
                <component :is="stat.icon" />
              </el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stat.value }}</div>
              <div class="stat-label">{{ stat.label }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" class="charts-section">
      <!-- 分类分布饼图 -->
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="chart-header">
              <span>词典分类分布</span>
              <el-button size="small" @click="refreshData">刷新</el-button>
            </div>
          </template>
          <div ref="categoryPieChart" class="chart-container"></div>
        </el-card>
      </el-col>

      <!-- 关系类型柱状图 -->
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="chart-header">
              <span>关系类型分布</span>
              <el-button size="small" @click="exportChart">导出</el-button>
            </div>
          </template>
          <div ref="relationBarChart" class="chart-container"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 标签云 -->
    <el-row :gutter="20" class="charts-section">
      <el-col :span="24">
        <el-card class="chart-card">
          <template #header>
            <div class="chart-header">
              <span>热门标签</span>
              <div class="chart-controls">
                <el-button size="small" @click="resetView">重置视图</el-button>
              </div>
            </div>
          </template>
          <div class="tags-container">
            <el-tag 
              v-for="tag in topTags" 
              :key="tag.name"
              :size="getTagSize(tag.count)"
              :type="getTagType(tag.count)"
              class="tag-item"
            >
              {{ tag.name }} ({{ tag.count }})
            </el-tag>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { 
  Document, 
  Share, 
  Warning, 
  Grid 
} from '@element-plus/icons-vue'
import { kgApi } from '../api'

export default {
  name: 'RealDataVisualization',
  components: {
    Document,
    Share,
    Warning,
    Grid
  },
  setup() {
    // 响应式数据
    const realData = reactive({
      stats: {
        totalNodes: 1124,
        totalRelations: 7581,
        totalCategories: 8,
        totalTags: 79
      },
      categories: [],
      relations: [],
      tags: []
    })

    // 图表引用
    const categoryPieChart = ref(null)
    const relationBarChart = ref(null)

    // 图表实例
    let pieChartInstance = null
    let barChartInstance = null

    // 主要统计数据
    const mainStats = reactive([
      {
        key: 'totalNodes',
        label: '词典条目',
        value: 1124,
        icon: 'Document',
        color: '#409EFF',
        type: 'primary'
      },
      {
        key: 'totalRelations',
        label: '关系数量',
        value: 7581,
        icon: 'Share',
        color: '#67C23A',
        type: 'success'
      },
      {
        key: 'totalCategories',
        label: '分类数量',
        value: 8,
        icon: 'Grid',
        color: '#E6A23C',
        type: 'warning'
      },
      {
        key: 'totalTags',
        label: '标签数量',
        value: 79,
        icon: 'Warning',
        color: '#F56C6C',
        type: 'danger'
      }
    ])

    const topTags = ref([
      { name: '可靠性', count: 45 },
      { name: '质量控制', count: 38 },
      { name: '测试', count: 35 },
      { name: '工艺', count: 32 },
      { name: 'SMT', count: 28 },
      { name: '电路', count: 25 },
      { name: '焊接', count: 22 },
      { name: '检测', count: 20 },
      { name: '失效', count: 18 },
      { name: '标准', count: 15 }
    ])

    // 初始化图表
    const initCharts = async () => {
      await nextTick()
      
      try {
        const echarts = await import('echarts')
        
        // 初始化分类饼图
        if (categoryPieChart.value) {
          pieChartInstance = echarts.init(categoryPieChart.value)
          updatePieChart()
        }

        // 初始化关系柱状图
        if (relationBarChart.value) {
          barChartInstance = echarts.init(relationBarChart.value)
          updateBarChart()
        }

      } catch (error) {
        console.error('初始化图表失败:', error)
        ElMessage.error('图表初始化失败')
      }
    }

    // 更新饼图
    const updatePieChart = () => {
      if (!pieChartInstance) return

      const pieOption = {
        title: {
          text: '词典分类分布',
          left: 'center'
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        series: [{
          name: '分类',
          type: 'pie',
          radius: '60%',
          data: [
            { value: 259, name: 'Symptom' },
            { value: 190, name: 'Metric' },
            { value: 181, name: 'Component' },
            { value: 170, name: 'Process' },
            { value: 104, name: 'TestCase' },
            { value: 102, name: 'Tool' },
            { value: 63, name: 'Role' },
            { value: 55, name: 'Material' }
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

    // 更新柱状图
    const updateBarChart = () => {
      if (!barChartInstance) return

      const barOption = {
        title: {
          text: '关系类型分布',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: ['HAS_TAG', 'IN_MODULE', 'HAS_ALIAS', 'IN_CATEGORY', 'SAME_AS']
        },
        yAxis: {
          type: 'value'
        },
        series: [{
          name: '关系数量',
          type: 'bar',
          data: [3015, 1900, 1506, 1124, 36],
          itemStyle: {
            color: '#409EFF'
          }
        }]
      }
      barChartInstance.setOption(barOption)
    }

    // 刷新数据
    const refreshData = async () => {
      try {
        const response = await kgApi.getRealGraphStats()
        if (response && response.data) {
          // 更新统计数据
          Object.assign(realData.stats, response.data.stats)
          
          // 更新主要统计卡片
          mainStats[0].value = realData.stats.totalNodes
          mainStats[1].value = realData.stats.totalRelations
          mainStats[2].value = realData.stats.totalCategories
          mainStats[3].value = realData.stats.totalTags

          // 更新图表
          updatePieChart()
          updateBarChart()

          ElMessage.success('数据刷新成功')
        }
      } catch (error) {
        ElMessage.error('刷新数据失败: ' + error.message)
      }
    }

    // 获取标签大小
    const getTagSize = (count) => {
      if (count > 40) return 'large'
      if (count > 25) return 'default'
      return 'small'
    }

    // 获取标签类型
    const getTagType = (count) => {
      if (count > 40) return 'danger'
      if (count > 30) return 'warning'
      if (count > 20) return 'success'
      return 'info'
    }

    const resetView = () => {
      if (pieChartInstance) pieChartInstance.resize()
      if (barChartInstance) barChartInstance.resize()
    }

    const exportChart = () => {
      ElMessage.info('导出功能开发中...')
    }

    onMounted(() => {
      initCharts()
    })

    return {
      realData,
      mainStats,
      topTags,
      categoryPieChart,
      relationBarChart,
      refreshData,
      resetView,
      exportChart,
      getTagSize,
      getTagType
    }
  }
}
</script>

<style scoped>
.real-data-visualization {
  padding: 20px;
}

.stats-section {
  margin-bottom: 20px;
}

.stat-card {
  height: 120px;
  cursor: pointer;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.stat-content {
  display: flex;
  align-items: center;
  height: 100%;
}

.stat-icon {
  margin-right: 15px;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 5px;
}

.stat-label {
  color: #666;
  font-size: 14px;
}

.charts-section {
  margin-bottom: 20px;
}

.chart-card {
  height: 400px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-container {
  height: 320px;
}

.tags-container {
  padding: 20px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tag-item {
  margin: 5px;
  cursor: pointer;
  transition: all 0.3s;
}

.tag-item:hover {
  transform: scale(1.1);
}
</style>
