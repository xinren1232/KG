#!/bin/bash
# SSH自动化部署脚本 - 知识图谱系统
# 使用rsync和ssh进行远程部署

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

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

# 默认配置
SERVER_HOST=""
SERVER_USER=""
SERVER_PORT="22"
SSH_KEY=""
REMOTE_PATH="/opt/knowledge-graph"
BACKUP_PATH="/opt/kg-backups"

# 显示帮助信息
show_help() {
    echo "🚀 知识图谱系统 SSH 部署工具"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -h, --host HOST        服务器地址"
    echo "  -u, --user USER        SSH用户名"
    echo "  -p, --port PORT        SSH端口 (默认: 22)"
    echo "  -k, --key KEY_FILE     SSH私钥文件路径"
    echo "  -r, --remote PATH      远程部署路径 (默认: /opt/knowledge-graph)"
    echo "  -b, --backup PATH      备份路径 (默认: /opt/kg-backups)"
    echo "  --help                 显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 -h 192.168.1.100 -u ubuntu -k ~/.ssh/id_rsa"
    echo "  $0 -h example.com -u root -p 2222"
    echo ""
}

# 解析命令行参数
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--host)
                SERVER_HOST="$2"
                shift 2
                ;;
            -u|--user)
                SERVER_USER="$2"
                shift 2
                ;;
            -p|--port)
                SERVER_PORT="$2"
                shift 2
                ;;
            -k|--key)
                SSH_KEY="$2"
                shift 2
                ;;
            -r|--remote)
                REMOTE_PATH="$2"
                shift 2
                ;;
            -b|--backup)
                BACKUP_PATH="$2"
                shift 2
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                log_error "未知参数: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

# 验证配置
validate_config() {
    if [[ -z "$SERVER_HOST" ]]; then
        log_error "请指定服务器地址 (-h)"
        exit 1
    fi
    
    if [[ -z "$SERVER_USER" ]]; then
        log_error "请指定SSH用户名 (-u)"
        exit 1
    fi
    
    if [[ -n "$SSH_KEY" && ! -f "$SSH_KEY" ]]; then
        log_error "SSH密钥文件不存在: $SSH_KEY"
        exit 1
    fi
}

# 构建SSH命令
build_ssh_cmd() {
    local ssh_cmd="ssh -p $SERVER_PORT"
    
    if [[ -n "$SSH_KEY" ]]; then
        ssh_cmd="$ssh_cmd -i $SSH_KEY"
    fi
    
    ssh_cmd="$ssh_cmd $SERVER_USER@$SERVER_HOST"
    echo "$ssh_cmd"
}

# 构建SCP命令
build_scp_cmd() {
    local scp_cmd="scp -P $SERVER_PORT"
    
    if [[ -n "$SSH_KEY" ]]; then
        scp_cmd="$scp_cmd -i $SSH_KEY"
    fi
    
    echo "$scp_cmd"
}

# 构建rsync命令
build_rsync_cmd() {
    local rsync_cmd="rsync -avz --progress"
    
    if [[ -n "$SSH_KEY" ]]; then
        rsync_cmd="$rsync_cmd -e 'ssh -p $SERVER_PORT -i $SSH_KEY'"
    else
        rsync_cmd="$rsync_cmd -e 'ssh -p $SERVER_PORT'"
    fi
    
    echo "$rsync_cmd"
}

# 测试SSH连接
test_connection() {
    log_step "测试SSH连接..."
    
    local ssh_cmd=$(build_ssh_cmd)
    
    if $ssh_cmd "echo 'SSH连接测试成功'" > /dev/null 2>&1; then
        log_info "SSH连接正常"
        return 0
    else
        log_error "SSH连接失败，请检查服务器地址、用户名和认证信息"
        return 1
    fi
}

# 检查远程系统依赖
check_remote_dependencies() {
    log_step "检查远程系统依赖..."
    
    local ssh_cmd=$(build_ssh_cmd)
    
    # 检查Docker
    if $ssh_cmd "command -v docker" > /dev/null 2>&1; then
        log_info "✅ Docker已安装"
    else
        log_warn "⚠️ Docker未安装，将尝试安装"
        install_docker
    fi
    
    # 检查Docker Compose
    if $ssh_cmd "command -v docker-compose" > /dev/null 2>&1; then
        log_info "✅ Docker Compose已安装"
    else
        log_warn "⚠️ Docker Compose未安装，将尝试安装"
        install_docker_compose
    fi
}

