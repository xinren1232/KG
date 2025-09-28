<template>
  <div class="dictionary-management">
    <el-card class="header-card">
      <div class="page-header">
        <h2>📚 词典管理</h2>
        <p>管理标准化词典，包括组件词典、异常词典、供应商词典等</p>
      </div>
    </el-card>

    <!-- 搜索和筛选 -->
    <el-card class="search-card">
      <el-row :gutter="20">
        <el-col :span="8">
          <el-input
            v-model="searchQuery"
            placeholder="搜索词条..."
            clearable
            @input="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-col>
        <el-col :span="6">
          <el-select
            v-model="selectedCategory"
            placeholder="选择类别"
            clearable
            @change="handleCategoryChange"
          >
            <el-option label="全部" value="" />
            <el-option label="工具" value="工具" />
            <el-option label="症状" value="症状" />
            <el-option label="组件" value="组件" />
            <el-option label="流程" value="流程" />
            <el-option label="测试用例" value="测试用例" />
            <el-option label="性能指标" value="性能指标" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="loadDictionary">
            <el-icon><Refresh /></el-icon>
            刷新
          </el-button>
        </el-col>
        <el-col :span="6">
          <div class="actions">
            <el-button type="success" @click="showAddDialog">
              <el-icon><Plus /></el-icon>
              添加词条
            </el-button>
            <el-button @click="exportDictionary">
              <el-icon><Download /></el-icon>
              导出
            </el-button>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <!-- 词典列表 -->
    <el-card class="dictionary-card">
      <div class="dictionary-header">
        <h3>📋 词典条目</h3>
        <el-tag type="info">共 {{ filteredEntries.length }} 条</el-tag>
      </div>

      <el-table
        :data="paginatedEntries"
        stripe
        style="width: 100%"
        v-loading="loading"
      >
        <el-table-column prop="name" label="术语" min-width="150" />
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
        <el-table-column prop="category" label="类别" width="120">
          <template #default="{ row }">
            <el-tag :type="getCategoryColor(row.category)" size="small">
              {{ row.category }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="多标签" min-width="200">
          <template #default="{ row }">
            <div class="tags">
              <el-tag
                v-for="tag in row.tags"
                :key="tag"
                size="small"
                type="success"
                class="tag-item"
              >
                {{ tag }}
              </el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="备注" min-width="250" show-overflow-tooltip />
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button size="small" @click="editEntry(row)">
              编辑
            </el-button>
            <el-button size="small" type="danger" @click="deleteEntry(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="filteredEntries.length"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 添加/编辑词条对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEditing ? '编辑词条' : '添加词条'"
      width="600px"
    >
      <el-form
        ref="formRef"
        :model="currentEntry"
        :rules="formRules"
        label-width="80px"
      >
        <el-form-item label="词条" prop="term">
          <el-input
            v-model="currentEntry.term"
            placeholder="请输入词条"
            @blur="checkDuplicate"
          />
          <!-- 查重提示 -->
          <div v-if="duplicateInfo.isDuplicate" class="duplicate-warning">
            <el-alert
              :title="duplicateInfo.message"
              type="warning"
              :closable="false"
              show-icon
            >
              <template #default>
                <div>
                  <p>{{ duplicateInfo.message }}</p>
                  <div v-if="duplicateInfo.suggestions.length > 0" class="suggestions">
                    <p><strong>相似词条建议：</strong></p>
                    <el-tag
                      v-for="suggestion in duplicateInfo.suggestions"
                      :key="suggestion"
                      size="small"
                      style="margin-right: 8px; margin-bottom: 4px; cursor: pointer;"
                      @click="selectSuggestion(suggestion)"
                    >
                      {{ suggestion }}
                    </el-tag>
                  </div>
                </div>
              </template>
            </el-alert>
          </div>
        </el-form-item>
        
        <el-form-item label="类别" prop="category">
          <el-select v-model="currentEntry.category" placeholder="请选择类别">
            <el-option label="组件" value="组件" />
            <el-option label="异常" value="异常" />
            <el-option label="供应商" value="供应商" />
            <el-option label="工厂" value="工厂" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="别名">
          <el-tag
            v-for="alias in currentEntry.aliases"
            :key="alias"
            closable
            @close="removeAlias(alias)"
            class="alias-input-tag"
          >
            {{ alias }}
          </el-tag>
          <el-input
            v-if="aliasInputVisible"
            ref="aliasInputRef"
            v-model="aliasInputValue"
            size="small"
            @keyup.enter="handleAliasInputConfirm"
            @blur="handleAliasInputConfirm"
            class="alias-input"
          />
          <el-button v-else size="small" @click="showAliasInput">
            + 添加别名
          </el-button>
        </el-form-item>
        
        <el-form-item label="定义" prop="definition">
          <el-input
            v-model="currentEntry.definition"
            type="textarea"
            :rows="3"
            placeholder="请输入词条定义"
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
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Refresh, Plus, Download } from '@element-plus/icons-vue'
import { kgApi } from '@/api/index.js'

