<template>
  <div class="file-upload">
    <el-card class="upload-card">
      <template #header>
        <div class="card-header">
          <span>📁 文件上传与数据抽取</span>
          <el-button type="primary" @click="refreshFileList" :loading="loading">
            刷新列表
          </el-button>
        </div>
      </template>

      <!-- 文件上传区域 -->
      <div class="upload-section">
        <el-upload
          ref="uploadRef"
          class="upload-dragger"
          drag
          :action="uploadUrl"
          :on-success="handleUploadSuccess"
          :on-error="handleUploadError"
          :before-upload="beforeUpload"
          :show-file-list="false"
          multiple
        >
          <el-icon class="el-icon--upload"><Upload /></el-icon>
          <div class="el-upload__text">
            将文件拖到此处，或<em>点击上传</em>
          </div>
          <template #tip>
            <div class="el-upload__tip">
              支持 Excel (.xlsx, .xls)、CSV、PDF、Word (.docx)、文本 (.txt) 格式
            </div>
          </template>
        </el-upload>
      </div>
    </el-card>

    <!-- 文件列表 -->
    <el-card class="file-list-card">
      <template #header>
        <span>📋 已上传文件列表</span>
      </template>

      <el-table :data="fileList" v-loading="loading" style="width: 100%">
        <el-table-column prop="filename" label="文件名" min-width="200">
          <template #default="scope">
            <el-icon style="margin-right: 8px">
              <Document v-if="scope.row.extension === '.pdf'" />
              <List v-else-if="['.xlsx', '.xls', '.csv'].includes(scope.row.extension)" />
              <Document v-else />
            </el-icon>
            {{ scope.row.filename }}
          </template>
        </el-table-column>
        
        <el-table-column prop="size" label="文件大小" width="120">
          <template #default="scope">
            {{ formatFileSize(scope.row.size) }}
          </template>
        </el-table-column>
        
        <el-table-column prop="modified" label="上传时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.modified) }}
          </template>
        </el-table-column>
        
        <el-table-column prop="extension" label="类型" width="80">
          <template #default="scope">
            <el-tag :type="getFileTypeColor(scope.row.extension)">
              {{ scope.row.extension }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="300">
          <template #default="scope">
            <el-button 
              type="primary" 
              size="small" 
              @click="extractFile(scope.row.filename)"
              :loading="extractingFiles.has(scope.row.filename)"
            >
              数据抽取
            </el-button>
            <el-button 
              type="success" 
              size="small" 
              @click="buildGraph(scope.row.filename)"
              :loading="buildingFiles.has(scope.row.filename)"
            >
              构建图谱
            </el-button>
            <el-button 
              type="info" 
              size="small" 
              @click="viewExtractionResult(scope.row.filename)"
            >
              查看结果
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 抽取结果对话框 -->
    <el-dialog 
      v-model="resultDialogVisible" 
      title="数据抽取结果" 
      width="80%"
      :close-on-click-modal="false"
    >
      <div v-if="currentResult">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="文件路径">
            {{ currentResult.file_path }}
          </el-descriptions-item>
          <el-descriptions-item label="文件类型">
            <el-tag>{{ currentResult.file_type }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="实体数量">
            <el-tag type="success">{{ currentResult.entities_count }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="关系数量">
            <el-tag type="warning">{{ currentResult.relations_count }}</el-tag>
          </el-descriptions-item>
        </el-descriptions>

        <el-divider>文件元数据</el-divider>
        <el-descriptions :column="1" border>
          <el-descriptions-item 
            v-for="(value, key) in currentResult.metadata" 
            :key="key" 
            :label="key"
          >
            {{ formatMetadataValue(value) }}
          </el-descriptions-item>
        </el-descriptions>

        <el-divider v-if="currentResult.errors.length > 0">处理错误</el-divider>
        <el-alert
          v-for="(error, index) in currentResult.errors"
          :key="index"
          :title="error"
          type="error"
          style="margin-bottom: 10px"
        />
      </div>
    </el-dialog>

    <!-- 图谱构建结果对话框 -->
    <el-dialog 
      v-model="buildResultDialogVisible" 
      title="知识图谱构建结果" 
      width="60%"
    >
      <div v-if="currentBuildResult">
        <el-result
          :icon="currentBuildResult.processing_errors.length > 0 ? 'warning' : 'success'"
          :title="currentBuildResult.processing_errors.length > 0 ? '构建完成（有警告）' : '构建成功'"
        >
          <template #sub-title>
            <p>源文件: {{ currentBuildResult.source_file }}</p>
            <p>创建节点: {{ currentBuildResult.created_nodes }} 个</p>
            <p>创建关系: {{ currentBuildResult.created_relationships }} 个</p>
          </template>
          
          <template #extra>
            <el-button type="primary" @click="$router.push('/graph')">
              查看图谱
            </el-button>
            <el-button @click="buildResultDialogVisible = false">
              关闭
            </el-button>
          </template>
        </el-result>

        <el-divider v-if="currentBuildResult.processing_errors.length > 0">处理警告</el-divider>
        <el-alert
          v-for="(error, index) in currentBuildResult.processing_errors"
          :key="index"
          :title="error"
          type="warning"
          style="margin-bottom: 10px"
        />
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Upload, Document, List } from '@element-plus/icons-vue'
import { kgApi } from '../api'

export default {
  name: 'FileUpload',
  components: {
    Upload,
    Document,
    List
  },
  setup() {
    const uploadUrl = ref('http://localhost:8000/kg/upload')
    const fileList = ref([])
    const loading = ref(false)
    const extractingFiles = ref(new Set())
    const buildingFiles = ref(new Set())
    
    const resultDialogVisible = ref(false)
    const currentResult = ref(null)
    
    const buildResultDialogVisible = ref(false)
    const currentBuildResult = ref(null)

    // 获取文件列表
    const refreshFileList = async () => {
      loading.value = true
      try {
        const response = await kgApi.getFiles()
        fileList.value = response.files || []
      } catch (error) {
        ElMessage.error('获取文件列表失败: ' + error.message)
      } finally {
        loading.value = false
      }
    }

    // 文件上传前检查
    const beforeUpload = (file) => {
      const supportedTypes = ['.xlsx', '.xls', '.csv', '.pdf', '.docx', '.txt']
      const fileExt = '.' + file.name.split('.').pop().toLowerCase()
      
      if (!supportedTypes.includes(fileExt)) {
        ElMessage.error(`不支持的文件格式: ${fileExt}`)
        return false
      }
      
      const maxSize = 50 * 1024 * 1024 // 50MB
      if (file.size > maxSize) {
        ElMessage.error('文件大小不能超过 50MB')
        return false
      }
      
      return true
    }

    // 文件上传成功
    const handleUploadSuccess = (response, file) => {
      ElMessage.success(`文件 ${file.name} 上传成功`)
      refreshFileList()
    }

    // 文件上传失败
    const handleUploadError = (error, file) => {
      ElMessage.error(`文件 ${file.name} 上传失败: ${error.message}`)
    }

    // 数据抽取
    const extractFile = async (filename) => {
      extractingFiles.value.add(filename)
      try {
        const response = await kgApi.extractFile(filename)
        currentResult.value = response
        resultDialogVisible.value = true
        ElMessage.success('数据抽取完成')
      } catch (error) {
        ElMessage.error('数据抽取失败: ' + error.message)
      } finally {
        extractingFiles.value.delete(filename)
      }
    }

    // 构建知识图谱
    const buildGraph = async (filename) => {
      buildingFiles.value.add(filename)
      try {
        const response = await kgApi.buildGraph(filename)
        currentBuildResult.value = response
        buildResultDialogVisible.value = true
        ElMessage.success('知识图谱构建完成')
      } catch (error) {
        ElMessage.error('知识图谱构建失败: ' + error.message)
      } finally {
        buildingFiles.value.delete(filename)
      }
    }

    // 查看抽取结果
    const viewExtractionResult = async (filename) => {
      try {
        const response = await kgApi.extractFile(filename)
        currentResult.value = response
        resultDialogVisible.value = true
      } catch (error) {
        ElMessage.error('获取抽取结果失败: ' + error.message)
      }
    }

    // 格式化文件大小
    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 B'
      const k = 1024
      const sizes = ['B', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }

    // 格式化日期
    const formatDate = (timestamp) => {
      return new Date(timestamp * 1000).toLocaleString()
    }

    // 获取文件类型颜色
    const getFileTypeColor = (extension) => {
      const colorMap = {
        '.xlsx': 'success',
        '.xls': 'success',
        '.csv': 'warning',
        '.pdf': 'danger',
        '.docx': 'info',
        '.txt': ''
      }
      return colorMap[extension] || ''
    }

    // 格式化元数据值
    const formatMetadataValue = (value) => {
      if (Array.isArray(value)) {
        return value.join(', ')
      }
      if (typeof value === 'object') {
        return JSON.stringify(value, null, 2)
      }
      return String(value)
    }

    onMounted(() => {
      refreshFileList()
    })

    return {
      uploadUrl,
      fileList,
      loading,
      extractingFiles,
      buildingFiles,
      resultDialogVisible,
      currentResult,
      buildResultDialogVisible,
      currentBuildResult,
      refreshFileList,
      beforeUpload,
      handleUploadSuccess,
      handleUploadError,
      extractFile,
      buildGraph,
      viewExtractionResult,
      formatFileSize,
      formatDate,
      getFileTypeColor,
      formatMetadataValue
    }
  }
}
</script>

<style scoped>
.file-upload {
  padding: 20px;
}

.upload-card, .file-list-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.upload-section {
  margin-bottom: 20px;
}

.upload-dragger {
  width: 100%;
}

.el-upload-dragger {
  width: 100%;
  height: 180px;
}

.el-icon--upload {
  font-size: 67px;
  color: #C0C4CC;
  margin: 40px 0 16px;
  line-height: 50px;
}

.el-upload__text {
  color: #606266;
  font-size: 14px;
  text-align: center;
}

.el-upload__text em {
  color: #409EFF;
  font-style: normal;
}

.el-upload__tip {
  font-size: 12px;
  color: #606266;
  margin-top: 7px;
}
</style>
