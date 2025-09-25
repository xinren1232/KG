#!/bin/bash

# API容器启动脚本
# 负责初始化Neo4j约束和索引，然后启动API服务

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_debug() {
    echo -e "${BLUE}[DEBUG]${NC} $1"
}

# 配置参数
NEO4J_URI=${NEO4J_URI:-bolt://neo4j:7687}
NEO4J_USER=${NEO4J_USER:-neo4j}
NEO4J_PASSWORD=${NEO4J_PASSWORD:-password123}
MAX_RETRIES=${MAX_RETRIES:-30}
RETRY_INTERVAL=${RETRY_INTERVAL:-5}

# 等待Neo4j服务可用
wait_for_neo4j() {
    log_info "Waiting for Neo4j to be ready..."
    
    local retries=0
    while [ $retries -lt $MAX_RETRIES ]; do
        if cypher-shell -a "$NEO4J_URI" -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" "RETURN 1" >/dev/null 2>&1; then
            log_info "Neo4j is ready!"
            return 0
        fi
        
        retries=$((retries + 1))
        log_debug "Attempt $retries/$MAX_RETRIES: Neo4j not ready, waiting ${RETRY_INTERVAL}s..."
        sleep $RETRY_INTERVAL
    done
    
    log_error "Neo4j is not available after $MAX_RETRIES attempts"
    return 1
}

# 检查约束和索引是否已初始化
check_initialization() {
    log_info "Checking if Neo4j constraints and indexes are already initialized..."
    
    local result=$(cypher-shell -a "$NEO4J_URI" -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" \
        "MATCH (init:SystemInit {type: 'constraints_and_indexes'}) RETURN init.version" 2>/dev/null | tail -n +2 | head -n 1 | tr -d '"')
    
    if [ -n "$result" ]; then
        log_info "Neo4j constraints and indexes already initialized (version: $result)"
        return 0
    else
        log_info "Neo4j constraints and indexes not initialized"
        return 1
    fi
}

# 初始化Neo4j约束和索引
initialize_neo4j() {
    log_info "Initializing Neo4j constraints and indexes..."
    
    local constraints_file="/import/neo4j_constraints.cypher"
    
    if [ ! -f "$constraints_file" ]; then
        log_error "Constraints file not found: $constraints_file"
        return 1
    fi
    
    log_info "Executing constraints and indexes from: $constraints_file"
    
    if cypher-shell -a "$NEO4J_URI" -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" -f "$constraints_file"; then
        log_info "Neo4j constraints and indexes initialized successfully"
        return 0
    else
        log_error "Failed to initialize Neo4j constraints and indexes"
        return 1
    fi
}

# 验证初始化结果
verify_initialization() {
    log_info "Verifying Neo4j initialization..."
    
    # 检查约束数量
    local constraints_count=$(cypher-shell -a "$NEO4J_URI" -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" \
        "SHOW CONSTRAINTS YIELD name RETURN count(name)" 2>/dev/null | tail -n +2 | head -n 1)
    
    # 检查索引数量
    local indexes_count=$(cypher-shell -a "$NEO4J_URI" -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" \
        "SHOW INDEXES YIELD name RETURN count(name)" 2>/dev/null | tail -n +2 | head -n 1)
    
    log_info "Verification results:"
    log_info "  Constraints: ${constraints_count:-0}"
    log_info "  Indexes: ${indexes_count:-0}"
    
    if [ "${constraints_count:-0}" -gt 0 ] && [ "${indexes_count:-0}" -gt 0 ]; then
        log_info "Neo4j initialization verification passed"
        return 0
    else
        log_warn "Neo4j initialization verification failed"
        return 1
    fi
}

# 启动API服务
start_api_service() {
    log_info "Starting API service..."
    
    # 设置Python路径
    export PYTHONPATH="/app:$PYTHONPATH"
    
    # 切换到应用目录
    cd /app
    
    # 启动FastAPI服务
    if [ "$ENVIRONMENT" = "development" ]; then
        log_info "Starting in development mode with auto-reload"
        exec uvicorn main_v01:app --host 0.0.0.0 --port 8000 --reload
    else
        log_info "Starting in production mode"
        exec uvicorn main_v01:app --host 0.0.0.0 --port 8000 --workers 4
    fi
}

# 健康检查
health_check() {
    log_info "Performing health check..."
    
    # 检查Neo4j连接
    if ! cypher-shell -a "$NEO4J_URI" -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" "RETURN 1" >/dev/null 2>&1; then
        log_error "Neo4j health check failed"
        return 1
    fi
    
    log_info "Health check passed"
    return 0
}

# 清理函数
cleanup() {
    log_info "Performing cleanup..."
    # 这里可以添加清理逻辑
}

# 信号处理
trap cleanup EXIT

# 显示环境信息
show_environment() {
    log_info "=== Environment Information ==="
    log_info "Neo4j URI: $NEO4J_URI"
    log_info "Neo4j User: $NEO4J_USER"
    log_info "Max Retries: $MAX_RETRIES"
    log_info "Retry Interval: ${RETRY_INTERVAL}s"
    log_info "Environment: ${ENVIRONMENT:-production}"
    log_info "Python Path: $PYTHONPATH"
    log_info "Working Directory: $(pwd)"
    log_info "================================"
}

# 主函数
main() {
    log_info "=== Knowledge Graph API Container Startup ==="
    log_info "Timestamp: $(date)"
    
    show_environment
    
    # 等待Neo4j可用
    if ! wait_for_neo4j; then
        log_error "Cannot connect to Neo4j, exiting..."
        exit 1
    fi
    
    # 检查是否需要初始化
    if ! check_initialization; then
        log_info "Initializing Neo4j for the first time..."
        if ! initialize_neo4j; then
            log_error "Neo4j initialization failed, exiting..."
            exit 1
        fi
        
        # 验证初始化结果
        if ! verify_initialization; then
            log_warn "Neo4j initialization verification failed, but continuing..."
        fi
    fi
    
    # 执行健康检查
    if ! health_check; then
        log_error "Health check failed, exiting..."
        exit 1
    fi
    
    log_info "=== Starting API Service ==="
    
    # 启动API服务
    start_api_service
}

# 如果脚本被直接执行，运行主函数
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi
