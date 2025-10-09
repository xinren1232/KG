#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
确保路径唯一性 - 确保前端使用正确的API端点
"""

import requests
import json

def test_all_endpoints():
    """测试所有端点返回的数据"""
    print("🔍 测试所有API端点...")
    
    endpoints = {
        "/kg/dictionary/entries": "主要端点（已更新）",
        "/api/dictionary": "前端默认端点",
        "/kg/dictionary": "旧端点"
    }
    
    results = {}
    
    for endpoint, description in endpoints.items():
        try:
            response = requests.get(f"http://localhost:8000{endpoint}?page_size=3", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if endpoint == "/kg/dictionary/entries":
                    # 新格式
                    if data.get("success") and "data" in data:
                        total = data["data"].get("total", 0)
                        entries = data["data"].get("entries", [])
                        results[endpoint] = {
                            "status": "✅ 正常",
                            "total": total,
                            "format": "新格式",
                            "description": description
                        }
                        print(f"  {endpoint}: ✅ {total} 条数据 ({description})")
                    else:
                        results[endpoint] = {"status": "❌ 格式错误", "description": description}
                        print(f"  {endpoint}: ❌ 格式错误")
                
                elif endpoint == "/api/dictionary":
                    # 检查是否返回Neo4j格式
                    if data.get("success") and "data" in data:
                        if isinstance(data["data"], list):
                            total = len(data["data"])
                        else:
                            total = 0
                        results[endpoint] = {
                            "status": "✅ 正常",
                            "total": total,
                            "format": "Neo4j格式",
                            "description": description
                        }
                        print(f"  {endpoint}: ✅ {total} 条数据 ({description})")
                    else:
                        results[endpoint] = {"status": "❌ 格式错误", "description": description}
                        print(f"  {endpoint}: ❌ 格式错误")
                
                elif endpoint == "/kg/dictionary":
                    # 旧格式
                    if data.get("ok") and "data" in data:
                        total = 0
                        if isinstance(data["data"], dict):
                            for category, items in data["data"].items():
                                if isinstance(items, list):
                                    total += len(items)
                        results[endpoint] = {
                            "status": "✅ 正常",
                            "total": total,
                            "format": "旧格式",
                            "description": description
                        }
                        print(f"  {endpoint}: ✅ {total} 条数据 ({description})")
                    else:
                        results[endpoint] = {"status": "❌ 格式错误", "description": description}
                        print(f"  {endpoint}: ❌ 格式错误")
            else:
                results[endpoint] = {"status": f"❌ HTTP {response.status_code}", "description": description}
                print(f"  {endpoint}: ❌ HTTP {response.status_code}")
                
        except Exception as e:
            results[endpoint] = {"status": f"❌ 异常: {e}", "description": description}
            print(f"  {endpoint}: ❌ 异常")
    
    return results

def check_frontend_api_call():
    """检查前端API调用配置"""
    print("🔍 检查前端API调用配置...")
    
    from pathlib import Path
    
    api_file = Path("apps/web/src/api/index.js")
    
    if api_file.exists():
        with open(api_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找getDictionary方法
        if "getDictionary(" in content:
            if "/kg/dictionary/entries" in content:
                print("  ✅ 前端已配置使用 /kg/dictionary/entries")
                return "/kg/dictionary/entries"
            elif "/api/dictionary" in content:
                print("  ⚠️ 前端配置使用 /api/dictionary")
                return "/api/dictionary"
            elif "/kg/dictionary" in content:
                print("  ⚠️ 前端配置使用 /kg/dictionary")
                return "/kg/dictionary"
            else:
                print("  ❌ 无法确定前端API配置")
                return None
        else:
            print("  ❌ 未找到getDictionary方法")
            return None
    else:
        print("  ❌ 前端API文件不存在")
        return None

def recommend_solution(endpoint_results, frontend_config):
    """推荐解决方案"""
    print("💡 推荐解决方案...")
    
    # 找到数据最多的端点
    best_endpoint = None
    max_total = 0
    
    for endpoint, result in endpoint_results.items():
        if result.get("status", "").startswith("✅") and result.get("total", 0) > max_total:
            max_total = result["total"]
            best_endpoint = endpoint
    
    if best_endpoint:
        print(f"📊 数据最多的端点: {best_endpoint} ({max_total} 条)")
        
        if frontend_config == best_endpoint:
            print("✅ 前端已使用最佳端点，无需修改")
            return "no_change"
        else:
            print(f"⚠️ 建议修改前端配置使用: {best_endpoint}")
            return best_endpoint
    else:
        print("❌ 没有找到可用的端点")
        return None

def update_frontend_config(target_endpoint):
    """更新前端配置"""
    print(f"🔧 更新前端配置使用: {target_endpoint}")
    
    from pathlib import Path
    
    api_file = Path("apps/web/src/api/index.js")
    
    if not api_file.exists():
        print("❌ 前端API文件不存在")
        return False
    
    try:
        with open(api_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换getDictionary方法的URL
        if target_endpoint == "/kg/dictionary/entries":
            new_content = content.replace(
                "return api.get('/api/dictionary')",
                "return api.get('/kg/dictionary/entries', { params })"
            ).replace(
                "return api.get('/kg/dictionary')",
                "return api.get('/kg/dictionary/entries', { params })"
            )
        else:
            new_content = content.replace(
                "return api.get('/kg/dictionary/entries', { params })",
                f"return api.get('{target_endpoint}')"
            )
        
        if new_content != content:
            with open(api_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ 前端配置已更新使用: {target_endpoint}")
            return True
        else:
            print("⚠️ 前端配置无需更改")
            return True
            
    except Exception as e:
        print(f"❌ 更新前端配置失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 确保路径唯一性")
    print("=" * 50)
    
    # 1. 测试所有端点
    endpoint_results = test_all_endpoints()
    
    # 2. 检查前端配置
    frontend_config = check_frontend_api_call()
    
    # 3. 推荐解决方案
    recommendation = recommend_solution(endpoint_results, frontend_config)
    
    # 4. 执行更新（如果需要）
    if recommendation and recommendation != "no_change":
        success = update_frontend_config(recommendation)
        if success:
            print("🔄 建议重启前端服务以加载新配置")
    
    print("\n" + "=" * 50)
    print("📊 总结:")
    
    # 显示各端点状态
    for endpoint, result in endpoint_results.items():
        status = result.get("status", "未知")
        total = result.get("total", 0)
        description = result.get("description", "")
        print(f"  {endpoint}: {status} - {total} 条 ({description})")
    
    print(f"\n前端配置: {frontend_config if frontend_config else '未知'}")
    print(f"推荐配置: {recommendation if recommendation != 'no_change' else '无需更改'}")
    
    # 找到最佳端点
    best_endpoint = None
    max_total = 0
    for endpoint, result in endpoint_results.items():
        if result.get("status", "").startswith("✅") and result.get("total", 0) > max_total:
            max_total = result["total"]
            best_endpoint = endpoint
    
    if best_endpoint and max_total > 1000:
        print(f"\n✅ 系统状态良好!")
        print(f"📊 最佳端点: {best_endpoint}")
        print(f"📊 数据总量: {max_total} 条")
        print(f"🌐 前端地址: http://localhost:5173")
        print(f"💡 前端应该显示 {max_total} 条词典数据")
    else:
        print(f"\n⚠️ 系统需要优化")
        print(f"📊 当前最大数据量: {max_total} 条")

if __name__ == "__main__":
    main()
