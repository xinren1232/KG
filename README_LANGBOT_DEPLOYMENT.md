# LangBot 部署完整指南

**状态**: ✅ 评估完成，已准备部署  
**日期**: 2025-11-13  
**推荐等级**: ⭐⭐⭐⭐⭐

---

## 📌 快速导航

### 📖 文档清单
| 文档 | 用途 | 优先级 |
|------|------|--------|
| **LANGBOT_EVALUATION_COMPLETE.md** | 📊 评估完成报告 | ⭐⭐⭐ |
| **LANGBOT_DEPLOYMENT_READY.md** | 🚀 部署准备指南 | ⭐⭐⭐ |
| **langbot_deployment_checklist.md** | ✅ 部署执行清单 | ⭐⭐⭐ |
| **langbot_isolated_deployment.md** | 🔒 隔离部署方案 | ⭐⭐ |
| **langbot_deployment_guide.md** | 📋 详细实施指南 | ⭐⭐ |

### 🚀 自动化脚本
| 脚本 | 用途 | 推荐度 |
|------|------|--------|
| **execute_langbot_deployment.sh** | 一键部署 (Bash) | ⭐⭐⭐⭐⭐ |
| **deploy_langbot_isolated.py** | 一键部署 (Python) | ⭐⭐⭐⭐ |

---

## 🎯 核心结论

### ✅ 强烈推荐部署

**评估结果**: LangBot 完全可以部署，与现有知识图谱系统完全隔离

| 评估项 | 结果 | 详情 |
|--------|------|------|
| **资源充足** | ✅ | 内存可用1.6GB，LangBot仅需100-200MB |
| **网络完善** | ✅ | 公网IP、Nginx反向代理、端口开放 |
| **隔离性** | ✅ | Docker容器完全隔离，不影响现有系统 |
| **部署风险** | ✅ | 低风险，可随时回滚 |
| **扩展性** | ✅ | 支持多个IM平台 |

---

## 🚀 一键部署

### 方案A: Bash脚本 (推荐)

```bash
# 1. 给脚本执行权限
chmod +x execute_langbot_deployment.sh

# 2. 执行部署脚本
./execute_langbot_deployment.sh

# 3. 配置环境变量
ssh root@47.108.152.16
nano /opt/langbot/.env
# 编辑以下内容:
# DIFY_API_KEY=<从Dify获取>
# FEISHU_APP_ID=<飞书应用ID>
# FEISHU_APP_SECRET=<飞书应用Secret>
# WEBHOOK_TOKEN=<自定义Token>

# 4. 启动服务
systemctl start langbot

# 5. 验证
systemctl status langbot
curl http://localhost:8080/health
```

**预计耗时**: 30-40分钟

### 方案B: Python脚本

```bash
python3 deploy_langbot_isolated.py
```

---

## 📋 部署前准备

### 信息收集
```
【Dify配置】
- API URL: https://qmsai.transsion.com ✅
- API Key: [需要从Dify获取]
- 应用类型: chatbot

【飞书机器人配置】
- 应用ID: [需要创建机器人应用]
- 应用Secret: [需要创建机器人应用]
- Webhook Token: [自定义]
```

### 系统检查
```bash
# 检查SSH连接
ssh root@47.108.152.16 "echo 'SSH连接成功'"

# 检查Docker
ssh root@47.108.152.16 "docker --version"

# 检查现有系统
ssh root@47.108.152.16 "systemctl status kg-api kg-frontend neo4j redis-server nginx"

# 检查端口
ssh root@47.108.152.16 "netstat -tlnp | grep 8080"
```

---

## ✅ 部署验证

### 部署完成后的检查

```bash
# 1. 检查LangBot服务
systemctl status langbot
docker ps | grep langbot

# 2. 检查现有系统
systemctl status kg-api kg-frontend neo4j redis-server nginx

# 3. 检查端口
netstat -tlnp | grep -E ':(80|5173|8000|7474|7687|6379|8080)'

# 4. 健康检查
curl http://localhost:8080/health
curl http://localhost:8000/health

# 5. 查看日志
tail -f /var/log/langbot/langbot.log
```

---

## 🎯 后续步骤

### 第1步: 配置飞书机器人 (10分钟)
1. 登录飞书开发者后台
2. 创建机器人应用
3. 配置Webhook URL: `http://47.108.152.16/webhook/feishu`
4. 配置事件订阅
5. 获取应用ID和Secret

### 第2步: 测试功能 (5分钟)
1. 在飞书中发送测试消息
2. 验证LangBot是否回复
3. 检查日志

### 第3步: 监控和优化 (持续)
1. 监控资源使用
2. 检查日志
3. 根据需要调整配置

---

## 📊 架构设计

```
┌─────────────────────────────────────────────────────────┐
│                  Aliyun ECS 47.108.152.16               │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────────┐         ┌──────────────────┐      │
│  │  知识图谱系统    │         │  LangBot (新)    │      │
│  │  (现有)          │         │  (独立部署)      │      │
│  ├──────────────────┤         ├──────────────────┤      │
│  │ 端口: 5173       │         │ 端口: 8080       │      │
│  │ 端口: 8000       │         │ 进程: Docker     │      │
│  │ 端口: 7474       │         │ 日志: /var/log/  │      │
│  │ 端口: 7687       │         │ 数据: /opt/      │      │
│  │ 端口: 6379       │         │                  │      │
│  │ 进程: systemd    │         │ 隔离: ⭐⭐⭐⭐⭐ │      │
│  └──────────────────┘         └──────────────────┘      │
│           ↓                            ↓                 │
│  ┌──────────────────────────────────────────────┐       │
│  │         Nginx 反向代理 (端口80)              │       │
│  │  /api/* → 8000 (现有API)                     │       │
│  │  /langbot/* → 8080 (LangBot)                 │       │
│  │  /webhook/feishu → 8080 (飞书Webhook)       │       │
│  └──────────────────────────────────────────────┘       │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

---

## 📞 故障排查

### 常见问题

**Q: LangBot无法启动?**
```bash
journalctl -u langbot -n 50
docker logs langbot
```

**Q: 无法连接Dify?**
```bash
curl -v https://qmsai.transsion.com
docker exec langbot curl -H "Authorization: Bearer KEY" \
  https://qmsai.transsion.com/api/apps
```

**Q: 现有系统是否受影响?**
```bash
systemctl status kg-api kg-frontend neo4j redis-server
# 应该都显示 active (running)
```

---

## 🎉 总结

### ✅ 已完成
- ✅ 可行性评估 (强烈推荐)
- ✅ 隔离部署方案设计
- ✅ 自动化部署脚本
- ✅ 详细部署文档
- ✅ 故障排查指南

### 📋 待执行
- ⏳ 准备配置信息
- ⏳ 执行部署脚本
- ⏳ 配置环境变量
- ⏳ 启动LangBot服务
- ⏳ 配置飞书机器人
- ⏳ 测试功能

---

**推荐等级**: ⭐⭐⭐⭐⭐ (5/5)  
**隔离等级**: ⭐⭐⭐⭐⭐ (完全隔离)  
**风险等级**: 🟢 低风险

**准备就绪！可以开始部署了！** 🚀

