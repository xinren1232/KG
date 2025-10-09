#!/usr/bin/env python3
"""
部署图谱修复到服务器
"""
import subprocess
import sys
import os

def run_command(cmd, description):
    """执行命令并显示结果"""
    print(f"\n🔄 {description}")
    print(f"执行命令: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
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
    print("🚀 开始部署图谱修复到服务器...")
    
    # 1. 上传后端API修复
    if not run_command(
        "scp services/api/routers/kg_router.py root@47.108.152.16:/opt/knowledge-graph/services/api/routers/",
        "上传后端API修复"
    ):
        return False
    
    # 2. 上传前端修复
    if not run_command(
        "scp apps/web/src/views/GraphVisualization.vue root@47.108.152.16:/opt/knowledge-graph/apps/web/src/views/",
        "上传前端修复"
    ):
        return False
    
    # 3. 重启后端服务
    if not run_command(
        'ssh root@47.108.152.16 "cd /opt/knowledge-graph && systemctl restart kg-api"',
        "重启后端API服务"
    ):
        return False
    
    # 4. 重新构建前端
    if not run_command(
        'ssh root@47.108.152.16 "cd /opt/knowledge-graph/apps/web && npm run build"',
        "重新构建前端"
    ):
        return False
    
    # 5. 验证服务状态
    if not run_command(
        'ssh root@47.108.152.16 "systemctl status kg-api | head -10"',
        "验证后端服务状态"
    ):
        return False
    
    # 6. 测试API响应
    if not run_command(
        'ssh root@47.108.152.16 "curl -s \'http://localhost:8000/kg/graph?show_all=true&limit=5\' | head -100"',
        "测试API响应"
    ):
        return False
    
    print("\n🎉 图谱修复部署完成！")
    print("\n📋 修复内容:")
    print("✅ 1. 修复节点分类颜色映射")
    print("✅ 2. 优化力导向布局参数")
    print("✅ 3. 调整节点大小计算")
    print("✅ 4. 改进标签显示策略")
    print("\n🌐 请访问: http://47.108.152.16 查看修复效果")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
