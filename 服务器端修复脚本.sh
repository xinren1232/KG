#!/bin/bash
# 服务器端图谱可视化修复脚本
# 在服务器上执行此脚本

set -e  # 遇到错误立即退出

echo "============================================================"
echo "🚀 图谱可视化修复脚本"
echo "============================================================"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 项目路径
PROJECT_DIR="/root/KG"
VUE_FILE="$PROJECT_DIR/apps/web/src/views/GraphVisualization.vue"
BACKUP_FILE="$VUE_FILE.backup.$(date +%Y%m%d_%H%M%S)"

# 检查文件是否存在
if [ ! -f "$VUE_FILE" ]; then
    echo -e "${RED}❌ 文件不存在: $VUE_FILE${NC}"
    exit 1
fi

# 备份当前文件
echo -e "\n${YELLOW}📦 备份当前文件...${NC}"
cp "$VUE_FILE" "$BACKUP_FILE"
echo -e "${GREEN}✅ 备份完成: $BACKUP_FILE${NC}"

# 检查关键配置
echo -e "\n${YELLOW}🔍 检查当前配置...${NC}"

# 检查颜色配置
if grep -q "categoryColors = {" "$VUE_FILE"; then
    echo -e "${GREEN}✅ 找到颜色配置${NC}"
    
    # 检查是否有完整的颜色定义
    color_count=$(grep -c "'#[0-9A-F]\{6\}'" "$VUE_FILE" || true)
    echo "   颜色定义数量: $color_count"
    
    if [ "$color_count" -lt 10 ]; then
        echo -e "${RED}⚠️  颜色定义不完整（应该有10个）${NC}"
    fi
else
    echo -e "${RED}❌ 未找到颜色配置${NC}"
fi

# 检查标签显示配置
if grep -q "label: {" "$VUE_FILE" && grep -q "show: true" "$VUE_FILE"; then
    echo -e "${GREEN}✅ 标签配置正确${NC}"
else
    echo -e "${RED}❌ 标签配置可能有问题${NC}"
fi

# 检查图例配置
if grep -q "legend: \[{" "$VUE_FILE"; then
    echo -e "${GREEN}✅ 找到图例配置${NC}"
else
    echo -e "${RED}❌ 图例配置可能有问题${NC}"
fi

# 提示用户
echo -e "\n${YELLOW}============================================================${NC}"
echo -e "${YELLOW}⚠️  重要提示${NC}"
echo -e "${YELLOW}============================================================${NC}"
echo "此脚本将检查并提示需要修复的配置。"
echo "如果需要完整替换文件，请："
echo "1. 从本地上传完整的 GraphVisualization.vue 文件"
echo "2. 或者手动编辑文件修复配置"
echo ""
echo "本地文件路径: d:\\KG\\apps\\web\\src\\views\\GraphVisualization.vue"
echo "服务器文件路径: $VUE_FILE"
echo ""

# 询问是否继续
read -p "是否继续重新构建前端？(y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}⏸️  操作已取消${NC}"
    exit 0
fi

# 重新构建前端
echo -e "\n${YELLOW}🔨 重新构建前端...${NC}"
cd "$PROJECT_DIR/apps/web"

# 清理旧的构建
if [ -d "dist" ]; then
    echo "清理旧的构建文件..."
    rm -rf dist
fi

# 执行构建
echo "开始构建..."
npm run build

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 构建成功${NC}"
else
    echo -e "${RED}❌ 构建失败${NC}"
    exit 1
fi

# 重启前端服务
echo -e "\n${YELLOW}🔄 重启前端服务...${NC}"
systemctl restart kg-frontend

# 等待服务启动
sleep 3

# 检查服务状态
echo -e "\n${YELLOW}📊 检查服务状态...${NC}"
systemctl status kg-frontend --no-pager | head -20

# 检查端口
if netstat -tuln | grep -q ":5173"; then
    echo -e "${GREEN}✅ 前端服务正在运行（端口5173）${NC}"
else
    echo -e "${RED}❌ 前端服务未在端口5173上监听${NC}"
fi

# 完成
echo -e "\n${GREEN}============================================================${NC}"
echo -e "${GREEN}✅ 修复脚本执行完成${NC}"
echo -e "${GREEN}============================================================${NC}"
echo ""
echo "下一步："
echo "1. 访问: http://47.97.161.175:5173"
echo "2. 检查图谱可视化页面"
echo "3. 验证以下特性："
echo "   - 节点显示不同颜色"
echo "   - 较大节点显示名称标签"
echo "   - 右侧显示完整图例"
echo "   - 节点大小根据连接数变化"
echo ""
echo "如果问题仍然存在，请："
echo "1. 检查浏览器控制台错误"
echo "2. 查看服务日志: journalctl -u kg-frontend -n 100"
echo "3. 确认文件已正确上传: $VUE_FILE"
echo ""
echo "备份文件位置: $BACKUP_FILE"
echo ""

