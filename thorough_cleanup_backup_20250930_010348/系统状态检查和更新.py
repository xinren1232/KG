#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统状态检查和更新 - 确保前端显示最新的词典数据
"""

import requests
import json
import time
from pathlib import Path

def check_api_status():
    """检查API服务状态"""
    print("🔍 检查API服务状态...")
    
    try:
        # 检查API根路径
        response = requests.get("http://localhost:8000/docs", timeout=5)
        if response.status_code == 200:
            print("✅ API服务运行正常 (端口8000)")
        else:
            print(f"❌ API服务异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API服务连接失败: {e}")
        return False
    
    return True

def check_frontend_status():
    """检查前端服务状态"""
    print("🔍 检查前端服务状态...")
    
    try:
        response = requests.get("http://localhost:5173", timeout=5)
        if response.status_code == 200:
            print("✅ 前端服务运行正常 (端口5173)")
        else:
            print(f"❌ 前端服务异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 前端服务连接失败: {e}")
        return False
    
    return True

def check_dictionary_data():
    """检查词典数据状态"""
    print("📊 检查词典数据状态...")
    
    # 检查统一词典文件
    unified_dir = Path("data/unified_dictionary")
    if not unified_dir.exists():
        print("❌ 统一词典目录不存在")
        return False
    
    stats_file = unified_dir / "statistics.json"
    if stats_file.exists():
        try:
            with open(stats_file, 'r', encoding='utf-8') as f:
                stats = json.load(f)
            
            total_terms = stats.get('total_terms', 0)
            categories = stats.get('categories', {})
            last_updated = stats.get('last_updated', 'Unknown')
            
            print(f"📊 词典数据统计:")
            print(f"  总词条数: {total_terms}")
            print(f"  最后更新: {last_updated}")
            print(f"  分类分布:")
            for cat, count in categories.items():
                print(f"    {cat}: {count}条")
            
            if total_terms > 1000:
                print("✅ 词典数据已更新 (包含硬件模块数据)")
                return True
            else:
                print("⚠️ 词典数据可能未完全更新")
                return False
                
        except Exception as e:
            print(f"❌ 读取统计文件失败: {e}")
            return False
    else:
        print("❌ 统计文件不存在")
        return False

def test_api_endpoints():
    """测试API端点"""
    print("🔍 测试API端点...")
    
    # 测试不同的API路径
    endpoints = [
        "/api/dictionary/search?query=显示屏",
        "/api/dictionary/stats",
        "/kg/dictionary/entries",
        "/dictionary/search?query=显示屏",
        "/search?query=显示屏"
    ]
    
    for endpoint in endpoints:
        try:
            url = f"http://localhost:8000{endpoint}"
            response = requests.get(url, timeout=5)
            print(f"  {endpoint}: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, dict) and data.get('success') is not False:
                        print(f"    ✅ 端点可用")
                        return endpoint
                    else:
                        print(f"    ⚠️ 返回错误: {data.get('error', 'Unknown')}")
                except:
                    print(f"    ✅ 端点可用 (非JSON响应)")
            else:
                print(f"    ❌ HTTP错误")
                
        except Exception as e:
            print(f"  {endpoint}: 连接失败 - {e}")
    
    return None

def create_api_test_script():
    """创建API测试脚本"""
    print("📝 创建API测试脚本...")
    
    script_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API测试脚本 - 测试词典API功能
"""

import requests
import json

def test_dictionary_api():
    """测试词典API"""
    base_url = "http://localhost:8000"
    
    # 测试搜索功能
    search_terms = ["显示屏", "OLED", "电池", "摄像头", "传感器"]
    
    for term in search_terms:
        print(f"🔍 搜索: {term}")
        
        # 尝试不同的API路径
        paths = [
            f"/api/dictionary/search?query={term}",
            f"/kg/dictionary/entries?search={term}",
            f"/dictionary/search?query={term}",
            f"/search?query={term}"
        ]
        
        for path in paths:
            try:
                response = requests.get(f"{base_url}{path}", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, dict) and 'data' in data:
                        results = data['data']
                        if isinstance(results, list) and len(results) > 0:
                            print(f"  ✅ {path}: 找到 {len(results)} 条结果")
                            return path
                        else:
                            print(f"  ⚠️ {path}: 无结果")
                    else:
                        print(f"  ⚠️ {path}: 响应格式异常")
                else:
                    print(f"  ❌ {path}: HTTP {response.status_code}")
            except Exception as e:
                print(f"  ❌ {path}: {e}")
    
    return None