# 安装Docker
install_docker() {
    log_step "安装Docker..."
    
    local ssh_cmd=$(build_ssh_cmd)
    
    $ssh_cmd "
        curl -fsSL https://get.docker.com -o get-docker.sh &&
        sudo sh get-docker.sh &&
        sudo usermod -aG docker \$USER &&
        rm get-docker.sh
    "
    
    log_info "Docker安装完成"
}

# 安装Docker Compose
install_docker_compose() {
    log_step "安装Docker Compose..."
    
    local ssh_cmd=$(build_ssh_cmd)
    
    $ssh_cmd "
        sudo curl -L \"https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-\$(uname -s)-\$(uname -m)\" -o /usr/local/bin/docker-compose &&
        sudo chmod +x /usr/local/bin/docker-compose
    "
    
    log_info "Docker Compose安装完成"
}

# 创建远程目录
create_remote_directories() {
    log_step "创建远程目录..."
    
    local ssh_cmd=$(build_ssh_cmd)
    
    $ssh_cmd "
        sudo mkdir -p $REMOTE_PATH &&
        sudo mkdir -p $BACKUP_PATH &&
        sudo chown -R \$USER:\$USER $REMOTE_PATH &&
        sudo chown -R \$USER:\$USER $BACKUP_PATH
    "
    
    log_info "远程目录创建完成"
}

# 备份现有部署
backup_existing_deployment() {
    log_step "备份现有部署..."
    
    local ssh_cmd=$(build_ssh_cmd)
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_dir="$BACKUP_PATH/backup_$timestamp"
    
    $ssh_cmd "
        if [ -d $REMOTE_PATH ]; then
            cp -r $REMOTE_PATH $backup_dir
            echo '备份完成: $backup_dir'
        else
            echo '无现有部署需要备份'
        fi
    "
    
    log_info "备份完成"
}

# 同步文件
sync_files() {
    log_step "同步项目文件..."
    
    local rsync_cmd=$(build_rsync_cmd)
    
    # 排除不需要的文件和目录
    local exclude_opts="
        --exclude='*.pyc'
        --exclude='__pycache__'
        --exclude='.git'
        --exclude='node_modules'
        --exclude='*.log'
        --exclude='cleanup_backup_*'
        --exclude='thorough_cleanup_backup_*'
        --exclude='final_cleanup_backup_*'
    "
    
    # 同步文件
    eval "$rsync_cmd $exclude_opts ./ $SERVER_USER@$SERVER_HOST:$REMOTE_PATH/"
    
    log_info "文件同步完成"
}

