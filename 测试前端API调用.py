#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试前端API调用 - 验证前端能否获取完整数据
"""

import requests
import json

def test_frontend_api_call():
    """测试前端API调用"""
    print("🔍 测试前端API调用...")
    
    # 模拟前端的API调用
    try:
        # 测试默认调用（之前只返回50条）
        print("1. 测试默认调用:")
        response1 = requests.get("http://localhost:8000/kg/dictionary/entries", timeout=10)
        
        if response1.status_code == 200:
            data1 = response1.json()
            if data1.get("success"):
                total1 = data1["data"].get("total", 0)
                entries1 = len(data1["data"].get("entries", []))
                print(f"   默认调用: 总数={total1}, 返回={entries1}")
            else:
                print(f"   默认调用失败: {data1}")
        else:
            print(f"   默认调用HTTP错误: {response1.status_code}")
        
        # 测试大页面调用（修复后应该返回所有数据）
        print("2. 测试大页面调用:")
        response2 = requests.get("http://localhost:8000/kg/dictionary/entries?page_size=10000", timeout=10)
        
        if response2.status_code == 200:
            data2 = response2.json()
            if data2.get("success"):
                total2 = data2["data"].get("total", 0)
                entries2 = len(data2["data"].get("entries", []))
                print(f"   大页面调用: 总数={total2}, 返回={entries2}")
                
                if entries2 > 1000:
                    print("   ✅ 前端应该能获取到完整数据!")
                    
                    # 显示一些示例数据
                    print("   📊 示例数据:")
                    for i, entry in enumerate(data2["data"]["entries"][:3]):
                        print(f"     {i+1}. {entry.get('name', 'N/A')} ({entry.get('type', 'N/A')})")
                    
                    return True, total2
                else:
                    print(f"   ⚠️ 数据量仍然不足: {entries2}")
                    return False, entries2
            else:
                print(f"   大页面调用失败: {data2}")
                return False, 0
        else:
            print(f"   大页面调用HTTP错误: {response2.status_code}")
            return False, 0
            
    except Exception as e:
        print(f"❌ API测试异常: {e}")
        return False, 0

def check_api_data_source():
    """检查API数据源"""
    print("📁 检查API数据源...")
    
    from pathlib import Path
    
    api_data_file = Path("api/data/dictionary.json")
    
    if api_data_file.exists():
        try:
            with open(api_data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                print(f"   ✅ API数据文件包含 {len(data)} 条记录")
                
                # 检查数据格式
                if data:
                    sample = data[0]
                    print(f"   📊 数据格式示例:")
                    for key in ['term', 'category', 'aliases', 'tags', 'description']:
                        if key in sample:
                            value = sample[key]
                            if isinstance(value, list):
                                print(f"     {key}: {len(value)} 项")
                            else:
                                print(f"     {key}: {str(value)[:50]}...")
                
                return len(data)
            else:
                print(f"   ❌ API数据文件格式错误")
                return 0
                
        except Exception as e:
            print(f"   ❌ 读取API数据文件失败: {e}")
            return 0
    else:
        print(f"   ❌ API数据文件不存在: {api_data_file}")
        return 0

def generate_frontend_test_summary():
    """生成前端测试总结"""
    print("📝 生成前端测试总结...")
    
    # 检查数据源
    data_count = check_api_data_source()
    
    # 测试API调用
    api_ok, api_count = test_frontend_api_call()
    
    print("\n" + "=" * 50)
    print("📊 前端数据获取测试总结")
    print("=" * 50)
    
    print(f"API数据源: {data_count} 条记录")
    print(f"API调用: {'✅ 成功' if api_ok else '❌ 失败'}")
    print(f"API返回: {api_count} 条数据")
    
    if api_ok and api_count > 1000:
        print("\n✅ 前端修复成功!")
        print(f"📊 前端现在应该显示 {api_count} 条词典数据")
        print("🌐 请刷新浏览器页面: http://localhost:5173")
        print("💡 如果仍显示50条，请:")
        print("   1. 硬刷新浏览器 (Ctrl+F5)")
        print("   2. 清除浏览器缓存")
        print("   3. 检查浏览器开发者工具的网络请求")
    elif api_ok and api_count > 0:
        print(f"\n⚠️ 数据量不足")
        print(f"📊 当前只有 {api_count} 条数据")
        print("💡 需要检查数据统一汇总是否完整")
    else:
        print("\n❌ API调用失败")
        print("💡 需要检查API服务状态")
    
    return api_ok, api_count

def main():
    """主函数"""
    print("🚀 测试前端API调用")
    print("=" * 40)
    
    success, count = generate_frontend_test_summary()
    
    if success and count > 1000:
        print(f"\n🎉 系统状态: 正常")
        print(f"📊 词典数据: {count} 条")
        print(f"🔧 前端修复: 完成")
        print(f"💡 下一步: 刷新浏览器验证显示")
    else:
        print(f"\n⚠️ 需要进一步调试")

if __name__ == "__main__":
    main()
