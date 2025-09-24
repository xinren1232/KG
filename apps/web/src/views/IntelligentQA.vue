<template>
  <div class="intelligent-qa">
    <el-card class="qa-header">
      <template #header>
        <div class="header-content">
          <h2>🤖 智能问答助手</h2>
          <p>基于知识图谱的智能问答，帮您快速获取质量管理信息</p>
        </div>
      </template>
      
      <!-- 快速问题模板 -->
      <div class="quick-questions">
        <h4>💡 常见问题</h4>
        <el-row :gutter="10">
          <el-col :span="8" v-for="template in questionTemplates" :key="template.id">
            <el-button 
              type="primary" 
              plain 
              size="small" 
              @click="selectTemplate(template)"
              class="template-btn"
            >
              {{ template.title }}
            </el-button>
          </el-col>
        </el-row>
      </div>
    </el-card>

    <!-- 问答界面 -->
    <el-card class="qa-interface">
      <div class="chat-container">
        <!-- 对话历史 -->
        <div class="chat-history" ref="chatHistory">
          <div 
            v-for="(message, index) in chatHistory" 
            :key="index"
            class="message-item"
            :class="message.type"
          >
            <div class="message-avatar">
              <el-icon v-if="message.type === 'user'" :size="20">
                <User />
              </el-icon>
              <el-icon v-else :size="20" color="#409EFF">
                <ChatDotRound />
              </el-icon>
            </div>
            
            <div class="message-content">
              <div class="message-text" v-html="formatMessage(message.content)"></div>
              
              <!-- 答案的额外信息 -->
              <div v-if="message.type === 'assistant' && message.metadata" class="message-metadata">
                <!-- 置信度 -->
                <div class="confidence-bar" v-if="message.metadata.confidence">
                  <span class="confidence-label">置信度:</span>
                  <el-progress 
                    :percentage="message.metadata.confidence * 100" 
                    :stroke-width="6"
                    :show-text="false"
                    class="confidence-progress"
                  />
                  <span class="confidence-value">{{ (message.metadata.confidence * 100).toFixed(0) }}%</span>
                </div>
                
                <!-- 信息源 -->
                <div class="sources" v-if="message.metadata.sources && message.metadata.sources.length > 0">
                  <h5>📚 信息来源:</h5>
                  <el-tag 
                    v-for="source in message.metadata.sources" 
                    :key="source.title"
                    size="small"
                    :type="getSourceTagType(source.relevance)"
                    class="source-tag"
                  >
                    {{ source.title }}
                  </el-tag>
                </div>
                
                <!-- 建议 -->
                <div class="suggestions" v-if="message.metadata.suggestions && message.metadata.suggestions.length > 0">
                  <h5>💡 相关建议:</h5>
                  <ul class="suggestion-list">
                    <li v-for="suggestion in message.metadata.suggestions" :key="suggestion">
                      {{ suggestion }}
                    </li>
                  </ul>
                </div>
              </div>
              
              <div class="message-time">{{ formatTime(message.timestamp) }}</div>
            </div>
          </div>
          
          <!-- 加载指示器 -->
          <div v-if="isLoading" class="message-item assistant">
            <div class="message-avatar">
              <el-icon :size="20" color="#409EFF">
                <ChatDotRound />
              </el-icon>
            </div>
            <div class="message-content">
              <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 输入区域 -->
        <div class="chat-input">
          <el-input
            v-model="currentQuestion"
            type="textarea"
            :rows="3"
            placeholder="请输入您的问题，例如：iPhone 15的摄像头测试流程是什么？"
            @keyup.ctrl.enter="sendQuestion"
            class="question-input"
          />
          
          <div class="input-actions">
            <div class="input-tips">
              <el-icon><InfoFilled /></el-icon>
              <span>Ctrl + Enter 发送</span>
            </div>
            
            <div class="action-buttons">
              <el-button @click="clearHistory" size="small" type="info" plain>
                <el-icon><Delete /></el-icon>
                清空历史
              </el-button>
              
              <el-button 
                @click="sendQuestion" 
                type="primary" 
                :loading="isLoading"
                :disabled="!currentQuestion.trim()"
              >
                <el-icon><ChatDotRound /></el-icon>
                发送问题
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 相似异常查询 -->
    <el-card class="similar-anomalies" v-if="showSimilarAnomalies">
      <template #header>
        <h3>🔍 相似异常分析</h3>
      </template>
      
      <div class="anomaly-search">
        <el-input
          v-model="symptomDescription"
          placeholder="描述您遇到的症状，例如：摄像头无法对焦"
          @keyup.enter="findSimilarAnomalies"
        >
          <template #append>
            <el-button @click="findSimilarAnomalies" :loading="searchingAnomalies">
              搜索
            </el-button>
          </template>
        </el-input>
      </div>
      
      <div v-if="similarAnomalies.length > 0" class="anomaly-results">
        <el-timeline>
          <el-timeline-item
            v-for="anomaly in similarAnomalies"
            :key="anomaly.anomaly_id"
            :timestamp="anomaly.anomaly_id"
            placement="top"
          >
            <el-card shadow="hover" class="anomaly-card">
              <div class="anomaly-header">
                <h4>{{ anomaly.title }}</h4>
                <el-tag :type="getSimilarityTagType(anomaly.similarity_score)">
                  相似度: {{ (anomaly.similarity_score * 100).toFixed(0) }}%
                </el-tag>
              </div>
              
              <p class="anomaly-description">{{ anomaly.description }}</p>
              
              <el-row :gutter="20">
                <el-col :span="8">
                  <h5>🔍 症状:</h5>
                  <el-tag v-for="symptom in anomaly.symptoms" :key="symptom" size="small" class="tag-item">
                    {{ symptom }}
                  </el-tag>
                </el-col>
                
                <el-col :span="8">
                  <h5>🎯 根因:</h5>
                  <el-tag v-for="cause in anomaly.root_causes" :key="cause" size="small" type="warning" class="tag-item">
                    {{ cause }}
                  </el-tag>
                </el-col>
                
                <el-col :span="8">
                  <h5>💡 对策:</h5>
                  <el-tag v-for="measure in anomaly.countermeasures" :key="measure" size="small" type="success" class="tag-item">
                    {{ measure }}
                  </el-tag>
                </el-col>
              </el-row>
            </el-card>
          </el-timeline-item>
        </el-timeline>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import {
  User,
  InfoFilled,
  Delete,
  ChatDotRound
} from '@element-plus/icons-vue'
import { kgApi } from '../api'

