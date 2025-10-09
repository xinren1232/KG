#!/usr/bin/env python3
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
        print(f"\n✅ 可用的API端点: {working_endpoint}")
    else:
        print("\n❌ 未找到可用的词典API端点")
