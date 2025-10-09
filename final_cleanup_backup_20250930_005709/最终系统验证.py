#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终系统验证 - 验证词典和图谱数据更新是否成功
"""

import requests
import json
from datetime import datetime

def test_api_endpoints():
    """测试API端点"""
    print("🔍 测试API端点...")
    
    endpoints = [
        {
            "name": "词典条目列表",
            "url": "http://localhost:8000/kg/dictionary/entries?page=1&page_size=5",
            "expected_fields": ["success", "data"]
        },
        {
            "name": "词典搜索功能",
            "url": "http://localhost:8000/kg/dictionary/entries?search=显示屏&page_size=3",
            "expected_fields": ["success", "data"]
        },
        {
            "name": "词典分页功能",
            "url": "http://localhost:8000/kg/dictionary/entries?page=2&page_size=10",
            "expected_fields": ["success", "data"]
        }
    ]
    
    results = {}
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint["url"], timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("success") and "data" in data:
                    entries = data["data"].get("entries", [])
                    total = data["data"].get("total", 0)
                    
                    results[endpoint["name"]] = {
                        "status": "✅ 成功",
                        "total": total,
                        "returned": len(entries),
                        "sample": entries[0]["name"] if entries else "无数据"
                    }
                    
                    print(f"  {endpoint['name']}: ✅ 成功")
                    print(f"    总数: {total}, 返回: {len(entries)}")
                    if entries:
                        print(f"    示例: {entries[0]['name']}")
                else:
                    results[endpoint["name"]] = {
                        "status": "❌ 数据格式错误",
                        "error": data.get("error", "Unknown")
                    }
                    print(f"  {endpoint['name']}: ❌ 数据格式错误")
            else:
                results[endpoint["name"]] = {
                    "status": f"❌ HTTP {response.status_code}",
                    "error": response.text[:100]
                }
                print(f"  {endpoint['name']}: ❌ HTTP {response.status_code}")
                
        except Exception as e:
            results[endpoint["name"]] = {
                "status": "❌ 连接失败",
                "error": str(e)
            }
            print(f"  {endpoint['name']}: ❌ 连接失败 - {e}")
    
    return results

def test_search_terms():
    """测试特定搜索词"""
    print("🔍 测试硬件模块搜索...")
    
    search_terms = [
        "显示屏", "OLED", "电池", "摄像头", "传感器", 
        "充电", "马达", "天线", "散热", "连接器"
    ]
    
    search_results = {}
    
    for term in search_terms:
        try:
            url = f"http://localhost:8000/kg/dictionary/entries?search={term}&page_size=5"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    entries = data["data"].get("entries", [])
                    search_results[term] = {
                        "count": len(entries),
                        "samples": [entry["name"] for entry in entries[:3]]
                    }
                    print(f"  '{term}': {len(entries)} 条结果")
                    if entries:
                        for i, entry in enumerate(entries[:2]):
                            print(f"    {i+1}. {entry['name']}")
                else:
                    search_results[term] = {"count": 0, "error": data.get("error")}
                    print(f"  '{term}': 搜索失败")
            else:
                search_results[term] = {"count": 0, "error": f"HTTP {response.status_code}"}
                print(f"  '{term}': HTTP错误")
                
        except Exception as e:
            search_results[term] = {"count": 0, "error": str(e)}
            print(f"  '{term}': 异常 - {e}")
    
    return search_results

def test_frontend_api():
    """测试前端可能调用的API"""
    print("🔍 测试前端API兼容性...")
    
    # 测试前端可能调用的其他端点
    frontend_apis = [
        "/api/dictionary",
        "/api/dictionary/labels", 
        "/api/dictionary/tags",
        "/kg/dictionary",
        "/kg/dictionary/categories"
    ]
    
    frontend_results = {}
    
    for api in frontend_apis:
        try:
            response = requests.get(f"http://localhost:8000{api}", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                frontend_results[api] = {
                    "status": "✅ 可用",
                    "has_data": bool(data)
                }
                print(f"  {api}: ✅ 可用")
            else:
                frontend_results[api] = {
                    "status": f"❌ HTTP {response.status_code}",
                    "has_data": False
                }
                print(f"  {api}: ❌ HTTP {response.status_code}")
                
        except Exception as e:
            frontend_results[api] = {
                "status": "❌ 连接失败",
                "error": str(e)
            }
            print(f"  {api}: ❌ 连接失败")
    
    return frontend_results

def check_services():
    """检查服务状态"""
    print("🔍 检查服务状态...")
    
    services = {
        "API服务": "http://localhost:8000/docs",
        "前端服务": "http://localhost:5173",
        "Neo4j服务": "http://localhost:7474"
    }
    
    service_status = {}
    
    for name, url in services.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                service_status[name] = "✅ 运行正常"
                print(f"  {name}: ✅ 运行正常")
            else:
                service_status[name] = f"⚠️ HTTP {response.status_code}"
                print(f"  {name}: ⚠️ HTTP {response.status_code}")
        except Exception as e:
            service_status[name] = "❌ 无法连接"
            print(f"  {name}: ❌ 无法连接")
    
    return service_status

def generate_report(api_results, search_results, frontend_results, service_status):
    """生成验证报告"""
    print("📝 生成验证报告...")
    
    # 统计成功的API
    successful_apis = sum(1 for result in api_results.values() if "✅" in result["status"])
    total_apis = len(api_results)
    
    # 统计搜索结果
    successful_searches = sum(1 for result in search_results.values() if result["count"] > 0)
    total_searches = len(search_results)
    
    # 统计前端API
    available_frontend_apis = sum(1 for result in frontend_results.values() if "✅" in result["status"])
    total_frontend_apis = len(frontend_results)
    
    # 统计服务状态
    running_services = sum(1 for status in service_status.values() if "✅" in status)
    total_services = len(service_status)
    
    report = {
        "验证时间": datetime.now().isoformat(),
        "API端点测试": {
            "成功率": f"{successful_apis}/{total_apis}",
            "详情": api_results
        },
        "搜索功能测试": {
            "成功率": f"{successful_searches}/{total_searches}",
            "详情": search_results
        },
        "前端API兼容性": {
            "成功率": f"{available_frontend_apis}/{total_frontend_apis}",
            "详情": frontend_results
        },
        "服务状态": {
            "运行率": f"{running_services}/{total_services}",
            "详情": service_status
        }
    }
    
    # 保存报告
    with open("系统验证报告.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    return report

def main():
    """主函数"""
    print("🚀 最终系统验证")
    print("=" * 60)
    
    # 1. 检查服务状态
    service_status = check_services()
    
    # 2. 测试API端点
    api_results = test_api_endpoints()
    
    # 3. 测试搜索功能
    search_results = test_search_terms()
    
    # 4. 测试前端API兼容性
    frontend_results = test_frontend_api()
    
    # 5. 生成报告
    report = generate_report(api_results, search_results, frontend_results, service_status)
    
    print("\n" + "=" * 60)
    print("📊 验证结果总结")
    print("=" * 60)
    
    # 获取总词典数量
    total_entries = 0
    if "词典条目列表" in api_results and "total" in api_results["词典条目列表"]:
        total_entries = api_results["词典条目列表"]["total"]
    
    print(f"📚 词典数据: {total_entries} 条")
    print(f"🔧 API端点: {report['API端点测试']['成功率']}")
    print(f"🔍 搜索功能: {report['搜索功能测试']['成功率']}")
    print(f"🌐 前端兼容: {report['前端API兼容性']['成功率']}")
    print(f"⚙️ 服务状态: {report['服务状态']['运行率']}")
    
    # 判断整体状态
    if total_entries >= 1000:
        print("\n✅ 词典数据更新成功！包含完整的硬件模块数据")
    else:
        print(f"\n⚠️ 词典数据可能不完整，当前只有 {total_entries} 条")
    
    if report['API端点测试']['成功率'].startswith('3/3'):
        print("✅ API功能正常，支持列表、搜索、分页")
    else:
        print("⚠️ 部分API功能异常")
    
    if report['搜索功能测试']['成功率'].split('/')[0] >= '8':
        print("✅ 硬件模块搜索功能正常")
    else:
        print("⚠️ 部分硬件模块搜索异常")
    
    print(f"\n📄 详细报告已保存: 系统验证报告.json")
    
    print(f"\n💡 下一步操作:")
    print(f"1. 🌐 访问前端验证: http://localhost:5173")
    print(f"2. 📚 检查词典管理页面数据显示")
    print(f"3. 🔍 测试搜索硬件模块词汇")
    print(f"4. 📊 执行Neo4j图谱数据导入")

if __name__ == "__main__":
    main()
