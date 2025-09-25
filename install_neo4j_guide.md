# Neo4j安装指南

## 方案一：Neo4j Desktop（推荐）

### 1. 下载安装
1. 访问 https://neo4j.com/download/
2. 点击"Download"按钮
3. 填写简单信息获取下载链接
4. 下载并运行安装程序

### 2. 创建数据库
1. 启动Neo4j Desktop
2. 点击"New Project"创建项目
3. 点击"Add Database" -> "Create a Local Database"
4. 设置数据库名称：`kg_database`
5. 设置密码：`password123`
6. 选择Neo4j版本：5.x（最新版本）

### 3. 启动数据库
1. 点击数据库旁的"Start"按钮
2. 等待状态变为"Active"
3. 点击"Open"可以访问Neo4j Browser

### 4. 验证安装
- 浏览器地址：http://localhost:7474
- 用户名：neo4j
- 密码：password123

## 方案二：Docker安装（如果有Docker）

```bash
# 拉取Neo4j镜像
docker pull neo4j:5.23

# 运行Neo4j容器
docker run -d \
  --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password123 \
  neo4j:5.23
```

## 方案三：Windows服务安装

### 1. 下载社区版
1. 访问 https://neo4j.com/download-center/
2. 选择"Community Server"
3. 下载Windows版本

### 2. 安装配置
1. 解压到 C:\neo4j
2. 编辑 conf\neo4j.conf
3. 设置密码：
   ```
   dbms.default_database=neo4j
   dbms.security.auth_enabled=true
   ```

### 3. 启动服务
```cmd
# 安装服务
C:\neo4j\bin\neo4j.bat install-service

# 启动服务
C:\neo4j\bin\neo4j.bat start
```

## 配置知识图谱项目

### 1. 更新.env文件
```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASS=password123
NEO4J_DATABASE=neo4j
```

### 2. 初始化约束
```cypher
// 创建节点约束
CREATE CONSTRAINT component_name IF NOT EXISTS FOR (c:Component) REQUIRE c.name IS UNIQUE;
CREATE CONSTRAINT symptom_name IF NOT EXISTS FOR (s:Symptom) REQUIRE s.name IS UNIQUE;
CREATE CONSTRAINT cause_name IF NOT EXISTS FOR (c:Cause) REQUIRE c.name IS UNIQUE;
CREATE CONSTRAINT countermeasure_name IF NOT EXISTS FOR (c:Countermeasure) REQUIRE c.name IS UNIQUE;
```

### 3. 测试连接
```python
# 测试脚本
import requests
response = requests.get('http://localhost:8000/health')
print(response.json())
```

## 故障排除

### 常见问题
1. **端口冲突**：确保7474和7687端口未被占用
2. **内存不足**：Neo4j需要至少2GB内存
3. **Java版本**：需要Java 17或更高版本

### 检查命令
```bash
# 检查端口
netstat -ano | findstr ":7474"
netstat -ano | findstr ":7687"

# 检查Java版本
java -version
```
