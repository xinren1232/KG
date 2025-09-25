#!/usr/bin/env python3
"""
快速功能测试
"""
import requests
import json

API_BASE = "http://127.0.0.1:8000"

def test_function(name, func):
    try:
        result = func()
        print(f"✅ {name}: 正常")
        return True
    except Exception as e:
        print(f"❌ {name}: 错误 - {e}")
        return False

def test_health():
    r = requests.get(f"{API_BASE}/health")
    assert r.status_code == 200
    return r.json()

def test_dictionary():
    r = requests.get(f"{API_BASE}/kg/dictionary")
    assert r.status_code == 200
    data = r.json()
    assert data["success"] == True
    return data

def test_upload():
    files = {'file': ('test.txt', 'Hello World', 'text/plain')}
    r = requests.post(f"{API_BASE}/kg/upload", files=files)
    assert r.status_code == 200
    data = r.json()
    assert data["success"] == True
    return data

def test_extract():
    r = requests.post(f"{API_BASE}/kg/extract", json={"file_id": "test"})
    assert r.status_code == 200
    data = r.json()
    assert data["success"] == True
    assert "entities" in data
    assert "relations" in data
    assert "metadata" in data
    return data

def test_build():
    r = requests.post(f"{API_BASE}/kg/build", json={"entities": [], "relations": []})
    assert r.status_code == 200
    data = r.json()
    assert data["success"] == True
    return data

def test_stats():
    r = requests.get(f"{API_BASE}/kg/stats")
    assert r.status_code == 200
    data = r.json()
    assert data["success"] == True
    return data

def main():
    print("🔍 快速功能测试开始...")
    
    tests = [
        ("健康检查", test_health),
        ("词典管理", test_dictionary),
        ("文件上传", test_upload),
        ("知识抽取", test_extract),
        ("图谱构建", test_build),
        ("统计信息", test_stats),
    ]
    
    passed = 0
    total = len(tests)
    
    for name, func in tests:
        if test_function(name, func):
            passed += 1
    
    print(f"\n📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有功能正常工作！")
    else:
        print("⚠️ 部分功能需要检查")

if __name__ == "__main__":
    main()
