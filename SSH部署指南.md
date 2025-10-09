# 🚀 知识图谱系统 SSH 部署指南

## 📋 概述

本指南提供了使用SSH自动化部署知识图谱系统到远程服务器的完整方案。支持一键部署包括Neo4j、Redis、API服务、前端应用和监控系统在内的完整技术栈。

## 🛠️ 部署工具

### 1. **Python版本** (推荐)
- **文件**: `ssh_deploy.py`
- **特点**: 功能完整、错误处理完善、支持配置文件
- **依赖**: `paramiko` (SSH客户端库)

### 2. **Shell脚本版本** (Linux/macOS)
- **文件**: `ssh_deploy.sh`
- **特点**: 无Python依赖、使用系统SSH工具
- **适用**: Linux、macOS、WSL环境

### 3. **批处理版本** (Windows)
- **文件**: `ssh_deploy.bat`
- **特点**: Windows原生支持、使用系统SSH工具
- **适用**: Windows 10/11 (需要OpenSSH)

## 🔧 环境准备

### 本地环境要求

#### Windows环境
```bash
# 启用OpenSSH客户端 (Windows 10/11)
# 设置 -> 应用 -> 可选功能 -> 添加功能 -> OpenSSH客户端

# 或安装Git Bash (包含SSH工具)
# https://git-scm.com/download/win

# Python版本需要安装依赖
pip install paramiko
```

#### Linux/macOS环境
```bash
# 通常已预装SSH客户端
ssh -V

# 如果未安装
# Ubuntu/Debian
sudo apt-get install openssh-client

# CentOS/RHEL
sudo yum install openssh-clients

# macOS (通常已安装)
brew install openssh
```

### 远程服务器要求

#### 系统要求
- **操作系统**: Ubuntu 18.04+, CentOS 7+, Debian 9+
- **内存**: 最少4GB，推荐8GB+
- **磁盘**: 最少20GB可用空间
- **网络**: 开放端口 22(SSH), 7474(Neo4j), 8000(API), 9090(Prometheus), 3000(Grafana)

#### 用户权限
- SSH访问权限
- sudo权限 (用于安装Docker等系统依赖)
- Docker用户组权限 (部署后自动配置)

## 🔑 SSH认证配置

### 方式1: SSH密钥认证 (推荐)

#### 生成SSH密钥对
```bash
# 生成新的SSH密钥对
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# 默认保存位置
# Windows: C:\Users\用户名\.ssh\id_rsa
# Linux/macOS: ~/.ssh/id_rsa
```

#### 上传公钥到服务器
```bash
# 方法1: 使用ssh-copy-id (Linux/macOS)
ssh-copy-id user@server_ip

# 方法2: 手动复制
# 1. 复制公钥内容
cat ~/.ssh/id_rsa.pub

# 2. 登录服务器，添加到authorized_keys
mkdir -p ~/.ssh
echo "公钥内容" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh
```

### 方式2: 密码认证

确保服务器SSH配置允许密码认证：
```bash
# 编辑SSH配置
sudo nano /etc/ssh/sshd_config

# 确保以下配置
PasswordAuthentication yes

# 重启SSH服务
sudo systemctl restart sshd
```

## 📝 配置文件

### Python版本配置 (`deploy_config.json`)

```json
{
  "server": {
    "host": "your-server-ip",
    "port": 22,
    "username": "your-username",
    "password": "",
    "key_file": "C:\\Users\\用户名\\.ssh\\id_rsa",
    "timeout": 30
  },
  "deployment": {
    "remote_path": "/opt/knowledge-graph",
    "backup_path": "/opt/kg-backups",
    "services": ["neo4j", "redis", "api", "web", "prometheus", "grafana"]
  }
}
```

**配置说明**:
- `host`: 服务器IP地址或域名
- `username`: SSH用户名
- `password`: SSH密码 (如使用密钥认证可留空)
- `key_file`: SSH私钥文件路径
- `remote_path`: 远程部署目录
- `backup_path`: 备份目录

## 🚀 部署步骤

