<template>
  <div class="text-display">
    <div v-if="data && data.length > 0">
      <!-- 文本文档统计信息 -->
      <div class="text-header">
        <el-row :gutter="20" style="margin-bottom: 16px;">
          <el-col :span="6">
            <el-statistic title="📄 段落数量" :value="getParagraphCount()" />
          </el-col>
          <el-col :span="6">
            <el-statistic title="📝 总字数" :value="getTotalWords()" />
          </el-col>
          <el-col :span="6">
            <el-statistic title="🔤 总字符数" :value="getTotalChars()" />
          </el-col>
          <el-col :span="6">
            <el-statistic title="📊 平均段落长度" :value="getAverageParagraphLength()" />
          </el-col>
        </el-row>
      </div>

      <!-- 文本控制工具 -->
      <div class="text-controls" style="margin-bottom: 16px;">
        <el-row :gutter="16" type="flex" align="middle">
          <el-col :span="8">
            <el-input
              v-model="searchText"
              placeholder="搜索文本内容..."
              prefix-icon="Search"
              clearable
              @input="handleSearch"
            />
          </el-col>
          <el-col :span="8">
            <el-select v-model="viewMode" placeholder="显示模式" style="width: 100%;">
              <el-option label="段落视图" value="paragraph" />
              <el-option label="连续文本" value="continuous" />
              <el-option label="统计分析" value="analysis" />
            </el-select>
          </el-col>
          <el-col :span="8">
            <el-switch
              v-model="showLineNumbers"
              active-text="显示行号"
              inactive-text="隐藏行号"
            />
          </el-col>
        </el-row>
      </div>

      <!-- 文本内容展示 -->
      <div class="text-content">
        <!-- 段落视图 -->
        <div v-if="viewMode === 'paragraph'">
          <el-card 
            v-for="(item, index) in getFilteredParagraphs()" 
            :key="`para-${index}`"
            class="content-card paragraph-card"
            shadow="hover"
          >
            <template #header>
              <div class="card-header">
                <span class="content-type-tag">
                  <el-tag type="primary" size="small">📄 段落 {{ item.paragraph_number || index + 1 }}</el-tag>
                </span>
                <span class="content-meta">
                  <el-tag size="small" type="info">{{ item.word_count || getWordCount(item.content) }} 词</el-tag>
                  <el-tag size="small" type="success">{{ item.char_count || item.content.length }} 字符</el-tag>
                </span>
              </div>
            </template>
            <div class="paragraph-content">
              <div v-if="showLineNumbers" class="line-numbers">
                <span v-for="(line, lineIndex) in item.content.split('\n')" :key="lineIndex" class="line-number">
                  {{ lineIndex + 1 }}
                </span>
              </div>
              <div class="text-lines">
                <div v-for="(line, lineIndex) in item.content.split('\n')" :key="lineIndex" class="text-line">
                  <span v-html="highlightSearchText(line)"></span>
                </div>
              </div>
            </div>
          </el-card>
        </div>

        <!-- 连续文本视图 -->
        <div v-else-if="viewMode === 'continuous'">
          <el-card class="continuous-text-card">
            <template #header>
              <span>📄 完整文档内容</span>
            </template>
            <div class="continuous-content">
              <div v-if="showLineNumbers" class="line-numbers">
                <span v-for="(line, lineIndex) in getAllLines()" :key="lineIndex" class="line-number">
                  {{ lineIndex + 1 }}
                </span>
              </div>
              <div class="text-lines">
                <div v-for="(line, lineIndex) in getAllLines()" :key="lineIndex" class="text-line">
                  <span v-html="highlightSearchText(line)"></span>
                </div>
              </div>
            </div>
          </el-card>
        </div>

        <!-- 统计分析视图 -->
        <div v-else-if="viewMode === 'analysis'">
          <el-row :gutter="16">
            <el-col :span="12">
              <el-card>
                <template #header>
                  <span>📊 词频分析</span>
                </template>
                <div class="word-frequency">
                  <div v-for="word in getTopWords()" :key="word.text" class="word-item">
                    <div class="word-info">
                      <span class="word-text">{{ word.text }}</span>
                      <span class="word-count">{{ word.count }} 次</span>
                    </div>
                    <el-progress 
                      :percentage="word.percentage" 
                      :color="getWordColor(word.percentage)"
                      :stroke-width="6"
                    />
                  </div>
                </div>
              </el-card>
            </el-col>
            <el-col :span="12">
              <el-card>
                <template #header>
                  <span>📈 段落长度分布</span>
                </template>
                <div class="paragraph-length-analysis">
                  <div v-for="range in getParagraphLengthDistribution()" :key="range.label" class="length-item">
                    <div class="length-info">
                      <span class="length-label">{{ range.label }}</span>
                      <span class="length-count">{{ range.count }} 段</span>
                    </div>
                    <el-progress 
                      :percentage="range.percentage" 
                      :color="getLengthColor(range.label)"
                      :stroke-width="6"
                    />
                  </div>
                </div>
              </el-card>
            </el-col>
          </el-row>

          <!-- 文本质量分析 -->
          <el-card style="margin-top: 16px;">
            <template #header>
              <span>📋 文本质量分析</span>
            </template>
            <el-descriptions :column="3" border>
              <el-descriptions-item label="可读性评分">
                <el-tag :type="getReadabilityTagType()">{{ getReadabilityScore() }}/100</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="平均句长">
                <el-tag type="info">{{ getAverageSentenceLength() }} 字符</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="词汇丰富度">
                <el-tag :type="getVocabularyTagType()">{{ getVocabularyRichness() }}%</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="段落一致性">
                <el-tag type="success">{{ getParagraphConsistency() }}%</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="文本密度">
                <el-tag type="warning">{{ getTextDensity() }}%</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="整体质量">
                <el-tag :type="getOverallQualityTagType()">{{ getOverallQuality() }}/100</el-tag>
              </el-descriptions-item>
            </el-descriptions>
          </el-card>
        </div>
      </div>
    </div>
    <el-empty v-else description="未提取到文本内容" />
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'TextDisplay',
  props: {
    data: {
      type: Array,
      default: () => []
    },
    metadata: {
      type: Object,
      default: () => ({})
    },
    fileInfo: {
      type: Object,
      default: () => ({})
    }
  },
  setup(props) {
    const searchText = ref('')
    const viewMode = ref('paragraph')
    const showLineNumbers = ref(false)

    const getParagraphCount = () => {
      return props.data.length
    }

    const getTotalWords = () => {
      return props.data.reduce((total, item) => {
        return total + (item.word_count || getWordCount(item.content))
      }, 0)
    }

    const getTotalChars = () => {
      return props.data.reduce((total, item) => {
        return total + (item.char_count || item.content.length)
      }, 0)
    }

    const getAverageParagraphLength = () => {
      if (props.data.length === 0) return 0
      return Math.round(getTotalChars() / props.data.length)
    }

    const getWordCount = (text) => {
      if (!text) return 0
      return text.trim().split(/\s+/).filter(word => word.length > 0).length
    }

    const getFilteredParagraphs = () => {
      if (!searchText.value) return props.data
      
      return props.data.filter(item => 
        item.content.toLowerCase().includes(searchText.value.toLowerCase())
      )
    }

    const getAllLines = () => {
      const allText = props.data.map(item => item.content).join('\n')
      return allText.split('\n')
    }

    const highlightSearchText = (text) => {
      if (!searchText.value) return text
      
      const regex = new RegExp(`(${searchText.value})`, 'gi')
      return text.replace(regex, '<mark style="background-color: #ffeb3b; padding: 2px 4px; border-radius: 2px;">$1</mark>')
    }

    const getTopWords = () => {
      const allText = props.data.map(item => item.content).join(' ')
      const words = allText.toLowerCase().match(/[\u4e00-\u9fa5a-zA-Z]+/g) || []
      
      // 过滤常见停用词
      const stopWords = new Set(['的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'])
      const filteredWords = words.filter(word => word.length > 1 && !stopWords.has(word))
      
      const wordCount = {}
      filteredWords.forEach(word => {
        wordCount[word] = (wordCount[word] || 0) + 1
      })
      
      const sortedWords = Object.entries(wordCount)
        .sort(([,a], [,b]) => b - a)
        .slice(0, 10)
      
      const maxCount = sortedWords[0]?.[1] || 1
      
      return sortedWords.map(([text, count]) => ({
        text,
        count,
        percentage: Math.round((count / maxCount) * 100)
      }))
    }

    const getParagraphLengthDistribution = () => {
      const lengths = props.data.map(item => item.content.length)
      const ranges = [
        { label: '短段落 (0-100字)', min: 0, max: 100 },
        { label: '中段落 (101-300字)', min: 101, max: 300 },
        { label: '长段落 (301-500字)', min: 301, max: 500 },
        { label: '超长段落 (500字+)', min: 501, max: Infinity }
      ]
      
      const distribution = ranges.map(range => {
        const count = lengths.filter(len => len >= range.min && len <= range.max).length
        return {
          label: range.label,
          count,
          percentage: Math.round((count / lengths.length) * 100)
        }
      })
      
      return distribution.filter(item => item.count > 0)
    }

    const getReadabilityScore = () => {
      // 简化的可读性评分算法
      const avgParagraphLength = getAverageParagraphLength()
      const avgSentenceLength = getAverageSentenceLength()
      
      let score = 100
      if (avgParagraphLength > 500) score -= 20
      if (avgSentenceLength > 50) score -= 15
      if (avgSentenceLength < 10) score -= 10
      
      return Math.max(0, score)
    }

    const getAverageSentenceLength = () => {
      const allText = props.data.map(item => item.content).join('')
      const sentences = allText.split(/[。！？.!?]/).filter(s => s.trim().length > 0)
      
      if (sentences.length === 0) return 0
      
      const totalLength = sentences.reduce((sum, sentence) => sum + sentence.length, 0)
      return Math.round(totalLength / sentences.length)
    }

    const getVocabularyRichness = () => {
      const allText = props.data.map(item => item.content).join(' ')
      const words = allText.toLowerCase().match(/[\u4e00-\u9fa5a-zA-Z]+/g) || []
      const uniqueWords = new Set(words)
      
      if (words.length === 0) return 0
      return Math.round((uniqueWords.size / words.length) * 100)
    }

    const getParagraphConsistency = () => {
      const lengths = props.data.map(item => item.content.length)
      const avgLength = lengths.reduce((sum, len) => sum + len, 0) / lengths.length
      
      const variance = lengths.reduce((sum, len) => sum + Math.pow(len - avgLength, 2), 0) / lengths.length
      const standardDeviation = Math.sqrt(variance)
      
      const consistency = Math.max(0, 100 - (standardDeviation / avgLength) * 100)
      return Math.round(consistency)
    }

    const getTextDensity = () => {
      const totalChars = getTotalChars()
      const totalWords = getTotalWords()
      
      if (totalWords === 0) return 0
      return Math.round((totalChars / totalWords) * 10) // 平均每词字符数 * 10
    }

    const getOverallQuality = () => {
      const readability = getReadabilityScore()
      const vocabulary = getVocabularyRichness()
      const consistency = getParagraphConsistency()
      
      return Math.round((readability * 0.4 + vocabulary * 0.3 + consistency * 0.3))
    }

    const getWordColor = (percentage) => {
      if (percentage >= 80) return '#f56c6c'
      if (percentage >= 60) return '#e6a23c'
      if (percentage >= 40) return '#67c23a'
      return '#409eff'
    }

    const getLengthColor = (label) => {
      if (label.includes('短段落')) return '#67c23a'
      if (label.includes('中段落')) return '#409eff'
      if (label.includes('长段落')) return '#e6a23c'
      return '#f56c6c'
    }

    const getReadabilityTagType = () => {
      const score = getReadabilityScore()
      if (score >= 80) return 'success'
      if (score >= 60) return 'warning'
      return 'danger'
    }

    const getVocabularyTagType = () => {
      const richness = getVocabularyRichness()
      if (richness >= 15) return 'success'
      if (richness >= 10) return 'warning'
      return 'danger'
    }

    const getOverallQualityTagType = () => {
      const quality = getOverallQuality()
      if (quality >= 80) return 'success'
      if (quality >= 60) return 'warning'
      return 'danger'
    }

    const handleSearch = () => {
      // 搜索逻辑已在computed中处理
    }

    return {
      searchText,
      viewMode,
      showLineNumbers,
      getParagraphCount,
      getTotalWords,
      getTotalChars,
      getAverageParagraphLength,
      getWordCount,
      getFilteredParagraphs,
      getAllLines,
      highlightSearchText,
      getTopWords,
      getParagraphLengthDistribution,
      getReadabilityScore,
      getAverageSentenceLength,
      getVocabularyRichness,
      getParagraphConsistency,
      getTextDensity,
      getOverallQuality,
      getWordColor,
      getLengthColor,
      getReadabilityTagType,
      getVocabularyTagType,
      getOverallQualityTagType,
      handleSearch
    }
  }
}
</script>

