# 阿里云服务器问题修复说明

## 问题现状

访问 **http://47.108.152.16/** 时：

✅ **前端正常**：页面可以加载，显示"质量知识图谱助手"标题  
❌ **API异常**：返回 502 Bad Gateway 错误  
❌ **数据无法加载**：`/api/kg/real-stats` 端点失败

**错误截图显示**：
```
GET http://47.108.152.16/api/kg/real-stats 502 (Bad Gateway)
真实统计API不可用，使用默认数据：Request failed with status code 502
```

---

## 快速修复（3种方法）

### 方法1：双击运行批处理文件（最简单）

1. **检查状态**：双击 `检查服务器状态.bat`
2. **一键修复**：双击 `一键修复服务器.bat`
3. **刷新浏览器**：访问 http://47.108.152.16/

### 方法2：使用SSH命令（推荐）

打开命令行（CMD或PowerShell），复制粘贴以下命令：

```bash
ssh root@47.108.152.16 "cd /opt/kg && docker-compose -f docker-compose.prod.yml restart redis && docker-compose -f docker-compose.prod.yml restart api"
```

等待30秒后刷新浏览器。

### 方法3：手动登录服务器修复

```bash
# 1. 登录服务器
ssh root@47.108.152.16

# 2. 进入项目目录
cd /opt/kg

# 3. 查看问题
docker-compose -f docker-compose.prod.yml logs api --tail=50

# 4. 重启服务
docker-compose -f docker-compose.prod.yml restart redis
docker-compose -f docker-compose.prod.yml restart api

# 5. 验证修复
docker-compose -f docker-compose.prod.yml ps
curl http://localhost/api/kg/real-stats
```

---

## 工具文件说明

本次创建的修复工具：

| 文件名 | 用途 | 使用方法 |
|--------|------|----------|
| `检查服务器状态.bat` | 检查服务器各项状态 | 双击运行 |
| `一键修复服务器.bat` | 自动修复API服务 | 双击运行 |
| `服务器问题诊断和修复指南.md` | 详细的诊断和修复文档 | 阅读参考 |
| `check_server_status.py` | Python版本的状态检查 | `python check_server_status.py` |
| `diagnose_server.py` | 深度诊断工具 | `python diagnose_server.py` |
| `fix_api_service.sh` | Linux/Mac修复脚本 | `bash fix_api_service.sh` |

---

## 问题原因分析

### 502错误的含义

**502 Bad Gateway** = Nginx正常运行，但无法连接到后端API服务

可能的原因：
1. ❌ API容器未启动或崩溃
2. ❌ API服务启动失败（依赖问题）
3. ❌ Redis连接失败
4. ❌ Neo4j连接失败
5. ❌ Docker网络问题

### 为什么前端能访问但API不能？

- **前端**：静态HTML/JS文件，由Nginx直接提供
- **API**：需要Python服务运行，依赖Redis和Neo4j

所以前端正常不代表后端正常。

---

## 详细诊断步骤

### 步骤1：检查容器是否运行

```bash
ssh root@47.108.152.16
cd /opt/kg
docker-compose -f docker-compose.prod.yml ps
```

**期望输出**：
```
NAME                STATUS
kg_nginx_prod       Up
kg_api_prod         Up        ← 这个最重要
kg_neo4j_prod       Up
kg_redis_prod       Up
```

如果`kg_api_prod`不是`Up`状态，说明API服务有问题。

### 步骤2：查看API错误日志

```bash
docker-compose -f docker-compose.prod.yml logs api --tail=100
```

**常见错误类型**：

#### A. Redis连接错误
```
redis.exceptions.ConnectionError
```
**解决**：`docker-compose -f docker-compose.prod.yml restart redis`

#### B. Neo4j连接错误
```
neo4j.exceptions.ServiceUnavailable
```
**解决**：`docker-compose -f docker-compose.prod.yml restart neo4j`

#### C. 模块导入错误
```
ModuleNotFoundError: No module named 'cache.redis_manager'
```
**解决**：重新构建容器
```bash
docker-compose -f docker-compose.prod.yml build api
docker-compose -f docker-compose.prod.yml up -d api
```

#### D. 配置文件缺失
```
FileNotFoundError: config/frontend_real_data.json
```
**解决**：检查配置文件是否存在
```bash
docker exec kg_api_prod ls -la /app/config/
```

### 步骤3：测试API内部访问

```bash
# 进入API容器
docker exec -it kg_api_prod bash

# 测试健康检查
curl http://localhost:8000/health

# 测试real-stats端点
curl http://localhost:8000/kg/real-stats

# 测试Redis连接
python -c "import redis; r=redis.Redis(host='redis'); print(r.ping())"

# 退出容器
exit
```

---

## 完全重启方案

如果简单重启不行，执行完全重启：

```bash
ssh root@47.108.152.16

cd /opt/kg

# 停止所有服务
docker-compose -f docker-compose.prod.yml down

# 重新启动
docker-compose -f docker-compose.prod.yml up -d

# 查看启动过程
docker-compose -f docker-compose.prod.yml logs -f

# 按Ctrl+C退出日志查看

# 检查状态
docker-compose -f docker-compose.prod.yml ps
```

---

## 验证修复成功

### 1. 命令行验证

```bash
# 测试健康检查
curl http://47.108.152.16/health

# 测试API
curl http://47.108.152.16/api/kg/real-stats
```

应该返回JSON数据，而不是502错误。

### 2. 浏览器验证

访问 http://47.108.152.16/

打开浏览器开发者工具（F12），查看Console：
- ✅ 应该看到：`Home page loaded successfully`
- ✅ 应该看到：`最终统计数据: {dictEntries: 1275, ...}`
- ❌ 不应该看到：`真实统计API不可用`

### 3. 网络请求验证

在开发者工具的Network标签：
- ✅ `/api/kg/real-stats` 应该返回 `200 OK`
- ❌ 不应该返回 `502 Bad Gateway`

---

## 预防措施

### 1. 设置自动重启

确保所有服务配置了自动重启：
```yaml
restart: unless-stopped
```

### 2. 配置监控

可以使用以下命令定期检查：
```bash
# 每5分钟检查一次
*/5 * * * * cd /opt/kg && docker-compose -f docker-compose.prod.yml ps | grep -q "Up" || docker-compose -f docker-compose.prod.yml restart api
```

### 3. 日志管理

定期清理日志，防止磁盘占满：
```bash
# 查看日志大小
docker-compose -f docker-compose.prod.yml logs --tail=0 | wc -l

# 清理旧日志
docker-compose -f docker-compose.prod.yml logs --tail=1000 > /dev/null
```

---

## 常见问题FAQ

**Q: 为什么重启后还是502？**  
A: 可能需要等待30秒让服务完全启动。也可能是依赖服务（Redis/Neo4j）有问题。

**Q: 如何查看实时日志？**  
A: `ssh root@47.108.152.16 "cd /opt/kg && docker-compose -f docker-compose.prod.yml logs -f api"`

**Q: 如何进入容器调试？**  
A: `ssh root@47.108.152.16 "docker exec -it kg_api_prod bash"`

**Q: 如何完全重新部署？**  
A: 参考 `阿里云部署修复指南.md` 中的完整部署流程。

---

## 需要帮助？

如果问题仍未解决，请提供：

1. 容器状态：`docker-compose -f docker-compose.prod.yml ps`
2. API日志：`docker-compose -f docker-compose.prod.yml logs api --tail=200`
3. 错误截图

---

**创建时间**: 2025-10-03  
**服务器IP**: 47.108.152.16  
**项目路径**: /opt/kg

