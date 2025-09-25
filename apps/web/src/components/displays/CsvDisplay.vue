<template>
  <div class="csv-display">
    <div v-if="data && data.length > 0">
      <!-- CSV数据统计信息 -->
      <div class="csv-header">
        <el-row :gutter="20" style="margin-bottom: 16px;">
          <el-col :span="6">
            <el-statistic title="📊 数据行数" :value="data.length" />
          </el-col>
          <el-col :span="6">
            <el-statistic title="📋 字段数量" :value="getColumnCount()" />
          </el-col>
          <el-col :span="6">
            <el-statistic title="✅ 数据完整性" :value="getDataCompleteness()" suffix="%" />
          </el-col>
          <el-col :span="6">
            <el-statistic title="📈 有效记录" :value="getValidRecords()" />
          </el-col>
        </el-row>
      </div>

      <!-- 数据预览控制 -->
      <div class="csv-controls" style="margin-bottom: 16px;">
        <el-row :gutter="16" type="flex" align="middle">
          <el-col :span="8">
            <el-input
              v-model="searchText"
              placeholder="搜索数据..."
              prefix-icon="Search"
              clearable
              @input="handleSearch"
            />
          </el-col>
          <el-col :span="8">
            <el-select v-model="selectedColumns" multiple placeholder="选择显示列" style="width: 100%;">
              <el-option
                v-for="column in getAllColumns()"
                :key="column"
                :label="column"
                :value="column"
              />
            </el-select>
          </el-col>
          <el-col :span="8">
            <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              :page-sizes="[10, 20, 50, 100]"
              :total="filteredData.length"
              layout="sizes, prev, pager, next"
              small
            />
          </el-col>
        </el-row>
      </div>

      <!-- CSV数据表格 -->
      <el-table 
        :data="getPaginatedData()" 
        style="width: 100%" 
        max-height="500"
        stripe
        border
        :header-cell-style="{ background: '#f5f7fa', color: '#606266' }"
        v-loading="loading"
      >
        <el-table-column
          v-for="(column, index) in getDisplayColumns()"
          :key="index"
          :prop="column.prop"
          :label="column.label"
          :width="column.width"
          :min-width="column.minWidth"
          show-overflow-tooltip
          sortable
        >
          <template #default="{ row }">
            <div class="cell-content">
              <!-- 行号特殊显示 -->
              <el-tag 
                v-if="column.prop === '_row_number'" 
                type="info" 
                size="small"
              >
                {{ row[column.prop] }}
              </el-tag>
              <!-- 数值类型特殊显示 -->
              <el-tag 
                v-else-if="isNumericField(column.prop, row[column.prop])" 
                type="success" 
                size="small"
              >
                {{ formatNumber(row[column.prop]) }}
              </el-tag>
              <!-- 普通文本 -->
              <span v-else>{{ formatCellValue(row[column.prop]) }}</span>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <!-- 数据统计图表 -->
      <el-row :gutter="16" style="margin-top: 20px;">
        <el-col :span="12">
          <el-card>
            <template #header>
              <span>📊 字段完整性分析</span>
            </template>
            <div v-for="field in getFieldAnalysis()" :key="field.name" class="field-analysis">
              <div class="field-name">{{ field.name }}</div>
              <el-progress 
                :percentage="field.completeness" 
                :color="getProgressColor(field.completeness)"
                :stroke-width="8"
              >
                <template #default="{ percentage }">
                  <span class="progress-text">{{ field.validCount }}/{{ field.totalCount }} ({{ percentage }}%)</span>
                </template>
              </el-progress>
            </div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card>
            <template #header>
              <span>📈 数据类型分布</span>
            </template>
            <div class="data-type-analysis">
              <div v-for="type in getDataTypeAnalysis()" :key="type.name" class="type-item">
                <div class="type-header">
                  <el-tag :type="getTypeTagType(type.name)" size="small">{{ type.name }}</el-tag>
                  <span class="type-count">{{ type.count }} 个字段</span>
                </div>
                <el-progress 
                  :percentage="type.percentage" 
                  :color="getTypeColor(type.name)"
                  :stroke-width="6"
                />
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 数据质量报告 -->
      <el-card style="margin-top: 20px;">
        <template #header>
          <span>📋 数据质量报告</span>
        </template>
        <el-descriptions :column="3" border>
          <el-descriptions-item label="总记录数">
            <el-tag type="primary">{{ data.length }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="字段数量">
            <el-tag type="success">{{ getColumnCount() }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="数据完整性">
            <el-tag :type="getCompletenessTagType()">{{ getDataCompleteness() }}%</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="空值数量">
            <el-tag type="warning">{{ getNullCount() }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="重复记录">
            <el-tag type="info">{{ getDuplicateCount() }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="数据质量评分">
            <el-tag :type="getQualityScoreTagType()">{{ getQualityScore() }}/100</el-tag>
          </el-descriptions-item>
        </el-descriptions>
      </el-card>
    </div>
    <el-empty v-else description="未提取到CSV数据" />
  </div>
</template>

<script>
import { ref, computed, watch } from 'vue'

export default {
  name: 'CsvDisplay',
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
    const searchText = ref('')
    const selectedColumns = ref([])
    const currentPage = ref(1)
    const pageSize = ref(20)
    const loading = ref(false)

    // 初始化选中的列
    watch(() => props.data, (newData) => {
      if (newData && newData.length > 0) {
        selectedColumns.value = Object.keys(newData[0])
      }
    }, { immediate: true })

    const getColumnCount = () => {
      if (!props.data || props.data.length === 0) return 0
      return Object.keys(props.data[0]).length
    }

    const getAllColumns = () => {
      if (!props.data || props.data.length === 0) return []
      return Object.keys(props.data[0])
    }

    const getDisplayColumns = () => {
      const columns = selectedColumns.value.length > 0 ? selectedColumns.value : getAllColumns()
      
      return columns.map(key => {
        const isRowNumber = key === '_row_number'
        
        return {
          prop: key,
          label: key,
          width: isRowNumber ? 100 : undefined,
          minWidth: isRowNumber ? 100 : 120
        }
      })
    }

    const filteredData = computed(() => {
      if (!searchText.value) return props.data
      
      return props.data.filter(row => {
        return Object.values(row).some(value => 
          String(value).toLowerCase().includes(searchText.value.toLowerCase())
        )
      })
    })

    const getPaginatedData = () => {
      const start = (currentPage.value - 1) * pageSize.value
      const end = start + pageSize.value
      return filteredData.value.slice(start, end)
    }

    const getDataCompleteness = () => {
      if (!props.data || props.data.length === 0) return 0
      
      const totalCells = props.data.length * Object.keys(props.data[0]).length
      const validCells = props.data.reduce((count, row) => {
        return count + Object.values(row).filter(value => 
          value !== null && value !== undefined && String(value).trim() !== ''
        ).length
      }, 0)
      
      return Math.round((validCells / totalCells) * 100)
    }

    const getValidRecords = () => {
      if (!props.data || props.data.length === 0) return 0
      
      return props.data.filter(row => {
        const values = Object.values(row).filter(value => 
          value !== null && value !== undefined && String(value).trim() !== ''
        )
        return values.length > Object.keys(row).length * 0.5
      }).length
    }

    const getFieldAnalysis = () => {
      if (!props.data || props.data.length === 0) return []

      const fields = Object.keys(props.data[0])
      
      return fields.map(field => {
        const validCount = props.data.filter(row => {
          const value = row[field]
          return value !== null && value !== undefined && String(value).trim() !== ''
        }).length
        
        const completeness = Math.round((validCount / props.data.length) * 100)
        
        return {
          name: field,
          validCount,
          totalCount: props.data.length,
          completeness
        }
      }).sort((a, b) => b.completeness - a.completeness)
    }

    const getDataTypeAnalysis = () => {
      if (!props.data || props.data.length === 0) return []

      const fields = Object.keys(props.data[0])
      const typeCount = {
        '数值': 0,
        '文本': 0,
        '日期': 0,
        '布尔': 0,
        '其他': 0
      }

      fields.forEach(field => {
        const sampleValues = props.data.slice(0, 10).map(row => row[field]).filter(v => v !== null && v !== undefined)
        
        if (sampleValues.length === 0) {
          typeCount['其他']++
          return
        }

        const isNumeric = sampleValues.every(v => !isNaN(Number(v)))
        const isDate = sampleValues.some(v => /\d{4}-\d{2}-\d{2}/.test(String(v)))
        const isBoolean = sampleValues.every(v => ['true', 'false', '是', '否', '1', '0'].includes(String(v).toLowerCase()))

        if (isNumeric) typeCount['数值']++
        else if (isDate) typeCount['日期']++
        else if (isBoolean) typeCount['布尔']++
        else typeCount['文本']++
      })

      const total = fields.length
      
      return Object.entries(typeCount)
        .filter(([, count]) => count > 0)
        .map(([name, count]) => ({
          name,
          count,
          percentage: Math.round((count / total) * 100)
        }))
        .sort((a, b) => b.count - a.count)
    }

    const getNullCount = () => {
      if (!props.data || props.data.length === 0) return 0
      
      return props.data.reduce((count, row) => {
        return count + Object.values(row).filter(value => 
          value === null || value === undefined || String(value).trim() === ''
        ).length
      }, 0)
    }

    const getDuplicateCount = () => {
      if (!props.data || props.data.length === 0) return 0
      
      const seen = new Set()
      let duplicates = 0
      
      props.data.forEach(row => {
        const key = JSON.stringify(row)
        if (seen.has(key)) {
          duplicates++
        } else {
          seen.add(key)
        }
      })
      
      return duplicates
    }

    const getQualityScore = () => {
      const completeness = getDataCompleteness()
      const duplicateRate = (getDuplicateCount() / props.data.length) * 100
      const nullRate = (getNullCount() / (props.data.length * getColumnCount())) * 100
      
      let score = completeness
      score -= duplicateRate * 0.5  // 重复记录扣分
      score -= nullRate * 0.3       // 空值扣分
      
      return Math.max(0, Math.round(score))
    }

    const formatCellValue = (value) => {
      if (value === null || value === undefined) return '-'
      if (String(value).trim() === '') return '-'
      return String(value)
    }

    const isNumericField = (fieldName, value) => {
      return !isNaN(Number(value)) && value !== null && value !== undefined && String(value).trim() !== ''
    }

    const formatNumber = (value) => {
      const num = Number(value)
      return num.toLocaleString()
    }

    const getProgressColor = (percentage) => {
      if (percentage >= 80) return '#67c23a'
      if (percentage >= 60) return '#e6a23c'
      if (percentage >= 40) return '#f56c6c'
      return '#909399'
    }

    const getTypeColor = (typeName) => {
      const colors = {
        '数值': '#67c23a',
        '文本': '#409eff',
        '日期': '#e6a23c',
        '布尔': '#f56c6c',
        '其他': '#909399'
      }
      return colors[typeName] || '#909399'
    }

    const getTypeTagType = (typeName) => {
      const types = {
        '数值': 'success',
        '文本': 'primary',
        '日期': 'warning',
        '布尔': 'danger',
        '其他': 'info'
      }
      return types[typeName] || 'info'
    }

    const getCompletenessTagType = () => {
      const completeness = getDataCompleteness()
      if (completeness >= 80) return 'success'
      if (completeness >= 60) return 'warning'
      return 'danger'
    }

    const getQualityScoreTagType = () => {
      const score = getQualityScore()
      if (score >= 80) return 'success'
      if (score >= 60) return 'warning'
      return 'danger'
    }

    const handleSearch = () => {
      currentPage.value = 1
    }

    return {
      searchText,
      selectedColumns,
      currentPage,
      pageSize,
      loading,
      filteredData,
      getColumnCount,
      getAllColumns,
      getDisplayColumns,
      getPaginatedData,
      getDataCompleteness,
      getValidRecords,
      getFieldAnalysis,
      getDataTypeAnalysis,
      getNullCount,
      getDuplicateCount,
      getQualityScore,
      formatCellValue,
      isNumericField,
      formatNumber,
      getProgressColor,
      getTypeColor,
      getTypeTagType,
      getCompletenessTagType,
      getQualityScoreTagType,
      handleSearch
    }
  }
}
</script>

<style scoped>
.csv-display {
  padding: 16px;
}

.csv-header {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 16px;
}

.csv-controls {
  background: #fafafa;
  padding: 12px;
  border-radius: 6px;
}

.cell-content {
  display: flex;
  align-items: center;
}

.field-analysis {
  margin-bottom: 16px;
}

.field-name {
  font-weight: 600;
  margin-bottom: 8px;
  color: #303133;
  font-size: 14px;
}

.progress-text {
  font-size: 12px;
  color: #606266;
}

.data-type-analysis {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.type-item {
  margin-bottom: 12px;
}

.type-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.type-count {
  font-size: 12px;
  color: #909399;
}

:deep(.el-table th) {
  background-color: #f5f7fa !important;
}

:deep(.el-statistic__content) {
  font-size: 18px;
  font-weight: 600;
}

:deep(.el-progress-bar__outer) {
  border-radius: 3px;
}

:deep(.el-pagination) {
  justify-content: center;
}
</style>
