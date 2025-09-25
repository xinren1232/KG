#!/bin/bash

# Neo4j 数据库恢复脚本
# 使用 neo4j-admin database load 命令进行恢复

set -e

# 配置参数
BACKUP_DIR="${BACKUP_DIR:-./backups}"
NEO4J_CONTAINER="${NEO4J_CONTAINER:-kg_neo4j}"
DATABASE_NAME="${DATABASE_NAME:-neo4j}"
BACKUP_FILE=""

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

# 列出可用的备份文件
list_backups() {
    log_info "Available backup files in $BACKUP_DIR:"
    if [ -d "$BACKUP_DIR" ]; then
        local backups=($(find "$BACKUP_DIR" -name "neo4j_backup_*.dump" -type f | sort -r))
        if [ ${#backups[@]} -eq 0 ]; then
            log_warn "No backup files found in $BACKUP_DIR"
            return 1
        fi
        
        for i in "${!backups[@]}"; do
            local file="${backups[$i]}"
            local size=$(du -h "$file" | cut -f1)
            local date=$(stat -c %y "$file" | cut -d' ' -f1,2 | cut -d'.' -f1)
            printf "%2d) %s (%s, %s)\n" $((i+1)) "$(basename "$file")" "$size" "$date"
        done
        return 0
    else
        log_error "Backup directory does not exist: $BACKUP_DIR"
        return 1
    fi
}

# 选择备份文件
select_backup() {
    if [ -n "$BACKUP_FILE" ]; then
        if [ ! -f "$BACKUP_FILE" ]; then
            log_error "Backup file not found: $BACKUP_FILE"
            exit 1
        fi
        return 0
    fi
    
    list_backups || exit 1
    
    echo
    read -p "Select backup file number (or 'q' to quit): " selection
    
    if [ "$selection" = "q" ] || [ "$selection" = "Q" ]; then
        log_info "Restore cancelled by user"
        exit 0
    fi
    
    local backups=($(find "$BACKUP_DIR" -name "neo4j_backup_*.dump" -type f | sort -r))
    local index=$((selection - 1))
    
    if [ $index -ge 0 ] && [ $index -lt ${#backups[@]} ]; then
        BACKUP_FILE="${backups[$index]}"
        log_info "Selected backup file: $BACKUP_FILE"
    else
        log_error "Invalid selection: $selection"
        exit 1
    fi
}

# 确认恢复操作
confirm_restore() {
    log_warn "WARNING: This operation will replace the current database!"
    log_warn "Database: $DATABASE_NAME"
    log_warn "Container: $NEO4J_CONTAINER"
    log_warn "Backup file: $BACKUP_FILE"
    echo
    read -p "Are you sure you want to continue? (yes/no): " confirmation
    
    if [ "$confirmation" != "yes" ]; then
        log_info "Restore cancelled by user"
        exit 0
    fi
}

# 执行恢复
perform_restore() {
    log_info "Starting Neo4j database restore..."
    
    local backup_filename=$(basename "$BACKUP_FILE")
    local container_backup_path="/var/lib/neo4j/import/$backup_filename"
    
    # 复制备份文件到容器
    log_info "Copying backup file to container..."
    docker cp "$BACKUP_FILE" "$NEO4J_CONTAINER:$container_backup_path"
    
    # 停止数据库
    log_info "Stopping database..."
    docker exec "$NEO4J_CONTAINER" cypher-shell -u neo4j -p "${NEO4J_PASS:-password123}" \
        "STOP DATABASE $DATABASE_NAME" || log_warn "Failed to stop database (may already be stopped)"
    
    # 删除现有数据库
    log_info "Dropping existing database..."
    docker exec "$NEO4J_CONTAINER" cypher-shell -u neo4j -p "${NEO4J_PASS:-password123}" \
        "DROP DATABASE $DATABASE_NAME IF EXISTS" || log_warn "Failed to drop database"
    
    # 恢复数据库
    log_info "Loading database from backup..."
    docker exec "$NEO4J_CONTAINER" neo4j-admin database load \
        --from-path="/var/lib/neo4j/import" \
        --database="$DATABASE_NAME" \
        --overwrite-destination=true \
        "$backup_filename"
    
    # 创建数据库
    log_info "Creating database..."
    docker exec "$NEO4J_CONTAINER" cypher-shell -u neo4j -p "${NEO4J_PASS:-password123}" \
        "CREATE DATABASE $DATABASE_NAME IF NOT EXISTS"
    
    # 启动数据库
    log_info "Starting database..."
    docker exec "$NEO4J_CONTAINER" cypher-shell -u neo4j -p "${NEO4J_PASS:-password123}" \
        "START DATABASE $DATABASE_NAME"
    
    # 清理容器中的备份文件
    log_info "Cleaning up temporary files..."
    docker exec "$NEO4J_CONTAINER" rm -f "$container_backup_path"
    
    log_info "Database restore completed successfully!"
}

# 验证恢复结果
verify_restore() {
    log_info "Verifying database restore..."
    
    # 等待数据库启动
    sleep 5
    
    # 检查数据库状态
    local status=$(docker exec "$NEO4J_CONTAINER" cypher-shell -u neo4j -p "${NEO4J_PASS:-password123}" \
        "SHOW DATABASES YIELD name, currentStatus WHERE name = '$DATABASE_NAME' RETURN currentStatus" 2>/dev/null | tail -n +2 | head -n 1 | tr -d '"')
    
    if [ "$status" = "online" ]; then
        log_info "Database is online and ready"
        
        # 获取节点和关系数量
        local node_count=$(docker exec "$NEO4J_CONTAINER" cypher-shell -u neo4j -p "${NEO4J_PASS:-password123}" \
            -d "$DATABASE_NAME" "MATCH (n) RETURN count(n)" 2>/dev/null | tail -n +2 | head -n 1)
        local rel_count=$(docker exec "$NEO4J_CONTAINER" cypher-shell -u neo4j -p "${NEO4J_PASS:-password123}" \
            -d "$DATABASE_NAME" "MATCH ()-[r]->() RETURN count(r)" 2>/dev/null | tail -n +2 | head -n 1)
        
        log_info "Database statistics:"
        log_info "  Nodes: ${node_count:-0}"
        log_info "  Relationships: ${rel_count:-0}"
    else
        log_warn "Database status: $status"
    fi
}

# 显示帮助信息
show_help() {
    cat << EOF
Neo4j Database Restore Script

Usage: $0 [OPTIONS]

Options:
    -h, --help              Show this help message
    -f, --file FILE         Backup file to restore
    -d, --database NAME     Database name (default: neo4j)
    -c, --container NAME    Container name (default: kg_neo4j)
    -b, --backup-dir DIR    Backup directory (default: ./backups)
    -l, --list              List available backup files and exit
    --force                 Skip confirmation prompt

Environment Variables:
    NEO4J_CONTAINER        Neo4j container name
    NEO4J_PASS            Neo4j password
    BACKUP_DIR            Backup directory

Examples:
    $0                                          # Interactive restore
    $0 -l                                       # List available backups
    $0 -f /path/to/backup.dump                 # Restore specific file
    $0 -d mydb -c my_neo4j                     # Custom database and container
    $0 --force                                  # Skip confirmation

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
            -f|--file)
                BACKUP_FILE="$2"
                shift 2
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
            -l|--list)
                LIST_ONLY=true
                shift
                ;;
            --force)
                FORCE=true
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
    
    if [ "$LIST_ONLY" = "true" ]; then
        list_backups
        exit 0
    fi
    
    log_info "=== Neo4j Database Restore ==="
    log_info "Timestamp: $(date)"
    
    check_docker
    check_neo4j_container
    select_backup
    
    if [ "$FORCE" != "true" ]; then
        confirm_restore
    fi
    
    perform_restore
    verify_restore
    
    log_info "=== Restore Process Completed ==="
}

# 执行主函数
main "$@"
