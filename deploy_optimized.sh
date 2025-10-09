#!/bin/bash
# 知识图谱系统优化部署脚本

set -e

echo "🚀 开始知识图谱系统优化部署"
echo "=================================="

# 颜色定义
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

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# 检查Docker和Docker Compose
check_prerequisites() {
    log_step "检查系统依赖..."
    
    if ! command -v docker &> /dev/null; then
        log_error "Docker未安装，请先安装Docker"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose未安装，请先安装Docker Compose"
        exit 1
    fi
    
    log_info "系统依赖检查通过"
}

# 停止现有服务
stop_existing_services() {
    log_step "停止现有服务..."
    
    # 停止主服务
    if docker-compose ps | grep -q "Up"; then
        log_info "停止主服务..."
        docker-compose down
    fi
    
    # 停止监控服务
    if docker-compose -f docker-compose.monitoring.yml ps | grep -q "Up"; then
        log_info "停止监控服务..."
        docker-compose -f docker-compose.monitoring.yml down
    fi
    
    log_info "现有服务已停止"
}

# 创建网络
create_network() {
    log_step "创建Docker网络..."
    
    if ! docker network ls | grep -q "kg_network"; then
        docker network create kg_network
        log_info "Docker网络 kg_network 已创建"
    else
        log_info "Docker网络 kg_network 已存在"
    fi
}

# 构建和启动主服务
start_main_services() {
    log_step "启动主服务（Neo4j + Redis + API）..."
    
    # 拉取最新镜像
    log_info "拉取Docker镜像..."
    docker-compose pull
    
    # 启动服务
    log_info "启动主服务..."
    docker-compose up -d
    
    # 等待服务启动
    log_info "等待服务启动..."
    sleep 30
    
    # 检查服务状态
    log_info "检查服务状态..."
    docker-compose ps
}

# 安装Python依赖
install_dependencies() {
    log_step "安装Python依赖..."
    
    if [ -f "api/requirements.txt" ]; then
        log_info "安装API依赖..."
        pip install -r api/requirements.txt
    else
        log_warn "未找到requirements.txt文件"
    fi
}

# 优化Neo4j数据库
optimize_neo4j() {
    log_step "优化Neo4j数据库..."
    
    # 等待Neo4j完全启动
    log_info "等待Neo4j启动..."
    sleep 60
    
    # 运行优化脚本
    if [ -f "scripts/optimize_neo4j.py" ]; then
        log_info "运行Neo4j优化脚本..."
        python scripts/optimize_neo4j.py
    else
        log_warn "未找到Neo4j优化脚本"
    fi
}

# 启动监控服务
start_monitoring() {
    log_step "启动监控服务（Prometheus + Grafana）..."
    
    # 创建监控目录
    mkdir -p monitoring/grafana/dashboards
    mkdir -p monitoring/grafana/datasources
    mkdir -p monitoring/rules
    
    # 启动监控服务
    log_info "启动监控服务..."
    docker-compose -f docker-compose.monitoring.yml up -d
    
    # 等待监控服务启动
    log_info "等待监控服务启动..."
    sleep 30
    
    # 检查监控服务状态
    log_info "检查监控服务状态..."
    docker-compose -f docker-compose.monitoring.yml ps
}

# 验证部署
verify_deployment() {
    log_step "验证部署状态..."
    
    # 检查主服务
    log_info "检查主服务..."
    
    # Neo4j
    if curl -f http://localhost:7474 > /dev/null 2>&1; then
        log_info "✅ Neo4j服务正常 (http://localhost:7474)"
    else
        log_error "❌ Neo4j服务异常"
    fi
    
    # Redis
    if docker exec kg_redis redis-cli ping > /dev/null 2>&1; then
        log_info "✅ Redis服务正常"
    else
        log_error "❌ Redis服务异常"
    fi
    
    # API
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        log_info "✅ API服务正常 (http://localhost:8000)"
    else
        log_error "❌ API服务异常"
    fi
    
    # 检查监控服务
    log_info "检查监控服务..."
    
    # Prometheus
    if curl -f http://localhost:9090 > /dev/null 2>&1; then
        log_info "✅ Prometheus服务正常 (http://localhost:9090)"
    else
        log_warn "⚠️ Prometheus服务异常"
    fi
    
    # Grafana
    if curl -f http://localhost:3000 > /dev/null 2>&1; then
        log_info "✅ Grafana服务正常 (http://localhost:3000)"
    else
        log_warn "⚠️ Grafana服务异常"
    fi
}

# 显示访问信息
show_access_info() {
    log_step "部署完成！访问信息："
    echo ""
    echo "🌐 主要服务："
    echo "   • API服务:        http://localhost:8000"
    echo "   • API文档:        http://localhost:8000/docs"
    echo "   • 健康检查:       http://localhost:8000/health"
    echo "   • Neo4j浏览器:    http://localhost:7474"
    echo ""
    echo "📊 监控服务："
    echo "   • Prometheus:     http://localhost:9090"
    echo "   • Grafana:        http://localhost:3000 (admin/admin123)"
    echo "   • 系统指标:       http://localhost:8000/metrics"
    echo ""
    echo "🔧 管理命令："
    echo "   • 查看日志:       docker-compose logs -f"
    echo "   • 重启服务:       docker-compose restart"
    echo "   • 停止服务:       docker-compose down"
    echo "   • 查看状态:       docker-compose ps"
    echo ""
    echo "📈 性能优化："
    echo "   • Redis缓存已启用"
    echo "   • Neo4j索引已优化"
    echo "   • Prometheus监控已配置"
    echo "   • Grafana仪表板已准备"
    echo ""
}

# 主函数
main() {
    log_info "开始优化部署流程..."
    
    # 检查依赖
    check_prerequisites
    
    # 停止现有服务
    stop_existing_services
    
    # 创建网络
    create_network
    
    # 启动主服务
    start_main_services
    
    # 安装依赖
    install_dependencies
    
    # 优化数据库
    optimize_neo4j
    
    # 启动监控
    start_monitoring
    
    # 验证部署
    verify_deployment
    
    # 显示访问信息
    show_access_info
    
    log_info "🎉 优化部署完成！"
}

# 错误处理
trap 'log_error "部署过程中发生错误，请检查日志"; exit 1' ERR

# 运行主函数
main "$@"
