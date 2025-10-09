# 📁 统一数据管理方案

## 🔍 问题根源

### 发现的问题
服务器上存在**3个**dictionary.json文件，导致数据不一致：

1. `/opt/knowledge-graph/api/data/dictionary.json` - **1326条** ✅ (API使用)
2. `/opt/knowledge-graph/apps/web/src/data/dictionary.json` - **1275条** ❌ (前端打包使用，旧数据)
3. `/opt/knowledge-graph/data/vocab/dictionary.json` - **4条** ❌ (废弃文件)

### 问题表现
- 后端API返回正确数据（1326条）
- 前端显示旧数据（1275条）
- 原因：前端构建时打包了旧的`apps/web/src/data/dictionary.json`

---

## ✅ 已完成的修复

### 1. 统一数据源
```bash
# 将最新数据复制到前端源码目录
cp /opt/knowledge-graph/api/data/dictionary.json \
   /opt/knowledge-graph/apps/web/src/data/dictionary.json
```

### 2. 重新构建前端
```bash
cd /opt/knowledge-graph/apps/web
npm run build
```

### 3. 重启服务
```bash
systemctl restart nginx
systemctl restart kg-api
```

---

## 📋 统一数据管理规范

### 唯一数据源（Single Source of Truth）

**主数据文件**: `/opt/knowledge-graph/api/data/dictionary.json`

**所有其他位置的dictionary.json都应该从主数据文件同步**

### 数据更新流程

#### 方法1: 本地更新后部署（推荐）⭐

```bash
# 1. 在本地更新 d:\KG\api\data\dictionary.json

# 2. 上传到服务器主数据文件
scp api/data/dictionary.json root@47.108.152.16:/opt/knowledge-graph/api/data/

# 3. 同步到前端源码目录
ssh root@47.108.152.16 "cp /opt/knowledge-graph/api/data/dictionary.json /opt/knowledge-graph/apps/web/src/data/dictionary.json"

# 4. 同步到Neo4j
ssh root@47.108.152.16 "cd /opt/knowledge-graph && python3 sync_to_neo4j.py"

# 5. 重新构建前端
ssh root@47.108.152.16 "cd /opt/knowledge-graph/apps/web && npm run build"

# 6. 重启服务
ssh root@47.108.152.16 "systemctl restart nginx && systemctl restart kg-api"
```

#### 方法2: 服务器直接更新

```bash
# 1. SSH登录服务器
ssh root@47.108.152.16

# 2. 编辑主数据文件
cd /opt/knowledge-graph
vim api/data/dictionary.json
# 或使用Python脚本更新

# 3. 同步到前端源码目录
cp api/data/dictionary.json apps/web/src/data/dictionary.json

# 4. 同步到Neo4j
python3 sync_to_neo4j.py

# 5. 重新构建前端
cd apps/web && npm run build

# 6. 重启服务
systemctl restart nginx && systemctl restart kg-api
```

---

## 🔧 自动化同步脚本

### 创建统一更新脚本

在服务器上创建 `/opt/knowledge-graph/update_dictionary.sh`:

```bash
#!/bin/bash
# 统一词典更新脚本

set -e  # 遇到错误立即退出

echo "================================"
echo "词典数据统一更新脚本"
echo "================================"

# 主数据文件
MAIN_DATA="/opt/knowledge-graph/api/data/dictionary.json"
FRONTEND_DATA="/opt/knowledge-graph/apps/web/src/data/dictionary.json"

# 检查主数据文件是否存在
if [ ! -f "$MAIN_DATA" ]; then
    echo "❌ 错误: 主数据文件不存在: $MAIN_DATA"
    exit 1
fi

# 显示主数据文件信息
ENTRY_COUNT=$(python3 -c "import json; print(len(json.load(open('$MAIN_DATA'))))")
echo "📊 主数据文件: $ENTRY_COUNT 条"

# 1. 备份现有数据
echo ""
echo "1️⃣ 备份现有数据..."
BACKUP_DIR="/opt/knowledge-graph/backups"
mkdir -p "$BACKUP_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
cp "$MAIN_DATA" "$BACKUP_DIR/dictionary_backup_$TIMESTAMP.json"
echo "✅ 备份完成: $BACKUP_DIR/dictionary_backup_$TIMESTAMP.json"

# 2. 同步到前端源码目录
echo ""
echo "2️⃣ 同步到前端源码目录..."
cp "$MAIN_DATA" "$FRONTEND_DATA"
echo "✅ 同步完成: $FRONTEND_DATA"

# 3. 同步到Neo4j
echo ""
echo "3️⃣ 同步到Neo4j图谱..."
cd /opt/knowledge-graph
python3 sync_to_neo4j.py
echo "✅ Neo4j同步完成"

# 4. 重新构建前端
echo ""
echo "4️⃣ 重新构建前端..."
cd /opt/knowledge-graph/apps/web
npm run build > /dev/null 2>&1
echo "✅ 前端构建完成"

# 5. 重启服务
echo ""
echo "5️⃣ 重启服务..."
systemctl restart nginx
systemctl restart kg-api
sleep 2
echo "✅ 服务重启完成"

# 6. 验证
echo ""
echo "6️⃣ 验证更新..."
API_COUNT=$(curl -s http://localhost:8000/kg/dictionary | python3 -c "import sys, json; print(json.load(sys.stdin).get('total', 0))")
echo "✅ API返回: $API_COUNT 条"

echo ""
echo "================================"
echo "✅ 更新完成！"
echo "================================"
echo "主数据: $ENTRY_COUNT 条"
echo "API返回: $API_COUNT 条"
echo ""
echo "请在浏览器中按 Ctrl+Shift+R 强制刷新页面"
```

