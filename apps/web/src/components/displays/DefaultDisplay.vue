<template>
  <div class="default-display">
    <div v-if="data && data.length > 0">
      <!-- 通用数据表格展示 -->
      <div class="default-header">
        <el-row :gutter="20" style="margin-bottom: 16px;">
          <el-col :span="6">
            <el-statistic title="📊 数据记录" :value="data.length" />
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
          sortable
        >
          <template #default="{ row }">
            <div class="cell-content">
              <el-tag 
                v-if="column.prop === '_row_number'" 
                type="info" 
                size="small"
              >
                {{ row[column.prop] }}
              </el-tag>
              <span v-else>{{ formatCellValue(row[column.prop]) }}</span>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <!-- 如果没有原始数据，显示识别的实体 -->
      <div v-if="!data || data.length === 0">
        <el-table :data="entities || []" style="width: 100%" max-height="400">
          <el-table-column prop="name" label="识别内容" width="200" />
          <el-table-column prop="type" label="内容类型" width="120">
            <template #default="{ row }">
              <el-tag :type="getEntityTypeColor(row.type)" size="small">
                {{ row.type }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="properties" label="附加信息">
            <template #default="{ row }">
              <div v-if="row.properties">
                <el-tag
                  v-for="(value, key) in row.properties"
                  :key="key"
                  size="small"
                  style="margin: 2px;"
                  type="info"
                >
                  {{ key }}: {{ value }}
                </el-tag>
              </div>
              <el-text v-else type="info" size="small">无附加信息</el-text>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
    <el-empty v-else description="未提取到数据" />
  </div>
</template>

<script>
export default {
  name: 'DefaultDisplay',
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
    },
    entities: {
      type: Array,
      default: () => []
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
        
        return {
          prop: key,
          label: key,
          width: isRowNumber ? 100 : undefined,
          minWidth: isRowNumber ? 100 : 120
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
        return values.length > Object.keys(row).length * 0.5
      }).length
    }

    const formatCellValue = (value) => {
      if (value === null || value === undefined) return '-'
      if (String(value).trim() === '') return '-'
      return String(value)
    }

    const getEntityTypeColor = (type) => {
      const colorMap = {
        'PERSON': 'success',
        'ORG': 'warning',
        'LOC': 'info',
        'MISC': 'primary',
        'DATE': 'danger'
      }
      return colorMap[type] || 'info'
    }

    return {
      getColumnCount,
      getTableColumns,
      getDataCompleteness,
      getValidRecords,
      formatCellValue,
      getEntityTypeColor
    }
  }
}
</script>

<style scoped>
.default-display {
  padding: 16px;
}

.default-header {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 16px;
}

.cell-content {
  display: flex;
  align-items: center;
}

:deep(.el-table th) {
  background-color: #f5f7fa !important;
}

:deep(.el-statistic__content) {
  font-size: 18px;
  font-weight: 600;
}
</style>
