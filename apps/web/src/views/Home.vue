<template>
  <div class="home">
    <!-- 欢迎区域 -->
    <el-card class="welcome-card">
      <div class="welcome-content">
        <h2>📱 知识图谱构建助手</h2>
        <p class="subtitle">文档解析 · 知识抽取 · 图谱构建 · 系统管理</p>
        <p class="description">
          基于先进的NLP技术和知识图谱技术，提供智能化的文档解析、知识抽取和图谱构建服务，
          帮助企业从非结构化数据中提取结构化知识，构建领域知识图谱。
        </p>
      </div>
    </el-card>

    <!-- 核心功能卡片 -->
    <el-row :gutter="20" class="feature-cards">
      <el-col :xs="24" :sm="12" :md="8" :lg="6">
        <el-card shadow="hover" class="feature-card" @click="$router.push('/extract')">
          <div class="feature-content">
            <el-icon class="feature-icon" color="#409EFF"><Document /></el-icon>
            <h3>文档解析</h3>
            <p>上传Excel、PDF、Word等文档，智能抽取实体和关系</p>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :md="8" :lg="6">
        <el-card shadow="hover" class="feature-card" @click="$router.push('/graph-viz')">
          <div class="feature-content">
            <el-icon class="feature-icon" color="#67C23A"><Share /></el-icon>
            <h3>图谱可视化</h3>
            <p>交互式图谱展示，探索硬件质量术语的关联关系</p>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :md="8" :lg="6">
        <el-card shadow="hover" class="feature-card" @click="$router.push('/dictionary')">
          <div class="feature-content">
            <el-icon class="feature-icon" color="#E6A23C"><Collection /></el-icon>
            <h3>词典管理</h3>
            <p>管理标准化词典，支持实体标准化和别名映射</p>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :md="8" :lg="6">
        <el-card shadow="hover" class="feature-card" @click="$router.push('/system-management')">
          <div class="feature-content">
            <el-icon class="feature-icon" color="#F56C6C"><Setting /></el-icon>
            <h3>系统管理</h3>
            <p>数据质量监控、标准化管理和持续优化</p>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 系统状态 -->
    <el-row :gutter="20" class="status-section">
      <el-col :span="24">
        <el-card class="status-card">
          <template #header>
            <span>系统状态</span>
          </template>
          <el-row :gutter="20">
            <el-col :span="6">
              <div class="status-item">
                <el-icon color="#67C23A"><Connection /></el-icon>
                <span>API服务: 正常</span>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="status-item">
                <el-icon color="#67C23A"><DataAnalysis /></el-icon>
                <span>图数据库: 已连接</span>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="status-item">
                <el-icon color="#409EFF"><Document /></el-icon>
                <span>词典条目: {{ stats.dictEntries }}</span>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="status-item">
                <el-icon color="#E6A23C"><Collection /></el-icon>
                <span>关系数量: {{ stats.relations }}</span>
              </div>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Share,
  Connection,
  DataAnalysis,
  Document,
  Collection,
  Setting
} from '@element-plus/icons-vue'
import http from '@/api/http'

export default {
  name: 'Home',
  components: {
    Share,
    Connection,
    DataAnalysis,
    Document,
    Collection,
    Setting
  },
  setup() {
    const stats = ref({
      dictEntries: 0,
      relations: 0,
      categories: 0,
      tags: 0
    })

    const loading = ref(false)

    // 获取系统统计数据
    const fetchStats = async () => {
      try {
        loading.value = true
        console.log('🔄 开始获取系统统计数据...')

        // 调用后端API获取实时统计
        const response = await http.get('/kg/real-stats')
        console.log('📡 API响应:', response)

        if (response && response.data) {
          const data = response.data

          // 处理响应数据结构
          if (data.stats) {
            // 如果有stats字段
            stats.value.dictEntries = data.stats.dictEntries || data.stats.totalTerms || 0
            stats.value.relations = data.stats.totalRelations || 0
            stats.value.categories = data.stats.totalCategories || 0
            stats.value.tags = data.stats.totalTags || 0
          } else {
            // 直接使用data字段
            stats.value.dictEntries = data.dictEntries || data.totalTerms || 0
            stats.value.relations = data.totalRelations || 0
            stats.value.categories = data.totalCategories || 0
            stats.value.tags = data.totalTags || 0
          }

          console.log('✅ 成功获取实时统计数据:', stats.value)
        } else {
          console.warn('⚠️ API响应数据格式异常')
        }

      } catch (error) {
        console.error('❌ 获取统计数据失败:', error)
        ElMessage.error('获取统计数据失败，请刷新页面重试')
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      console.log('🏠 首页加载完成')
      fetchStats()
    })

    return {
      stats,
      loading,
      fetchStats
    }
  }
}
</script>

<style scoped>
.home {
  padding: 20px;
}

.welcome-card {
  margin-bottom: 30px;
  text-align: center;
}

.welcome-content h2 {
  margin: 0 0 15px 0;
  color: #303133;
  font-size: 28px;
}

.subtitle {
  color: #606266;
  font-size: 16px;
  margin: 0 0 15px 0;
}

.description {
  color: #909399;
  font-size: 14px;
  line-height: 1.6;
  max-width: 800px;
  margin: 0 auto;
}

.feature-cards {
  margin-bottom: 30px;
}

.feature-card {
  margin-bottom: 20px;
  cursor: pointer;
  transition: transform 0.2s;
}

.feature-card:hover {
  transform: translateY(-2px);
}

.feature-content {
  text-align: center;
  padding: 20px;
}

.feature-icon {
  font-size: 48px;
  margin-bottom: 15px;
}

.feature-content h3 {
  margin: 0 0 10px 0;
  color: #303133;
  font-size: 18px;
}

.feature-content p {
  color: #606266;
  font-size: 14px;
  margin: 0;
  line-height: 1.5;
}

.status-section {
  margin-top: 20px;
}

.status-card .el-card__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 4px;
}

@media (max-width: 768px) {
  .feature-cards .el-col {
    margin-bottom: 15px;
  }
  
  .status-section .el-col {
    margin-bottom: 10px;
  }
}
</style>
