<template>
  <div class="powerpoint-display">
    <div v-if="data && data.length > 0">
      <!-- PowerPoint统计信息 -->
      <div class="ppt-header">
        <el-row :gutter="20" style="margin-bottom: 16px;">
          <el-col :span="6">
            <el-statistic title="🎨 幻灯片数" :value="getTotalSlides()" />
          </el-col>
          <el-col :span="6">
            <el-statistic title="📝 文本内容" :value="getTextCount()" />
          </el-col>
          <el-col :span="6">
            <el-statistic title="📊 表格数量" :value="getTableCount()" />
          </el-col>
          <el-col :span="6">
            <el-statistic title="🔤 总字符数" :value="getTotalChars()" />
          </el-col>
        </el-row>
      </div>

      <!-- 幻灯片导航 -->
      <div class="slide-navigation" style="margin-bottom: 16px;">
        <el-select v-model="selectedSlide" placeholder="选择幻灯片" @change="handleSlideChange">
          <el-option label="全部幻灯片" value="all" />
          <el-option 
            v-for="slide in getSlideNumbers()" 
            :key="slide" 
            :label="`第 ${slide} 张幻灯片`" 
            :value="slide" 
          />
        </el-select>
        
        <el-radio-group v-model="contentFilter" style="margin-left: 16px;">
          <el-radio-button label="all">全部内容</el-radio-button>
          <el-radio-button label="text">文本内容</el-radio-button>
          <el-radio-button label="table">表格数据</el-radio-button>
        </el-radio-group>
      </div>

      <!-- PowerPoint内容展示 -->
      <div class="ppt-content">
        <div v-for="slide in getGroupedBySlide()" :key="`slide-${slide.slideNumber}`">
          <!-- 幻灯片标题 -->
          <el-divider content-position="left">
            <el-tag type="primary" size="large">🎨 第 {{ slide.slideNumber }} 张幻灯片</el-tag>
          </el-divider>

          <!-- 幻灯片内容 -->
          <div class="slide-content">
            <!-- 文本内容 -->
            <div v-if="contentFilter === 'all' || contentFilter === 'text'">
              <el-card 
                v-for="(item, index) in slide.textItems" 
                :key="`text-${slide.slideNumber}-${index}`"
                class="content-card text-card"
                shadow="hover"
              >
                <template #header>
                  <div class="card-header">
                    <span class="content-type-tag">
                      <el-tag type="success" size="small">📝 文本框 {{ index + 1 }}</el-tag>
                    </span>
                    <span class="content-meta">
                      <el-tag size="small" type="info">{{ item.word_count || getWordCount(item.content) }} 词</el-tag>
                      <el-tag size="small" type="warning">{{ item.char_count || item.content.length }} 字符</el-tag>
                    </span>
                  </div>
                </template>
                <div class="text-content">
                  {{ item.content }}
                </div>
              </el-card>
            </div>

            <!-- 表格内容 -->
            <div v-if="contentFilter === 'all' || contentFilter === 'table'">
              <div v-for="(table, tableIndex) in slide.tables" :key="`table-${slide.slideNumber}-${tableIndex}`">
                <el-card class="content-card table-card" shadow="hover">
                  <template #header>
                    <div class="card-header">
                      <span class="content-type-tag">
                        <el-tag type="warning" size="small">📊 表格 {{ table.tableNumber }}</el-tag>
                      </span>
                      <span class="content-meta">
                        <el-tag size="small" type="info">{{ table.rows.length }} 行</el-tag>
                      </span>
                    </div>
                  </template>
                  <el-table 
                    :data="table.rows" 
                    style="width: 100%"
                    size="small"
                    border
                    stripe
                  >
                    <el-table-column
                      v-for="(column, colIndex) in table.columns"
                      :key="colIndex"
                      :prop="column.prop"
                      :label="column.label"
                      :min-width="120"
                      show-overflow-tooltip
                    />
                  </el-table>
                </el-card>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- PowerPoint结构分析 -->
      <el-card style="margin-top: 20px;">
        <template #header>
          <span>📊 演示文稿分析</span>
        </template>
        <el-row :gutter="16">
          <el-col :span="8">
            <div class="analysis-item">
              <h4>🎨 幻灯片内容分布</h4>
              <div v-for="slide in getSlideAnalysis()" :key="slide.slideNumber" class="slide-item">
                <el-progress 
                  :percentage="slide.contentPercentage" 
                  :color="getSlideColor(slide.contentPercentage)"
                  :stroke-width="8"
                >
                  <template #default="{ percentage }">
                    <span class="progress-text">第{{ slide.slideNumber }}张: {{ slide.contentCount }}项 ({{ percentage }}%)</span>
                  </template>
                </el-progress>
              </div>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="analysis-item">
              <h4>📊 内容类型统计</h4>
              <div class="content-type-stats">
                <div class="stat-item">
                  <el-tag type="success">文本内容</el-tag>
                  <span class="stat-value">{{ getTextCount() }} 个</span>
                </div>
                <div class="stat-item">
                  <el-tag type="warning">表格数据</el-tag>
                  <span class="stat-value">{{ getTableCount() }} 个</span>
                </div>
                <div class="stat-item">
                  <el-tag type="info">平均幻灯片内容</el-tag>
                  <span class="stat-value">{{ getAverageContentPerSlide() }} 项</span>
                </div>
              </div>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="analysis-item">
              <h4>📈 演示质量指标</h4>
              <div class="quality-stats">
                <div class="quality-item">
                  <span class="quality-label">内容丰富度</span>
                  <el-progress 
                    :percentage="getContentRichness()" 
                    :color="getQualityColor(getContentRichness())"
                    :stroke-width="6"
                  />
                </div>
                <div class="quality-item">
                  <span class="quality-label">结构完整性</span>
                  <el-progress 
                    :percentage="getStructureCompleteness()" 
                    :color="getQualityColor(getStructureCompleteness())"
                    :stroke-width="6"
                  />
                </div>
              </div>
            </div>
          </el-col>
        </el-row>
      </el-card>
    </div>
    <el-empty v-else description="未提取到PowerPoint内容" />
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'PowerPointDisplay',
  props: {
    data: {
      type: Array,
      default: () => []
    },
    metadata: {
      type: Object,
      default: () => ({})
    },
    fileInfo: {
      type: Object,
      default: () => ({})
    }
  },
  setup(props) {
    const selectedSlide = ref('all')
    const contentFilter = ref('all')

    const getTotalSlides = () => {
      const slides = new Set()
      props.data.forEach(item => {
        if (item.slide_number) {
          slides.add(item.slide_number)
        }
      })
      return slides.size
    }

    const getTextCount = () => {
      return props.data.filter(item => item.content_type === 'text').length
    }

    const getTableCount = () => {
      const tables = new Set()
      props.data.forEach(item => {
        if (item.content_type === 'table' && item.table_number && item.slide_number) {
          tables.add(`${item.slide_number}-${item.table_number}`)
        }
      })
      return tables.size
    }

    const getTotalChars = () => {
      return props.data.reduce((total, item) => {
        return total + (item.char_count || item.content?.length || 0)
      }, 0)
    }

    const getWordCount = (text) => {
      if (!text) return 0
      return text.trim().split(/\s+/).filter(word => word.length > 0).length
    }

    const getSlideNumbers = () => {
      const slides = new Set()
      props.data.forEach(item => {
        if (item.slide_number) {
          slides.add(item.slide_number)
        }
      })
      return Array.from(slides).sort((a, b) => a - b)
    }

    const getGroupedBySlide = () => {
      const slides = {}
      
      props.data.forEach(item => {
        const slideNum = item.slide_number || 1
        
        if (selectedSlide.value !== 'all' && slideNum !== selectedSlide.value) {
          return
        }
        
        if (!slides[slideNum]) {
          slides[slideNum] = {
            slideNumber: slideNum,
            textItems: [],
            tables: {}
          }
        }
        
        if (item.content_type === 'text') {
          slides[slideNum].textItems.push(item)
        } else if (item.content_type === 'table') {
          const tableKey = item.table_number || 'default'
          if (!slides[slideNum].tables[tableKey]) {
            slides[slideNum].tables[tableKey] = {
              tableNumber: tableKey,
              rows: [],
              columns: []
            }
          }
          
          // 提取表格行数据
          const rowData = {}
          Object.keys(item).forEach(key => {
            if (key.startsWith('column_')) {
              const columnName = key.replace(/^column_\d+_/, '')
              rowData[columnName] = item[key]
            }
          })
          
          if (Object.keys(rowData).length > 0) {
            slides[slideNum].tables[tableKey].rows.push(rowData)
            
            // 更新列信息
            Object.keys(rowData).forEach(colName => {
              if (!slides[slideNum].tables[tableKey].columns.find(col => col.prop === colName)) {
                slides[slideNum].tables[tableKey].columns.push({
                  prop: colName,
                  label: colName
                })
              }
            })
          }
        }
      })
      
      // 转换表格对象为数组
      Object.values(slides).forEach(slide => {
        slide.tables = Object.values(slide.tables)
      })
      
      return Object.values(slides).sort((a, b) => a.slideNumber - b.slideNumber)
    }

    const getSlideAnalysis = () => {
      const slideStats = {}
      
      props.data.forEach(item => {
        const slideNum = item.slide_number || 1
        slideStats[slideNum] = (slideStats[slideNum] || 0) + 1
      })
      
      const maxContent = Math.max(...Object.values(slideStats))
      
      return Object.entries(slideStats).map(([slideNumber, contentCount]) => ({
        slideNumber: parseInt(slideNumber),
        contentCount,
        contentPercentage: Math.round((contentCount / maxContent) * 100)
      })).sort((a, b) => a.slideNumber - b.slideNumber)
    }

    const getAverageContentPerSlide = () => {
      const totalSlides = getTotalSlides()
      return totalSlides > 0 ? Math.round(props.data.length / totalSlides) : 0
    }

    const getContentRichness = () => {
      const textItems = getTextCount()
      const tableItems = getTableCount()
      const totalSlides = getTotalSlides()
      
      if (totalSlides === 0) return 0
      
      const avgContentPerSlide = (textItems + tableItems) / totalSlides
      return Math.min(100, Math.round(avgContentPerSlide * 20)) // 每张幻灯片5项内容为满分
    }

    const getStructureCompleteness = () => {
      const slidesWithText = new Set()
      const slidesWithTables = new Set()
      
      props.data.forEach(item => {
        if (item.content_type === 'text' && item.slide_number) {
          slidesWithText.add(item.slide_number)
        }
        if (item.content_type === 'table' && item.slide_number) {
          slidesWithTables.add(item.slide_number)
        }
      })
      
      const totalSlides = getTotalSlides()
      if (totalSlides === 0) return 0
      
      const textCoverage = (slidesWithText.size / totalSlides) * 100
      const tableCoverage = (slidesWithTables.size / totalSlides) * 50 // 表格权重较低
      
      return Math.round(textCoverage + tableCoverage)
    }

    const getSlideColor = (percentage) => {
      if (percentage >= 80) return '#67c23a'
      if (percentage >= 60) return '#e6a23c'
      if (percentage >= 40) return '#f56c6c'
      return '#909399'
    }

    const getQualityColor = (percentage) => {
      if (percentage >= 70) return '#67c23a'
      if (percentage >= 50) return '#e6a23c'
      if (percentage >= 30) return '#f56c6c'
      return '#909399'
    }

    const handleSlideChange = (value) => {
      selectedSlide.value = value
    }

    return {
      selectedSlide,
      contentFilter,
      getTotalSlides,
      getTextCount,
      getTableCount,
      getTotalChars,
      getWordCount,
      getSlideNumbers,
      getGroupedBySlide,
      getSlideAnalysis,
      getAverageContentPerSlide,
      getContentRichness,
      getStructureCompleteness,
      getSlideColor,
      getQualityColor,
      handleSlideChange
    }
  }
}
</script>

