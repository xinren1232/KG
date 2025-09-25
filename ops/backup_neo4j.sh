#!/bin/bash

# Neo4j 数据库备份脚本
# 使用 neo4j-admin database dump 命令进行备份

set -e

# 配置参数
BACKUP_DIR="${BACKUP_DIR:-./backups}"
NEO4J_CONTAINER="${NEO4J_CONTAINER:-kg_neo4j}"
DATABASE_NAME="${DATABASE_NAME:-neo4j}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/neo4j_backup_${TIMESTAMP}.dump"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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

# 检查Docker是否运行
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        log_error "Docker is not running"
        exit 1
    fi
}

# 检查Neo4j容器是否运行
check_neo4j_container() {
    if ! docker ps | grep -q "$NEO4J_CONTAINER"; then
        log_error "Neo4j container '$NEO4J_CONTAINER' is not running"
        exit 1
    fi
}

# 创建备份目录
create_backup_dir() {
    if [ ! -d "$BACKUP_DIR" ]; then
        log_info "Creating backup directory: $BACKUP_DIR"
        mkdir -p "$BACKUP_DIR"
    fi
}

# 执行备份
perform_backup() {
    log_info "Starting Neo4j database backup..."
    log_info "Database: $DATABASE_NAME"
    log_info "Container: $NEO4J_CONTAINER"
    log_info "Backup file: $BACKUP_FILE"
    
    # 停止数据库（可选，对于在线备份可以跳过）
    log_info "Stopping database for backup..."
    docker exec "$NEO4J_CONTAINER" cypher-shell -u neo4j -p "${NEO4J_PASS:-password123}" \
        "STOP DATABASE $DATABASE_NAME" || log_warn "Failed to stop database (may already be stopped)"
    
    # 执行备份
    log_info "Creating database dump..."
    docker exec "$NEO4J_CONTAINER" neo4j-admin database dump \
        --database="$DATABASE_NAME" \
        --to-path="/var/lib/neo4j/import" \
        --overwrite-destination=true \
        "backup_${TIMESTAMP}.dump"
    
    # 复制备份文件到主机
    log_info "Copying backup file to host..."
    docker cp "$NEO4J_CONTAINER:/var/lib/neo4j/import/backup_${TIMESTAMP}.dump" "$BACKUP_FILE"
    
    # 重启数据库
    log_info "Starting database..."
    docker exec "$NEO4J_CONTAINER" cypher-shell -u neo4j -p "${NEO4J_PASS:-password123}" \
        "START DATABASE $DATABASE_NAME" || log_warn "Failed to start database"
    
    # 验证备份文件
    if [ -f "$BACKUP_FILE" ]; then
        BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
        log_info "Backup completed successfully!"
        log_info "Backup file: $BACKUP_FILE"
        log_info "Backup size: $BACKUP_SIZE"
    else
        log_error "Backup file not found: $BACKUP_FILE"
        exit 1
    fi
}

# 清理旧备份
cleanup_old_backups() {
    local keep_days=${KEEP_DAYS:-7}
    log_info "Cleaning up backups older than $keep_days days..."
    
    find "$BACKUP_DIR" -name "neo4j_backup_*.dump" -type f -mtime +$keep_days -delete
    
    local remaining_count=$(find "$BACKUP_DIR" -name "neo4j_backup_*.dump" -type f | wc -l)
    log_info "Remaining backup files: $remaining_count"
}

# 显示帮助信息
show_help() {
    cat << EOF
Neo4j Database Backup Script

Usage: $0 [OPTIONS]

Options:
    -h, --help              Show this help message
    -d, --database NAME     Database name (default: neo4j)
    -c, --container NAME    Container name (default: kg_neo4j)
    -b, --backup-dir DIR    Backup directory (default: ./backups)
    -k, --keep-days DAYS    Keep backups for N days (default: 7)
    --no-cleanup           Skip cleanup of old backups

Environment Variables:
    NEO4J_CONTAINER        Neo4j container name
    NEO4J_PASS            Neo4j password
    BACKUP_DIR            Backup directory
    KEEP_DAYS             Days to keep backups

Examples:
    $0                                          # Basic backup
    $0 -d mydb -c my_neo4j                     # Custom database and container
    $0 -b /path/to/backups -k 30               # Custom backup dir and retention
    $0 --no-cleanup                            # Skip cleanup

EOF
}

# 解析命令行参数
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -d|--database)
                DATABASE_NAME="$2"
                shift 2
                ;;
            -c|--container)
                NEO4J_CONTAINER="$2"
                shift 2
                ;;
            -b|--backup-dir)
                BACKUP_DIR="$2"
                shift 2
                ;;
            -k|--keep-days)
                KEEP_DAYS="$2"
                shift 2
                ;;
            --no-cleanup)
                NO_CLEANUP=true
                shift
                ;;
            *)
                log_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

# 主函数
main() {
    parse_args "$@"
    
    log_info "=== Neo4j Database Backup ==="
    log_info "Timestamp: $(date)"
    
    check_docker
    check_neo4j_container
    create_backup_dir
    perform_backup
    
    if [ "$NO_CLEANUP" != "true" ]; then
        cleanup_old_backups
    fi
    
    log_info "=== Backup Process Completed ==="
}

# 执行主函数
main "$@"
