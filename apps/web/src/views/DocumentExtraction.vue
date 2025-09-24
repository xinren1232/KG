<template>
  <div class="document-extraction">
    <el-card class="header-card">
      <div class="page-header">
        <h2>📄 文档解析</h2>
        <p>上传文档并进行智能知识抽取，支持Excel、PDF、Word等多种格式</p>
      </div>
    </el-card>

    <!-- 文件上传区域 -->
    <el-card class="upload-card">
      <h3>📤 文档上传</h3>
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
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          将文件拖到此处，或<em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            支持 Excel(.xlsx/.xls)、PDF、Word(.docx/.doc)、CSV、TXT 格式，单个文件不超过10MB
          </div>
        </template>
      </el-upload>
    </el-card>

    <!-- 已上传文件列表 -->
    <el-card v-if="uploadedFiles.length > 0" class="files-card">
      <h3>📋 已上传文件</h3>
      <el-table :data="uploadedFiles" stripe style="width: 100%">
        <el-table-column prop="filename" label="文件名" min-width="200" />
        <el-table-column prop="file_type" label="类型" width="120" />
        <el-table-column prop="size" label="大小" width="100">
          <template #default="{ row }">
            {{ formatFileSize(row.size) }}
          </template>
        </el-table-column>
        <el-table-column prop="upload_time" label="上传时间" width="180">
          <template #default="{ row }">
            {{ formatTime(row.upload_time) }}
          </template>
        </el-table-column>
        <el-table-column label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button 
              size="small" 
              type="primary" 
              @click="extractKnowledge(row)"
              :loading="row.extracting"
              :disabled="row.status === '已抽取'"
            >
              知识抽取
            </el-button>
            <el-button 
              size="small" 
              type="success" 
              @click="viewResults(row)"
              :disabled="!row.extracted_data"
            >
              查看结果
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 抽取结果展示 -->
    <el-card v-if="currentResults" class="results-card">
      <h3>🔍 抽取结果</h3>
      
      <el-tabs v-model="activeTab" type="card">
        <!-- 实体标签页 -->
        <el-tab-pane label="实体" name="entities">
          <div class="entities-section">
            <div class="section-header">
              <h4>📊 实体统计</h4>
              <el-tag type="info">共 {{ currentResults.entities.length }} 个实体</el-tag>
            </div>
            
            <el-table :data="currentResults.entities" stripe style="width: 100%">
              <el-table-column prop="name" label="实体名称" min-width="150" />
              <el-table-column prop="type" label="类型" width="120">
                <template #default="{ row }">
                  <el-tag :type="getEntityTypeColor(row.type)" size="small">
                    {{ row.type }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="属性" min-width="200">
                <template #default="{ row }">
                  <div class="properties">
                    <el-tag 
                      v-for="(value, key) in row.properties" 
                      :key="key"
                      size="small"
                      class="property-tag"
                    >
                      {{ key }}: {{ value }}
                    </el-tag>
                  </div>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>

        <!-- 关系标签页 -->
        <el-tab-pane label="关系" name="relations">
          <div class="relations-section">
            <div class="section-header">
              <h4>🔗 关系统计</h4>
              <el-tag type="info">共 {{ currentResults.relations.length }} 个关系</el-tag>
            </div>
            
            <el-table :data="currentResults.relations" stripe style="width: 100%">
              <el-table-column prop="source" label="源实体" width="150" />
              <el-table-column prop="type" label="关系类型" width="150">
                <template #default="{ row }">
                  <el-tag type="warning" size="small">
                    {{ row.type }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="target" label="目标实体" width="150" />
              <el-table-column label="属性" min-width="200">
                <template #default="{ row }">
                  <div class="properties">
                    <el-tag 
                      v-for="(value, key) in row.properties" 
                      :key="key"
                      size="small"
                      class="property-tag"
                    >
                      {{ key }}: {{ value }}
                    </el-tag>
                  </div>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>

        <!-- 元数据标签页 -->
        <el-tab-pane label="元数据" name="metadata">
          <div class="metadata-section">
            <el-descriptions :column="2" border>
              <el-descriptions-item label="抽取类型">
                {{ currentResults.metadata.extraction_type }}
              </el-descriptions-item>
              <el-descriptions-item label="实体数量">
                {{ currentResults.metadata.entity_count }}
              </el-descriptions-item>
              <el-descriptions-item label="关系数量">
                {{ currentResults.metadata.relation_count }}
              </el-descriptions-item>
              <el-descriptions-item label="源文件">
                {{ currentResults.metadata.source_file }}
              </el-descriptions-item>
            </el-descriptions>
          </div>
        </el-tab-pane>
      </el-tabs>

      <!-- 操作按钮 -->
      <div class="actions">
        <el-button type="primary" @click="buildGraph">
          构建知识图谱
        </el-button>
        <el-button @click="exportResults">
          导出结果
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { UploadFilled } from '@element-plus/icons-vue'

export default {
  name: 'DocumentExtraction',
  components: {
    UploadFilled
  },
  setup() {
    const uploadUrl = 'http://127.0.0.1:8000/kg/upload'
    const uploadedFiles = ref([])
    const currentResults = ref(null)
    const activeTab = ref('entities')

    const handleUploadSuccess = (response, file) => {
      if (response.success) {
        uploadedFiles.value.push({
          file_id: response.file_id,
          filename: response.filename,
          file_type: response.file_type,
          size: response.size,
          upload_time: new Date().toISOString(),
          status: '已上传',
          extracting: false,
          extracted_data: null
        })
        ElMessage.success('文件上传成功')
      } else {
        ElMessage.error(`上传失败: ${response.message}`)
      }
    }

    const handleUploadError = (error) => {
      ElMessage.error('文件上传失败')
      console.error('Upload error:', error)
    }

    const beforeUpload = (file) => {
      const isValidType = /\.(xlsx?|pdf|docx?|csv|txt)$/i.test(file.name)
      const isValidSize = file.size / 1024 / 1024 < 10

      if (!isValidType) {
        ElMessage.error('文件格式不支持')
        return false
      }
      if (!isValidSize) {
        ElMessage.error('文件大小不能超过10MB')
        return false
      }
      return true
    }

    const extractKnowledge = async (file) => {
      file.extracting = true
      
      try {
        const response = await fetch('http://127.0.0.1:8000/kg/extract', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            file_id: file.file_id,
            extraction_type: 'auto'
          })
        })

        const result = await response.json()
        
        if (result.success) {
          file.status = '已抽取'
          file.extracted_data = result
          ElMessage.success('知识抽取完成')
        } else {
          ElMessage.error('知识抽取失败')
        }
      } catch (error) {
        ElMessage.error('知识抽取失败')
        console.error('Extraction error:', error)
      } finally {
        file.extracting = false
      }
    }

    const viewResults = (file) => {
      if (file.extracted_data) {
        currentResults.value = file.extracted_data
        activeTab.value = 'entities'
      }
    }

    const buildGraph = async () => {
      if (!currentResults.value) return

      try {
        const response = await fetch('http://127.0.0.1:8000/kg/build', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            entities: currentResults.value.entities,
            relations: currentResults.value.relations,
            merge_strategy: 'auto'
          })
        })

        const result = await response.json()
        
        if (result.success) {
          ElMessage.success(`图谱构建成功！创建 ${result.nodes_created} 个节点，${result.relations_created} 个关系`)
        } else {
          ElMessage.error('图谱构建失败')
        }
      } catch (error) {
        ElMessage.error('图谱构建失败')
        console.error('Build error:', error)
      }
    }

    const exportResults = () => {
      if (!currentResults.value) return
      
      const dataStr = JSON.stringify(currentResults.value, null, 2)
      const dataBlob = new Blob([dataStr], { type: 'application/json' })
      const url = URL.createObjectURL(dataBlob)
      const link = document.createElement('a')
      link.href = url
      link.download = `extraction_results_${Date.now()}.json`
      link.click()
      URL.revokeObjectURL(url)
    }

    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 B'
      const k = 1024
      const sizes = ['B', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }

    const formatTime = (timeStr) => {
      return new Date(timeStr).toLocaleString()
    }

    const getStatusType = (status) => {
      const types = {
        '已上传': 'info',
        '已抽取': 'success',
        '抽取中': 'warning',
        '失败': 'danger'
      }
      return types[status] || 'info'
    }

    const getEntityTypeColor = (type) => {
      const colors = {
        'Material': 'primary',
        'Anomaly': 'danger',
        'Symptom': 'warning',
        'RootCause': 'info',
        'Countermeasure': 'success'
      }
      return colors[type] || 'default'
    }

    return {
      uploadUrl,
      uploadedFiles,
      currentResults,
      activeTab,
      handleUploadSuccess,
      handleUploadError,
      beforeUpload,
      extractKnowledge,
      viewResults,
      buildGraph,
      exportResults,
      formatFileSize,
      formatTime,
      getStatusType,
      getEntityTypeColor
    }
  }
}
</script>

<style scoped>
.document-extraction {
  padding: 20px;
}

.header-card {
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

.upload-card, .files-card, .results-card {
  margin-bottom: 20px;
}

.upload-dragger {
  width: 100%;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.section-header h4 {
  margin: 0;
}

.properties {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.property-tag {
  margin: 2px;
}

.actions {
  margin-top: 20px;
  text-align: center;
}

.actions .el-button {
  margin: 0 10px;
}
</style>
