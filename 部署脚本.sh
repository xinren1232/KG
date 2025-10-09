#!/bin/bash
# 知识图谱系统生产环境部署脚本

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查是否为root用户
check_root() {
    if [[ $EUID -eq 0 ]]; then
        log_error "请不要使用root用户运行此脚本"
        exit 1
    fi
}

# 检查系统要求
check_system_requirements() {
    log_info "检查系统要求..."
    
    # 检查操作系统
    if [[ ! -f /etc/os-release ]]; then
        log_error "不支持的操作系统"
        exit 1
    fi
    
    # 检查内存
    MEMORY_GB=$(free -g | awk '/^Mem:/{print $2}')
    if [[ $MEMORY_GB -lt 8 ]]; then
        log_warning "建议内存至少8GB，当前: ${MEMORY_GB}GB"
    fi
    
    # 检查磁盘空间
    DISK_GB=$(df -BG / | awk 'NR==2{print $4}' | sed 's/G//')
    if [[ $DISK_GB -lt 50 ]]; then
        log_warning "建议磁盘空间至少50GB，当前可用: ${DISK_GB}GB"
    fi
    
    log_success "系统要求检查完成"
}

# 安装Docker和Docker Compose
install_docker() {
    log_info "安装Docker和Docker Compose..."
    
    # 检查Docker是否已安装
    if command -v docker &> /dev/null; then
        log_info "Docker已安装，版本: $(docker --version)"
    else
        log_info "安装Docker..."
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
        sudo usermod -aG docker $USER
        rm get-docker.sh
        log_success "Docker安装完成"
    fi
    
    # 检查Docker Compose是否已安装
    if command -v docker-compose &> /dev/null; then
        log_info "Docker Compose已安装，版本: $(docker-compose --version)"
    else
        log_info "安装Docker Compose..."
        sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
        log_success "Docker Compose安装完成"
    fi
}

# 创建目录结构
create_directories() {
    log_info "创建目录结构..."
    
    # 创建主目录
    sudo mkdir -p /opt/kg/{data,logs,backup,config,ssl,cache,import}
    
    # 创建子目录
    sudo mkdir -p /opt/kg/data/{neo4j,redis,uploads,minio,prometheus,grafana}
    sudo mkdir -p /opt/kg/logs/{neo4j,api,nginx}
    sudo mkdir -p /opt/kg/cache/nginx
    
    # 设置权限
    sudo chown -R $USER:$USER /opt/kg
    chmod -R 755 /opt/kg
    
    log_success "目录结构创建完成"
}

# 配置防火墙
configure_firewall() {
    log_info "配置防火墙..."
    
    if command -v ufw &> /dev/null; then
        sudo ufw --force enable
        sudo ufw allow 22/tcp    # SSH
        sudo ufw allow 80/tcp    # HTTP
        sudo ufw allow 443/tcp   # HTTPS
        log_success "防火墙配置完成"
    else
        log_warning "未找到ufw，请手动配置防火墙"
    fi
}

# 备份现有数据
backup_existing_data() {
    log_info "备份现有数据..."
    
    BACKUP_DIR="/opt/kg/backup/migration_$(date +%Y%m%d_%H%M%S)"
    mkdir -p $BACKUP_DIR
    
    # 备份Neo4j数据 (如果存在)
    if [[ -d "./neo4j_standalone/data" ]]; then
        log_info "备份Neo4j数据..."
        cp -r ./neo4j_standalone/data $BACKUP_DIR/neo4j_data
    fi
    
    # 备份应用数据
    if [[ -d "./data" ]]; then
        log_info "备份应用数据..."
        cp -r ./data $BACKUP_DIR/app_data
    fi
    
    # 备份上传文件
    if [[ -d "./api/uploads" ]]; then
        log_info "备份上传文件..."
        cp -r ./api/uploads $BACKUP_DIR/uploads
    fi
    
    # 创建备份清单
    find $BACKUP_DIR -type f -exec sha256sum {} \; > $BACKUP_DIR/checksums.txt
    
    log_success "数据备份完成: $BACKUP_DIR"
}

