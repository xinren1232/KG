#!/usr/bin/env python3
"""
测试最终词典状态
"""

import requests

def test_final_dictionary():
    try:
        response = requests.get('http://127.0.0.1:8000/kg/dictionary')
        data = response.json()
        
        if data.get('ok'):
            total = sum(len(entries) for entries in data['data'].values())
            print(f"✅ API状态: 正常")
            print(f"📊 总条目: {total}")
            print(f"📚 分类统计:")
            for category, entries in data['data'].items():
                print(f"   {category}: {len(entries)} 条")
            
            # 显示一些新增术语示例
            print(f"\n🆕 新增术语示例:")
            if data['data']['components']:
                comp = data['data']['components'][-1]  # 最后一个组件
                print(f"   组件: {comp.get('name')} - {comp.get('tags', [])}")
            
            if data['data']['symptoms']:
                symp = data['data']['symptoms'][-1]  # 最后一个症状
                print(f"   症状: {symp.get('name')} - {symp.get('tags', [])}")
                
            if data['data']['tools_processes']:
                tool = data['data']['tools_processes'][-1]  # 最后一个工具
                print(f"   工具: {tool.get('name')} - {tool.get('tags', [])}")
                
        else:
            print(f"❌ API错误: {data.get('error', {}).get('message', 'Unknown')}")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_final_dictionary()