<style scoped>
.powerpoint-display {
  padding: 16px;
}

.ppt-header {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 16px;
}

.slide-navigation {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px;
  background: #fafafa;
  border-radius: 6px;
}

.ppt-content {
  max-height: 700px;
  overflow-y: auto;
}

.slide-content {
  margin-bottom: 24px;
}

.content-card {
  margin-bottom: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.content-type-tag {
  flex: 1;
}

.content-meta {
  display: flex;
  gap: 8px;
}

.text-content {
  line-height: 1.6;
  color: #303133;
  font-size: 14px;
  text-align: justify;
  padding: 8px 0;
}

.text-card {
  border-left: 4px solid #67c23a;
}

.table-card {
  border-left: 4px solid #e6a23c;
}

.analysis-item h4 {
  margin-bottom: 16px;
  color: #303133;
}

.slide-item {
  margin-bottom: 12px;
}

.progress-text {
  font-size: 12px;
  color: #606266;
}

.content-type-stats {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: #f5f7fa;
  border-radius: 4px;
}

.stat-value {
  font-weight: 600;
  color: #303133;
}

.quality-stats {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.quality-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.quality-label {
  font-size: 14px;
  color: #606266;
  font-weight: 500;
}

:deep(.el-statistic__content) {
  font-size: 18px;
  font-weight: 600;
}

:deep(.el-progress-bar__outer) {
  border-radius: 4px;
}

:deep(.el-divider__text) {
  background-color: #fff;
  padding: 0 20px;
}
</style>