if __name__ == "__main__":
    working_endpoint = test_dictionary_api()
    if working_endpoint:
        print(f"\\n✅ 可用的API端点: {working_endpoint}")
    else:
        print("\\n❌ 未找到可用的词典API端点")
'''
    
    with open("测试词典API.py", "w", encoding="utf-8") as f:
        f.write(script_content)
    
    print("✅ API测试脚本已创建: 测试词典API.py")

def create_frontend_update_guide():
    """创建前端更新指南"""
    print("📝 创建前端更新指南...")
    
    guide_content = '''# 前端数据更新指南

## 问题诊断
当前前端可能显示的是旧的词典数据，需要确保前端能够正确加载新的1192条词典数据。

## 解决步骤

### 1. 检查API连接
- 确认API服务运行在 http://localhost:8000
- 确认前端服务运行在 http://localhost:5173
- 测试API端点是否返回正确数据

### 2. 清除缓存
```bash
# 清除浏览器缓存
Ctrl + F5 (强制刷新)

# 清除前端构建缓存
cd frontend
npm run build
```

### 3. 重启服务
```bash
# 重启API服务
cd api
python main.py

# 重启前端服务
cd frontend
npm run dev
```

### 4. 验证数据
- 访问 http://localhost:5173
- 检查词典页面是否显示1192条数据
- 搜索硬件模块相关词条（如"显示屏"、"OLED"、"传感器"）

### 5. 如果仍有问题
- 检查前端API调用路径是否正确
- 检查API返回的数据格式
- 查看浏览器开发者工具的网络请求
- 查看控制台错误信息

## 预期结果
- 词典总数: 1192条
- 包含20个硬件模块的专业词汇
- 支持按Label和标签筛选
- 支持模糊搜索功能
'''
    
    with open("前端数据更新指南.md", "w", encoding="utf-8") as f:
        f.write(guide_content)
    
    print("✅ 前端更新指南已创建: 前端数据更新指南.md")

def main():
    """主函数"""
    print("🔧 系统状态检查和更新")
    print("=" * 50)
    
    # 1. 检查服务状态
    api_ok = check_api_status()
    frontend_ok = check_frontend_status()
    
    # 2. 检查词典数据
    data_ok = check_dictionary_data()
    
    # 3. 测试API端点
    working_endpoint = test_api_endpoints()
    
    # 4. 创建辅助文件
    create_api_test_script()
    create_frontend_update_guide()
    
    print("\n" + "=" * 50)
    print("📊 系统状态总结:")
    print(f"API服务: {'✅ 正常' if api_ok else '❌ 异常'}")
    print(f"前端服务: {'✅ 正常' if frontend_ok else '❌ 异常'}")
    print(f"词典数据: {'✅ 已更新' if data_ok else '❌ 需要更新'}")
    print(f"API端点: {'✅ 可用' if working_endpoint else '❌ 不可用'}")
    
    if working_endpoint:
        print(f"可用端点: {working_endpoint}")
    
    print(f"\n💡 建议操作:")
    if not api_ok:
        print("1. 重启API服务")
    if not frontend_ok:
        print("2. 重启前端服务")
    if not data_ok:
        print("3. 检查词典数据文件")
    if not working_endpoint:
        print("4. 检查API路由配置")
    
    print("5. 清除浏览器缓存并强制刷新")
    print("6. 运行 测试词典API.py 进行详细测试")
    print("7. 参考 前端数据更新指南.md")
    
    print(f"\n🎯 预期结果:")
    print(f"- 前端显示1192条词典数据")
    print(f"- 包含20个硬件模块专业词汇")
    print(f"- 支持搜索硬件相关术语")

if __name__ == "__main__":
    main()