<style scoped>
.text-display {
  padding: 16px;
}

.text-header {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 16px;
}

.text-controls {
  background: #fafafa;
  padding: 12px;
  border-radius: 6px;
}

.text-content {
  max-height: 700px;
  overflow-y: auto;
}

.content-card {
  margin-bottom: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.content-type-tag {
  flex: 1;
}

.content-meta {
  display: flex;
  gap: 8px;
}

.paragraph-content {
  display: flex;
  line-height: 1.8;
  font-family: 'Courier New', monospace;
}

.continuous-content {
  display: flex;
  line-height: 1.8;
  font-family: 'Courier New', monospace;
  max-height: 500px;
  overflow-y: auto;
}

.line-numbers {
  background: #f5f7fa;
  padding: 8px;
  border-right: 1px solid #dcdfe6;
  user-select: none;
  min-width: 50px;
  text-align: right;
}

.line-number {
  display: block;
  color: #909399;
  font-size: 12px;
  line-height: 1.8;
}

.text-lines {
  flex: 1;
  padding: 8px 12px;
}

.text-line {
  line-height: 1.8;
  color: #303133;
  font-size: 14px;
}

.paragraph-card {
  border-left: 4px solid #67c23a;
}

.continuous-text-card {
  border-left: 4px solid #409eff;
}

.word-frequency {
  max-height: 300px;
  overflow-y: auto;
}

.word-item {
  margin-bottom: 12px;
}

.word-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.word-text {
  font-weight: 600;
  color: #303133;
}

.word-count {
  font-size: 12px;
  color: #909399;
}

.paragraph-length-analysis {
  max-height: 300px;
  overflow-y: auto;
}

.length-item {
  margin-bottom: 12px;
}

.length-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.length-label {
  font-weight: 600;
  color: #303133;
  font-size: 14px;
}

.length-count {
  font-size: 12px;
  color: #909399;
}

:deep(.el-statistic__content) {
  font-size: 18px;
  font-weight: 600;
}

:deep(.el-progress-bar__outer) {
  border-radius: 3px;
}

:deep(mark) {
  background-color: #ffeb3b !important;
  padding: 2px 4px !important;
  border-radius: 2px !important;
}
</style>
