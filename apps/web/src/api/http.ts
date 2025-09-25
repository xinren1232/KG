/**
 * Axios HTTP client with request/response interceptors
 * Base URL: /api (proxied to http://localhost:8000 by Vite)
 */
import axios, { AxiosInstance, AxiosResponse, AxiosError } from 'axios'
import { ElMessage } from 'element-plus'

// Create axios instance
const http: AxiosInstance = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Request interceptor
http.interceptors.request.use(
  (config) => {
    // Add auth token if available (for future use)
    const token = localStorage.getItem('api_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // Add request timestamp for logging
    config.metadata = { startTime: Date.now() }
    
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
http.interceptors.response.use(
  (response: AxiosResponse) => {
    // Log response time
    const endTime = Date.now()
    const duration = endTime - (response.config.metadata?.startTime || endTime)
    console.log(`API ${response.config.method?.toUpperCase()} ${response.config.url} - ${duration}ms`)
    
    // Check if response follows standard format
    if (response.data && typeof response.data === 'object') {
      if (response.data.ok === false && response.data.error) {
        // Handle API-level errors
        const errorMsg = response.data.error.message || 'API Error'
        const errorCode = response.data.error.code

        // Don't show error messages for known database connection issues
        // These are handled gracefully by the frontend with fallback data
        const silentErrors = ['NEO4J_CONN', 'STATS_FAILED']

        if (!silentErrors.includes(errorCode)) {
          ElMessage.error(errorMsg)
        } else {
          console.warn(`⚠️ ${errorCode}: ${errorMsg} (使用降级数据)`)
        }

        return Promise.reject(new Error(errorMsg))
      }
    }
    
    return response
  },
  (error: AxiosError) => {
    // Handle network/HTTP errors
    let errorMessage = 'Network Error'
    
    if (error.response) {
      // Server responded with error status
      const status = error.response.status
      const data = error.response.data as any
      
      if (data && data.error && data.error.message) {
        errorMessage = data.error.message
      } else {
        switch (status) {
          case 401:
            errorMessage = 'Unauthorized - Please check your credentials'
            break
          case 403:
            errorMessage = 'Forbidden - Access denied'
            break
          case 404:
            errorMessage = 'API endpoint not found'
            break
          case 500:
            errorMessage = 'Internal server error'
            break
          case 503:
            errorMessage = 'Service unavailable - Please try again later'
            break
          default:
            errorMessage = `HTTP ${status} Error`
        }
      }
    } else if (error.request) {
      // Request made but no response received
      errorMessage = 'No response from server - Please check your connection'
    } else {
      // Request setup error
      errorMessage = error.message || 'Request failed'
    }
    
    // Show error message to user
    ElMessage.error(errorMessage)
    
    return Promise.reject(error)
  }
)

export default http