### 使用方法

```bash
# 1. 创建脚本
ssh root@47.108.152.16 "cat > /opt/knowledge-graph/update_dictionary.sh" < update_dictionary.sh

# 2. 添加执行权限
ssh root@47.108.152.16 "chmod +x /opt/knowledge-graph/update_dictionary.sh"

# 3. 执行更新
ssh root@47.108.152.16 "/opt/knowledge-graph/update_dictionary.sh"
```

---

## 🎯 验证数据一致性

### 检查脚本

```bash
#!/bin/bash
# 检查所有dictionary.json文件的一致性

echo "检查所有dictionary.json文件:"
echo ""

for file in $(find /opt/knowledge-graph -name "dictionary.json" -type f); do
    count=$(python3 -c "import json; print(len(json.load(open('$file'))))" 2>/dev/null || echo "错误")
    size=$(ls -lh "$file" | awk '{print $5}')
    date=$(ls -l "$file" | awk '{print $6, $7, $8}')
    echo "文件: $file"
    echo "  条目数: $count"
    echo "  大小: $size"
    echo "  修改时间: $date"
    echo ""
done
```

---

## 📊 当前状态

### 修复后的文件状态

```
/opt/knowledge-graph/api/data/dictionary.json
  条目数: 1326 ✅
  大小: 632K
  修改时间: Oct 6 02:16

/opt/knowledge-graph/apps/web/src/data/dictionary.json
  条目数: 1326 ✅
  大小: 632K
  修改时间: Oct 6 02:16

/opt/knowledge-graph/data/vocab/dictionary.json
  条目数: 4 (废弃文件，可删除)
```

### 服务状态

```
✅ Nginx: 运行中
✅ kg-api: 运行中 (PID: 71526)
✅ Neo4j: 1331个Term节点
```

---

## 🔄 后续更新流程

### 每次更新词典数据时：

1. **本地更新**: 编辑 `d:\KG\api\data\dictionary.json`

2. **运行统一更新脚本**:
   ```bash
   # 上传主数据文件
   scp api/data/dictionary.json root@47.108.152.16:/opt/knowledge-graph/api/data/
   
   # 执行统一更新脚本
   ssh root@47.108.152.16 "/opt/knowledge-graph/update_dictionary.sh"
   ```

3. **浏览器强制刷新**: `Ctrl + Shift + R`

---

## 💡 最佳实践

### 1. 单一数据源原则
- **主数据文件**: `/opt/knowledge-graph/api/data/dictionary.json`
- 所有其他位置的文件都从主数据文件同步

### 2. 版本控制
- 每次更新前自动备份到 `/opt/knowledge-graph/backups/`
- 备份文件命名: `dictionary_backup_YYYYMMDD_HHMMSS.json`

### 3. 自动化部署
- 使用统一更新脚本，避免手动操作遗漏
- 脚本包含验证步骤，确保更新成功

### 4. 数据验证
- 更新后检查API返回的total
- 检查Neo4j节点数量
- 前端强制刷新验证

---

## 🎉 总结

### 问题
- 3个dictionary.json文件不一致
- 前端显示1275条，后端1326条

### 解决方案
- ✅ 统一数据源到 `/opt/knowledge-graph/api/data/dictionary.json`
- ✅ 同步到前端源码目录
- ✅ 重新构建前端
- ✅ 重启服务

### 验证
- ✅ 主数据文件: 1326条
- ✅ 前端源码文件: 1326条
- ✅ API返回: 1326条
- ✅ Neo4j: 1331个Term节点

### 后续
- 使用统一更新脚本
- 保持单一数据源原则
- 每次更新后验证一致性

---

**🎯 现在请在浏览器中按 `Ctrl + Shift + R` 强制刷新，应该能看到正确的1326条数据！**