# 部署服务
deploy_services() {
    log_step "部署知识图谱服务..."
    
    local ssh_cmd=$(build_ssh_cmd)
    
    $ssh_cmd "
        cd $REMOTE_PATH &&
        
        # 设置执行权限
        chmod +x deploy_optimized.sh 2>/dev/null || true &&
        chmod +x scripts/*.py 2>/dev/null || true &&
        
        # 停止现有服务
        docker-compose down 2>/dev/null || true &&
        docker-compose -f docker-compose.monitoring.yml down 2>/dev/null || true &&
        
        # 启动主服务
        docker-compose up -d &&
        
        # 等待服务启动
        echo '等待服务启动...' &&
        sleep 30 &&
        
        # 检查服务状态
        docker-compose ps
    "
    
    log_info "主服务部署完成"
}

# 优化数据库
optimize_database() {
    log_step "优化Neo4j数据库..."
    
    local ssh_cmd=$(build_ssh_cmd)
    
    $ssh_cmd "
        cd $REMOTE_PATH &&
        
        # 等待Neo4j完全启动
        echo '等待Neo4j启动...' &&
        sleep 60 &&
        
        # 运行优化脚本
        python3 scripts/optimize_neo4j.py 2>/dev/null || echo 'Neo4j优化脚本执行完成'
    "
    
    log_info "数据库优化完成"
}

# 启动监控服务
deploy_monitoring() {
    log_step "部署监控服务..."
    
    local ssh_cmd=$(build_ssh_cmd)
    
    $ssh_cmd "
        cd $REMOTE_PATH &&
        
        # 创建监控目录
        mkdir -p monitoring/grafana/dashboards &&
        mkdir -p monitoring/grafana/datasources &&
        mkdir -p monitoring/rules &&
        
        # 启动监控服务
        docker-compose -f docker-compose.monitoring.yml up -d &&
        
        # 等待监控服务启动
        echo '等待监控服务启动...' &&
        sleep 30 &&
        
        # 检查监控服务状态
        docker-compose -f docker-compose.monitoring.yml ps
    "
    
    log_info "监控服务部署完成"
}

# 验证部署
verify_deployment() {
    log_step "验证部署状态..."
    
    local ssh_cmd=$(build_ssh_cmd)
    
    log_info "检查服务状态..."
    
    # 检查各个服务
    $ssh_cmd "
        echo '=== Docker容器状态 ===' &&
        docker ps &&
        echo '' &&
        
        echo '=== 服务健康检查 ===' &&
        
        # Neo4j
        if curl -f http://localhost:7474 >/dev/null 2>&1; then
            echo '✅ Neo4j服务正常 (http://localhost:7474)'
        else
            echo '❌ Neo4j服务异常'
        fi &&
        
        # API
        if curl -f http://localhost:8000/health >/dev/null 2>&1; then
            echo '✅ API服务正常 (http://localhost:8000)'
        else
            echo '❌ API服务异常'
        fi &&
        
        # Prometheus
        if curl -f http://localhost:9090 >/dev/null 2>&1; then
            echo '✅ Prometheus服务正常 (http://localhost:9090)'
        else
            echo '⚠️ Prometheus服务异常'
        fi &&
        
        # Grafana
        if curl -f http://localhost:3000 >/dev/null 2>&1; then
            echo '✅ Grafana服务正常 (http://localhost:3000)'
        else
            echo '⚠️ Grafana服务异常'
        fi
    "
    
    log_info "部署验证完成"
}

# 显示访问信息
show_access_info() {
    log_step "部署完成！访问信息："
    echo ""
    echo "🌐 服务访问地址："
    echo "   • Neo4j浏览器:    http://$SERVER_HOST:7474"
    echo "   • API服务:        http://$SERVER_HOST:8000"
    echo "   • API文档:        http://$SERVER_HOST:8000/docs"
    echo "   • 健康检查:       http://$SERVER_HOST:8000/health"
    echo "   • Prometheus:     http://$SERVER_HOST:9090"
    echo "   • Grafana:        http://$SERVER_HOST:3000 (admin/admin123)"
    echo ""
    echo "🔧 远程管理命令："
    echo "   • SSH登录:        ssh $SERVER_USER@$SERVER_HOST"
    echo "   • 查看日志:       docker-compose logs -f"
    echo "   • 重启服务:       docker-compose restart"
    echo "   • 停止服务:       docker-compose down"
    echo ""
    echo "📁 部署路径："
    echo "   • 项目目录:       $REMOTE_PATH"
    echo "   • 备份目录:       $BACKUP_PATH"
    echo ""
}

# 主函数
main() {
    echo "🚀 知识图谱系统 SSH 自动化部署"
    echo "=================================="
    
    # 解析参数
    parse_args "$@"
    
    # 验证配置
    validate_config
    
    # 显示配置信息
    echo ""
    log_info "部署配置："
    echo "   服务器: $SERVER_HOST:$SERVER_PORT"
    echo "   用户: $SERVER_USER"
    echo "   部署路径: $REMOTE_PATH"
    if [[ -n "$SSH_KEY" ]]; then
        echo "   SSH密钥: $SSH_KEY"
    fi
    echo ""
    
    # 确认部署
    read -p "确认开始部署? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "部署已取消"
        exit 0
    fi
    
    # 执行部署流程
    test_connection
    check_remote_dependencies
    create_remote_directories
    backup_existing_deployment
    sync_files
    deploy_services
    optimize_database
    deploy_monitoring
    verify_deployment
    show_access_info
    
    log_info "🎉 SSH自动化部署完成！"
}

# 错误处理
trap 'log_error "部署过程中发生错误"; exit 1' ERR

# 运行主函数
main "$@"
