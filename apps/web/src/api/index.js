import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:8000',
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
    return api.get('/kg/stats')
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

  // 获取图谱可视化数据
  getGraphData(nodeLimit = 100, includeRelations = true) {
    return api.get('/kg/graph/data', {
      params: {
        node_limit: nodeLimit,
        include_relations: includeRelations
      }
    })
  },

  // 清空图谱
  clearGraph() {
    return api.delete('/kg/clear')
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
  }
}

export default api
