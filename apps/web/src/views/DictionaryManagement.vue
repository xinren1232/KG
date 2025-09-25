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
            <el-option label="组件" value="组件" />
            <el-option label="异常" value="异常" />
            <el-option label="供应商" value="供应商" />
            <el-option label="工厂" value="工厂" />
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
          <el-input v-model="currentEntry.term" placeholder="请输入词条" />
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
        const response = await fetch('http://127.0.0.1:8000/kg/dictionary')
        const result = await response.json()
        
        if (result.ok && result.data) {
          // 转换API数据格式为前端期望的格式
          const entries = []

          // 添加组件词典
          if (result.data.components) {
            result.data.components.forEach(comp => {
              entries.push({
                id: `comp_${comp.name}`,
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

          // 添加症状词典
          if (result.data.symptoms) {
            result.data.symptoms.forEach(symptom => {
              entries.push({
                id: `symptom_${symptom.name}`,
                name: symptom.name || symptom.canonical_name,
                type: '症状',
                category: symptom.category || '未分类',
                aliases: symptom.aliases || [],
                tags: symptom.tags || [],
                description: symptom.description || '',
                standardName: symptom.canonical_name || symptom.name,
                severity: symptom.severity
              })
            })
          }

          // 添加工具流程词典
          if (result.data.tools_processes) {
            result.data.tools_processes.forEach(tool => {
              entries.push({
                id: `tool_${tool.name}`,
                name: tool.name || tool.canonical_name,
                type: '工具流程',
                category: tool.category || '未分类',
                aliases: tool.aliases || [],
                tags: tool.tags || [],
                description: tool.description || '',
                standardName: tool.canonical_name || tool.name
              })
            })
          }

          dictionaryEntries.value = entries
        } else {
          ElMessage.error('加载词典失败: ' + (result.error?.message || '未知错误'))
        }
      } catch (error) {
        ElMessage.error('加载词典失败')
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
        '异常': 'danger',
        '供应商': 'success',
        '工厂': 'warning'
      }
      return colors[category] || 'info'
    }

    const showAddDialog = () => {
      isEditing.value = false
      resetCurrentEntry()
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

    const saveEntry = () => {
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
</style>