export default {
  name: 'IntelligentQA',
  components: {
    User,
    InfoFilled,
    Delete,
    ChatDotRound
  },
  setup() {
    const currentQuestion = ref('')
    const isLoading = ref(false)
    const chatHistory = ref([])
    const chatHistoryRef = ref(null)
    
    const showSimilarAnomalies = ref(true)
    const symptomDescription = ref('')
    const searchingAnomalies = ref(false)
    const similarAnomalies = ref([])
    
    // 问题模板
    const questionTemplates = ref([
      { id: 1, title: 'iPhone 15摄像头测试流程', question: 'iPhone 15的摄像头测试流程是什么？' },
      { id: 2, title: '电池异常分析', question: '手机电池发热异常的原因和解决方案？' },
      { id: 3, title: '屏幕测试要点', question: '屏幕模块的主要测试要点有哪些？' },
      { id: 4, title: '常见故障排查', question: '手机无法开机的常见原因和排查步骤？' },
      { id: 5, title: '质量标准查询', question: '摄像头模块的质量标准是什么？' },
      { id: 6, title: '测试用例推荐', question: '新产品测试需要哪些核心测试用例？' }
    ])
    
    // 选择问题模板
    const selectTemplate = (template) => {
      currentQuestion.value = template.question
      sendQuestion()
    }
    
    // 发送问题
    const sendQuestion = async () => {
      if (!currentQuestion.value.trim() || isLoading.value) return
      
      const question = currentQuestion.value.trim()
      
      // 添加用户消息
      chatHistory.value.push({
        type: 'user',
        content: question,
        timestamp: new Date()
      })
      
      currentQuestion.value = ''
      isLoading.value = true
      
      try {
        // 调用智能问答API
        const response = await kgApi.askQuestion(question)
        
        if (response.success) {
          // 添加助手回答
          chatHistory.value.push({
            type: 'assistant',
            content: response.data.answer,
            metadata: {
              confidence: response.data.confidence,
              sources: response.data.sources,
              suggestions: response.data.suggestions
            },
            timestamp: new Date()
          })
        } else {
          throw new Error(response.message || '问答服务异常')
        }
      } catch (error) {
        ElMessage.error('问答失败: ' + error.message)
        
        // 添加错误消息
        chatHistory.value.push({
          type: 'assistant',
          content: '抱歉，我暂时无法回答您的问题。请稍后重试或联系技术支持。',
          timestamp: new Date()
        })
      } finally {
        isLoading.value = false
        scrollToBottom()
      }
    }
    
    // 查找相似异常
    const findSimilarAnomalies = async () => {
      if (!symptomDescription.value.trim()) {
        ElMessage.warning('请输入症状描述')
        return
      }
      
      searchingAnomalies.value = true
      
      try {
        const response = await kgApi.findSimilarAnomalies(symptomDescription.value)
        
        if (response.success) {
          similarAnomalies.value = response.data
          ElMessage.success(`找到 ${response.data.length} 个相似异常`)
        } else {
          throw new Error(response.message || '搜索失败')
        }
      } catch (error) {
        ElMessage.error('搜索相似异常失败: ' + error.message)
      } finally {
        searchingAnomalies.value = false
      }
    }
    
    // 清空历史
    const clearHistory = () => {
      chatHistory.value = []
      ElMessage.success('对话历史已清空')
    }
    
    // 滚动到底部
    const scrollToBottom = () => {
      nextTick(() => {
        if (chatHistoryRef.value) {
          chatHistoryRef.value.scrollTop = chatHistoryRef.value.scrollHeight
        }
      })
    }
    
    // 格式化消息
    const formatMessage = (content) => {
      return content.replace(/\n/g, '<br>')
    }
    
    // 格式化时间
    const formatTime = (timestamp) => {
      return new Date(timestamp).toLocaleTimeString()
    }
    
    // 获取信息源标签类型
    const getSourceTagType = (relevance) => {
      switch (relevance) {
        case 'high': return 'danger'
        case 'medium': return 'warning'
        case 'low': return 'info'
        default: return ''
      }
    }
    
    // 获取相似度标签类型
    const getSimilarityTagType = (score) => {
      if (score >= 0.8) return 'danger'
      if (score >= 0.6) return 'warning'
      return 'info'
    }
    
    onMounted(() => {
      // 添加欢迎消息
      chatHistory.value.push({
        type: 'assistant',
        content: '您好！我是质量知识图谱智能助手。我可以帮您：\n\n• 查询测试流程和用例\n• 分析异常原因和解决方案\n• 提供组件信息和测试要点\n• 搜索相似异常案例\n\n请输入您的问题，或选择上方的常见问题模板。',
        timestamp: new Date()
      })
    })
    
    return {
      currentQuestion,
      isLoading,
      chatHistory,
      chatHistoryRef,
      showSimilarAnomalies,
      symptomDescription,
      searchingAnomalies,
      similarAnomalies,
      questionTemplates,
      selectTemplate,
      sendQuestion,
      findSimilarAnomalies,
      clearHistory,
      formatMessage,
      formatTime,
      getSourceTagType,
      getSimilarityTagType
    }
  }
}
</script>

