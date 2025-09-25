<template>
  <div class="excel-display">
    <div v-if="data && data.length > 0">
      <!-- Excel数据表格展示 -->
      <div class="excel-header">
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

      <!-- 数据表格 -->
      <el-table 
        :data="data" 
        style="width: 100%" 
        max-height="500"
        stripe
        border
        :header-cell-style="{ background: '#f5f7fa', color: '#606266' }"
      >
        <el-table-column
          v-for="(column, index) in getTableColumns()"
          :key="index"
          :prop="column.prop"
          :label="column.label"
          :width="column.width"
          :min-width="column.minWidth"
          show-overflow-tooltip
          :sortable="column.sortable"
        >
          <template #default="{ row }">
            <div class="cell-content">
              <!-- 特殊字段样式 -->
              <el-tag 
                v-if="column.prop === '_row_number'" 
                type="info" 
                size="small"
              >
                {{ row[column.prop] }}
              </el-tag>
              <el-tag 
                v-else-if="isStatusField(column.prop)" 
                :type="getStatusTagType(row[column.prop])" 
                size="small"
              >
                {{ row[column.prop] }}
              </el-tag>
              <el-tag 
                v-else-if="isSeverityField(column.prop)" 
                :type="getSeverityTagType(row[column.prop])" 
                size="small"
              >
                {{ row[column.prop] }}
              </el-tag>
              <span v-else>{{ formatCellValue(row[column.prop]) }}</span>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <!-- 字段分析 -->
      <el-card style="margin-top: 20px;">
        <template #header>
          <span>📊 字段分析</span>
        </template>
        <el-row :gutter="16">
          <el-col 
            v-for="field in getFieldAnalysis()" 
            :key="field.name" 
            :span="6"
            style="margin-bottom: 12px;"
          >
            <el-card shadow="hover" class="field-card">
              <div class="field-info">
                <div class="field-name">{{ field.name }}</div>
                <div class="field-stats">
                  <el-progress 
                    :percentage="field.completeness" 
                    :color="getProgressColor(field.completeness)"
                    :stroke-width="6"
                  />
                  <div class="field-details">
                    <span>{{ field.validCount }}/{{ field.totalCount }} 有效</span>
                  </div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-card>
    </div>
    <el-empty v-else description="未提取到Excel数据" />
  </div>
</template>

<script>
export default {
  name: 'ExcelDisplay',
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
    const getColumnCount = () => {
      if (!props.data || props.data.length === 0) return 0
      return Object.keys(props.data[0]).length
    }

    const getTableColumns = () => {
      if (!props.data || props.data.length === 0) return []

      const firstRow = props.data[0]
      return Object.keys(firstRow).map(key => {
        const isRowNumber = key === '_row_number'
        const isSystemField = key.startsWith('_')
        
        return {
          prop: key,
          label: key,
          width: isRowNumber ? 100 : undefined,
          minWidth: isRowNumber ? 100 : 120,
          sortable: true
        }
      })
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
        return values.length > Object.keys(row).length * 0.5 // 至少50%字段有值
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
      })
    }

    const formatCellValue = (value) => {
      if (value === null || value === undefined) return '-'
      if (String(value).trim() === '') return '-'
      return String(value)
    }

    const isStatusField = (fieldName) => {
      const statusFields = ['状态', 'status', '进度', 'progress']
      return statusFields.some(field => fieldName.toLowerCase().includes(field.toLowerCase()))
    }

    const isSeverityField = (fieldName) => {
      const severityFields = ['严重度', 'severity', '优先级', 'priority', '等级', 'level']
      return severityFields.some(field => fieldName.toLowerCase().includes(field.toLowerCase()))
    }

    const getStatusTagType = (value) => {
      if (!value) return 'info'
      const val = String(value).toLowerCase()
      if (val.includes('完成') || val.includes('已解决') || val.includes('success')) return 'success'
      if (val.includes('进行') || val.includes('处理') || val.includes('progress')) return 'warning'
      if (val.includes('失败') || val.includes('错误') || val.includes('error')) return 'danger'
      return 'info'
    }

    const getSeverityTagType = (value) => {
      if (!value) return 'info'
      const val = String(value).toLowerCase()
      if (val.includes('高') || val.includes('严重') || val.includes('critical')) return 'danger'
      if (val.includes('中') || val.includes('medium')) return 'warning'
      if (val.includes('低') || val.includes('low')) return 'success'
      return 'info'
    }

    const getProgressColor = (percentage) => {
      if (percentage >= 80) return '#67c23a'
      if (percentage >= 60) return '#e6a23c'
      if (percentage >= 40) return '#f56c6c'
      return '#909399'
    }

    return {
      getColumnCount,
      getTableColumns,
      getDataCompleteness,
      getValidRecords,
      getFieldAnalysis,
      formatCellValue,
      isStatusField,
      isSeverityField,
      getStatusTagType,
      getSeverityTagType,
      getProgressColor
    }
  }
}
</script>

<style scoped>
.excel-display {
  padding: 16px;
}

.excel-header {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 16px;
}

.cell-content {
  display: flex;
  align-items: center;
}

.field-card {
  height: 100%;
}

.field-info {
  text-align: center;
}

.field-name {
  font-weight: 600;
  margin-bottom: 8px;
  color: #303133;
  font-size: 14px;
}

.field-stats {
  margin-top: 8px;
}

.field-details {
  margin-top: 4px;
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
</style>
