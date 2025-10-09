<template>
  <div class="dictionary-schema">
    <div class="schema-header">
      <h2>📚 词典分类Schema设计</h2>
      <p class="description">展示词典的分类结构、统计信息和设计逻辑</p>
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
              <el-icon><Collection /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ stats.totalTerms }}</div>
              <div class="stat-label">术语总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="stat-icon" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
              <el-icon><FolderOpened /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ stats.totalCategories }}</div>
              <div class="stat-label">分类数量</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="stat-icon" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
              <el-icon><PriceTag /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ stats.totalTags }}</div>
              <div class="stat-label">标签数量</div>
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
              <div class="stat-number">{{ stats.totalAliases }}</div>
              <div class="stat-label">别名数量</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 分类详情 -->
    <el-card class="category-details" shadow="hover">
      <template #header>
        <div class="card-header">
          <span><el-icon><FolderOpened /></el-icon> 分类详情</span>
          <el-input
            v-model="searchText"
            placeholder="搜索分类..."
            style="width: 200px"
            clearable
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </div>
      </template>

      <el-table
        :data="filteredCategories"
        style="width: 100%"
        :default-sort="{ prop: 'termCount', order: 'descending' }"
        v-loading="loading"
      >
        <el-table-column type="index" label="#" width="60" />
        <el-table-column prop="name" label="分类名称" min-width="150">
          <template #default="{ row }">
            <el-tag :type="getCategoryTagType(row.name)" effect="plain">
              {{ row.name }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="termCount" label="术语数量" width="120" sortable>
          <template #default="{ row }">
            <el-badge :value="row.termCount" :max="999" class="item">
              <el-button size="small">术语</el-button>
            </el-badge>
          </template>
        </el-table-column>
        <el-table-column prop="tagCount" label="标签数量" width="120" sortable>
          <template #default="{ row }">
            <span class="count-badge">{{ row.tagCount }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="aliasCount" label="别名数量" width="120" sortable>
          <template #default="{ row }">
            <span class="count-badge">{{ row.aliasCount }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="percentage" label="占比" width="120" sortable>
          <template #default="{ row }">
            <el-progress
              :percentage="row.percentage"
              :color="getProgressColor(row.percentage)"
              :stroke-width="12"
            />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button size="small" type="primary" @click="viewCategoryDetails(row)">
              查看详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 分类分布图表 -->
    <el-row :gutter="20" class="charts-section">
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <span><el-icon><PieChart /></el-icon> 分类分布（饼图）</span>
          </template>
          <div ref="pieChartRef" style="height: 400px;"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <span><el-icon><Histogram /></el-icon> 分类统计（柱状图）</span>
          </template>
          <div ref="barChartRef" style="height: 400px;"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 设计说明 -->
    <el-card class="design-notes" shadow="hover">
      <template #header>
        <span><el-icon><Document /></el-icon> 词典Schema设计说明</span>
      </template>
      <el-descriptions :column="1" border>
        <el-descriptions-item label="设计目的">
          建立标准化的质量术语词典，支持多领域（摄像头、显示、射频等）的术语管理和别名映射
        </el-descriptions-item>
        <el-descriptions-item label="核心实体">
          <el-tag type="success" class="entity-tag">Term (术语)</el-tag>
          <el-tag type="warning" class="entity-tag">Category (分类)</el-tag>
          <el-tag type="info" class="entity-tag">Tag (标签)</el-tag>
          <el-tag type="danger" class="entity-tag">Alias (别名)</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="关系设计">
          <div class="relationship-list">
            <div class="relationship-item">
              <code>Term -[BELONGS_TO]-> Category</code>
              <span class="desc">术语归属于分类</span>
            </div>
            <div class="relationship-item">
              <code>Term -[HAS_TAG]-> Tag</code>
              <span class="desc">术语具有标签</span>
            </div>
            <div class="relationship-item">
              <code>Alias -[ALIAS_OF]-> Term</code>
              <span class="desc">别名指向术语</span>
            </div>
          </div>
        </el-descriptions-item>
        <el-descriptions-item label="应用场景">
          文档解析、实体识别、知识抽取、智能问答、数据标准化
        </el-descriptions-item>
        <el-descriptions-item label="扩展性">
          支持动态添加新分类、新术语、新标签，支持多对多关系
        </el-descriptions-item>
      </el-descriptions>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Refresh,
  Collection,
  FolderOpened,
  PriceTag,
  Link,
  Search,
  Document,
  PieChart,
  Histogram
} from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import { httpClient as api } from '@/api'

// 响应式数据
const loading = ref(false)
const searchText = ref('')
const pieChartRef = ref(null)
const barChartRef = ref(null)

const stats = reactive({
  totalTerms: 0,
  totalCategories: 0,
  totalTags: 0,
  totalAliases: 0
})

const categories = ref([])

// 计算属性
const filteredCategories = computed(() => {
  if (!searchText.value) return categories.value
  return categories.value.filter(cat =>
    cat.name.toLowerCase().includes(searchText.value.toLowerCase())
  )
})

// 方法
const refreshData = async () => {
  loading.value = true
  try {
    // 获取词典统计数据
    const statsRes = await api.get('/kg/dictionary/stats')
    if (statsRes.data.ok) {
      Object.assign(stats, statsRes.data.data)
    }

    // 获取分类详情
    const categoriesRes = await api.get('/kg/dictionary/categories')
    if (categoriesRes.data.ok) {
      categories.value = categoriesRes.data.data.map(cat => ({
        ...cat,
        percentage: parseFloat(((cat.termCount / stats.totalTerms) * 100).toFixed(1))
      }))
    }

    // 渲染图表
    await nextTick()
    renderCharts()

    ElMessage.success('数据刷新成功')
  } catch (error) {
    console.error('刷新数据失败:', error)
    ElMessage.error('数据刷新失败')
  } finally {
    loading.value = false
  }
}

const getCategoryTagType = (name) => {
  const typeMap = {
    '摄像头': 'success',
    '显示': 'warning',
    '射频': 'danger',
    '音频': 'info',
    '电池': 'primary'
  }
  return typeMap[name] || 'info'  // 默认返回 'info' 而不是空字符串
}

const getProgressColor = (percentage) => {
  if (percentage > 20) return '#67c23a'
  if (percentage > 10) return '#e6a23c'
  return '#f56c6c'
}

const viewCategoryDetails = (row) => {
  ElMessage.info(`查看分类详情: ${row.name}`)
  // TODO: 实现详情查看
}

let renderRetryCount = 0
const MAX_RETRY = 10

const renderCharts = () => {
  if (!pieChartRef.value || !barChartRef.value) return

  // 确保容器有尺寸
  if (!pieChartRef.value.clientWidth || !pieChartRef.value.clientHeight) {
    if (renderRetryCount < MAX_RETRY) {
      renderRetryCount++
      setTimeout(renderCharts, 100)
    } else {
      console.error('图表容器尺寸始终为0，无法渲染')
    }
    return
  }

  renderRetryCount = 0  // 重置重试计数

  // 饼图
  const pieChart = echarts.init(pieChartRef.value)
  pieChart.setOption({
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '分类分布',
        type: 'pie',
        radius: '50%',
        data: categories.value.map(cat => ({
          name: cat.name,
          value: cat.termCount
        })),
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  })

  // 柱状图
  const barChart = echarts.init(barChartRef.value)
  barChart.setOption({
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    xAxis: {
      type: 'category',
      data: categories.value.map(cat => cat.name),
      axisLabel: {
        rotate: 45
      }
    },
    yAxis: {
      type: 'value',
      name: '数量'
    },
    series: [
      {
        name: '术语数量',
        type: 'bar',
        data: categories.value.map(cat => cat.termCount),
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#83bff6' },
            { offset: 0.5, color: '#188df0' },
            { offset: 1, color: '#188df0' }
          ])
        },
        emphasis: {
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#2378f7' },
              { offset: 0.7, color: '#2378f7' },
              { offset: 1, color: '#83bff6' }
            ])
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
  renderCharts  // 暴露 renderCharts 方法，供父组件在标签页切换时调用
})
</script>

<style scoped>
.dictionary-schema {
  padding: 20px;
}

.schema-header {
  margin-bottom: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
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

.category-details {
  margin-bottom: 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.count-badge {
  display: inline-block;
  padding: 4px 12px;
  background: #f0f9ff;
  color: #409eff;
  border-radius: 12px;
  font-weight: 500;
}

.charts-section {
  margin-bottom: 24px;
}

.design-notes {
  margin-bottom: 24px;
}

.entity-tag {
  margin-right: 8px;
  margin-bottom: 8px;
}

.relationship-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.relationship-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.relationship-item code {
  background: #f5f7fa;
  padding: 4px 8px;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  color: #e6a23c;
}

.relationship-item .desc {
  color: #606266;
  font-size: 14px;
}
</style>

