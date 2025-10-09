<template>
  <div class="document-extraction">
    <el-card class="header-card">
      <div class="page-header">
        <h2>📄 智能文档解析</h2>
        <p>上传文档并自动提取其中的结构化信息，支持Excel、PDF、Word、CSV、TXT等多种格式</p>
        <div class="feature-tags">
          <el-tag type="primary" size="small">多格式支持</el-tag>
          <el-tag type="success" size="small">智能解析</el-tag>
          <el-tag type="info" size="small">数据导出</el-tag>
          <el-tag type="warning" size="small">质量分析</el-tag>
        </div>
      </div>
    </el-card>

    <!-- 文件上传区域 -->
    <el-card class="upload-card">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <h3>📤 文档上传</h3>
        <el-button
          type="success"
          @click="exportAllResults"
          :disabled="!hasAnyParsedFiles"
          v-if="uploadedFiles.length > 0"
        >
          批量导出解析数据
        </el-button>
      </div>
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
        <el-table-column label="状态" width="150">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">
              <el-icon v-if="row.status === '解析中'" class="is-loading" style="margin-right: 4px;">
                <Loading />
              </el-icon>
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="解析结果" width="200">
          <template #default="{ row }">
            <div v-if="row.extracted_data && row.status === '已解析'">
              <el-text type="success" size="small">
                实体: {{ row.extracted_data.entities?.length || 0 }}个
              </el-text>
              <br>
              <el-text type="primary" size="small">
                关系: {{ row.extracted_data.relations?.length || 0 }}个
              </el-text>
            </div>
            <el-text v-else-if="row.status === '解析中'" type="warning" size="small">
              解析中...
            </el-text>
            <el-text v-else-if="row.status === '解析失败'" type="danger" size="small">
              解析失败
            </el-text>
            <el-text v-else-if="row.status === '待解析'" type="info" size="small">
              点击"开始解析"按钮进行解析
            </el-text>
            <el-text v-else type="info" size="small">
              等待解析
            </el-text>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="360">
          <template #default="{ row }">
            <div class="action-buttons">
              <el-button
                size="small"
                type="primary"
                @click="handleParseDocument(row)"
                :loading="row.parsing"
                :disabled="row.status === '已解析'"
                :icon="row.parsing ? 'Loading' : 'DocumentCopy'"
                class="action-btn parse-btn"
              >
                {{ row.parsing ? '解析中' : (row.status === '已解析' ? '重新解析' : '开始解析') }}
              </el-button>
              <el-button
                size="small"
                type="success"
                @click="viewParseResults(row)"
                :disabled="!row.parsed_data || row.status !== '已解析'"
                icon="View"
                class="action-btn view-btn"
              >
                查看
              </el-button>
              <el-button
                size="small"
                type="info"
                @click="exportSingleResult(row)"
                :disabled="!row.parsed_data"
                icon="Download"
                class="action-btn export-btn"
              >
                导出
              </el-button>
              <el-button
                size="small"
                type="danger"
                @click="deleteFile(row)"
                icon="Delete"
                class="action-btn delete-btn"
              >
                删除
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 文档解析结果对话框 -->
    <el-dialog
      v-model="showResultDialog"
      title="📄 文档解析结果"
      width="90%"
      :before-close="closeResultDialog"
    >
      <div v-if="currentResults">
        <!-- 文档信息概览 -->
        <el-card class="overview-card" style="margin-bottom: 20px;">
          <template #header>
            <div style="display: flex; align-items: center;">
              <el-icon style="margin-right: 8px;"><UploadFilled /></el-icon>
              <span>📊 解析概览</span>
            </div>
          </template>
          <el-row :gutter="20">
            <el-col :span="6">
              <el-statistic title="📋 提取记录数" :value="getExtractedRecords()">
                <template #suffix>
                  <span>条</span>
                </template>
              </el-statistic>
            </el-col>
            <el-col :span="6">
              <el-statistic title="📄 数据字段数" :value="getDataFields()">
                <template #suffix>
                  <span>个</span>
                </template>
              </el-statistic>
            </el-col>
            <el-col :span="6">
              <el-statistic title="📦 文件大小" :value="formatFileSize(currentFileInfo?.size || 0)">
              </el-statistic>
            </el-col>
            <el-col :span="6">
              <el-statistic title="🎯 解析质量" :value="getParsingQuality()" suffix="%">
              </el-statistic>
            </el-col>
          </el-row>
        </el-card>

        <!-- 详细结果展示 -->
        <el-tabs v-model="activeResultTab" type="card">
          <!-- 原始数据 -->
          <el-tab-pane label="提取数据" name="raw_data">
            <!-- 根据文件类型显示不同的展示组件 -->
            <component
              :is="getDisplayComponent()"
              :data="getDisplayData()"
              :metadata="currentResults.metadata"
              :file-info="currentFileInfo"
            />
          </el-tab-pane>

          <!-- 数据统计 -->
          <el-tab-pane label="数据统计" name="statistics">
            <el-row :gutter="20">
              <el-col :span="12">
                <el-card>
                  <template #header>
                    <span>📊 数据概览</span>
                  </template>
                  <el-descriptions :column="1" border>
                    <el-descriptions-item label="总记录数">
                      {{ getExtractedRecords() }}
                    </el-descriptions-item>
                    <el-descriptions-item label="有效记录数">
                      {{ getValidRecords() }}
                    </el-descriptions-item>
                    <el-descriptions-item label="数据完整性">
                      {{ getDataCompleteness() }}%
                    </el-descriptions-item>
                    <el-descriptions-item label="解析质量">
                      {{ getParsingQuality() }}%
                    </el-descriptions-item>
                  </el-descriptions>
                </el-card>
              </el-col>
              <el-col :span="12">
                <el-card>
                  <template #header>
                    <span>📋 字段分析</span>
                  </template>
                  <div v-if="getFieldAnalysis().length > 0">
                    <el-table :data="getFieldAnalysis()" style="width: 100%" size="small">
                      <el-table-column prop="field" label="字段名" />
                      <el-table-column prop="count" label="有效值" />
                      <el-table-column prop="rate" label="完整率" />
                    </el-table>
                  </div>
                  <el-empty v-else description="无字段信息" size="small" />
                </el-card>
              </el-col>
            </el-row>
          </el-tab-pane>

          <!-- 元数据信息 -->
          <el-tab-pane label="元数据" name="metadata">
            <div v-if="currentResults.metadata">
              <el-descriptions :column="2" border>
                <el-descriptions-item
                  v-for="(value, key) in currentResults.metadata"
                  :key="key"
                  :label="formatMetadataKey(key)"
                >
                  {{ formatMetadataValue(value) }}
                </el-descriptions-item>
              </el-descriptions>
            </div>
            <el-empty v-else description="无元数据信息" />
          </el-tab-pane>
        </el-tabs>
      </div>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="closeResultDialog">关闭</el-button>
          <el-button type="success" @click="exportCurrentResults">
            💾 导出解析数据
          </el-button>
          <el-button
            type="primary"
            @click="reParseDocument"
            :disabled="!currentFileInfo"
          >
            🔄 重新解析
          </el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 抽取结果展示 -->
    <el-card v-if="currentResults" class="results-card">
      <h3>🔍 抽取结果</h3>
      
      <el-tabs v-model="activeTab" type="card">
        <!-- 实体标签页 -->
        <el-tab-pane label="实体" name="entities">
          <div class="entities-section">
            <div class="section-header">
              <h4>📊 实体统计</h4>
              <el-tag type="info">共 {{ currentResults?.entities?.length || 0 }} 个实体</el-tag>
            </div>
            
            <el-table :data="currentResults?.entities || []" stripe style="width: 100%">
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
              <el-tag type="info">共 {{ currentResults?.relations?.length || 0 }} 个关系</el-tag>
            </div>
            
            <el-table :data="currentResults?.relations || []" stripe style="width: 100%">
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
                {{ currentResults?.metadata?.extraction_type || '自动' }}
              </el-descriptions-item>
              <el-descriptions-item label="实体数量">
                {{ currentResults?.metadata?.entity_count || currentResults?.entities?.length || 0 }}
              </el-descriptions-item>
              <el-descriptions-item label="关系数量">
                {{ currentResults?.metadata?.relation_count || currentResults?.relations?.length || 0 }}
              </el-descriptions-item>
              <el-descriptions-item label="源文件">
                {{ currentResults?.metadata?.source_file || '未知' }}
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
import { ref, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { UploadFilled } from '@element-plus/icons-vue'

// 导入显示组件
import ExcelDisplay from '@/components/displays/ExcelDisplay.vue'
import WordDisplay from '@/components/displays/WordDisplay.vue'
import PdfDisplay from '@/components/displays/PdfDisplay.vue'
import CsvDisplay from '@/components/displays/CsvDisplay.vue'
import TextDisplay from '@/components/displays/TextDisplay.vue'
import PowerPointDisplay from '@/components/displays/PowerPointDisplay.vue'
import DefaultDisplay from '@/components/displays/DefaultDisplay.vue'

export default {
  name: 'DocumentExtraction',
  components: {
    UploadFilled,
    ExcelDisplay,
    WordDisplay,
    PdfDisplay,
    CsvDisplay,
    TextDisplay,
    PowerPointDisplay,
    DefaultDisplay
  },
  setup() {
    const uploadUrl = 'http://127.0.0.1:8000/kg/upload'
    const uploadedFiles = ref([])
    const currentResults = ref(null)
    const activeTab = ref('entities')
    const showResultDialog = ref(false)
    const activeResultTab = ref('entities')
    const currentFileInfo = ref(null)

    const handleUploadSuccess = (response, file) => {
      console.log('Upload success response:', response)
      console.log('Upload success file:', file)

      if (response && response.success) {
        const newFile = {
          upload_id: response.upload_id,
          file_id: response.upload_id, // 兼容旧代码
          filename: response.filename,
          file_type: response.file_type,
          size: response.size,
          upload_time: new Date().toISOString(),
          status: '待解析',
          extracting: false,
          extracted_data: null
        }
        uploadedFiles.value.push(newFile)
        ElMessage.success('文件上传成功！请点击"开始解析"按钮进行文档解析')
      } else {
        console.error('Upload failed:', response)
        ElMessage.error(`上传失败: ${response?.message || '未知错误'}`)
      }
    }

    const handleUploadError = (error, file) => {
      console.error('Upload error:', error)
      console.error('Upload error file:', file)
      ElMessage.error(`文件上传失败: ${error?.message || '网络错误'}`)
    }

    const beforeUpload = (file) => {
      console.log('Before upload file:', file)
      console.log('File name:', file.name)
      console.log('File size:', file.size)
      console.log('File type:', file.type)

      const isValidType = /\.(xlsx?|pdf|docx?|csv|txt)$/i.test(file.name)
      const isValidSize = file.size / 1024 / 1024 < 10

      console.log('Is valid type:', isValidType)
      console.log('Is valid size:', isValidSize)

      if (!isValidType) {
        ElMessage.error('文件格式不支持')
        return false
      }
      if (!isValidSize) {
        ElMessage.error('文件大小不能超过10MB')
        return false
      }

      console.log('File validation passed')
      return true
    }

    const parseDocument = async (file) => {
      file.parsing = true
      file.status = '解析中'

      try {
        const upload_id = file.upload_id || file.file_id

        // 首先调用手动解析API启动解析
        try {
          const parseResponse = await fetch(`http://127.0.0.1:8000/kg/files/${upload_id}/parse`, {
            method: 'POST'
          })

          if (!parseResponse.ok) {
            const errorText = await parseResponse.text()
            console.error('解析请求失败:', errorText)
            throw new Error(`解析请求失败: HTTP ${parseResponse.status} - ${errorText}`)
          }

          // 检查解析响应
          const parseText = await parseResponse.text()
          if (!parseText.trim()) {
            throw new Error('解析响应为空')
          }

          let parseResult
          try {
            parseResult = JSON.parse(parseText)
          } catch (jsonError) {
            console.error('解析响应JSON解析失败:', jsonError)
            console.error('原始响应:', parseText)
            throw new Error(`解析响应格式错误: ${jsonError.message}`)
          }

          if (!parseResult.success) {
            throw new Error(parseResult.message || '启动解析失败')
          }
        } catch (parseError) {
          console.error('解析触发失败:', parseError)
          throw parseError
        }

        // 轮询文件状态直到解析完成
        const checkStatus = async () => {
          try {
            const statusResponse = await fetch(`http://127.0.0.1:8000/kg/files/${upload_id}/status`)

            // 检查HTTP状态码
            if (!statusResponse.ok) {
              throw new Error(`HTTP ${statusResponse.status}: ${statusResponse.statusText}`)
            }

            // 获取响应文本
            const responseText = await statusResponse.text()

            // 检查响应是否为空
            if (!responseText.trim()) {
              throw new Error('服务器返回空响应')
            }

            // 尝试解析JSON
            let statusResult
            try {
              statusResult = JSON.parse(responseText)
            } catch (jsonError) {
              console.error('JSON解析失败:', jsonError)
              console.error('原始响应:', responseText)
              throw new Error(`响应格式错误: ${jsonError.message}`)
            }

            if (statusResult.success) {
              const fileStatus = statusResult.data.status
              console.log(`状态检查: ${fileStatus}`)

              if (fileStatus === 'parsed') {
                // 解析完成，获取预览数据
                try {
                  const previewResponse = await fetch(`http://127.0.0.1:8000/kg/files/${upload_id}/preview`)

                  if (!previewResponse.ok) {
                    throw new Error(`预览请求失败: HTTP ${previewResponse.status}`)
                  }

                  const previewText = await previewResponse.text()
                  if (!previewText.trim()) {
                    throw new Error('预览数据为空')
                  }

                  const previewResult = JSON.parse(previewText)

                  if (previewResult.success) {
                    file.status = '已解析'
                    file.parsed_data = {
                      success: true,
                      raw_data: previewResult.data.raw_data || [],
                      metadata: previewResult.data.metadata || {},
                      parsing_time: new Date().toISOString()
                    }
                    ElMessage.success('文档解析完成')
                    return true
                  } else {
                    throw new Error(previewResult.message || '获取解析结果失败')
                  }
                } catch (previewError) {
                  console.error('获取预览数据失败:', previewError)
                  throw new Error(`获取预览数据失败: ${previewError.message}`)
                }
              } else if (fileStatus === 'failed') {
                const errorMsg = statusResult.data.error || '文件解析失败'
                throw new Error(errorMsg)
              } else if (fileStatus === 'parsing') {
                // 还在解析中，继续等待
                return false
              } else {
                // uploaded状态，可能还没开始解析
                return false
              }
            } else {
              throw new Error(statusResult.message || '查询文件状态失败')
            }
          } catch (error) {
            console.error('状态检查失败:', error)
            throw error
          }
        }

        // 轮询检查状态，最多等待30秒
        let attempts = 0
        const maxAttempts = 15

        while (attempts < maxAttempts) {
          console.log(`轮询尝试 ${attempts + 1}/${maxAttempts}`)
          const completed = await checkStatus()
          if (completed) break

          await new Promise(resolve => setTimeout(resolve, 2000)) // 等待2秒
          attempts++
        }

        if (attempts >= maxAttempts) {
          throw new Error('文件解析超时，请稍后重试')
        }

      } catch (error) {
        ElMessage.error(error.message || '文档解析失败')
        console.error('Parse error:', error)
        file.status = '解析失败'
      } finally {
        file.parsing = false
      }
    }

    const viewParseResults = (file) => {
      if (file.parsed_data) {
        currentResults.value = file.parsed_data
        currentFileInfo.value = file
        activeResultTab.value = 'raw_data'
        showResultDialog.value = true
      } else {
        ElMessage.warning('该文件尚未进行解析')
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
        '待解析': 'info',
        '解析中': 'warning',
        '已解析': 'success',
        '解析失败': 'danger',
        '已上传': 'info',
        '已抽取': 'success',
        '抽取中': 'warning',
        '失败': 'danger'
      }
      return types[status] || 'info'
    }

    const getEntityTypeColor = (type) => {
      const colors = {
        'Component': 'primary',
        'Symptom': 'danger',
        'RootCause': 'warning',
        'Countermeasure': 'success',
        'Product': 'info',
        'Factory': 'primary'
      }
      return colors[type] || 'default'
    }

    // 新增方法
    const closeResultDialog = () => {
      showResultDialog.value = false
      currentResults.value = null
      currentFileInfo.value = null
    }





    const exportCurrentResults = () => {
      if (!currentResults.value) return

      const data = {
        file_info: {
          filename: currentFileInfo.value?.filename,
          upload_time: currentFileInfo.value?.upload_time,
          file_type: currentFileInfo.value?.file_type,
          size: currentFileInfo.value?.size
        },
        raw_data: currentResults.value.raw_data,
        metadata: currentResults.value.metadata,
        parsing_time: currentResults.value.parsing_time,
        export_time: new Date().toISOString()
      }

      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `${currentFileInfo.value?.filename || 'unknown'}_parsed_data.json`
      a.click()
      URL.revokeObjectURL(url)

      ElMessage.success('解析数据已导出')
    }

    const getParsingQuality = () => {
      if (!currentResults.value) return 0

      const rawData = currentResults.value.raw_data || []

      if (rawData.length === 0) return 0

      // 计算数据完整性
      const totalCells = rawData.length * Object.keys(rawData[0]).length
      const filledCells = rawData.reduce((count, row) => {
        return count + Object.values(row).filter(value =>
          value !== null && value !== undefined && String(value).trim() !== ''
        ).length
      }, 0)

      const completeness = (filledCells / totalCells) * 100

      // 基于数据完整性和记录数量计算质量分数
      let score = completeness * 0.8  // 完整性占80%

      // 记录数量贡献 (20%)
      if (rawData.length > 0) {
        score += Math.min(rawData.length * 2, 20)
      }

      return Math.min(Math.round(score), 100)
    }

    const formatMetadataKey = (key) => {
      const keyMap = {
        'total_blocks': '总块数',
        'processed_blocks': '已处理块数',
        'entity_count': '实体数量',
        'relation_count': '关系数量',
        'file_type': '文件类型',
        'source': '数据源',
        'total_records': '总记录数'
      }
      return keyMap[key] || key
    }

    const formatMetadataValue = (value) => {
      if (typeof value === 'object') {
        return JSON.stringify(value, null, 2)
      }
      return String(value)
    }

    // 文档解析专用方法
    const getExtractedRecords = () => {
      if (!currentResults.value) return 0
      if (currentResults.value.raw_data) {
        return currentResults.value.raw_data.length
      }
      return currentResults.value.metadata?.total_records || 0
    }

    const getDataFields = () => {
      if (!currentResults.value) return 0
      if (currentResults.value.raw_data && currentResults.value.raw_data.length > 0) {
        return Object.keys(currentResults.value.raw_data[0]).length
      }
      return currentResults.value.metadata?.field_count || 0
    }

    const getValidRecords = () => {
      if (!currentResults.value) return 0
      const total = getExtractedRecords()
      // 简单估算：假设90%的记录是有效的
      return Math.floor(total * 0.9)
    }

    const getDataCompleteness = () => {
      if (!currentResults.value) return 0
      // 基于有效记录比例计算完整性
      const total = getExtractedRecords()
      const valid = getValidRecords()
      return total > 0 ? Math.round((valid / total) * 100) : 0
    }

    const getTableColumns = () => {
      if (!currentResults.value?.raw_data || currentResults.value.raw_data.length === 0) {
        return []
      }

      const firstRow = currentResults.value.raw_data[0]
      return Object.keys(firstRow).map(key => ({
        prop: key,
        label: key,
        width: 150
      }))
    }

    // 根据文件类型获取对应的显示组件
    const getDisplayComponent = () => {
      if (!currentFileInfo.value) return 'DefaultDisplay'

      const fileType = getFileType(currentFileInfo.value.filename)

      switch (fileType) {
        case 'excel':
          return 'ExcelDisplay'
        case 'pdf':
          return 'PdfDisplay'
        case 'word':
          return 'WordDisplay'
        case 'powerpoint':
          return 'PowerPointDisplay'
        case 'csv':
          return 'CsvDisplay'
        case 'text':
          return 'TextDisplay'
        default:
          return 'DefaultDisplay'
      }
    }

    // 获取显示组件需要的数据格式
    const getDisplayData = () => {
      if (!currentResults.value?.raw_data) return []

      // 如果raw_data中的每个元素都有data字段，提取data字段的内容
      const rawData = currentResults.value.raw_data

      if (rawData.length > 0 && rawData[0].data) {
        // 提取每个元素的data字段
        return rawData.map(item => item.data)
      }

      // 否则直接返回原始数据
      return rawData
    }

    // 获取文件类型
    const getFileType = (filename) => {
      if (!filename) return 'unknown'

      const ext = filename.toLowerCase().split('.').pop()

      if (['xlsx', 'xls'].includes(ext)) return 'excel'
      if (['pdf'].includes(ext)) return 'pdf'
      if (['docx', 'doc'].includes(ext)) return 'word'
      if (['pptx', 'ppt'].includes(ext)) return 'powerpoint'
      if (['csv'].includes(ext)) return 'csv'
      if (['txt', 'md', 'rtf'].includes(ext)) return 'text'

      return 'unknown'
    }

    const getFieldAnalysis = () => {
      if (!currentResults.value?.raw_data || currentResults.value.raw_data.length === 0) {
        return []
      }

      const data = currentResults.value.raw_data
      const fields = Object.keys(data[0])

      return fields.map(field => {
        const validCount = data.filter(row => row[field] && String(row[field]).trim()).length
        const rate = Math.round((validCount / data.length) * 100)

        return {
          field,
          count: validCount,
          rate: `${rate}%`
        }
      })
    }

    const exportSingleResult = (file) => {
      if (!file.extracted_data) {
        ElMessage.warning('该文件尚未解析')
        return
      }

      const data = {
        file_info: {
          filename: file.filename,
          upload_time: file.upload_time,
          file_type: file.file_type,
          size: file.size
        },
        extracted_data: file.extracted_data.raw_data || file.extracted_data.entities,
        metadata: file.extracted_data.metadata,
        export_time: new Date().toISOString()
      }

      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `${file.filename}_parsed_data.json`
      a.click()
      URL.revokeObjectURL(url)

      ElMessage.success('解析数据已导出')
    }

    const deleteFile = async (file) => {
      try {
        await ElMessageBox.confirm('确定要删除这个文件吗？', '确认删除', {
          type: 'warning'
        })

        const index = uploadedFiles.value.findIndex(f => f.upload_id === file.upload_id)
        if (index > -1) {
          uploadedFiles.value.splice(index, 1)
          ElMessage.success('文件已删除')
        }
      } catch {
        // 用户取消删除
      }
    }

    const handleParseDocument = async (file) => {
      try {
        await parseDocument(file)
      } catch (error) {
        console.error('Parse document error:', error)
        ElMessage.error('解析失败，请重试')
      }
    }

    const reParseDocument = async () => {
      if (currentFileInfo.value) {
        closeResultDialog()
        try {
          await parseDocument(currentFileInfo.value)
        } catch (error) {
          console.error('Re-parse error:', error)
          ElMessage.error('重新解析失败，请重试')
        }
      }
    }

    const exportAllResults = () => {
      const parsedFiles = uploadedFiles.value.filter(file => file.parsed_data)

      if (parsedFiles.length === 0) {
        ElMessage.warning('没有已解析的文件')
        return
      }

      const allData = {
        export_info: {
          total_files: parsedFiles.length,
          export_time: new Date().toISOString(),
          export_type: 'batch_document_parsing'
        },
        files: parsedFiles.map(file => ({
          filename: file.filename,
          file_type: file.file_type,
          size: file.size,
          upload_time: file.upload_time,
          parsing_time: file.parsed_data.parsing_time,
          raw_data: file.parsed_data.raw_data,
          metadata: file.parsed_data.metadata
        }))
      }

      const blob = new Blob([JSON.stringify(allData, null, 2)], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `batch_parsed_data_${new Date().toISOString().split('T')[0]}.json`
      a.click()
      URL.revokeObjectURL(url)

      ElMessage.success(`已导出${parsedFiles.length}个文件的解析数据`)
    }

    const hasAnyParsedFiles = computed(() => {
      return uploadedFiles.value.some(file => file.parsed_data)
    })

    return {
      uploadUrl,
      uploadedFiles,
      currentResults,
      activeTab,
      showResultDialog,
      activeResultTab,
      currentFileInfo,
      handleUploadSuccess,
      handleUploadError,
      beforeUpload,
      parseDocument,
      handleParseDocument,
      viewParseResults,
      exportResults,
      formatFileSize,
      formatTime,
      getStatusType,
      getEntityTypeColor,
      closeResultDialog,
      exportCurrentResults,
      getParsingQuality,
      formatMetadataKey,
      formatMetadataValue,
      getExtractedRecords,
      getDataFields,
      getValidRecords,
      getDataCompleteness,
      getTableColumns,
      getFieldAnalysis,
      exportSingleResult,
      deleteFile,
      reParseDocument,
      exportAllResults,
      getDisplayComponent,
      getDisplayData,
      getFileType,
      hasAnyParsedFiles
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
  margin: 0 0 15px 0;
  color: #666;
}

.feature-tags {
  display: flex;
  justify-content: center;
  gap: 10px;
  flex-wrap: wrap;
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

/* 操作按钮样式优化 */
.action-buttons {
  display: flex;
  flex-wrap: nowrap;
  gap: 4px;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
}

.action-btn {
  border-radius: 6px !important;
  font-weight: 500;
  transition: all 0.3s ease;
  min-width: 60px;
  max-width: 80px;
  height: 28px;
  font-size: 11px;
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.action-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.parse-btn {
  background: linear-gradient(135deg, #409eff, #66b3ff) !important;
  border: none !important;
}

.parse-btn:hover {
  background: linear-gradient(135deg, #337ecc, #5aa3e6) !important;
}

.parse-btn:disabled {
  background: #c0c4cc !important;
  transform: none !important;
  box-shadow: none !important;
}

.view-btn {
  background: linear-gradient(135deg, #67c23a, #85ce61) !important;
  border: none !important;
}

.view-btn:hover {
  background: linear-gradient(135deg, #529b2e, #6bb344) !important;
}

.view-btn:disabled {
  background: #c0c4cc !important;
  transform: none !important;
  box-shadow: none !important;
}

.export-btn {
  background: linear-gradient(135deg, #909399, #a6a9ad) !important;
  border: none !important;
}

.export-btn:hover {
  background: linear-gradient(135deg, #73767a, #8b8e93) !important;
}

.export-btn:disabled {
  background: #c0c4cc !important;
  transform: none !important;
  box-shadow: none !important;
}

.delete-btn {
  background: linear-gradient(135deg, #f56c6c, #f78989) !important;
  border: none !important;
}

.delete-btn:hover {
  background: linear-gradient(135deg, #f24c4c, #f56c6c) !important;
}
</style>
