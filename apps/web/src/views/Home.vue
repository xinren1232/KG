<template>
  <div class="home">
    <!-- 欢迎区域 -->
    <el-card class="welcome-card">
      <div class="welcome-content">
        <h2>📱 知识图谱构建助手</h2>
        <p class="subtitle">文档解析 · 知识抽取 · 图谱构建 · 数据治理</p>
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
        <el-card shadow="hover" class="feature-card" @click="$router.push('/graph')">
          <div class="feature-content">
            <el-icon class="feature-icon" color="#67C23A"><Share /></el-icon>
            <h3>知识图谱</h3>
            <p>可视化浏览知识图谱，探索实体关系和数据洞察</p>
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
        <el-card shadow="hover" class="feature-card" @click="$router.push('/governance')">
          <div class="feature-content">
            <el-icon class="feature-icon" color="#F56C6C"><Setting /></el-icon>
            <h3>数据治理</h3>
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
                <span>图谱节点: {{ stats.nodes }}</span>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="status-item">
                <el-icon color="#E6A23C"><Collection /></el-icon>
                <span>词典条目: {{ stats.dictEntries }}</span>
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
import {
  Share,
  Connection,
  DataAnalysis,
  Document,
  Collection,
  Setting
} from '@element-plus/icons-vue'

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
      nodes: 1250,
      dictEntries: 156,
      extractedFiles: 23,
      qualityScore: 87
    })

    onMounted(() => {
      console.log('Home page loaded successfully')
    })

    return {
      stats
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
