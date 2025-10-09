#!/bin/bash
# 完整修复前端API连接问题

echo "🔧 开始修复前端API连接..."
echo "================================"

# 1. 备份原配置
echo "📦 备份原配置..."
cp /opt/knowledge-graph/apps/web/vite.config.js /opt/knowledge-graph/apps/web/vite.config.js.backup

# 2. 创建新的vite.config.js
echo "📝 创建新的vite.config.js..."
cat > /opt/knowledge-graph/apps/web/vite.config.js << 'EOFVITE'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  server: {
    port: 5173,
    host: '0.0.0.0',
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
EOFVITE

echo "✅ vite.config.js已更新"

# 3. 创建.env文件
echo "📝 创建.env文件..."
cat > /opt/knowledge-graph/apps/web/.env << 'EOFENV'
VITE_API_URL=/api
VITE_API_BASE_URL=/api
EOFENV

echo "✅ .env文件已创建"

# 4. 重启前端服务
echo ""
echo "🔄 重启前端服务..."
systemctl restart kg-frontend

echo "⏳ 等待服务启动..."
sleep 10

# 5. 检查服务状态
echo ""
echo "📊 检查服务状态..."
systemctl status kg-frontend | head -15

echo ""
echo "🔌 检查端口..."
netstat -tlnp | grep 5173

echo ""
echo "🧪 测试前端访问..."
curl -s http://localhost:5173/ | head -10

echo ""
echo "🧪 测试API代理..."
curl -s http://localhost:5173/api/health | python3 -m json.tool

echo ""
echo "================================"
echo "✅ 修复完成！"
echo ""
echo "请刷新浏览器访问: http://47.108.152.16/"

