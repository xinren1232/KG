<template>
  <div class="data-governance">
    <el-card class="header-card">
      <div class="page-header">
        <h2>🏛️ 数据治理</h2>
        <p>基于真实数据的质量监控、标准化管理和持续优化</p>
        <div class="header-actions">
          <el-button type="primary" @click="refreshData" :loading="loading">
            <el-icon><Refresh /></el-icon>
            刷新数据
          </el-button>
          <el-button @click="exportReport">
            <el-icon><Download /></el-icon>
            导出报告
          </el-button>
        </div>
      </div>
    </el-card>

    <!-- 数据质量概览 -->
    <el-row :gutter="20" class="overview-cards">
      <el-col :span="6">
        <el-card class="metric-card" shadow="hover">
          <div class="metric">
            <div class="metric-icon">
              <el-icon color="#409EFF"><DataAnalysis /></el-icon>
            </div>
            <div class="metric-content">
              <div class="metric-value">{{ overallStats.total_entries || 0 }}</div>
              <div class="metric-label">硬件质量术语</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="metric-card" shadow="hover">
          <div class="metric">
            <div class="metric-icon">
              <el-icon color="#67C23A"><Connection /></el-icon>
            </div>
            <div class="metric-content">
              <div class="metric-value">{{ overallStats.total_relations || 0 }}</div>
              <div class="metric-label">关系连接</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="metric-card" shadow="hover">
          <div class="metric">
            <div class="metric-icon">
              <el-icon :color="getQualityColor(overallStats.quality_score)"><TrendCharts /></el-icon>
            </div>
            <div class="metric-content">
              <div class="metric-value">{{ overallStats.quality_score || 0 }}%</div>
              <div class="metric-label">数据质量分</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="metric-card" shadow="hover">
          <div class="metric">
            <div class="metric-icon">
              <el-icon color="#E6A23C"><Calendar /></el-icon>
            </div>
            <div class="metric-content">
              <div class="metric-value">{{ overallStats.last_update || 'N/A' }}</div>
              <div class="metric-label">最后更新</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 数据质量指标 -->
    <el-card class="quality-card">
      <div class="card-header">
        <h3>📊 数据质量指标</h3>
        <el-tag :type="getOverallStatusType()" size="large">
          {{ getOverallStatusText() }}
        </el-tag>
      </div>
      
      <el-table :data="qualityMetrics" stripe style="width: 100%" v-loading="loading">
        <el-table-column prop="metric" label="质量指标" width="180">
          <template #default="scope">
            <div class="metric-name">
              <el-icon><TrendCharts /></el-icon>
              {{ scope.row.metric }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="说明" width="200" show-overflow-tooltip />
        <el-table-column prop="value" label="当前值" width="120">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)" size="small">
              {{ scope.row.value }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="percentage" label="完成度" width="150">
          <template #default="scope">
            <div class="progress-container">
              <el-progress 
                :percentage="scope.row.percentage" 
                :status="getProgressStatus(scope.row.percentage)"
                :stroke-width="8"
              />
              <span class="progress-text">{{ scope.row.percentage }}%</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="target" label="目标值" width="80">
          <template #default="scope">
            <span class="target-value">{{ scope.row.target }}%</span>
          </template>
        </el-table-column>
        <el-table-column prop="trend" label="趋势" width="100">
          <template #default="scope">
            <el-tag 
              :type="getTrendType(scope.row.trend)" 
              size="small"
              effect="plain"
            >
              <el-icon>
                <component :is="getTrendIcon(scope.row.trend)" />
              </el-icon>
              {{ getTrendText(scope.row.trend) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 分类分布和问题统计 -->
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card class="chart-card">
          <h3>📈 分类分布</h3>
          <div ref="categoryChart" style="height: 300px;"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="issues-card">
          <h3>⚠️ 数据质量问题</h3>
          <div class="issues-list">
            <div 
              v-for="issue in issues" 
              :key="issue.description"
              class="issue-item"
              :class="`issue-${issue.severity}`"
            >
              <div class="issue-header">
                <el-tag :type="getIssueType(issue.type)" size="small">
                  {{ issue.category }}
                </el-tag>
                <span class="issue-count">{{ issue.affected_records }}条</span>
              </div>
              <div class="issue-description">{{ issue.description }}</div>
              <div class="issue-recommendation">
                <el-icon><TrendCharts /></el-icon>
                {{ issue.recommendation }}
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 治理规则和建议 -->
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card class="rules-card">
          <h3>📋 治理规则</h3>
          <el-table :data="governanceRules" size="small">
            <el-table-column prop="name" label="规则名称" />
            <el-table-column prop="type" label="类型" width="100">
              <template #default="scope">
                <el-tag size="small" :type="scope.row.type === 'validation' ? 'primary' : 'success'">
                  {{ scope.row.type === 'validation' ? '验证' : '标准化' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="80">
              <template #default="scope">
                <el-tag size="small" :type="scope.row.status === 'active' ? 'success' : 'warning'">
                  {{ scope.row.status === 'active' ? '启用' : '禁用' }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="recommendations-card">
          <h3>💡 优化建议</h3>
          <div class="recommendations-list">
            <div 
              v-for="rec in recommendations" 
              :key="rec.title"
              class="recommendation-item"
              :class="`priority-${rec.priority}`"
            >
              <div class="rec-header">
                <el-tag :type="getPriorityType(rec.priority)" size="small">
                  {{ getPriorityText(rec.priority) }}
                </el-tag>
                <span class="rec-effort">{{ rec.estimated_effort }}</span>
              </div>
              <div class="rec-title">{{ rec.title }}</div>
              <div class="rec-description">{{ rec.description }}</div>
              <div class="rec-impact">
                <el-icon><TrendCharts /></el-icon>
                {{ rec.impact }}
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Refresh,
  Download,
  DataAnalysis,
  Connection,
  TrendCharts,
  Calendar,
  ArrowUp,
  ArrowDown,
  Minus
} from '@element-plus/icons-vue'
import api from '@/api'

export default {
  name: 'DataGovernanceNew',
  components: {
    Refresh,
    Download,
    DataAnalysis,
    Connection,
    TrendCharts,
    Calendar,
    ArrowUp,
    ArrowDown,
    Minus
  },
  setup() {
    const loading = ref(false)
    const overallStats = ref({})
    const qualityMetrics = ref([])
    const categoryDistribution = ref({})
    const issues = ref([])
    const governanceRules = ref([])
    const recommendations = ref([])
    const categoryChart = ref(null)

    // 获取数据治理信息
    const fetchGovernanceData = async () => {
      loading.value = true
      try {
        const response = await api.getGovernanceData()
        if (response.success && response.data) {
          const data = response.data
          overallStats.value = data.data_overview || {}
          qualityMetrics.value = data.quality_metrics || []
          categoryDistribution.value = data.category_distribution || {}
          issues.value = data.issues || []
          governanceRules.value = data.governance_rules || []
          recommendations.value = data.recommendations || []
          
          // 渲染图表
          nextTick(() => {
            renderCategoryChart()
          })
        }
      } catch (error) {
        console.error('获取数据治理信息失败:', error)
        ElMessage.error('获取数据治理信息失败')
      } finally {
        loading.value = false
      }
    }

    // 渲染分类分布图表
    const renderCategoryChart = async () => {
      if (!categoryChart.value) return
      
      const echarts = await import('echarts')
      const chart = echarts.init(categoryChart.value)
      
      const data = Object.entries(categoryDistribution.value).map(([name, value]) => ({
        name,
        value
      }))
      
      const option = {
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        series: [{
          name: '分类分布',
          type: 'pie',
          radius: ['40%', '70%'],
          avoidLabelOverlap: false,
          label: {
            show: false,
            position: 'center'
          },
          emphasis: {
            label: {
              show: true,
              fontSize: '18',
              fontWeight: 'bold'
            }
          },
          labelLine: {
            show: false
          },
          data: data
        }]
      }
      
      chart.setOption(option)
    }

    // 工具函数
    const getQualityColor = (score) => {
      if (score >= 90) return '#67C23A'
      if (score >= 80) return '#E6A23C'
      return '#F56C6C'
    }

    const getStatusType = (status) => {
      const types = {
        'excellent': 'success',
        'good': 'primary',
        'warning': 'warning',
        'error': 'danger'
      }
      return types[status] || 'info'
    }

    const getStatusText = (status) => {
      const texts = {
        'excellent': '优秀',
        'good': '良好',
        'warning': '警告',
        'error': '错误'
      }
      return texts[status] || '未知'
    }

    const getProgressStatus = (percentage) => {
      if (percentage >= 95) return 'success'
      if (percentage >= 85) return ''
      if (percentage >= 70) return 'warning'
      return 'exception'
    }

    const getTrendType = (trend) => {
      const types = {
        'improving': 'success',
        'stable': 'primary',
        'declining': 'warning'
      }
      return types[trend] || 'info'
    }

    const getTrendIcon = (trend) => {
      const icons = {
        'improving': 'ArrowUp',
        'stable': 'Minus',
        'declining': 'ArrowDown'
      }
      return icons[trend] || 'Minus'
    }

    const getTrendText = (trend) => {
      const texts = {
        'improving': '改善',
        'stable': '稳定',
        'declining': '下降'
      }
      return texts[trend] || '稳定'
    }

    const getOverallStatusType = () => {
      const score = overallStats.value.quality_score || 0
      if (score >= 90) return 'success'
      if (score >= 80) return 'primary'
      if (score >= 70) return 'warning'
      return 'danger'
    }

    const getOverallStatusText = () => {
      const score = overallStats.value.quality_score || 0
      if (score >= 90) return '优秀'
      if (score >= 80) return '良好'
      if (score >= 70) return '一般'
      return '需改进'
    }

    const getIssueType = (type) => {
      const types = {
        'warning': 'warning',
        'error': 'danger',
        'info': 'info'
      }
      return types[type] || 'info'
    }

    const getPriorityType = (priority) => {
      const types = {
        'high': 'danger',
        'medium': 'warning',
        'low': 'info'
      }
      return types[priority] || 'info'
    }

    const getPriorityText = (priority) => {
      const texts = {
        'high': '高优先级',
        'medium': '中优先级',
        'low': '低优先级'
      }
      return texts[priority] || '未知'
    }

    // 刷新数据
    const refreshData = () => {
      fetchGovernanceData()
    }

    // 导出报告
    const exportReport = () => {
      ElMessage.info('导出功能开发中...')
    }

    onMounted(() => {
      fetchGovernanceData()
    })

    return {
      loading,
      overallStats,
      qualityMetrics,
      categoryDistribution,
      issues,
      governanceRules,
      recommendations,
      categoryChart,
      refreshData,
      exportReport,
      getQualityColor,
      getStatusType,
      getStatusText,
      getProgressStatus,
      getTrendType,
      getTrendIcon,
      getTrendText,
      getOverallStatusType,
      getOverallStatusText,
      getIssueType,
      getPriorityType,
      getPriorityText
    }
  }
}
</script>

<style scoped>
.data-governance {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.header-card {
  margin-bottom: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-header h2 {
  margin: 0;
  color: #303133;
  font-size: 24px;
}

.page-header p {
  margin: 5px 0 0 0;
  color: #909399;
  font-size: 14px;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.overview-cards {
  margin-bottom: 20px;
}

.metric-card {
  height: 120px;
  transition: all 0.3s ease;
}

.metric-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.metric {
  display: flex;
  align-items: center;
  height: 100%;
  padding: 20px;
}

.metric-icon {
  margin-right: 15px;
  font-size: 32px;
}

.metric-content {
  flex: 1;
}

.metric-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
  line-height: 1;
}

.metric-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}

.quality-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.card-header h3 {
  margin: 0;
  color: #303133;
  font-size: 18px;
}

.metric-name {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
}

.progress-container {
  display: flex;
  align-items: center;
  gap: 10px;
}

.progress-text {
  font-size: 12px;
  color: #909399;
  min-width: 35px;
}

.target-value {
  color: #909399;
  font-size: 12px;
}

.chart-card, .issues-card, .rules-card, .recommendations-card {
  margin-bottom: 20px;
}

.chart-card h3, .issues-card h3, .rules-card h3, .recommendations-card h3 {
  margin: 0 0 20px 0;
  color: #303133;
  font-size: 16px;
}

.issues-list {
  max-height: 300px;
  overflow-y: auto;
}

.issue-item {
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 8px;
  border-left: 4px solid #dcdfe6;
}

.issue-item.issue-high {
  border-left-color: #f56c6c;
  background-color: #fef0f0;
}

.issue-item.issue-medium {
  border-left-color: #e6a23c;
  background-color: #fdf6ec;
}

.issue-item.issue-low {
  border-left-color: #909399;
  background-color: #f4f4f5;
}

.issue-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.issue-count {
  font-size: 12px;
  color: #909399;
  font-weight: bold;
}

.issue-description {
  font-size: 14px;
  color: #303133;
  margin-bottom: 8px;
}

.issue-recommendation {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  color: #606266;
  font-style: italic;
}

.recommendations-list {
  max-height: 300px;
  overflow-y: auto;
}

.recommendation-item {
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 8px;
  border: 1px solid #dcdfe6;
  background-color: #fff;
}

.recommendation-item.priority-high {
  border-color: #f56c6c;
  background-color: #fef0f0;
}

.recommendation-item.priority-medium {
  border-color: #e6a23c;
  background-color: #fdf6ec;
}

.recommendation-item.priority-low {
  border-color: #67c23a;
  background-color: #f0f9ff;
}

.rec-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.rec-effort {
  font-size: 12px;
  color: #909399;
}

.rec-title {
  font-size: 14px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 5px;
}

.rec-description {
  font-size: 13px;
  color: #606266;
  margin-bottom: 8px;
}

.rec-impact {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  color: #67c23a;
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .data-governance {
    padding: 10px;
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .header-actions {
    width: 100%;
    justify-content: flex-end;
  }

  .metric {
    padding: 15px;
  }

  .metric-value {
    font-size: 24px;
  }

  .metric-icon {
    font-size: 28px;
  }
}
</style>