<style scoped>
.intelligent-qa {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.qa-header {
  margin-bottom: 20px;
}

.header-content h2 {
  margin: 0 0 10px 0;
  color: #303133;
}

.header-content p {
  margin: 0;
  color: #606266;
}

.quick-questions {
  margin-top: 20px;
}

.quick-questions h4 {
  margin: 0 0 15px 0;
  color: #303133;
}

.template-btn {
  width: 100%;
  margin-bottom: 10px;
  text-align: left;
}

.qa-interface {
  margin-bottom: 20px;
}

.chat-container {
  height: 600px;
  display: flex;
  flex-direction: column;
}

.chat-history {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 20px;
}

.message-item {
  display: flex;
  margin-bottom: 20px;
  align-items: flex-start;
}

.message-item.user {
  flex-direction: row-reverse;
}

.message-item.user .message-content {
  background: #409EFF;
  color: white;
  margin-right: 10px;
}

.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #e4e7ed;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.message-content {
  max-width: 70%;
  background: white;
  border-radius: 12px;
  padding: 15px;
  margin-left: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.message-text {
  line-height: 1.6;
  margin-bottom: 10px;
}

.message-metadata {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #e4e7ed;
}

.confidence-bar {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.confidence-label {
  font-size: 12px;
  color: #606266;
  margin-right: 10px;
}

.confidence-progress {
  flex: 1;
  margin-right: 10px;
}

.confidence-value {
  font-size: 12px;
  color: #606266;
}

.sources h5, .suggestions h5 {
  margin: 10px 0 8px 0;
  font-size: 14px;
  color: #303133;
}

.source-tag {
  margin-right: 8px;
  margin-bottom: 5px;
}

.suggestion-list {
  margin: 0;
  padding-left: 20px;
}

.suggestion-list li {
  margin-bottom: 5px;
  color: #606266;
  font-size: 14px;
}

.message-time {
  font-size: 12px;
  color: #909399;
  text-align: right;
  margin-top: 5px;
}

.typing-indicator {
  display: flex;
  align-items: center;
  gap: 4px;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #409EFF;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 80%, 100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

.chat-input {
  border-top: 1px solid #e4e7ed;
  padding-top: 20px;
}

.question-input {
  margin-bottom: 10px;
}

.input-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.input-tips {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #909399;
  font-size: 12px;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

.similar-anomalies {
  margin-bottom: 20px;
}

.anomaly-search {
  margin-bottom: 20px;
}

.anomaly-results {
  max-height: 500px;
  overflow-y: auto;
}

.anomaly-card {
  margin-bottom: 10px;
}

.anomaly-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.anomaly-header h4 {
  margin: 0;
  color: #303133;
}

.anomaly-description {
  color: #606266;
  margin-bottom: 15px;
  line-height: 1.5;
}

.anomaly-results h5 {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #303133;
}

.tag-item {
  margin-right: 8px;
  margin-bottom: 5px;
}
</style>
