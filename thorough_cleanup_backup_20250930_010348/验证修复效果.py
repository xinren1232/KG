#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证数据模型修复效果
"""

import requests
import json

def verify_fix():
    """验证修复效果"""
    print("🔍 验证数据模型修复效果")
    
    # 1. 检查API统计
    try:
        response = requests.get("http://localhost:8000/kg/real-stats", timeout=10)
        if response.status_code == 200:
            data = response.json()
            stats = data.get("data", {}).get("stats", {})
            
            dict_entries = stats.get("dictEntries", 0)
            total_terms = stats.get("totalTerms", 0)
            
            print(f"📊 词典条目数: {dict_entries}")
            print(f"📊 Term节点数: {total_terms}")
            
            if dict_entries > 0 and dict_entries == total_terms:
                print("✅ 修复成功！词典条目数正常")
                return True
            else:
                print("❌ 修复失败，词典条目数仍为0")
                return False
        else:
            print("❌ API请求失败")
            return False
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False

if __name__ == "__main__":
    verify_fix()
