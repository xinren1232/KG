#!/usr/bin/env python3

# 修改vite.config.js启用代理
vite_config = """import { defineConfig } from 'vite'
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
        rewrite: (path) => path.replace(/^\\/api/, '')
      }
    }
  }
})
"""

with open('/opt/knowledge-graph/apps/web/vite.config.js', 'w', encoding='utf-8') as f:
    f.write(vite_config)

print('✅ vite.config.js已更新，启用了API代理')

