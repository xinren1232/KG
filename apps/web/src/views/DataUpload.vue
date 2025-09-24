<template>
  <div class="data-upload">
    <el-card class="header-card">
      <div class="page-header">
        <h2>📤 数据导入</h2>
        <p>上传Excel文件，自动抽取数据并构建知识图谱</p>
      </div>
    </el-card>

    <!-- 上传区域 -->
    <el-card class="upload-card">
      <template #header>
        <span>文件上传</span>
      </template>

      <el-upload
        ref="uploadRef"
        class="upload-demo"
        drag
        :action="uploadUrl"
        :headers="uploadHeaders"
        :on-preview="handlePreview"
        :on-remove="handleRemove"
        :on-success="handleSuccess"
        :on-error="handleError"
        :before-upload="beforeUpload"
        :file-list="fileList"
        accept=".xlsx,.xls,.csv"
        multiple
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          将文件拖到此处，或<em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            支持 .xlsx/.xls/.csv 格式，单个文件不超过 10MB
          </div>
        </template>
      </el-upload>
    </el-card>

    <!-- 处理进度 -->
    <el-card v-if="processing" class="progress-card">
      <template #header>
        <span>处理进度</span>
      </template>
      
      <div class="progress-content">
        <el-steps :active="currentStep" finish-status="success">
          <el-step title="文件解析" description="解析Excel文件结构"></el-step>
          <el-step title="智能抽取" description="抽取实体和关系"></el-step>
          <el-step title="数据标准化" description="标准化字段和格式"></el-step>
          <el-step title="图谱构建" description="构建知识图谱"></el-step>
          <el-step title="完成" description="数据导入完成"></el-step>
        </el-steps>

        <div class="progress-details">
          <el-progress 
            :percentage="progressPercentage" 
            :status="progressStatus"
            :stroke-width="8"
          />
          <p class="progress-text">{{ progressText }}</p>
        </div>
      </div>
    </el-card>

    <!-- 处理结果 -->
    <el-card v-if="results.length > 0" class="results-card">
      <template #header>
        <div class="results-header">
          <span>处理结果</span>
          <el-button type="primary" @click="viewKnowledgeGraph">
            查看知识图谱
          </el-button>
        </div>
      </template>

      <el-table :data="results" stripe style="width: 100%">
        <el-table-column prop="fileName" label="文件名" width="200" />
        <el-table-column prop="fileType" label="文件类型" width="120">
          <template #default="{ row }">
            <el-tag :type="getFileTypeColor(row.fileType)">
              {{ getFileTypeLabel(row.fileType) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="nodeCount" label="节点数" width="100" />
        <el-table-column prop="relationCount" label="关系数" width="100" />
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="row.status === 'success' ? 'success' : 'danger'">
              {{ row.status === 'success' ? '成功' : '失败' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="processedAt" label="处理时间" />
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button size="small" @click="viewDetails(row)">详情</el-button>
            <el-button size="small" type="danger" @click="deleteResult(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 统计信息 -->
    <el-row :gutter="20" class="stats-section" v-if="stats.totalFiles > 0">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">{{ stats.totalFiles }}</div>
            <div class="stat-label">处理文件</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">{{ stats.totalNodes }}</div>
            <div class="stat-label">总节点数</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">{{ stats.totalRelations }}</div>
            <div class="stat-label">总关系数</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">{{ stats.successRate }}%</div>
            <div class="stat-label">成功率</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, reactive, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { UploadFilled } from '@element-plus/icons-vue'

export default {
  name: 'DataUpload',
  components: {
    UploadFilled
  },
  setup() {
    const uploadRef = ref(null)
    const fileList = ref([])
    const processing = ref(false)
    const currentStep = ref(0)
    const progressPercentage = ref(0)
    const progressStatus = ref('')
    const progressText = ref('')
    
    const results = ref([
      // 示例数据
      {
        fileName: '来料问题先后版.xlsx',
        fileType: 'anomaly_data',
        nodeCount: 156,
        relationCount: 234,
        status: 'success',
        processedAt: '2024-12-07 10:30:00'
      },
      {
        fileName: '相关测试用例.xlsx',
        fileType: 'testcase_data',
        nodeCount: 45,
        relationCount: 67,
        status: 'success',
        processedAt: '2024-12-07 10:32:00'
      }
    ])

    const stats = computed(() => {
      const totalFiles = results.value.length
      const successFiles = results.value.filter(r => r.status === 'success').length
      const totalNodes = results.value.reduce((sum, r) => sum + r.nodeCount, 0)
      const totalRelations = results.value.reduce((sum, r) => sum + r.relationCount, 0)
      const successRate = totalFiles > 0 ? Math.round((successFiles / totalFiles) * 100) : 0

      return {
        totalFiles,
        totalNodes,
        totalRelations,
        successRate
      }
    })

    const uploadUrl = '/api/upload'
    const uploadHeaders = {
      'Authorization': 'Bearer token'
    }

    const beforeUpload = (file) => {
      const isValidType = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                          'application/vnd.ms-excel',
                          'text/csv'].includes(file.type)
      const isLt10M = file.size / 1024 / 1024 < 10

      if (!isValidType) {
        ElMessage.error('只能上传 Excel 或 CSV 文件!')
        return false
      }
      if (!isLt10M) {
        ElMessage.error('文件大小不能超过 10MB!')
        return false
      }
      return true
    }

    const handlePreview = (file) => {
      console.log('预览文件:', file)
    }

    const handleRemove = (file) => {
      console.log('移除文件:', file)
    }

    const handleSuccess = (response, file) => {
      ElMessage.success('文件上传成功!')
      
      // 模拟处理流程
      simulateProcessing(file)
    }

    const handleError = (error, file) => {
      ElMessage.error('文件上传失败!')
      console.error('上传错误:', error)
    }

    const simulateProcessing = async (file) => {
      processing.value = true
      currentStep.value = 0
      progressPercentage.value = 0
      progressStatus.value = ''

      const steps = [
        { step: 0, text: '正在解析文件结构...', duration: 1000 },
        { step: 1, text: '正在抽取实体和关系...', duration: 2000 },
        { step: 2, text: '正在标准化数据...', duration: 1500 },
        { step: 3, text: '正在构建知识图谱...', duration: 2000 },
        { step: 4, text: '处理完成!', duration: 500 }
      ]

      for (let i = 0; i < steps.length; i++) {
        const stepInfo = steps[i]
        currentStep.value = stepInfo.step
        progressText.value = stepInfo.text
        progressPercentage.value = ((i + 1) / steps.length) * 100

        if (i === steps.length - 1) {
          progressStatus.value = 'success'
        }

        await new Promise(resolve => setTimeout(resolve, stepInfo.duration))
      }

      // 添加处理结果
      results.value.unshift({
        fileName: file.name,
        fileType: 'generic_data',
        nodeCount: Math.floor(Math.random() * 100) + 50,
        relationCount: Math.floor(Math.random() * 150) + 80,
        status: 'success',
        processedAt: new Date().toLocaleString()
      })

      setTimeout(() => {
        processing.value = false
        ElMessage.success('数据处理完成!')
      }, 1000)
    }

    const getFileTypeColor = (type) => {
      const colorMap = {
        'anomaly_data': 'danger',
        'testcase_data': 'primary',
        'supplier_data': 'warning',
        'generic_data': 'info'
      }
      return colorMap[type] || 'info'
    }

    const getFileTypeLabel = (type) => {
      const labelMap = {
        'anomaly_data': '异常数据',
        'testcase_data': '测试用例',
        'supplier_data': '供应商数据',
        'generic_data': '通用数据'
      }
      return labelMap[type] || '未知类型'
    }

    const viewDetails = (row) => {
      console.log('查看详情:', row)
      ElMessage.info('详情功能开发中...')
    }

    const deleteResult = (row) => {
      const index = results.value.indexOf(row)
      if (index > -1) {
        results.value.splice(index, 1)
        ElMessage.success('删除成功!')
      }
    }

    const viewKnowledgeGraph = () => {
      // 跳转到图谱探索页面
      window.location.href = '#/graph'
    }

    return {
      uploadRef,
      fileList,
      processing,
      currentStep,
      progressPercentage,
      progressStatus,
      progressText,
      results,
      stats,
      uploadUrl,
      uploadHeaders,
      beforeUpload,
      handlePreview,
      handleRemove,
      handleSuccess,
      handleError,
      getFileTypeColor,
      getFileTypeLabel,
      viewDetails,
      deleteResult,
      viewKnowledgeGraph
    }
  }
}
</script>

<style scoped>
.data-upload {
  padding: 20px;
}

.header-card, .upload-card, .progress-card, .results-card {
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0 0 10px 0;
  color: #303133;
}

.page-header p {
  margin: 0;
  color: #606266;
}

.upload-demo {
  width: 100%;
}

.progress-content {
  padding: 20px 0;
}

.progress-details {
  margin-top: 30px;
  text-align: center;
}

.progress-text {
  margin-top: 10px;
  color: #606266;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stats-section {
  margin-top: 20px;
}

.stat-card {
  text-align: center;
}

.stat-content {
  padding: 20px;
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #606266;
}

@media (max-width: 768px) {
  .results-header {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }
  
  .stats-section .el-col {
    margin-bottom: 15px;
  }
}
</style>
