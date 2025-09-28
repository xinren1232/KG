import axios from 'axios'
import { mockApi } from './mock.js'

// 判断是否使用Mock数据 - 现在后端已启动，使用真实API
const USE_MOCK = false

// 创建axios实例
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    console.log('API Request:', config.method?.toUpperCase(), config.url, config.data)
    return config
  },
  error => {
    console.error('Request Error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    console.log('API Response:', response.status, response.data)
    return response.data
  },
  error => {
    console.error('Response Error:', error)
    const message = error.response?.data?.detail || error.message || '请求失败'
    return Promise.reject(new Error(message))
  }
)

// API方法
export const kgApi = {
  // 健康检查
  healthCheck() {
    if (USE_MOCK) {
      return mockApi.healthCheck()
    }
    return api.get('/health')
  },

  // 文件上传
  uploadFile(file) {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/kg/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  // 获取已上传文件列表
  getFiles() {
    if (USE_MOCK) {
      return mockApi.getFiles()
    }
    return api.get('/kg/files')
  },

  // 抽取文件数据
  extractFile(filename) {
    return api.post(`/kg/extract/${filename}`)
  },

  // 构建知识图谱
  buildGraph(filename) {
    return api.post(`/kg/build/${filename}`)
  },

  // 获取图谱统计
  getGraphStats() {
    if (USE_MOCK) {
      return mockApi.getGraphStats()
    }
    return api.get('/kg/stats')
  },

  // 获取真实图谱统计
  getRealGraphStats() {
    if (USE_MOCK) {
      return mockApi.getRealGraphStats()
    }
    return api.get('/kg/real-stats')
  },

  // 获取图谱可视化数据
  getGraphVisualizationData(showAll = true) {
    console.log('getGraphVisualizationData called with showAll:', showAll, typeof showAll)
    if (USE_MOCK) {
      return mockApi.getGraphVisualizationData()
    }
    const params = {
      show_all: showAll,
      limit: showAll ? 1000 : 100
    }
    console.log('API params:', params)
    return api.get('/kg/graph', { params })
  },

  // 获取数据治理信息
  getGovernanceData() {
    return api.get('/kg/governance-data')
  },



  // 系统管理相关API
  getSystemStatus() {
    if (USE_MOCK) {
      return mockApi.getSystemStatus()
    }
    return api.get('/system/status')
  },

  exportSystemConfig() {
    return api.get('/system/export-config')
  },

  // 规则管理
  getRules() {
    if (USE_MOCK) {
      return mockApi.getRules()
    }
    return api.get('/system/rules')
  },

  createRule(rule) {
    if (USE_MOCK) {
      return mockApi.createRule(rule)
    }
    return api.post('/system/rules', rule)
  },

  updateRule(ruleId, rule) {
    if (USE_MOCK) {
      return mockApi.updateRule(ruleId, rule)
    }
    return api.put(`/system/rules/${ruleId}`, rule)
  },

  updateRuleStatus(ruleId, status) {
    return api.patch(`/system/rules/${ruleId}/status`, { status })
  },

  deleteRule(ruleId) {
    if (USE_MOCK) {
      return mockApi.deleteRule(ruleId)
    }
    return api.delete(`/system/rules/${ruleId}`)
  },

  testRule(testData) {
    if (USE_MOCK) {
      return mockApi.testRule(testData)
    }
    return api.post('/system/rules/test', testData)
  },

  // 获取实体列表
  getEntities(entityType = null, limit = 100) {
    const params = { limit }
    if (entityType) params.entity_type = entityType
    return api.get('/kg/entities', { params })
  },

  // 获取关系列表
  getRelations(relationType = null, limit = 100) {
    const params = { limit }
    if (relationType) params.relation_type = relationType
    return api.get('/kg/relations', { params })
  },

  // 查询图谱
  queryGraph(cypherQuery, parameters = {}) {
    return api.post('/kg/query', {
      cypher_query: cypherQuery,
      parameters
    })
  },

  // 获取图谱数据 (已废弃，使用 getGraphVisualizationData 替代)
  getGraphData(nodeLimit = 100, includeRelations = true) {
    console.warn('getGraphData is deprecated, use getGraphVisualizationData instead')
    return this.getGraphVisualizationData(true)
  },

  // 清空图谱
  clearGraph() {
    return api.delete('/kg/clear')
  },

  // 词典管理API
  getDictionary(params = {}) {
    if (USE_MOCK) {
      return mockApi.getDictionary(params)
    }
    return api.get('/kg/dictionary/entries', { params })
  },

  getDictionaryLabels() {
    return api.get('/api/dictionary/labels')
  },

  getDictionaryTags() {
    return api.get('/api/dictionary/tags')
  },

  getDictionaryByLabel(label) {
    return api.get(`/api/dictionary/${label}`)
  },

  // 兼容旧API的词典方法（用于向后兼容）
  getOldDictionary() {
    return api.get('/kg/dictionary')
  },

  // 兼容旧API的方法（保持向后兼容）
  getProducts() {
    return this.queryGraph('MATCH (n:Entity {type: "product"}) RETURN n.name as name, n.id as id LIMIT 50')
  },

  getComponents(productName) {
    return this.queryGraph(
      'MATCH (p:Entity {type: "product", name: $productName})-[r]-(c:Entity {type: "component"}) RETURN c.name as name, c.id as id',
      { productName }
    )
  },

  // 系统管理相关API
  getSystemVersions() {
    if (USE_MOCK) {
      return mockApi.getVersions()
    }
    return api.get('/api/system/versions')
  },

  getSystemPrompts() {
    if (USE_MOCK) {
      return mockApi.getPrompts()
    }
    return api.get('/api/system/prompts')
  },

  getSystemScenarios() {
    if (USE_MOCK) {
      return mockApi.getScenarios()
    }
    return api.get('/api/system/scenarios')
  },

  publishVersion(versionData) {
    if (USE_MOCK) {
      return mockApi.publishVersion(versionData)
    }
    return api.post('/api/system/versions', versionData)
  }
}

export default kgApi
