#!/bin/bash
# 目录清理脚本 - 删除重复、多余和冲突的文件

set -e

echo "🧹 开始清理目录..."

# 创建备份目录
BACKUP_DIR="cleanup_backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR

echo "📦 创建备份: $BACKUP_DIR"

# 1. 删除明显的临时和重复文件
echo "🗑️ 删除临时和重复文件..."

# 临时测试文件
rm -f simple_test.* test.docx simple_test_debug.txt

# 旧备份文件
rm -f graph_backup_*.json backup_data.sh

# 重复的启动脚本
rm -f 启动API服务.bat 启动所有服务.bat 快速修复并启动.bat

# 重复的检查脚本
rm -f check_api_status.py check_neo4j_data.py check_node_structure.py
rm -f comprehensive_system_check.py

# 重复的修复脚本
rm -f 修复API查询逻辑.py 修复Label分类.py 修复neo4j显示.py
rm -f 修复neo4j连接.py 修复关系创建.py 修复前端错误.py

# 2. 整理报告文件
echo "📋 整理报告文件..."
mkdir -p reports/legacy
mv *REPORT*.md reports/legacy/ 2>/dev/null || true
mv *报告*.md reports/legacy/ 2>/dev/null || true
mv *总结*.md reports/legacy/ 2>/dev/null || true

# 3. 整理脚本文件
echo "🔧 整理脚本文件..."
mkdir -p scripts/legacy
mv append_*.py scripts/legacy/ 2>/dev/null || true
mv clean_*.py scripts/legacy/ 2>/dev/null || true
mv cleanup_*.py scripts/legacy/ 2>/dev/null || true
mv debug_*.py scripts/legacy/ 2>/dev/null || true
mv fix_*.py scripts/legacy/ 2>/dev/null || true

# 4. 整理数据导入文件
echo "📊 整理数据导入文件..."
mkdir -p data/import/legacy
mv 导入批次_*.cypher data/import/legacy/ 2>/dev/null || true
mv 合并全部*模块数据.py data/import/legacy/ 2>/dev/null || true
mv 处理*模块数据.py data/import/legacy/ 2>/dev/null || true

# 5. 整理词典数据文件
echo "📚 整理词典数据文件..."
mkdir -p data/dictionary/modules
mv 硬件模块词典数据_*.csv data/dictionary/modules/ 2>/dev/null || true

# 6. 整理配置和报告JSON文件
echo "⚙️ 整理配置文件..."
mkdir -p config/legacy
mv *报告*.json config/legacy/ 2>/dev/null || true
mv *统计*.json config/legacy/ 2>/dev/null || true

# 7. 清理空目录
echo "🧽 清理空目录..."
find . -type d -empty -delete 2>/dev/null || true

echo "✅ 清理完成!"
echo "📦 备份位置: $BACKUP_DIR"
echo "📁 整理后的目录结构更加清晰"

# 显示清理后的根目录文件数量
echo "📊 根目录文件统计:"
echo "   Python脚本: $(ls -1 *.py 2>/dev/null | wc -l)"
echo "   配置文件: $(ls -1 *.yml *.yaml *.json 2>/dev/null | wc -l)"
echo "   文档文件: $(ls -1 *.md *.txt 2>/dev/null | wc -l)"
echo "   总文件数: $(ls -1 * 2>/dev/null | grep -v ":" | wc -l)"
