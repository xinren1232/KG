#!/usr/bin/env python3
"""
完整复制本地图谱效果到服务器
"""
import subprocess
import sys
import os

def run_command(cmd, description):
    """执行命令并显示结果"""
    print(f"\n🔄 {description}")
    print(f"执行命令: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print(f"✅ 成功: {description}")
            if result.stdout.strip():
                print(f"输出: {result.stdout.strip()}")
        else:
            print(f"❌ 失败: {description}")
            print(f"错误: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print(f"⏰ 超时: {description}")
        return False
    except Exception as e:
        print(f"💥 异常: {description} - {str(e)}")
        return False
    
    return True

def main():
    """主函数"""
    print("🚀 开始完整复制本地图谱效果到服务器...")
    
    # 1. 上传修复后的前端文件
    if not run_command(
        "scp apps/web/src/views/GraphVisualization.vue root@47.108.152.16:/opt/knowledge-graph/apps/web/src/views/",
        "上传修复后的前端文件"
    ):
        return False
    
    # 2. 上传修复后的后端文件
    if not run_command(
        "scp api/main.py root@47.108.152.16:/opt/knowledge-graph/api/",
        "上传修复后的后端文件"
    ):
        return False
    
    # 3. 重启后端服务
    if not run_command(
        'ssh root@47.108.152.16 "cd /opt/knowledge-graph && systemctl restart kg-api && sleep 5"',
        "重启后端API服务"
    ):
        return False
    
    # 4. 检查后端服务状态
    if not run_command(
        'ssh root@47.108.152.16 "systemctl is-active kg-api"',
        "检查后端服务状态"
    ):
        return False
    
    # 5. 重新构建前端
    if not run_command(
        'ssh root@47.108.152.16 "cd /opt/knowledge-graph/apps/web && npm run build"',
        "重新构建前端"
    ):
        return False
    
    # 6. 测试API数据结构
    if not run_command(
        'ssh root@47.108.152.16 "curl -s \'http://localhost:8000/kg/graph?show_all=true&limit=3\' | python3 -c \\"import sys, json; data=json.load(sys.stdin); print(f\'节点数: {len(data.get(\\\"data\\\", {}).get(\\\"sampleNodes\\\", []))}\'); print(f\'第一个节点: {data.get(\\\"data\\\", {}).get(\\\"sampleNodes\\\", [{}])[0] if data.get(\\\"data\\\", {}).get(\\\"sampleNodes\\\") else \\\"无数据\\\"}\')\\""',
        "测试API数据结构"
    ):
        return False
    
    print("\n🎉 完整图谱修复部署完成！")
    print("\n📋 修复内容:")
    print("✅ 1. 修复节点分类颜色映射问题")
    print("✅ 2. 修复数据源优先级问题")
    print("✅ 3. 添加调试日志输出")
    print("✅ 4. 确保前后端数据一致性")
    print("\n🌐 请访问: http://47.108.152.16 查看修复效果")
    print("📊 打开浏览器开发者工具查看控制台日志")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
