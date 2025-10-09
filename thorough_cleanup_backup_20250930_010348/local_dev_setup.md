# 本地开发环境配置

## 1. 环境要求

### Python 环境
- Python 3.11+
- pip

### Node.js 环境（前端）
- Node.js 18+
- npm 或 pnpm

### Neo4j 数据库
有几种选择：
1. **Neo4j Desktop**（推荐）：图形化界面，易于管理
2. **Neo4j Community Server**：命令行版本
3. **Neo4j AuraDB Free**：云端免费版本

## 2. 安装步骤

### 2.1 安装Neo4j Desktop
1. 访问 https://neo4j.com/download/
2. 下载并安装 Neo4j Desktop
3. 创建新项目和数据库
4. 设置用户名密码（建议：neo4j/password123）
5. 启动数据库，记录连接信息

### 2.2 配置Python环境
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境（Windows）
venv\Scripts\activate

# 安装API依赖
pip install -r services/api/requirements.txt

# 安装ETL依赖
pip install -r services/etl/requirements.txt
```

### 2.3 配置环境变量
复制 `.env.example` 到 `.env` 并修改：
```
NEO4J_USER=neo4j
NEO4J_PASS=password123
NEO4J_URI=bolt://localhost:7687
```

## 3. 启动服务

### 3.1 启动Neo4j
- 打开Neo4j Desktop
- 启动你的数据库实例
- 确保端口7474（HTTP）和7687（Bolt）可用

### 3.2 初始化数据库
```bash
# 方法1：使用Neo4j Browser（推荐）
# 打开 http://localhost:7474
# 复制并执行 services/api/neo4j_init/neo4j_constraints.cypher 中的内容
# 复制并执行 services/api/neo4j_init/sample_data.cypher 中的内容

# 方法2：使用命令行（如果安装了cypher-shell）
cypher-shell -u neo4j -p password123 -f services/api/neo4j_init/neo4j_constraints.cypher
cypher-shell -u neo4j -p password123 -f services/api/neo4j_init/sample_data.cypher
```

### 3.3 启动API服务
```bash
cd services/api
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3.4 启动前端（后续）
```bash
cd apps/web
npm install
npm run dev
```

## 4. 验证安装

### 4.1 检查Neo4j
- 访问 http://localhost:7474
- 使用用户名密码登录
- 执行查询：`MATCH (n) RETURN count(n)`

### 4.2 检查API
- 访问 http://localhost:8000/docs
- 测试健康检查：http://localhost:8000/health

### 4.3 测试API功能
```bash
# 获取产品列表
curl http://localhost:8000/kg/products

# 查询测试流程
curl -X POST http://localhost:8000/kg/query/flow \
  -H "Content-Type: application/json" \
  -d '{"product_name": "iPhone 15"}'
```

## 5. 开发工具推荐

### IDE/编辑器
- VS Code + Python扩展
- PyCharm

### Neo4j工具
- Neo4j Desktop（数据库管理）
- Neo4j Browser（查询界面）
- APOC插件（高级功能）

### API测试
- Postman
- Insomnia
- curl命令行

## 6. 常见问题

### Q: Neo4j连接失败
A: 检查数据库是否启动，端口是否正确，用户名密码是否匹配

### Q: Python模块导入错误
A: 确保虚拟环境已激活，依赖已正确安装

### Q: API启动失败
A: 检查端口8000是否被占用，Neo4j连接是否正常
