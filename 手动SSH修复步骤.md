# 手动SSH修复步骤

由于需要SSH密码，请按照以下步骤手动执行：

## 步骤1：登录服务器

打开命令行工具（CMD、PowerShell或Git Bash），执行：

```bash
ssh root@47.108.152.16
```

输入密码后登录。

---

## 步骤2：进入项目目录

```bash
cd /opt/kg
```

---

## 步骤3：检查当前容器状态

```bash
docker-compose -f docker-compose.prod.yml ps
```

**查看输出**，记录哪些容器的状态不是 `Up`。

---

## 步骤4：查看API日志（找出错误原因）

```bash
docker-compose -f docker-compose.prod.yml logs api --tail=50
```

**重点查看**：
- 是否有 `redis` 相关错误
- 是否有 `neo4j` 相关错误
- 是否有 `ModuleNotFoundError` 错误
- 是否有 `FileNotFoundError` 错误

把错误信息记录下来。

---

## 步骤5：执行修复

### 方案A：快速重启（推荐先试这个）

```bash
# 重启Redis
docker-compose -f docker-compose.prod.yml restart redis

# 等待3秒
sleep 3

# 重启API
docker-compose -f docker-compose.prod.yml restart api

# 等待5秒
sleep 5

# 检查状态
docker-compose -f docker-compose.prod.yml ps
```

### 方案B：如果方案A不行，完全重启

```bash
# 停止所有服务
docker-compose -f docker-compose.prod.yml down

# 重新启动
docker-compose -f docker-compose.prod.yml up -d

# 查看启动日志
docker-compose -f docker-compose.prod.yml logs -f
```

按 `Ctrl+C` 退出日志查看。

---

## 步骤6：验证修复

### 6.1 检查容器状态

```bash
docker-compose -f docker-compose.prod.yml ps
```

所有容器应该显示 `Up`。

### 6.2 测试API健康检查

```bash
docker exec kg_api_prod curl -s http://localhost:8000/health
```

应该返回类似：
```json
{"status": "healthy"}
```

### 6.3 测试real-stats端点

```bash
docker exec kg_api_prod curl -s http://localhost:8000/kg/real-stats | head -c 500
```

应该返回JSON数据，包含 `"ok": true` 或 `"success": true`。

### 6.4 从外部测试

```bash
curl http://localhost/api/kg/real-stats | head -c 500
```

---

## 步骤7：在浏览器中验证

打开浏览器访问：
- http://47.108.152.16/

按 `F12` 打开开发者工具，查看Console：
- ✅ 应该看到 `最终统计数据` 而不是 `真实统计API不可用`
- ✅ Network标签中 `/api/kg/real-stats` 应该返回 `200` 而不是 `502`

---

## 常见错误及解决方案

### 错误1：Redis连接失败

**日志显示**：
```
redis.exceptions.ConnectionError: Error connecting to Redis
```

**解决**：
```bash
docker-compose -f docker-compose.prod.yml restart redis
sleep 3
docker-compose -f docker-compose.prod.yml restart api
```

### 错误2：Neo4j连接失败

**日志显示**：
```
neo4j.exceptions.ServiceUnavailable
```

**解决**：
```bash
docker-compose -f docker-compose.prod.yml restart neo4j
sleep 10
docker-compose -f docker-compose.prod.yml restart api
```

### 错误3：模块导入错误

**日志显示**：
```
ModuleNotFoundError: No module named 'cache.redis_manager'
```

**解决**：
```bash
# 重新构建API容器
docker-compose -f docker-compose.prod.yml build api
docker-compose -f docker-compose.prod.yml up -d api
```

### 错误4：配置文件缺失

**日志显示**：
```
FileNotFoundError: config/frontend_real_data.json
```

**解决**：
```bash
# 检查配置文件
docker exec kg_api_prod ls -la /app/config/

# 如果文件缺失，创建默认配置
docker exec kg_api_prod bash -c 'cat > /app/config/frontend_real_data.json << EOF
{
  "stats": {
    "totalNodes": 4432,
    "totalRelations": 17412,
    "totalTerms": 1275,
    "totalCategories": 8,
    "totalTags": 128,
    "totalAliases": 1746,
    "dictEntries": 1275
  },
  "categories": [
    {"name": "Symptom", "count": 259},
    {"name": "Metric", "count": 190},
    {"name": "Component", "count": 181},
    {"name": "Process", "count": 170},
    {"name": "TestCase", "count": 104},
    {"name": "Tool", "count": 102},
    {"name": "Role", "count": 63},
    {"name": "Material", "count": 55}
  ]
}
EOF'

# 重启API
docker-compose -f docker-compose.prod.yml restart api
```

---

## 一键执行脚本

如果你想一次性执行所有修复命令，可以复制以下脚本：

```bash
#!/bin/bash
cd /opt/kg

echo "=== 1. 当前容器状态 ==="
docker-compose -f docker-compose.prod.yml ps

echo ""
echo "=== 2. API日志（最近30行） ==="
docker-compose -f docker-compose.prod.yml logs api --tail=30

echo ""
echo "=== 3. 重启Redis ==="
docker-compose -f docker-compose.prod.yml restart redis
sleep 3

echo ""
echo "=== 4. 重启API ==="
docker-compose -f docker-compose.prod.yml restart api
sleep 5

echo ""
echo "=== 5. 修复后容器状态 ==="
docker-compose -f docker-compose.prod.yml ps

echo ""
echo "=== 6. 测试API健康检查 ==="
docker exec kg_api_prod curl -s http://localhost:8000/health

echo ""
echo "=== 7. 测试real-stats端点 ==="
docker exec kg_api_prod curl -s http://localhost:8000/kg/real-stats | head -c 300

echo ""
echo "=== 修复完成 ==="
echo "请在浏览器中访问: http://47.108.152.16/"
```

**使用方法**：
1. 登录服务器后，复制上面的脚本
2. 粘贴到终端
3. 按回车执行

---

## 需要记录的信息

请把以下命令的输出发给我，我可以进一步诊断：

```bash
# 1. 容器状态
docker-compose -f docker-compose.prod.yml ps

# 2. API日志
docker-compose -f docker-compose.prod.yml logs api --tail=100

# 3. Nginx日志
docker-compose -f docker-compose.prod.yml logs nginx --tail=30
```

---

**提示**：如果你配置了SSH密钥，可以避免每次输入密码。配置方法：

```bash
# 在本地生成SSH密钥（如果还没有）
ssh-keygen -t rsa -b 4096

# 复制公钥到服务器
ssh-copy-id root@47.108.152.16
```

之后就可以免密登录了。

