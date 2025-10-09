
# Neo4j 手动数据导入指南

## 方法1: 使用Neo4j浏览器
1. 打开浏览器访问: http://localhost:7474
2. 使用正确的用户名密码登录
3. 在查询框中粘贴以下命令来导入数据

## 方法2: 使用cypher-shell
1. 打开命令行
2. 执行: cypher-shell -u neo4j -p [你的密码]
3. 逐批执行CREATE语句

## 方法3: 重置Neo4j密码
1. 停止Neo4j服务
2. 删除 data/dbms/auth 文件
3. 重启Neo4j服务
4. 使用默认密码 neo4j/neo4j 登录并设置新密码

## 导入数据文件
文件位置: 终极完整词典补充数据导入脚本_20模块版.cypher
包含: 654条补充数据

## 验证导入结果
执行查询: MATCH (n) RETURN count(n) as total
预期结果: 应该增加654个节点
