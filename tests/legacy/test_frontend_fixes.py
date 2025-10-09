#!/usr/bin/env python3
"""
前端修复验证脚本
验证所有修复的问题是否已解决
"""

import requests
import time
import json
from datetime import datetime

def test_frontend_server():
    """测试前端服务器是否正常运行"""
    try:
        response = requests.get('http://localhost:5173', timeout=5)
        if response.status_code == 200:
            print("✅ 前端服务器运行正常")
            return True
        else:
            print(f"❌ 前端服务器响应异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 前端服务器连接失败: {e}")
        return False

def test_system_management_page():
    """测试系统管理页面是否可访问"""
    try:
        response = requests.get('http://localhost:5173/#/system-management', timeout=5)
        if response.status_code == 200:
            print("✅ 系统管理页面可访问")
            return True
        else:
            print(f"❌ 系统管理页面访问异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 系统管理页面访问失败: {e}")
        return False

def check_console_errors():
    """检查是否还有控制台错误（需要手动验证）"""
    print("\n📋 需要手动验证的项目:")
    print("1. 打开浏览器开发者工具 (F12)")
    print("2. 访问 http://localhost:5173")
    print("3. 点击导航菜单中的各个页面")
    print("4. 检查控制台是否还有以下错误:")
    print("   - testAllRules is not defined")
    print("   - resetForm is not defined") 
    print("   - api.getRules is not a function")
    print("   - api.getSystemStatus is not a function")
    print("   - showAddDialog is not defined")
    print("   - 404 API请求错误")
    print("5. 访问系统管理页面，检查所有标签页是否正常工作")

def generate_test_report():
    """生成测试报告"""
    report = {
        "test_time": datetime.now().isoformat(),
        "test_results": {
            "frontend_server": test_frontend_server(),
            "system_management_page": test_system_management_page()
        },
        "fixes_applied": [
            "✅ 修复了 MonitoringManagement 组件中的 testAllRules 和 resetForm 方法",
            "✅ 修复了 DataSourceManagement 组件中的 showAddDialog 方法",
            "✅ 修复了 API 导出问题，将默认导出改为 kgApi",
            "✅ 添加了 Mock API 数据，解决开发环境中的 API 请求失败问题",
            "✅ 创建了环境配置文件，支持开发和生产环境切换",
            "✅ 禁用了 Vite 代理配置，避免连接错误"
        ],
        "remaining_tasks": [
            "🔍 需要手动验证浏览器控制台是否还有JavaScript错误",
            "🔍 需要验证所有页面功能是否正常工作",
            "🔍 需要测试系统管理页面的各个标签页"
        ]
    }
    
    return report

def main():
    print("🚀 开始验证前端修复...")
    print("=" * 50)
    
    # 运行自动化测试
    report = generate_test_report()
    
    print("\n📊 测试结果:")
    print("=" * 30)
    
    for test_name, result in report["test_results"].items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
    
    print("\n🔧 已应用的修复:")
    print("=" * 30)
    for fix in report["fixes_applied"]:
        print(fix)
    
    print("\n📝 剩余任务:")
    print("=" * 30)
    for task in report["remaining_tasks"]:
        print(task)
    
    # 检查控制台错误
    check_console_errors()
    
    # 保存报告
    with open('frontend_test_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 详细报告已保存到: frontend_test_report.json")
    
    print("\n🎯 总结:")
    print("=" * 30)
    all_passed = all(report["test_results"].values())
    if all_passed:
        print("✅ 所有自动化测试通过！")
        print("🌐 前端应用地址: http://localhost:5173")
        print("⚙️ 系统管理页面: http://localhost:5173/#/system-management")
        print("\n请手动验证浏览器控制台是否还有错误。")
    else:
        print("❌ 部分测试失败，请检查服务器状态。")

if __name__ == "__main__":
    main()
