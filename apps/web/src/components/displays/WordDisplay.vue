<template>
  <div class="word-display">
    <div v-if="data && data.length > 0">
      <!-- Word文档统计信息 -->
      <div class="word-header">
        <el-row :gutter="20" style="margin-bottom: 16px;">
          <el-col :span="6">
            <el-statistic title="📄 段落数量" :value="getParagraphCount()" />
          </el-col>
          <el-col :span="6">
            <el-statistic title="📊 表格数量" :value="getTableCount()" />
          </el-col>
          <el-col :span="6">
            <el-statistic title="📝 总字数" :value="getTotalWords()" />
          </el-col>
          <el-col :span="6">
            <el-statistic title="🔤 总字符数" :value="getTotalChars()" />
          </el-col>
        </el-row>
      </div>

      <!-- 内容类型筛选 -->
      <div class="content-filter" style="margin-bottom: 16px;">
        <el-radio-group v-model="contentFilter" @change="handleFilterChange">
          <el-radio-button label="all">全部内容</el-radio-button>
          <el-radio-button label="paragraph">段落文本</el-radio-button>
          <el-radio-button label="table">表格数据</el-radio-button>
        </el-radio-group>
      </div>

      <!-- 文档内容展示 -->
      <div class="word-content">
        <!-- 段落内容展示 -->
        <div v-if="contentFilter === 'all' || contentFilter === 'paragraph'">
          <el-card 
            v-for="(item, index) in getFilteredParagraphs()" 
            :key="`para-${index}`"
            class="content-card paragraph-card"
            shadow="hover"
          >
            <template #header>
              <div class="card-header">
                <span class="content-type-tag">
                  <el-tag type="primary" size="small">📄 段落 {{ item.paragraph_number }}</el-tag>
                </span>
                <span class="content-meta">
                  <el-tag size="small" type="info">{{ item.style || 'Normal' }}</el-tag>
                  <el-tag size="small" type="success">{{ item.word_count }} 词</el-tag>
                </span>
              </div>
            </template>
            <div class="paragraph-content">
              {{ item.content }}
            </div>
          </el-card>
        </div>

        <!-- 表格内容展示 -->
        <div v-if="contentFilter === 'all' || contentFilter === 'table'">
          <div v-for="(table, tableIndex) in getGroupedTables()" :key="`table-${tableIndex}`">
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

      <!-- 文档结构分析 -->
      <el-card style="margin-top: 20px;">
        <template #header>
          <span>📊 文档结构分析</span>
        </template>
        <el-row :gutter="16">
          <el-col :span="12">
            <div class="analysis-item">
              <h4>📄 段落样式分布</h4>
              <div v-for="style in getStyleAnalysis()" :key="style.name" class="style-item">
                <el-progress 
                  :percentage="style.percentage" 
                  :color="getStyleColor(style.name)"
                  :stroke-width="8"
                >
                  <template #default="{ percentage }">
                    <span class="progress-text">{{ style.name }}: {{ style.count }}个 ({{ percentage }}%)</span>
                  </template>
                </el-progress>
              </div>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="analysis-item">
              <h4>📊 内容类型分布</h4>
              <div class="content-type-stats">
                <div class="stat-item">
                  <el-tag type="primary">段落文本</el-tag>
                  <span class="stat-value">{{ getParagraphCount() }} 个</span>
                </div>
                <div class="stat-item">
                  <el-tag type="warning">表格数据</el-tag>
                  <span class="stat-value">{{ getTableCount() }} 个</span>
                </div>
                <div class="stat-item">
                  <el-tag type="success">平均段落长度</el-tag>
                  <span class="stat-value">{{ getAverageParagraphLength() }} 字</span>
                </div>
              </div>
            </div>
          </el-col>
        </el-row>
      </el-card>
    </div>
    <el-empty v-else description="未提取到Word文档内容" />
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'WordDisplay',
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
    const contentFilter = ref('all')

    const getParagraphCount = () => {
      return props.data.filter(item => item.content_type === 'paragraph').length
    }

    const getTableCount = () => {
      const tableNumbers = new Set()
      props.data.forEach(item => {
        if (item.content_type === 'table' && item.table_number) {
          tableNumbers.add(item.table_number)
        }
      })
      return tableNumbers.size
    }

    const getTotalWords = () => {
      return props.data.reduce((total, item) => {
        return total + (item.word_count || 0)
      }, 0)
    }

    const getTotalChars = () => {
      return props.data.reduce((total, item) => {
        return total + (item.char_count || 0)
      }, 0)
    }

    const getFilteredParagraphs = () => {
      return props.data.filter(item => item.content_type === 'paragraph')
    }

    const getGroupedTables = () => {
      const tables = {}
      
      props.data.forEach(item => {
        if (item.content_type === 'table' && item.table_number) {
          if (!tables[item.table_number]) {
            tables[item.table_number] = {
              tableNumber: item.table_number,
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
            tables[item.table_number].rows.push(rowData)
            
            // 更新列信息
            Object.keys(rowData).forEach(colName => {
              if (!tables[item.table_number].columns.find(col => col.prop === colName)) {
                tables[item.table_number].columns.push({
                  prop: colName,
                  label: colName
                })
              }
            })
          }
        }
      })
      
      return Object.values(tables)
    }

    const getStyleAnalysis = () => {
      const styles = {}
      const paragraphs = getFilteredParagraphs()
      
      paragraphs.forEach(item => {
        const style = item.style || 'Normal'
        styles[style] = (styles[style] || 0) + 1
      })
      
      const total = paragraphs.length
      
      return Object.entries(styles).map(([name, count]) => ({
        name,
        count,
        percentage: Math.round((count / total) * 100)
      })).sort((a, b) => b.count - a.count)
    }

    const getAverageParagraphLength = () => {
      const paragraphs = getFilteredParagraphs()
      if (paragraphs.length === 0) return 0
      
      const totalChars = paragraphs.reduce((total, item) => {
        return total + (item.char_count || 0)
      }, 0)
      
      return Math.round(totalChars / paragraphs.length)
    }

    const getStyleColor = (styleName) => {
      const colors = {
        'Normal': '#409eff',
        'Heading 1': '#f56c6c',
        'Heading 2': '#e6a23c',
        'Heading 3': '#67c23a',
        'Title': '#909399'
      }
      return colors[styleName] || '#409eff'
    }

    const handleFilterChange = (value) => {
      contentFilter.value = value
    }

    return {
      contentFilter,
      getParagraphCount,
      getTableCount,
      getTotalWords,
      getTotalChars,
      getFilteredParagraphs,
      getGroupedTables,
      getStyleAnalysis,
      getAverageParagraphLength,
      getStyleColor,
      handleFilterChange
    }
  }
}
</script>

<style scoped>
.word-display {
  padding: 16px;
}

.word-header {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 16px;
}

.content-filter {
  text-align: center;
}

.word-content {
  max-height: 600px;
  overflow-y: auto;
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

.paragraph-content {
  line-height: 1.6;
  color: #303133;
  font-size: 14px;
  text-align: justify;
  padding: 8px 0;
}

.table-card {
  border-left: 4px solid #e6a23c;
}

.paragraph-card {
  border-left: 4px solid #409eff;
}

.analysis-item h4 {
  margin-bottom: 16px;
  color: #303133;
}

.style-item {
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

:deep(.el-statistic__content) {
  font-size: 18px;
  font-weight: 600;
}

:deep(.el-progress-bar__outer) {
  border-radius: 4px;
}
</style>