export default {
  name: 'DictionaryManagement',
  components: {
    Search,
    Refresh,
    Plus,
    Download
  },
  setup() {
    const loading = ref(false)
    const searchQuery = ref('')
    const selectedCategory = ref('')
    const currentPage = ref(1)
    const pageSize = ref(20)
    
    const dictionaryEntries = ref([])
    const dialogVisible = ref(false)
    const isEditing = ref(false)
    const aliasInputVisible = ref(false)
    const aliasInputValue = ref('')

    // 查重相关
    const duplicateInfo = reactive({
      isDuplicate: false,
      message: '',
      suggestions: []
    })
    
    const currentEntry = reactive({
      id: '',
      term: '',
      category: '',
      aliases: [],
      definition: '',
      metadata: {}
    })

    const formRules = {
      term: [
        { required: true, message: '请输入词条', trigger: 'blur' }
      ],
      category: [
        { required: true, message: '请选择类别', trigger: 'change' }
      ],
      definition: [
        { required: true, message: '请输入定义', trigger: 'blur' }
      ]
    }

    // 计算属性
    const filteredEntries = computed(() => {
      let entries = dictionaryEntries.value
      
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        entries = entries.filter(entry => 
          entry.term.toLowerCase().includes(query) ||
          entry.definition.toLowerCase().includes(query) ||
          entry.aliases.some(alias => alias.toLowerCase().includes(query))
        )
      }
      
      if (selectedCategory.value) {
        entries = entries.filter(entry => entry.category === selectedCategory.value)
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
        // 使用新的API获取词典数据 - 获取所有数据
        const result = await kgApi.getDictionary({ size: 10000 })

        if (result.success && result.data && result.data.entries) {
          // 转换新API数据格式为前端期望的格式
          const entries = result.data.entries.map((item, index) => {
            return {
              id: `term_${index}`,
              term: item.term || '',
              name: item.term || '',
              type: item.category || '未分类',
              category: item.category || '未分类',
              subCategory: item.sub_category || '',
              aliases: Array.isArray(item.aliases) ? item.aliases : [],
              tags: Array.isArray(item.tags) ? item.tags : [],
              description: item.definition || item.description || '',
              standardName: item.term || '',
              source: item.source || '',
              status: item.status || 'active'
            }
          })

          dictionaryEntries.value = entries
          ElMessage.success(`成功加载${entries.length}条词典数据`)
        } else {
          // 如果新API失败，尝试旧API作为备用
          console.warn('新API失败，尝试旧API:', result)
          const fallbackResult = await kgApi.getOldDictionary()

          if (fallbackResult.ok && fallbackResult.data) {
            // 使用旧API的数据处理逻辑
            const entries = []

            // 处理旧格式数据...
            if (fallbackResult.data.components) {
              fallbackResult.data.components.forEach(comp => {
                entries.push({
                  id: `comp_${comp.name}`,
                  term: comp.name || comp.canonical_name,
                  name: comp.name || comp.canonical_name,
                  type: '组件',
                  category: comp.category || '未分类',
                  aliases: comp.aliases || [],
                  tags: comp.tags || [],
                  description: comp.description || '',
                  standardName: comp.canonical_name || comp.name
                })
              })
            }

            dictionaryEntries.value = entries
            ElMessage.warning('使用备用API加载词典数据')
          } else {
            ElMessage.error('加载词典失败: ' + (result.error || '未知错误'))
          }
        }
      } catch (error) {
        ElMessage.error('加载词典失败: ' + error.message)
        console.error('Load dictionary error:', error)
      } finally {
        loading.value = false
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

    const getCategoryColor = (category) => {
      const colors = {
        '组件': 'primary',
        '症状': 'danger',
        '原因分析': 'warning',
        '对策工具': 'success',
        '工具流程': 'info'
      }
      return colors[category] || 'info'
    }

    const showAddDialog = () => {
      isEditing.value = false
      resetCurrentEntry()
      resetDuplicateInfo()
      dialogVisible.value = true
    }

    const editEntry = (entry) => {
      isEditing.value = true
      Object.assign(currentEntry, entry)
      dialogVisible.value = true
    }

    const deleteEntry = async (entry) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除词条"${entry.term}"吗？`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
          }
        )
        
        // 模拟删除操作
        const index = dictionaryEntries.value.findIndex(e => e.id === entry.id)
        if (index > -1) {
          dictionaryEntries.value.splice(index, 1)
          ElMessage.success('删除成功')
        }
      } catch {
        // 用户取消删除
      }
    }

    const resetCurrentEntry = () => {
      currentEntry.id = ''
      currentEntry.term = ''
      currentEntry.category = ''
      currentEntry.aliases = []
      currentEntry.definition = ''
      currentEntry.metadata = {}
    }

    const showAliasInput = () => {
      aliasInputVisible.value = true
      nextTick(() => {
        // 聚焦到输入框
      })
    }

    const handleAliasInputConfirm = () => {
      if (aliasInputValue.value && !currentEntry.aliases.includes(aliasInputValue.value)) {
        currentEntry.aliases.push(aliasInputValue.value)
      }
      aliasInputVisible.value = false
      aliasInputValue.value = ''
    }

    const removeAlias = (alias) => {
      const index = currentEntry.aliases.indexOf(alias)
      if (index > -1) {
        currentEntry.aliases.splice(index, 1)
      }
    }

    // 查重检查
    const checkDuplicate = async () => {
      if (!currentEntry.term || currentEntry.term.trim() === '') {
        duplicateInfo.isDuplicate = false
        return
      }

      const term = currentEntry.term.trim().toLowerCase()

      // 检查完全重复
      const exactMatch = dictionaryEntries.value.find(entry =>
        entry.term.toLowerCase() === term &&
        (!isEditing.value || entry.id !== currentEntry.id)
      )

      if (exactMatch) {
        duplicateInfo.isDuplicate = true
        duplicateInfo.message = `词条 "${currentEntry.term}" 已存在！`
        duplicateInfo.suggestions = []
        return
      }

      // 检查相似词条（包含关系或别名匹配）
      const similarEntries = dictionaryEntries.value.filter(entry => {
        if (isEditing.value && entry.id === currentEntry.id) return false

        const entryTerm = entry.term.toLowerCase()
        const entryAliases = (entry.aliases || []).map(alias => alias.toLowerCase())

        // 检查包含关系
        const isContained = entryTerm.includes(term) || term.includes(entryTerm)

        // 检查别名匹配
        const aliasMatch = entryAliases.some(alias =>
          alias === term || alias.includes(term) || term.includes(alias)
        )

        return isContained || aliasMatch
      })

      if (similarEntries.length > 0) {
        duplicateInfo.isDuplicate = true
        duplicateInfo.message = `发现 ${similarEntries.length} 个相似词条，请确认是否重复`
        duplicateInfo.suggestions = similarEntries.slice(0, 5).map(entry => entry.term)
      } else {
        duplicateInfo.isDuplicate = false
        duplicateInfo.message = ''
        duplicateInfo.suggestions = []
      }
    }

    // 选择建议词条
    const selectSuggestion = (suggestion) => {
      currentEntry.term = suggestion
      duplicateInfo.isDuplicate = false
    }

    // 重置查重信息
    const resetDuplicateInfo = () => {
      duplicateInfo.isDuplicate = false
      duplicateInfo.message = ''
      duplicateInfo.suggestions = []
    }

    const saveEntry = () => {
      // 检查是否有重复
      if (duplicateInfo.isDuplicate && duplicateInfo.suggestions.length === 0) {
        ElMessage.error('词条已存在，请修改后再试')
        return
      }

      // 模拟保存操作
      if (isEditing.value) {
        const index = dictionaryEntries.value.findIndex(e => e.id === currentEntry.id)
        if (index > -1) {
          dictionaryEntries.value[index] = { ...currentEntry }
        }
        ElMessage.success('更新成功')
      } else {
        const newEntry = {
          ...currentEntry,
          id: `dict_${Date.now()}`
        }
        dictionaryEntries.value.push(newEntry)
        ElMessage.success('添加成功')
      }

      resetDuplicateInfo()
      dialogVisible.value = false
    }

    const exportDictionary = () => {
      const dataStr = JSON.stringify(filteredEntries.value, null, 2)
      const dataBlob = new Blob([dataStr], { type: 'application/json' })
      const url = URL.createObjectURL(dataBlob)
      const link = document.createElement('a')
      link.href = url
      link.download = `dictionary_${Date.now()}.json`
      link.click()
      URL.revokeObjectURL(url)
      ElMessage.success('导出成功')
    }

    // 生命周期
    onMounted(() => {
      loadDictionary()
    })

    return {
      loading,
      searchQuery,
      selectedCategory,
      currentPage,
      pageSize,
      dictionaryEntries,
      filteredEntries,
      paginatedEntries,
      dialogVisible,
      isEditing,
      currentEntry,
      formRules,
      aliasInputVisible,
      aliasInputValue,
      duplicateInfo,
      loadDictionary,
      handleSearch,
      handleCategoryChange,
      handleSizeChange,
      handleCurrentChange,
      getCategoryColor,
      showAddDialog,
      editEntry,
      deleteEntry,
      showAliasInput,
      handleAliasInputConfirm,
      removeAlias,
      checkDuplicate,
      selectSuggestion,
      saveEntry,
      exportDictionary
    }
  }
}
</script>

<style scoped>
.dictionary-management {
  padding: 20px;
}

.header-card, .search-card, .dictionary-card {
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0 0 10px 0;
  color: #409EFF;
}

.page-header p {
  margin: 0;
  color: #666;
}

.actions {
  text-align: right;
}

.dictionary-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.dictionary-header h3 {
  margin: 0;
}

.aliases, .metadata {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.alias-tag, .metadata-tag, .tag-item {
  margin: 2px;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.tag-item {
  background-color: #f0f9ff;
  border-color: #0ea5e9;
  color: #0369a1;
}

.pagination {
  margin-top: 20px;
  text-align: center;
}

.alias-input-tag {
  margin-right: 8px;
  margin-bottom: 8px;
}

.alias-input {
  width: 100px;
  margin-right: 8px;
  margin-bottom: 8px;
}

/* 查重提示样式 */
.duplicate-warning {
  margin-top: 8px;
}

.duplicate-warning .suggestions {
  margin-top: 8px;
}

.duplicate-warning .suggestions p {
  margin: 4px 0;
  font-size: 14px;
}

.duplicate-warning .el-tag {
  cursor: pointer;
  transition: all 0.3s;
}

.duplicate-warning .el-tag:hover {
  transform: scale(1.05);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
