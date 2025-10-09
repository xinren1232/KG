# Neo4j 启动指南

## 当前状态
✅ **API服务**: 正常运行 (http://localhost:8000)  
✅ **前端服务**: 正常运行 (http://localhost:5173)  
❌ **Neo4j数据库**: 未运行

## Neo4j 启动方法

### 方法1: Neo4j Desktop (推荐)
1. 打开 Neo4j Desktop 应用程序
2. 选择你的数据库实例
3. 点击 "Start" 按钮启动数据库
4. 等待状态变为 "Active"

### 方法2: 命令行启动
如果你有Neo4j命令行工具：
```bash
neo4j console
```

### 方法3: Windows 服务
如果Neo4j安装为Windows服务：
```cmd
net start neo4j
```

### 方法4: Docker (如果使用Docker)
```bash
docker-compose up neo4j
```

## 验证Neo4j启动
启动后，你可以通过以下方式验证：

1. **浏览器访问**: http://localhost:7474
2. **端口检查**: 
   ```cmd
   netstat -an | findstr :7687
   netstat -an | findstr :7474
   ```

## 默认连接信息
- **用户名**: neo4j
- **密码**: password123 (或你设置的密码)
- **Bolt端口**: 7687
- **HTTP端口**: 7474

## 启动后的完整系统
一旦Neo4j启动，你将拥有完整的知识图谱系统：

### 🌐 访问地址
- **前端界面**: http://localhost:5173
- **图谱可视化**: http://localhost:5173/graph-viz
- **系统管理**: http://localhost:5173/system
- **词典管理**: http://localhost:5173/dictionary
- **API服务**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **Neo4j浏览器**: http://localhost:7474

### 🔧 功能特性
- ✅ 文档解析和知识抽取
- ✅ 词典管理和维护
- ✅ 图谱可视化和查询
- ✅ 系统管理和监控
- ⚠️ 图谱数据存储 (需要Neo4j)

## 故障排除

### 如果Neo4j无法启动
1. 检查端口7687和7474是否被占用
2. 检查Neo4j Desktop是否正确安装
3. 查看Neo4j日志文件
4. 确保有足够的内存和磁盘空间

### 如果连接失败
1. 确认用户名和密码正确
2. 检查防火墙设置
3. 验证Neo4j配置文件

## 下一步
1. 启动Neo4j数据库
2. 访问 http://localhost:5173 使用系统
3. 如需帮助，查看API文档: http://localhost:8000/docs
