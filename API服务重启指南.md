
# API服务重启指南

## 方法1: 手动重启
1. 停止当前API服务 (Ctrl+C)
2. 重新启动:
   cd api
   python main.py

## 方法2: 检查数据加载
访问 http://localhost:8000/docs 查看API文档
测试词典端点是否返回新数据

## 验证步骤
1. 访问前端: http://localhost:5173
2. 进入词典管理页面
3. 检查是否显示1192条数据
4. 搜索硬件模块相关词条
