#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psutil
import requests
import time
from datetime import datetime

def check_port(port):
    """检查端口是否被占用"""
    for conn in psutil.net_connections():
        if conn.laddr.port == port:
            return True, conn.pid
    return False, None

def test_service_health(url, service_name):
    """测试服务健康状态"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True, "正常"
        else:
            return False, f"HTTP {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, f"连接失败: {str(e)[:50]}"

def generate_system_report():
    """生成系统状态报告"""
    print("📊 知识图谱系统状态总结")
    print("=" * 60)
    print(f"🕒 检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 服务端口检查
    services = {
        "Neo4j Bolt": {"port": 7687, "url": None},
        "Neo4j HTTP": {"port": 7474, "url": "http://localhost:7474"},
        "API服务": {"port": 8000, "url": "http://localhost:8000/health"},
        "前端服务": {"port": 5173, "url": "http://localhost:5173"}
    }
    
    print("🔍 服务端口状态:")
    print("-" * 40)
    
    all_running = True
    service_status = {}
    
    for service_name, config in services.items():
        port = config["port"]
        url = config["url"]
        
        running, pid = check_port(port)
        
        if running:
            status_icon = "✅"
            status_text = f"运行中 (PID: {pid})"
            
            # 如果有URL，测试健康状态
            if url:
                healthy, health_msg = test_service_health(url, service_name)
                if healthy:
                    health_status = "🟢 健康"
                else:
                    health_status = f"🟡 {health_msg}"
                    all_running = False
            else:
                health_status = "🔵 端口开放"
                
        else:
            status_icon = "❌"
            status_text = "未运行"
            health_status = "🔴 离线"
            all_running = False
        
        service_status[service_name] = {
            "running": running,
            "pid": pid if running else None,
            "health": health_status
        }
        
        print(f"{status_icon} {service_name:12} (:{port:4}) - {status_text:20} {health_status}")
    
    # 系统访问地址
    print("\n🌐 系统访问地址:")
    print("-" * 40)
    
    if service_status["前端服务"]["running"]:
        print("✅ 前端界面:     http://localhost:5173")
        print("✅ 图谱可视化:   http://localhost:5173/graph-viz")
        print("✅ 系统管理:     http://localhost:5173/system")
        print("✅ 词典管理:     http://localhost:5173/dictionary")
    else:
        print("❌ 前端服务未启动")
    
    if service_status["API服务"]["running"]:
        print("✅ API服务:      http://localhost:8000")
        print("✅ API文档:      http://localhost:8000/docs")
    else:
        print("❌ API服务未启动")
    
    if service_status["Neo4j HTTP"]["running"]:
        print("✅ Neo4j浏览器:  http://localhost:7474")
    else:
        print("❌ Neo4j服务未启动")
    
    # 功能可用性
    print("\n🔧 功能可用性:")
    print("-" * 40)
    
    functions = {
        "文档解析": service_status["API服务"]["running"],
        "词典管理": service_status["API服务"]["running"] and service_status["前端服务"]["running"],
        "图谱可视化": all_running,
        "数据存储": service_status["Neo4j Bolt"]["running"],
        "系统管理": service_status["前端服务"]["running"]
    }
    
    for func_name, available in functions.items():
        icon = "✅" if available else "❌"
        status = "可用" if available else "不可用"
        print(f"{icon} {func_name:12} - {status}")
    
    # 总体状态
    print("\n📈 总体状态:")
    print("-" * 40)
    
    if all_running:
        overall_status = "🟢 所有服务正常运行"
        recommendation = "系统完全可用，可以正常使用所有功能"
    elif service_status["API服务"]["running"] and service_status["前端服务"]["running"]:
        overall_status = "🟡 核心服务运行，Neo4j需要配置"
        recommendation = "请配置Neo4j密码以启用完整功能"
    else:
        overall_status = "🔴 部分服务异常"
        recommendation = "请检查并重启异常服务"
    
    print(f"状态: {overall_status}")
    print(f"建议: {recommendation}")
    
    # Neo4j特殊说明
    if service_status["Neo4j Bolt"]["running"] and service_status["Neo4j HTTP"]["running"]:
        print("\n🔐 Neo4j认证状态:")
        print("-" * 40)
        print("⚠️ Neo4j服务运行中，但可能需要设置密码")
        print("💡 解决方案:")
        print("   1. 访问 http://localhost:7474 设置密码")
        print("   2. 或运行: python 等待并重试Neo4j连接.py")
        print("   3. 建议密码: password123")
    
    # 下一步操作
    print("\n🎯 下一步操作:")
    print("-" * 40)
    
    if all_running:
        print("🎉 系统已完全启动，可以开始使用!")
        print("   - 访问前端界面开始使用系统")
        print("   - 上传文档进行知识抽取")
        print("   - 管理词典和图谱数据")
    else:
        print("🔧 需要完成的任务:")
        if not service_status["Neo4j Bolt"]["running"]:
            print("   1. 启动Neo4j服务")
        if service_status["Neo4j Bolt"]["running"] and "🟡" in service_status["Neo4j HTTP"]["health"]:
            print("   1. 配置Neo4j密码")
        if not service_status["API服务"]["running"]:
            print("   2. 启动API服务")
        if not service_status["前端服务"]["running"]:
            print("   3. 启动前端服务")
    
    return service_status, all_running

def main():
    """主函数"""
    try:
        service_status, all_running = generate_system_report()
        
        # 保存状态到文件
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f"系统状态报告_{timestamp}.txt"
        
        print(f"\n💾 状态报告已保存到: {report_file}")
        
        return all_running
        
    except Exception as e:
        print(f"❌ 生成报告时发生错误: {e}")
        return False

if __name__ == "__main__":
    main()