### 方法1: Python自动化部署

#### 1. 安装依赖
```bash
pip install paramiko
```

#### 2. 配置部署参数
编辑 `deploy_config.json` 文件，填入服务器信息。

#### 3. 执行部署
```bash
python ssh_deploy.py
```

### 方法2: Shell脚本部署 (Linux/macOS)

```bash
# 设置执行权限
chmod +x ssh_deploy.sh

# 使用SSH密钥部署
./ssh_deploy.sh --host 192.168.1.100 --user ubuntu --key ~/.ssh/id_rsa

# 使用密码部署
./ssh_deploy.sh --host 192.168.1.100 --user ubuntu
```

### 方法3: Windows批处理部署

```cmd
# 使用SSH密钥部署
ssh_deploy.bat --host 192.168.1.100 --user ubuntu --key C:\Users\用户名\.ssh\id_rsa

# 使用密码部署
ssh_deploy.bat --host 192.168.1.100 --user ubuntu
```

## 📊 部署流程

### 自动化部署流程

1. **🔍 连接测试**: 验证SSH连接和认证
2. **📦 创建部署包**: 打包项目文件 (排除不必要文件)
3. **📤 上传文件**: 使用rsync/scp上传到服务器
4. **💾 备份现有部署**: 自动备份现有版本
5. **🔧 安装依赖**: 自动安装Docker和Docker Compose
6. **🚀 部署主服务**: 启动Neo4j、Redis、API、前端服务
7. **⚡ 优化数据库**: 创建索引、优化查询性能
8. **📊 部署监控**: 启动Prometheus和Grafana监控
9. **🔍 验证部署**: 检查所有服务状态
10. **📋 显示访问信息**: 提供服务访问地址

### 部署包内容

**包含的目录**:
- `api/` - API服务代码
- `apps/` - 前端应用代码
- `config/` - 配置文件
- `data/` - 数据文件
- `monitoring/` - 监控配置
- `nginx/` - Nginx配置
- `scripts/` - 工具脚本

**包含的文件**:
- `docker-compose.yml` - 主服务编排
- `docker-compose.monitoring.yml` - 监控服务编排
- `Dockerfile.api` - API服务镜像
- `deploy_optimized.sh` - 优化部署脚本
- `README.md` - 项目说明

**排除的内容**:
- Python缓存文件 (`*.pyc`, `__pycache__`)
- 版本控制文件 (`.git`)
- 依赖目录 (`node_modules`)
- 日志文件 (`*.log`)
- 备份目录 (`cleanup_backup_*`)

## 🌐 服务访问

部署完成后，可以通过以下地址访问各个服务：

### 核心服务
- **Neo4j浏览器**: `http://服务器IP:7474`
  - 用户名: `neo4j`
  - 密码: `password123`

- **API服务**: `http://服务器IP:8000`
  - API文档: `http://服务器IP:8000/docs`
  - 健康检查: `http://服务器IP:8000/health`

### 监控服务
- **Prometheus**: `http://服务器IP:9090`
  - 指标监控和查询界面

- **Grafana**: `http://服务器IP:3000`
  - 用户名: `admin`
  - 密码: `admin123`

## 🔧 远程管理

### SSH登录
```bash
ssh username@server_ip
```

### Docker管理
```bash
# 查看所有容器状态
docker ps

# 查看服务日志
docker-compose logs -f

# 重启特定服务
docker-compose restart api

# 停止所有服务
docker-compose down

# 重新启动所有服务
docker-compose up -d
```

### 服务管理
```bash
# 进入项目目录
cd /opt/knowledge-graph

# 查看主服务状态
docker-compose ps

# 查看监控服务状态
docker-compose -f docker-compose.monitoring.yml ps

# 重新部署 (保留数据)
docker-compose down
docker-compose up -d

# 完全重置 (删除数据)
docker-compose down -v
docker-compose up -d
```

## 🛠️ 故障排除

### 常见问题

