<template>
  <div class="enhanced-dictionary-management">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>📚 词典管理</h1>
      <p>管理标准化词典，支持重复清除、批量导入等功能</p>
    </div>

    <!-- 操作工具栏 -->
    <el-card class="toolbar-card" shadow="never">
      <div class="toolbar">
        <!-- 搜索和筛选 -->
        <div class="search-section">
          <el-input
            v-model="searchQuery"
            placeholder="搜索术语、别名或定义..."
            :prefix-icon="Search"
            style="width: 300px; margin-right: 16px;"
            @input="handleSearch"
            clearable
          />
          <el-select
            v-model="selectedCategory"
            placeholder="选择类别"
            style="width: 150px; margin-right: 16px;"
            @change="handleCategoryChange"
            clearable
          >
            <el-option
              v-for="category in categories"
              :key="category"
              :label="category"
              :value="category"
            />
          </el-select>
        </div>

        <!-- 操作按钮 -->
        <div class="action-section">
          <el-button type="primary" :icon="Plus" @click="showAddDialog">
            新增词条
          </el-button>
          <el-button type="warning" :icon="Warning" @click="findDuplicates">
            查找重复
          </el-button>
          <el-button type="success" :icon="Upload" @click="showImportDialog">
            批量导入
          </el-button>
          <el-button type="info" :icon="Download" @click="exportDictionary">
            导出词典
          </el-button>
          <el-button :icon="Refresh" @click="loadDictionary">
            刷新
          </el-button>
        </div>
      </div>
    </el-card>

    <!-- 统计信息 -->
    <el-row :gutter="20" style="margin-bottom: 20px;">
      <el-col :span="6">
        <el-statistic title="📖 总词条数" :value="statistics.total_entries" />
      </el-col>
      <el-col :span="6">
        <el-statistic title="🏷️ 总别名数" :value="statistics.total_aliases" />
      </el-col>
      <el-col :span="6">
        <el-statistic title="📂 类别数量" :value="Object.keys(statistics.categories || {}).length" />
      </el-col>
      <el-col :span="6">
        <el-statistic title="📊 平均别名" :value="statistics.avg_aliases_per_entry" :precision="2" />
      </el-col>
    </el-row>

    <!-- 词典表格 -->
    <el-card class="table-card">
      <el-table 
        :data="paginatedEntries" 
        stripe 
        style="width: 100%"
        v-loading="loading"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="term" label="主术语" min-width="150" sortable />
        <el-table-column prop="category" label="类别" width="120" sortable>
          <template #default="{ row }">
            <el-tag :type="getCategoryColor(row.category)" size="small">
              {{ row.category }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="别名" min-width="200">
          <template #default="{ row }">
            <div class="aliases">
              <el-tag 
                v-for="alias in row.aliases" 
                :key="alias"
                size="small"
                class="alias-tag"
              >
                {{ alias }}
              </el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="标签" min-width="150">
          <template #default="{ row }">
            <div class="tags">
              <el-tag 
                v-for="tag in row.tags" 
                :key="tag"
                size="small"
                type="info"
                class="tag-item"
              >
                {{ tag }}
              </el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="definition" label="定义" min-width="250" show-overflow-tooltip />
        <el-table-column label="元数据" width="120">
          <template #default="{ row }">
            <div class="metadata">
              <el-tag size="small" type="success">{{ row.source }}</el-tag>
              <br>
              <span class="version">v{{ row.version }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="editEntry(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteEntry(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[20, 50, 100, 200]"
          :total="filteredEntries.length"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 批量操作 -->
    <el-card v-if="selectedEntries.length > 0" class="batch-actions">
      <div class="batch-toolbar">
        <span>已选择 {{ selectedEntries.length }} 个词条</span>
        <div>
          <el-button type="danger" @click="batchDelete">批量删除</el-button>
          <el-button type="warning" @click="batchMerge">合并选中</el-button>
        </div>
      </div>
    </el-card>

    <!-- 新增/编辑词条对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEditing ? '编辑词条' : '新增词条'"
      width="600px"
      @close="resetForm"
    >
      <el-form :model="currentEntry" :rules="formRules" ref="entryForm" label-width="100px">
        <el-form-item label="主术语" prop="term">
          <el-input v-model="currentEntry.term" placeholder="请输入主术语" />
        </el-form-item>
        <el-form-item label="类别" prop="category">
          <el-select v-model="currentEntry.category" placeholder="选择类别" style="width: 100%">
            <el-option
              v-for="category in categories"
              :key="category"
              :label="category"
              :value="category"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="别名">
          <el-input
            v-model="aliasesInput"
            type="textarea"
            :rows="3"
            placeholder="请输入别名，用分号(;)分隔"
          />
        </el-form-item>
        <el-form-item label="标签">
          <el-input
            v-model="tagsInput"
            type="textarea"
            :rows="2"
            placeholder="请输入标签，用分号(;)分隔"
          />
        </el-form-item>
        <el-form-item label="定义">
          <el-input
            v-model="currentEntry.definition"
            type="textarea"
            :rows="4"
            placeholder="请输入词条定义或备注"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveEntry">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 重复项对话框 -->
    <el-dialog
      v-model="duplicatesDialogVisible"
      title="🔍 重复项检查"
      width="800px"
    >
      <div v-if="duplicates.length === 0" class="no-duplicates">
        <el-empty description="未发现重复项" />
      </div>
      <div v-else>
        <div class="duplicates-header">
          <span>发现 {{ duplicates.length }} 个重复术语</span>
          <div>
            <el-button type="warning" @click="removeDuplicates('keep_latest')">
              保留最新
            </el-button>
            <el-button type="info" @click="removeDuplicates('keep_first')">
              保留最早
            </el-button>
            <el-button type="primary" @click="removeDuplicates('merge')">
              智能合并
            </el-button>
          </div>
        </div>
        
        <div class="duplicates-list">
          <el-card v-for="duplicate in duplicates" :key="duplicate.term" class="duplicate-item">
            <template #header>
              <div class="duplicate-header">
                <span class="duplicate-term">{{ duplicate.term }}</span>
                <el-tag type="warning">{{ duplicate.count }} 个重复</el-tag>
              </div>
            </template>
            
            <div class="duplicate-entries">
              <div v-for="entry in duplicate.entries" :key="entry.hash" class="entry-item">
                <div class="entry-info">
                  <strong>{{ entry.main_term }}</strong>
                  <el-tag size="small" type="info">{{ entry.category }}</el-tag>
                </div>
                <div class="entry-aliases">
                  别名: {{ entry.aliases.join(', ') || '无' }}
                </div>
                <div class="entry-definition">
                  {{ entry.definition || '无定义' }}
                </div>
              </div>
            </div>
          </el-card>
        </div>
      </div>
    </el-dialog>

    <!-- 批量导入对话框 -->
    <el-dialog
      v-model="importDialogVisible"
      title="📥 批量导入"
      width="600px"
    >
      <div class="import-section">
        <el-upload
          ref="uploadRef"
          :auto-upload="false"
          :on-change="handleFileChange"
          :show-file-list="false"
          accept=".csv,.xlsx,.xls"
          drag
        >
          <el-icon class="el-icon--upload"><upload-filled /></el-icon>
          <div class="el-upload__text">
            将文件拖到此处，或<em>点击上传</em>
          </div>
          <template #tip>
            <div class="el-upload__tip">
              支持 CSV、Excel 格式，需包含：术语、别名、类别、多标签、备注列
            </div>
          </template>
        </el-upload>
        
        <div v-if="importFile" class="file-info">
          <el-alert
            :title="`已选择文件: ${importFile.name}`"
            type="success"
            :closable="false"
          />
        </div>
      </div>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="importDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="importDictionary" :disabled="!importFile">
            开始导入
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Search, Refresh, Plus, Download, Upload, Warning, UploadFilled
} from '@element-plus/icons-vue'

export default {
  name: 'EnhancedDictionaryManagement',
  components: {
    Search, Refresh, Plus, Download, Upload, Warning, UploadFilled
  },
  setup() {
    // 响应式数据
    const loading = ref(false)
    const dictionaryEntries = ref([])
    const searchQuery = ref('')
    const selectedCategory = ref('')
    const categories = ref([])
    const statistics = ref({})

    // 分页
    const currentPage = ref(1)
    const pageSize = ref(50)

    // 对话框状态
    const dialogVisible = ref(false)
    const duplicatesDialogVisible = ref(false)
    const importDialogVisible = ref(false)
    const isEditing = ref(false)

    // 表单数据
    const currentEntry = reactive({
      term: '',
      category: '',
      aliases: [],
      tags: [],
      definition: ''
    })
    const aliasesInput = ref('')
    const tagsInput = ref('')

    // 重复项和批量操作
    const duplicates = ref([])
    const selectedEntries = ref([])
    const importFile = ref(null)

    // 表单验证规则
    const formRules = {
      term: [
        { required: true, message: '请输入主术语', trigger: 'blur' }
      ],
      category: [
        { required: true, message: '请选择类别', trigger: 'change' }
      ]
    }

    // 计算属性
    const filteredEntries = computed(() => {
      let entries = dictionaryEntries.value

      // 类别筛选
      if (selectedCategory.value) {
        entries = entries.filter(entry => entry.category === selectedCategory.value)
      }

      // 搜索筛选
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        entries = entries.filter(entry =>
          entry.term.toLowerCase().includes(query) ||
          entry.aliases.some(alias => alias.toLowerCase().includes(query)) ||
          entry.definition.toLowerCase().includes(query) ||
          entry.tags.some(tag => tag.toLowerCase().includes(query))
        )
      }

      return entries
    })

    const paginatedEntries = computed(() => {
      const start = (currentPage.value - 1) * pageSize.value
      const end = start + pageSize.value
      return filteredEntries.value.slice(start, end)
    })

    // 方法
    const loadDictionary = async () => {
      loading.value = true
      try {
        const response = await fetch('http://127.0.0.1:8000/kg/dictionary/entries')
        const result = await response.json()

        if (result.success) {
          dictionaryEntries.value = result.data.entries
          await loadCategories()
          await loadStatistics()
        } else {
          ElMessage.error('加载词典失败')
        }
      } catch (error) {
        ElMessage.error('加载词典失败: ' + error.message)
      } finally {
        loading.value = false
      }
    }

    const loadCategories = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/kg/dictionary/categories')
        const result = await response.json()

        if (result.success) {
          categories.value = result.data.categories
        }
      } catch (error) {
        console.error('加载类别失败:', error)
      }
    }

    const loadStatistics = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/kg/dictionary/statistics')
        const result = await response.json()

        if (result.success) {
          statistics.value = result.data
        }
      } catch (error) {
        console.error('加载统计失败:', error)
      }
    }

    const handleSearch = () => {
      currentPage.value = 1
    }

    const handleCategoryChange = () => {
      currentPage.value = 1
    }

    const handleSizeChange = (size) => {
      pageSize.value = size
      currentPage.value = 1
    }

    const handleCurrentChange = (page) => {
      currentPage.value = page
    }

    const handleSelectionChange = (selection) => {
      selectedEntries.value = selection
    }

    const getCategoryColor = (category) => {
      const colors = {
        '硬件相关': 'primary',
        '软件相关': 'success',
        '测试验证': 'warning',
        '异常现象': 'danger',
        '制造工艺': 'info',
        '流程相关': '',
        '工具': 'success',
        '组织职责': 'warning'
      }
      return colors[category] || ''
    }

    const showAddDialog = () => {
      isEditing.value = false
      resetForm()
      dialogVisible.value = true
    }

    const editEntry = (entry) => {
      isEditing.value = true
      currentEntry.term = entry.term
      currentEntry.category = entry.category
      currentEntry.aliases = [...entry.aliases]
      currentEntry.tags = [...entry.tags]
      currentEntry.definition = entry.definition
      aliasesInput.value = entry.aliases.join(';')
      tagsInput.value = entry.tags.join(';')
      dialogVisible.value = true
    }

    const resetForm = () => {
      currentEntry.term = ''
      currentEntry.category = ''
      currentEntry.aliases = []
      currentEntry.tags = []
      currentEntry.definition = ''
      aliasesInput.value = ''
      tagsInput.value = ''
    }

    const saveEntry = async () => {
      try {
        // 解析别名和标签
        currentEntry.aliases = aliasesInput.value ?
          aliasesInput.value.split(';').map(s => s.trim()).filter(s => s) : []
        currentEntry.tags = tagsInput.value ?
          tagsInput.value.split(';').map(s => s.trim()).filter(s => s) : []

        const url = isEditing.value ?
          `http://127.0.0.1:8000/kg/dictionary/entries/${currentEntry.id}` :
          'http://127.0.0.1:8000/kg/dictionary/entries'

        const method = isEditing.value ? 'PUT' : 'POST'

        const response = await fetch(url, {
          method,
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(currentEntry)
        })

        const result = await response.json()

        if (result.success) {
          ElMessage.success(isEditing.value ? '词条更新成功' : '词条创建成功')
          dialogVisible.value = false
          await loadDictionary()
        } else {
          ElMessage.error(result.message || '操作失败')
        }
      } catch (error) {
        ElMessage.error('操作失败: ' + error.message)
      }
    }

    const deleteEntry = async (entry) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除词条"${entry.term}"吗？`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )

        const response = await fetch(`http://127.0.0.1:8000/kg/dictionary/entries/${entry.id}`, {
          method: 'DELETE'
        })

        const result = await response.json()

        if (result.success) {
          ElMessage.success('词条删除成功')
          await loadDictionary()
        } else {
          ElMessage.error(result.message || '删除失败')
        }
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除失败: ' + error.message)
        }
      }
    }

    const findDuplicates = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/kg/dictionary/duplicates')
        const result = await response.json()

        if (result.success) {
          duplicates.value = result.data.duplicates
          duplicatesDialogVisible.value = true
        } else {
          ElMessage.error('查找重复项失败')
        }
      } catch (error) {
        ElMessage.error('查找重复项失败: ' + error.message)
      }
    }

    const removeDuplicates = async (strategy) => {
      try {
        await ElMessageBox.confirm(
          `确定要使用"${strategy}"策略清除重复项吗？`,
          '确认清除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )

        const response = await fetch('http://127.0.0.1:8000/kg/dictionary/remove-duplicates', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ strategy })
        })

        const result = await response.json()

        if (result.success) {
          ElMessage.success(result.message)
          duplicatesDialogVisible.value = false
          await loadDictionary()
        } else {
          ElMessage.error(result.message || '清除失败')
        }
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('清除失败: ' + error.message)
        }
      }
    }

    const showImportDialog = () => {
      importFile.value = null
      importDialogVisible.value = true
    }

    const handleFileChange = (file) => {
      importFile.value = file.raw
    }

    const importDictionary = async () => {
      if (!importFile.value) {
        ElMessage.warning('请选择文件')
        return
      }

      try {
        const formData = new FormData()
        formData.append('file', importFile.value)

        const response = await fetch('http://127.0.0.1:8000/kg/dictionary/import-file', {
          method: 'POST',
          body: formData
        })

        const result = await response.json()

        if (result.success) {
          ElMessage.success(result.message)
          importDialogVisible.value = false
          await loadDictionary()
        } else {
          ElMessage.error(result.message || '导入失败')
        }
      } catch (error) {
        ElMessage.error('导入失败: ' + error.message)
      }
    }

    const exportDictionary = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/kg/dictionary/export')

        if (response.ok) {
          const blob = await response.blob()
          const url = window.URL.createObjectURL(blob)
          const a = document.createElement('a')
          a.href = url
          a.download = `dictionary_export_${new Date().toISOString().slice(0, 10)}.csv`
          document.body.appendChild(a)
          a.click()
          document.body.removeChild(a)
          window.URL.revokeObjectURL(url)

          ElMessage.success('词典导出成功')
        } else {
          ElMessage.error('导出失败')
        }
      } catch (error) {
        ElMessage.error('导出失败: ' + error.message)
      }
    }

    const batchDelete = async () => {
      try {
        await ElMessageBox.confirm(
          `确定要删除选中的 ${selectedEntries.value.length} 个词条吗？`,
          '确认批量删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )

        // 批量删除逻辑
        for (const entry of selectedEntries.value) {
          await fetch(`http://127.0.0.1:8000/kg/dictionary/entries/${entry.id}`, {
            method: 'DELETE'
          })
        }

        ElMessage.success('批量删除成功')
        selectedEntries.value = []
        await loadDictionary()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('批量删除失败: ' + error.message)
        }
      }
    }

    const batchMerge = () => {
      ElMessage.info('批量合并功能开发中...')
    }

    // 生命周期
    onMounted(() => {
      loadDictionary()
    })

    return {
      // 数据
      loading,
      dictionaryEntries,
      searchQuery,
      selectedCategory,
      categories,
      statistics,
      currentPage,
      pageSize,
      dialogVisible,
      duplicatesDialogVisible,
      importDialogVisible,
      isEditing,
      currentEntry,
      aliasesInput,
      tagsInput,
      duplicates,
      selectedEntries,
      importFile,
      formRules,

      // 计算属性
      filteredEntries,
      paginatedEntries,

      // 方法
      loadDictionary,
      handleSearch,
      handleCategoryChange,
      handleSizeChange,
      handleCurrentChange,
      handleSelectionChange,
      getCategoryColor,
      showAddDialog,
      editEntry,
      resetForm,
      saveEntry,
      deleteEntry,
      findDuplicates,
      removeDuplicates,
      showImportDialog,
      handleFileChange,
      importDictionary,
      exportDictionary,
      batchDelete,
      batchMerge,

      // 图标
      Search,
      Refresh,
      Plus,
      Download,
      Upload,
      Warning,
      UploadFilled
    }
  }
}
</script>