# 生成SSL证书 (自签名，生产环境建议使用Let's Encrypt)
generate_ssl_certificate() {
    log_info "生成SSL证书..."
    
    SSL_DIR="/opt/kg/ssl"
    
    if [[ ! -f "$SSL_DIR/cert.pem" ]]; then
        log_info "生成自签名SSL证书..."
        sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout $SSL_DIR/key.pem \
            -out $SSL_DIR/cert.pem \
            -subj "/C=CN/ST=State/L=City/O=Organization/CN=localhost"
        
        sudo chown $USER:$USER $SSL_DIR/*
        log_success "SSL证书生成完成"
        log_warning "生产环境请使用Let's Encrypt或购买的SSL证书"
    else
        log_info "SSL证书已存在"
    fi
}

# 创建配置文件
create_config_files() {
    log_info "创建配置文件..."
    
    # 创建Neo4j配置
    cat > /opt/kg/config/neo4j.conf << 'EOF'
# Neo4j生产环境配置
server.memory.heap.initial_size=2g
server.memory.heap.max_size=4g
server.memory.pagecache.size=2g
server.bolt.thread_pool_min_size=5
server.bolt.thread_pool_max_size=400
server.bolt.connection_keep_alive=60s
cypher.default_language_version=5
cypher.hints_error=true
db.transaction.timeout=60s
server.default_listen_address=0.0.0.0
server.bolt.listen_address=:7687
server.http.listen_address=:7474
server.logs.user.stdout_enabled=true
server.logs.debug.level=WARN
EOF
    
    # 创建Redis配置
    cat > /opt/kg/config/redis.conf << 'EOF'
# Redis生产环境配置
maxmemory 2gb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
appendonly yes
appendfsync everysec
EOF
    
    # 创建API配置
    cat > /opt/kg/config/api_config.json << 'EOF'
{
    "environment": "production",
    "debug": false,
    "log_level": "INFO",
    "max_workers": 4,
    "upload_max_size": "100MB",
    "cache_ttl": 300,
    "database": {
        "neo4j_uri": "bolt://neo4j:7687",
        "redis_url": "redis://redis:6379"
    },
    "security": {
        "cors_origins": ["https://your-domain.com"],
        "rate_limit": {
            "requests_per_minute": 60
        }
    }
}
EOF
    
    log_success "配置文件创建完成"
}

# 构建和启动服务
deploy_services() {
    log_info "构建和启动服务..."
    
    # 复制配置文件到项目目录
    cp /opt/kg/config/neo4j.conf ./config/
    cp /opt/kg/ssl/* ./nginx/ssl/ 2>/dev/null || true
    
    # 构建镜像
    log_info "构建Docker镜像..."
    docker-compose -f docker-compose.prod.yml build
    
    # 启动服务
    log_info "启动服务..."
    docker-compose -f docker-compose.prod.yml up -d
    
    # 等待服务启动
    log_info "等待服务启动..."
    sleep 30
    
    log_success "服务部署完成"
}

# 验证部署
verify_deployment() {
    log_info "验证部署..."
    
    # 检查容器状态
    log_info "检查容器状态..."
    docker-compose -f docker-compose.prod.yml ps
    
    # 检查服务健康状态
    services=("neo4j" "redis" "api" "nginx")
    
    for service in "${services[@]}"; do
        if docker-compose -f docker-compose.prod.yml ps $service | grep -q "Up"; then
            log_success "$service 服务运行正常"
        else
            log_error "$service 服务启动失败"
            docker-compose -f docker-compose.prod.yml logs $service
        fi
    done
    
    # 测试API连接
    log_info "测试API连接..."
    sleep 10
    if curl -f http://localhost:8000/health &> /dev/null; then
        log_success "API服务响应正常"
    else
        log_error "API服务无响应"
    fi
    
    # 测试前端访问
    log_info "测试前端访问..."
    if curl -f http://localhost/ &> /dev/null; then
        log_success "前端服务响应正常"
    else
        log_error "前端服务无响应"
    fi
}

# 显示部署信息
show_deployment_info() {
    log_success "部署完成！"
    echo
    echo "=== 服务访问地址 ==="
    echo "前端界面: http://localhost (或 https://localhost)"
    echo "API服务: http://localhost:8000"
    echo "Neo4j浏览器: http://localhost:7474"
    echo "MinIO控制台: http://localhost:9001"
    echo "Prometheus: http://localhost:9090"
    echo "Grafana: http://localhost:3000"
    echo
    echo "=== 默认账号密码 ==="
    echo "Neo4j: neo4j / KG_Production_2024!"
    echo "MinIO: kg_admin / KG_MinIO_2024!"
    echo "Grafana: admin / KG_Grafana_2024!"
    echo
    echo "=== 重要提醒 ==="
    echo "1. 请修改所有默认密码"
    echo "2. 配置域名和正式SSL证书"
    echo "3. 设置监控告警"
    echo "4. 定期备份数据"
    echo
    echo "=== 常用命令 ==="
    echo "查看服务状态: docker-compose -f docker-compose.prod.yml ps"
    echo "查看日志: docker-compose -f docker-compose.prod.yml logs [service]"
    echo "重启服务: docker-compose -f docker-compose.prod.yml restart [service]"
    echo "停止服务: docker-compose -f docker-compose.prod.yml down"
}

# 主函数
main() {
    log_info "开始知识图谱系统生产环境部署"
    echo
    
    check_root
    check_system_requirements
    install_docker
    create_directories
    configure_firewall
    backup_existing_data
    generate_ssl_certificate
    create_config_files
    deploy_services
    verify_deployment
    show_deployment_info
    
    log_success "部署流程完成！"
}

# 执行主函数
main "$@"
