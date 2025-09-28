#!/usr/bin/env python3
"""
测试完整版API功能
"""
import requests
import json

def test_api_endpoint(url, description):
    """测试API端点"""
    try:
        print(f"🔍 测试 {description}...")
        response = requests.get(url, timeout=10)
        print(f"   状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 成功: {json.dumps(data, ensure_ascii=False, indent=2)[:200]}...")
            return True
        else:
            print(f"   ❌ 失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        return False

def main():
    """主函数"""
    print("🚀 完整版API功能测试")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # 测试各个端点
    endpoints = [
        ("/health", "健康检查"),
        ("/", "根路径"),
        ("/docs", "API文档"),
        ("/files/upload", "文件上传端点"),
        ("/extract", "数据抽取端点"),
        ("/kg/build", "知识图谱构建端点"),
    ]
    
    success_count = 0
    for endpoint, description in endpoints:
        url = base_url + endpoint
        if test_api_endpoint(url, description):
            success_count += 1
        print()
    
    print("=" * 50)
    print(f"📊 测试结果: {success_count}/{len(endpoints)} 个端点可用")
    
    if success_count > 0:
        print("🎉 API服务运行正常！")
        print(f"📍 访问API文档: {base_url}/docs")
    else:
        print("❌ API服务可能未正确启动")

if __name__ == "__main__":
    main()
