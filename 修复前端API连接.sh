#!/bin/bash
# 修复前端API连接问题

echo "🔧 修复前端API连接配置"
echo "================================"

# 1. 创建.env文件
echo "📝 创建前端.env配置文件..."
ssh root@47.108.152.16 "cat > /opt/knowledge-graph/apps/web/.env << 'EOF'
# API配置
VITE_API_URL=/api
VITE_API_BASE_URL=http://47.108.152.16/api
EOF
"

# 2. 修改vite.config.js启用代理
echo "📝 修改vite.config.js启用代理..."
ssh root@47.108.152.16 "cat > /opt/knowledge-graph/apps/web/vite.config.js << 'EOF'
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
EOF
"

# 3. 重启前端服务
echo ""
echo "🔄 重启前端服务..."
ssh root@47.108.152.16 "systemctl restart kg-frontend"

echo ""
echo "⏳ 等待服务启动..."
sleep 8

# 4. 测试
echo ""
echo "🧪 测试服务..."
ssh root@47.108.152.16 "curl -s http://localhost:5173/ | head -5"

echo ""
echo "✅ 修复完成！"
echo ""
echo "请刷新浏览器: http://47.108.152.16/"

