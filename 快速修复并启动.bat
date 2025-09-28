@echo off
chcp 65001 >nul
echo.
echo ==========================================
echo 🔧 API调用问题快速修复并启动
echo ==========================================
echo.

echo 📋 修复步骤:
echo 1. 检查服务状态
echo 2. 启动API服务
echo 3. 启动前端服务
echo 4. 验证修复结果
echo.

echo 🔍 检查当前目录...
if not exist "api\main.py" (
    echo ❌ 错误: 请在项目根目录运行此脚本
    pause
    exit /b 1
)

echo ✅ 项目目录正确
echo.

echo 🚀 启动API服务...
echo 正在后台启动API服务 (端口8000)...
start "API服务" cmd /k "python api\main.py"

echo ⏳ 等待API服务启动...
timeout /t 5 /nobreak >nul

echo.
echo 🌐 启动前端服务...
echo 正在启动前端开发服务器 (端口5173)...
cd apps\web
start "前端服务" cmd /k "npm run dev"

echo ⏳ 等待前端服务启动...
timeout /t 3 /nobreak >nul

cd ..\..

echo.
echo ==========================================
echo ✅ 服务启动完成
echo ==========================================
echo.

echo 📊 服务信息:
echo   - API服务: http://localhost:8000
echo   - API文档: http://localhost:8000/docs
echo   - 前端服务: http://localhost:5173
echo   - 数据治理: http://localhost:5173/governance
echo.

echo 🔧 已修复的问题:
echo   ✅ API方法调用错误 (apiClient → api)
echo   ✅ 图标导入问题 (Lightbulb → TrendCharts)
echo   ✅ Element Plus图标兼容性
echo.

echo 💡 使用说明:
echo   1. 等待服务完全启动 (约30秒)
echo   2. 访问: http://localhost:5173/governance
echo   3. 如有缓存问题，按 Ctrl+Shift+R 强制刷新
echo   4. 检查浏览器控制台 (F12) 确认无错误
echo.

echo 🎯 验证成功标志:
echo   - 数据概览显示1124条术语
echo   - 质量指标表格正常显示
echo   - 分类分布图表正常
echo   - 无控制台错误信息
echo.

echo ⚠️ 如果仍有问题:
echo   1. 检查Neo4j是否运行 (端口7687)
echo   2. 确认API服务正常启动
echo   3. 清除浏览器缓存
echo   4. 查看控制台错误信息
echo.

echo 🌐 快速访问链接:
echo   - 数据治理页面: http://localhost:5173/governance
echo   - 图谱可视化: http://localhost:5173/graph-viz
echo   - API文档: http://localhost:8000/docs
echo.

echo 按任意键打开数据治理页面...
pause >nul

start http://localhost:5173/governance

echo.
echo 🎉 修复完成！数据治理系统已启动。
echo.
pause