#### 1. SSH连接失败
```bash
# 检查SSH服务状态
sudo systemctl status sshd

# 检查防火墙设置
sudo ufw status

# 检查SSH配置
sudo nano /etc/ssh/sshd_config
```

#### 2. Docker安装失败
```bash
# 手动安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 添加用户到docker组
sudo usermod -aG docker $USER

# 重新登录或执行
newgrp docker
```

#### 3. 服务启动失败
```bash
# 查看详细日志
docker-compose logs service_name

# 检查端口占用
sudo netstat -tlnp | grep :8000

# 检查磁盘空间
df -h

# 检查内存使用
free -h
```

#### 4. 数据库连接失败
```bash
# 检查Neo4j日志
docker-compose logs neo4j

# 重启Neo4j服务
docker-compose restart neo4j

# 检查数据库状态
docker exec -it kg_neo4j cypher-shell -u neo4j -p password123
```

### 日志查看

```bash
# 查看所有服务日志
docker-compose logs

# 查看特定服务日志
docker-compose logs api
docker-compose logs neo4j
docker-compose logs redis

# 实时跟踪日志
docker-compose logs -f --tail=100
```

### 性能监控

```bash
# 系统资源使用
htop
df -h
free -h

# Docker资源使用
docker stats

# 服务健康检查
curl http://localhost:8000/health
curl http://localhost:7474
curl http://localhost:9090/-/healthy
```

## 🔄 更新部署

### 增量更新
```bash
# 重新运行部署脚本
python ssh_deploy.py

# 或使用rsync同步代码
rsync -avz --exclude='.git' ./ user@server:/opt/knowledge-graph/
```

### 回滚部署
```bash
# SSH登录服务器
ssh user@server

# 查看备份
ls /opt/kg-backups/

# 回滚到指定版本
sudo cp -r /opt/kg-backups/backup_20231201_120000/* /opt/knowledge-graph/

# 重启服务
cd /opt/knowledge-graph
docker-compose down
docker-compose up -d
```

## 📋 部署检查清单

### 部署前检查
- [ ] 服务器SSH访问正常
- [ ] 服务器满足硬件要求 (4GB+ RAM, 20GB+ 磁盘)
- [ ] 网络端口开放 (22, 7474, 8000, 9090, 3000)
- [ ] SSH认证配置完成 (密钥或密码)
- [ ] 部署配置文件填写正确

### 部署后验证
- [ ] 所有Docker容器运行正常
- [ ] Neo4j浏览器可访问
- [ ] API服务响应正常
- [ ] 健康检查端点返回OK
- [ ] Prometheus收集指标正常
- [ ] Grafana仪表板显示数据

### 功能测试
- [ ] 知识图谱数据查询正常
- [ ] 文件上传和解析功能正常
- [ ] 图谱可视化界面正常
- [ ] 监控告警配置正常
- [ ] 数据备份策略配置

## 🎯 最佳实践

### 安全建议
1. **使用SSH密钥认证**，禁用密码认证
2. **配置防火墙**，只开放必要端口
3. **定期更新系统**和Docker镜像
4. **设置强密码**，特别是数据库密码
5. **启用SSL/TLS**，使用HTTPS访问

### 性能优化
1. **监控资源使用**，及时扩容
2. **定期清理日志**，避免磁盘满
3. **优化数据库索引**，提升查询性能
4. **配置缓存策略**，减少数据库压力
5. **使用CDN**，加速前端资源加载

### 运维建议
1. **设置监控告警**，及时发现问题
2. **定期备份数据**，确保数据安全
3. **文档化配置**，便于团队协作
4. **版本控制部署脚本**，追踪变更
5. **建立应急预案**，快速响应故障

---

## 📞 技术支持

如果在部署过程中遇到问题，可以：

1. **查看日志**: 使用 `docker-compose logs` 查看详细错误信息
2. **检查文档**: 参考本指南的故障排除部分
3. **验证配置**: 确认服务器配置和网络设置
4. **重新部署**: 使用备份恢复后重新执行部署

**🎉 祝您部署成功！享受强大的知识图谱系统！**
