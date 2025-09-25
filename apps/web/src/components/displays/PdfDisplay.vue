<template>
  <div class="pdf-display">
    <div v-if="data && data.length > 0">
      <!-- PDF文档统计信息 -->
      <div class="pdf-header">
        <el-row :gutter="20" style="margin-bottom: 16px;">
          <el-col :span="6">
            <el-statistic title="📄 总页数" :value="getTotalPages()" />
          </el-col>
          <el-col :span="6">
            <el-statistic title="📝 文本段落" :value="getTextCount()" />
          </el-col>
          <el-col :span="6">
            <el-statistic title="📊 表格数量" :value="getTableCount()" />
          </el-col>
          <el-col :span="6">
            <el-statistic title="🔤 总字符数" :value="getTotalChars()" />
          </el-col>
        </el-row>
      </div>

      <!-- 页面导航 -->
      <div class="page-navigation" style="margin-bottom: 16px;">
        <el-select v-model="selectedPage" placeholder="选择页面" @change="handlePageChange">
          <el-option label="全部页面" value="all" />
          <el-option 
            v-for="page in getPageNumbers()" 
            :key="page" 
            :label="`第 ${page} 页`" 
            :value="page" 
          />
        </el-select>
        
        <el-radio-group v-model="contentFilter" style="margin-left: 16px;">
          <el-radio-button label="all">全部内容</el-radio-button>
          <el-radio-button label="text">文本内容</el-radio-button>
          <el-radio-button label="table">表格数据</el-radio-button>
        </el-radio-group>
      </div>

      <!-- PDF内容展示 -->
      <div class="pdf-content">
        <div v-for="page in getGroupedByPage()" :key="`page-${page.pageNumber}`">
          <!-- 页面标题 -->
          <el-divider content-position="left">
            <el-tag type="primary" size="large">📄 第 {{ page.pageNumber }} 页</el-tag>
          </el-divider>

          <!-- 页面内容 -->
          <div class="page-content">
            <!-- 文本内容 -->
            <div v-if="contentFilter === 'all' || contentFilter === 'text'">
              <el-card 
                v-for="(item, index) in page.textItems" 
                :key="`text-${page.pageNumber}-${index}`"
                class="content-card text-card"
                shadow="hover"
              >
                <template #header>
                  <div class="card-header">
                    <span class="content-type-tag">
                      <el-tag type="success" size="small">📝 段落 {{ item.paragraph_number }}</el-tag>
                    </span>
                    <span class="content-meta">
                      <el-tag size="small" type="info">{{ item.word_count }} 词</el-tag>
                      <el-tag size="small" type="warning">{{ item.char_count }} 字符</el-tag>
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
              <div v-for="(table, tableIndex) in page.tables" :key="`table-${page.pageNumber}-${tableIndex}`">
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

      <!-- PDF结构分析 -->
      <el-card style="margin-top: 20px;">
        <template #header>
          <span>📊 PDF结构分析</span>
        </template>
        <el-row :gutter="16">
          <el-col :span="8">
            <div class="analysis-item">
              <h4>📄 页面内容分布</h4>
              <div v-for="page in getPageAnalysis()" :key="page.pageNumber" class="page-item">
                <el-progress 
                  :percentage="page.contentPercentage" 
                  :color="getPageColor(page.contentPercentage)"
                  :stroke-width="8"
                >
                  <template #default="{ percentage }">
                    <span class="progress-text">第{{ page.pageNumber }}页: {{ page.contentCount }}项 ({{ percentage }}%)</span>
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
                  <el-tag type="success">文本段落</el-tag>
                  <span class="stat-value">{{ getTextCount() }} 个</span>
                </div>
                <div class="stat-item">
                  <el-tag type="warning">表格数据</el-tag>
                  <span class="stat-value">{{ getTableCount() }} 个</span>
                </div>
                <div class="stat-item">
                  <el-tag type="info">平均页面内容</el-tag>
                  <span class="stat-value">{{ getAverageContentPerPage() }} 项</span>
                </div>
              </div>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="analysis-item">
              <h4>📈 内容质量指标</h4>
              <div class="quality-stats">
                <div class="quality-item">
                  <span class="quality-label">文本密度</span>
                  <el-progress 
                    :percentage="getTextDensity()" 
                    :color="getQualityColor(getTextDensity())"
                    :stroke-width="6"
                  />
                </div>
                <div class="quality-item">
                  <span class="quality-label">表格覆盖率</span>
                  <el-progress 
                    :percentage="getTableCoverage()" 
                    :color="getQualityColor(getTableCoverage())"
                    :stroke-width="6"
                  />
                </div>
              </div>
            </div>
          </el-col>
        </el-row>
      </el-card>
    </div>
    <el-empty v-else description="未提取到PDF内容" />
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'PdfDisplay',
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
    const selectedPage = ref('all')
    const contentFilter = ref('all')

    const getTotalPages = () => {
      const pages = new Set()
      props.data.forEach(item => {
        if (item.page_number) {
          pages.add(item.page_number)
        }
      })
      return pages.size
    }

    const getTextCount = () => {
      return props.data.filter(item => item.content_type === 'text').length
    }

    const getTableCount = () => {
      const tables = new Set()
      props.data.forEach(item => {
        if (item.content_type === 'table' && item.table_number && item.page_number) {
          tables.add(`${item.page_number}-${item.table_number}`)
        }
      })
      return tables.size
    }

    const getTotalChars = () => {
      return props.data.reduce((total, item) => {
        return total + (item.char_count || 0)
      }, 0)
    }

    const getPageNumbers = () => {
      const pages = new Set()
      props.data.forEach(item => {
        if (item.page_number) {
          pages.add(item.page_number)
        }
      })
      return Array.from(pages).sort((a, b) => a - b)
    }

    const getGroupedByPage = () => {
      const pages = {}
      
      props.data.forEach(item => {
        const pageNum = item.page_number || 1
        
        if (selectedPage.value !== 'all' && pageNum !== selectedPage.value) {
          return
        }
        
        if (!pages[pageNum]) {
          pages[pageNum] = {
            pageNumber: pageNum,
            textItems: [],
            tables: {}
          }
        }
        
        if (item.content_type === 'text') {
          pages[pageNum].textItems.push(item)
        } else if (item.content_type === 'table') {
          const tableKey = item.table_number || 'default'
          if (!pages[pageNum].tables[tableKey]) {
            pages[pageNum].tables[tableKey] = {
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
            pages[pageNum].tables[tableKey].rows.push(rowData)
            
            // 更新列信息
            Object.keys(rowData).forEach(colName => {
              if (!pages[pageNum].tables[tableKey].columns.find(col => col.prop === colName)) {
                pages[pageNum].tables[tableKey].columns.push({
                  prop: colName,
                  label: colName
                })
              }
            })
          }
        }
      })
      
      // 转换表格对象为数组
      Object.values(pages).forEach(page => {
        page.tables = Object.values(page.tables)
      })
      
      return Object.values(pages).sort((a, b) => a.pageNumber - b.pageNumber)
    }

    const getPageAnalysis = () => {
      const pageStats = {}
      
      props.data.forEach(item => {
        const pageNum = item.page_number || 1
        pageStats[pageNum] = (pageStats[pageNum] || 0) + 1
      })
      
      const maxContent = Math.max(...Object.values(pageStats))
      
      return Object.entries(pageStats).map(([pageNumber, contentCount]) => ({
        pageNumber: parseInt(pageNumber),
        contentCount,
        contentPercentage: Math.round((contentCount / maxContent) * 100)
      })).sort((a, b) => a.pageNumber - b.pageNumber)
    }

    const getAverageContentPerPage = () => {
      const totalPages = getTotalPages()
      return totalPages > 0 ? Math.round(props.data.length / totalPages) : 0
    }

    const getTextDensity = () => {
      const textItems = getTextCount()
      const totalItems = props.data.length
      return totalItems > 0 ? Math.round((textItems / totalItems) * 100) : 0
    }

    const getTableCoverage = () => {
      const pagesWithTables = new Set()
      props.data.forEach(item => {
        if (item.content_type === 'table' && item.page_number) {
          pagesWithTables.add(item.page_number)
        }
      })
      const totalPages = getTotalPages()
      return totalPages > 0 ? Math.round((pagesWithTables.size / totalPages) * 100) : 0
    }

    const getPageColor = (percentage) => {
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

    const handlePageChange = (value) => {
      selectedPage.value = value
    }

    return {
      selectedPage,
      contentFilter,
      getTotalPages,
      getTextCount,
      getTableCount,
      getTotalChars,
      getPageNumbers,
      getGroupedByPage,
      getPageAnalysis,
      getAverageContentPerPage,
      getTextDensity,
      getTableCoverage,
      getPageColor,
      getQualityColor,
      handlePageChange
    }
  }
}
</script>

<style scoped>
.pdf-display {
  padding: 16px;
}

.pdf-header {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 16px;
}

.page-navigation {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px;
  background: #fafafa;
  border-radius: 6px;
}

.pdf-content {
  max-height: 700px;
  overflow-y: auto;
}

.page-content {
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

.page-item {
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