<style scoped>
.enhanced-dictionary-management {
  padding: 20px;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h1 {
  margin: 0 0 8px 0;
  color: #303133;
  font-size: 28px;
  font-weight: 600;
}

.page-header p {
  margin: 0;
  color: #606266;
  font-size: 14px;
}

.toolbar-card {
  margin-bottom: 20px;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.search-section {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.action-section {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.table-card {
  margin-bottom: 20px;
}

.aliases {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.alias-tag {
  margin: 2px 0;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.tag-item {
  margin: 2px 0;
}

.metadata {
  text-align: center;
}

.version {
  font-size: 12px;
  color: #909399;
}

.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.batch-actions {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.batch-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.no-duplicates {
  text-align: center;
  padding: 40px 0;
}

.duplicates-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 4px;
}

.duplicates-list {
  max-height: 400px;
  overflow-y: auto;
}

.duplicate-item {
  margin-bottom: 16px;
}

.duplicate-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.duplicate-term {
  font-weight: 600;
  font-size: 16px;
}

.duplicate-entries {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.entry-item {
  padding: 12px;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  background: #fafafa;
}

.entry-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.entry-aliases {
  font-size: 12px;
  color: #606266;
  margin-bottom: 4px;
}

.entry-definition {
  font-size: 12px;
  color: #909399;
}

.import-section {
  margin-bottom: 20px;
}

.file-info {
  margin-top: 16px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .toolbar {
    flex-direction: column;
    align-items: stretch;
  }

  .search-section {
    justify-content: center;
  }

  .action-section {
    justify-content: center;
  }

  .batch-actions {
    left: 20px;
    right: 20px;
    transform: none;
  }

  .batch-toolbar {
    flex-direction: column;
    gap: 12px;
  }

  .duplicates-header {
    flex-direction: column;
    gap: 12px;
  }
}

/* 动画效果 */
.el-table {
  transition: all 0.3s ease;
}

.alias-tag, .tag-item {
  transition: all 0.2s ease;
}

.alias-tag:hover, .tag-item:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.duplicate-item {
  transition: all 0.3s ease;
}

.duplicate-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>
