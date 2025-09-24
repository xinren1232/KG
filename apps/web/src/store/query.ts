/**
 * Pinia store for query state management
 * Stores recent query parameters and results cache
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface FlowQueryParams {
  product: string
  module: string
}

export interface CausePathParams {
  symptom: string
}

export interface FlowItem {
  id: string
  title: string
  priority?: string
}

export interface PathNode {
  id: string
  labels: string[]
  properties: Record<string, any>
}

export interface PathRelation {
  id: string
  type: string
  source: string
  target: string
}

export interface CausePath {
  nodes: PathNode[]
  relations: PathRelation[]
}

export const useQueryStore = defineStore('query', () => {
  // Recent query parameters
  const recentFlowQueries = ref<FlowQueryParams[]>([])
  const recentCauseQueries = ref<CausePathParams[]>([])
  
  // Current query results
  const currentFlowResult = ref<FlowItem[]>([])
  const currentCauseResult = ref<CausePath[]>([])
  
  // Loading states
  const flowLoading = ref(false)
  const causeLoading = ref(false)
  
  // Error states
  const flowError = ref<string | null>(null)
  const causeError = ref<string | null>(null)
  
  // Computed getters
  const hasFlowResults = computed(() => currentFlowResult.value.length > 0)
  const hasCauseResults = computed(() => currentCauseResult.value.length > 0)
  
  // Actions
  function addFlowQuery(params: FlowQueryParams) {
    // Remove duplicate if exists
    const index = recentFlowQueries.value.findIndex(
      q => q.product === params.product && q.module === params.module
    )
    if (index >= 0) {
      recentFlowQueries.value.splice(index, 1)
    }
    
    // Add to beginning
    recentFlowQueries.value.unshift(params)
    
    // Keep only last 10
    if (recentFlowQueries.value.length > 10) {
      recentFlowQueries.value = recentFlowQueries.value.slice(0, 10)
    }
    
    // Save to localStorage
    localStorage.setItem('recent_flow_queries', JSON.stringify(recentFlowQueries.value))
  }
  
  function addCauseQuery(params: CausePathParams) {
    // Remove duplicate if exists
    const index = recentCauseQueries.value.findIndex(
      q => q.symptom === params.symptom
    )
    if (index >= 0) {
      recentCauseQueries.value.splice(index, 1)
    }
    
    // Add to beginning
    recentCauseQueries.value.unshift(params)
    
    // Keep only last 10
    if (recentCauseQueries.value.length > 10) {
      recentCauseQueries.value = recentCauseQueries.value.slice(0, 10)
    }
    
    // Save to localStorage
    localStorage.setItem('recent_cause_queries', JSON.stringify(recentCauseQueries.value))
  }
  
  function setFlowResult(result: FlowItem[]) {
    currentFlowResult.value = result
    flowError.value = null
  }
  
  function setCauseResult(result: CausePath[]) {
    currentCauseResult.value = result
    causeError.value = null
  }
  
  function setFlowLoading(loading: boolean) {
    flowLoading.value = loading
    if (loading) {
      flowError.value = null
    }
  }
  
  function setCauseLoading(loading: boolean) {
    causeLoading.value = loading
    if (loading) {
      causeError.value = null
    }
  }
  
  function setFlowError(error: string) {
    flowError.value = error
    flowLoading.value = false
  }
  
  function setCauseError(error: string) {
    causeError.value = error
    causeLoading.value = false
  }
  
  function clearFlowResults() {
    currentFlowResult.value = []
    flowError.value = null
  }
  
  function clearCauseResults() {
    currentCauseResult.value = []
    causeError.value = null
  }
  
  // Load from localStorage on init
  function loadFromStorage() {
    try {
      const flowQueries = localStorage.getItem('recent_flow_queries')
      if (flowQueries) {
        recentFlowQueries.value = JSON.parse(flowQueries)
      }
      
      const causeQueries = localStorage.getItem('recent_cause_queries')
      if (causeQueries) {
        recentCauseQueries.value = JSON.parse(causeQueries)
      }
    } catch (error) {
      console.warn('Failed to load query history from localStorage:', error)
    }
  }
  
  // Initialize
  loadFromStorage()
  
  return {
    // State
    recentFlowQueries,
    recentCauseQueries,
    currentFlowResult,
    currentCauseResult,
    flowLoading,
    causeLoading,
    flowError,
    causeError,
    
    // Computed
    hasFlowResults,
    hasCauseResults,
    
    // Actions
    addFlowQuery,
    addCauseQuery,
    setFlowResult,
    setCauseResult,
    setFlowLoading,
    setCauseLoading,
    setFlowError,
    setCauseError,
    clearFlowResults,
    clearCauseResults
  }
})
