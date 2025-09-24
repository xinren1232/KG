<template>
  <div class="global-search">
    <el-input
      v-model="searchQuery"
      placeholder="搜索产品、组件、测试用例、异常..."
      :prefix-icon="Search"
      clearable
      @input="onSearchInput"
      @keyup.enter="performSearch"
      class="search-input"
    >
      <template #append>
        <el-button @click="performSearch" :loading="searching">
          搜索
        </el-button>
      </template>
    </el-input>

    <!-- 搜索建议下拉框 -->
    <div v-if="showSuggestions && suggestions.length > 0" class="suggestions-dropdown">
      <div class="suggestions-header">
        <span>搜索建议</span>
        <el-button type="text" size="small" @click="closeSuggestions">
          <el-icon><Close /></el-icon>
        </el-button>
      </div>
      
      <div class="suggestions-list">
        <div
          v-for="suggestion in suggestions"
          :key="suggestion.id"
          class="suggestion-item"
          @click="selectSuggestion(suggestion)"
        >
          <el-icon class="suggestion-icon" :color="getSuggestionColor(suggestion.type)">
            <component :is="getSuggestionIcon(suggestion.type)" />
          </el-icon>
          <div class="suggestion-content">
            <div class="suggestion-title">{{ suggestion.title }}</div>
            <div class="suggestion-type">{{ getSuggestionTypeText(suggestion.type) }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 搜索结果对话框 -->
    <el-dialog
      v-model="showResults"
      title="搜索结果"
      width="80%"
      :close-on-click-modal="false"
    >
      <div v-if="searchResults.length > 0">
        <el-tabs v-model="activeTab" type="card">
          <el-tab-pane
            v-for="category in resultCategories"
            :key="category.key"
            :label="`${category.label} (${category.count})`"
            :name="category.key"
          >
            <div class="search-results">
              <el-card
                v-for="result in category.items"
                :key="result.id"
                class="result-card"
                shadow="hover"
                @click="viewResultDetail(result)"
              >
                <div class="result-header">
                  <el-icon :color="getSuggestionColor(result.type)">
                    <component :is="getSuggestionIcon(result.type)" />
                  </el-icon>
                  <h4>{{ result.title }}</h4>
                  <el-tag size="small" :type="getResultTagType(result.type)">
                    {{ getSuggestionTypeText(result.type) }}
                  </el-tag>
                </div>
                <p class="result-description">{{ result.description }}</p>
                <div class="result-meta" v-if="result.meta">
                  <span v-for="(value, key) in result.meta" :key="key" class="meta-item">
                    {{ key }}: {{ value }}
                  </span>
                </div>
              </el-card>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
      
      <el-empty v-else description="未找到相关结果">
        <el-button type="primary" @click="showResults = false">关闭</el-button>
      </el-empty>
    </el-dialog>
  </div>
</template>

<script>
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { 
  Search, 
  Close,
  Document,
  Setting,
  Warning,
  List
} from '@element-plus/icons-vue'
import { kgApi } from '../api'

export default {
  name: 'GlobalSearch',
  components: {
    Search,
    Close,
    Document,
    Setting,
    Warning,
    List
  },
  setup() {
    const searchQuery = ref('')
    const searching = ref(false)
    const showSuggestions = ref(false)
    const showResults = ref(false)
    const activeTab = ref('all')
    
    const suggestions = ref([])
    const searchResults = ref([])
    
    // 模拟搜索建议数据
    const mockSuggestions = [
      { id: 1, title: 'iPhone 15', type: 'product', description: '苹果手机产品' },
      { id: 2, title: '摄像头模块', type: 'component', description: '摄像头硬件组件' },
      { id: 3, title: '摄像头对焦功能测试', type: 'testcase', description: '功能测试用例' },
      { id: 4, title: '摄像头无法对焦', type: 'anomaly', description: '已知异常问题' },
      { id: 5, title: 'Galaxy S24', type: 'product', description: '三星手机产品' },
      { id: 6, title: '电池模块', type: 'component', description: '电池硬件组件' }
    ]

    // 搜索结果分类
    const resultCategories = computed(() => {
      const categories = {
        all: { key: 'all', label: '全部', items: searchResults.value, count: searchResults.value.length },
        product: { key: 'product', label: '产品', items: [], count: 0 },
        component: { key: 'component', label: '组件', items: [], count: 0 },
        testcase: { key: 'testcase', label: '测试用例', items: [], count: 0 },
        anomaly: { key: 'anomaly', label: '异常', items: [], count: 0 }
      }

      searchResults.value.forEach(result => {
        if (categories[result.type]) {
          categories[result.type].items.push(result)
          categories[result.type].count++
        }
      })

      return Object.values(categories).filter(cat => cat.count > 0 || cat.key === 'all')
    })

    // 监听搜索输入
    const onSearchInput = (value) => {
      if (value.length >= 2) {
        showSuggestions.value = true
        // 过滤建议
        suggestions.value = mockSuggestions.filter(item =>
          item.title.toLowerCase().includes(value.toLowerCase()) ||
          item.description.toLowerCase().includes(value.toLowerCase())
        ).slice(0, 5)
      } else {
        showSuggestions.value = false
        suggestions.value = []
      }
    }

    // 执行搜索
    const performSearch = async () => {
      if (!searchQuery.value.trim()) {
        ElMessage.warning('请输入搜索关键词')
        return
      }

      searching.value = true
      showSuggestions.value = false

      try {
        // 模拟搜索结果
        const mockResults = mockSuggestions.filter(item =>
          item.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
          item.description.toLowerCase().includes(searchQuery.value.toLowerCase())
        ).map(item => ({
          ...item,
          meta: getResultMeta(item.type)
        }))

        searchResults.value = mockResults
        showResults.value = true
        activeTab.value = 'all'

        ElMessage.success(`找到 ${mockResults.length} 个相关结果`)
      } catch (error) {
        ElMessage.error('搜索失败: ' + error.message)
      } finally {
        searching.value = false
      }
    }

    // 选择搜索建议
    const selectSuggestion = (suggestion) => {
      searchQuery.value = suggestion.title
      showSuggestions.value = false
      performSearch()
    }

    // 关闭建议
    const closeSuggestions = () => {
      showSuggestions.value = false
    }

    // 查看结果详情
    const viewResultDetail = (result) => {
      ElMessage.info(`查看 ${result.title} 详情`)
      // 这里可以跳转到相应的详情页面
    }

    // 获取建议图标
    const getSuggestionIcon = (type) => {
      const iconMap = {
        product: 'Document',
        component: 'Setting',
        testcase: 'List',
        anomaly: 'Warning'
      }
      return iconMap[type] || 'Document'
    }

    // 获取建议颜色
    const getSuggestionColor = (type) => {
      const colorMap = {
        product: '#409EFF',
        component: '#67C23A',
        testcase: '#E6A23C',
        anomaly: '#F56C6C'
      }
      return colorMap[type] || '#909399'
    }

    // 获取类型文本
    const getSuggestionTypeText = (type) => {
      const textMap = {
        product: '产品',
        component: '组件',
        testcase: '测试用例',
        anomaly: '异常'
      }
      return textMap[type] || '未知'
    }

    // 获取结果标签类型
    const getResultTagType = (type) => {
      const typeMap = {
        product: 'primary',
        component: 'success',
        testcase: 'warning',
        anomaly: 'danger'
      }
      return typeMap[type] || 'info'
    }

    // 获取结果元数据
    const getResultMeta = (type) => {
      const metaMap = {
        product: { '状态': '活跃', '版本': 'V1.0' },
        component: { '类型': '硬件', '重要性': '高' },
        testcase: { '优先级': '高', '类型': '功能测试' },
        anomaly: { '严重程度': '中', '状态': '已解决' }
      }
      return metaMap[type] || {}
    }

    // 点击外部关闭建议
    watch(showSuggestions, (newVal) => {
      if (newVal) {
        document.addEventListener('click', handleClickOutside)
      } else {
        document.removeEventListener('click', handleClickOutside)
      }
    })

    const handleClickOutside = (event) => {
      const searchElement = document.querySelector('.global-search')
      if (searchElement && !searchElement.contains(event.target)) {
        showSuggestions.value = false
      }
    }

    return {
      searchQuery,
      searching,
      showSuggestions,
      showResults,
      activeTab,
      suggestions,
      searchResults,
      resultCategories,
      onSearchInput,
      performSearch,
      selectSuggestion,
      closeSuggestions,
      viewResultDetail,
      getSuggestionIcon,
      getSuggestionColor,
      getSuggestionTypeText,
      getResultTagType,
      Search,
      Close,
      Document,
      Setting,
      Warning,
      List
    }
  }
}
</script>

<style scoped>
.global-search {
  position: relative;
  width: 100%;
  max-width: 600px;
}

.search-input {
  width: 100%;
}

.suggestions-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #E4E7ED;
  border-radius: 4px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  margin-top: 4px;
}

.suggestions-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  border-bottom: 1px solid #E4E7ED;
  background: #F5F7FA;
  font-size: 12px;
  color: #909399;
}

.suggestions-list {
  max-height: 300px;
  overflow-y: auto;
}

.suggestion-item {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.suggestion-item:hover {
  background-color: #F5F7FA;
}

.suggestion-icon {
  margin-right: 8px;
}

.suggestion-content {
  flex: 1;
}

.suggestion-title {
  font-size: 14px;
  color: #303133;
  margin-bottom: 2px;
}

.suggestion-type {
  font-size: 12px;
  color: #909399;
}

.search-results {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.result-card {
  cursor: pointer;
  transition: all 0.2s;
}

.result-card:hover {
  transform: translateY(-2px);
}

.result-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.result-header h4 {
  margin: 0;
  flex: 1;
  color: #303133;
}

.result-description {
  color: #606266;
  font-size: 14px;
  margin: 0 0 8px 0;
  line-height: 1.5;
}

.result-meta {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: #909399;
}

.meta-item {
  white-space: nowrap;
}
</style>
