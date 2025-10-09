#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查API服务状态和当前数据
"""

import requests

def check_api_status():
    """检查API服务状态"""
    try:
        response = requests.get('http://localhost:8000/api/dictionary', timeout=5)
        if response.status_code == 200:
            data = response.json()
            total_count = len(data['data'])
            print(f'✅ API服务正常，当前词典数据: {total_count}条')
            
            # 检查Label分布
            response2 = requests.get('http://localhost:8000/api/dictionary/labels')
            if response2.status_code == 200:
                labels_data = response2.json()
                print('当前Label分布:')
                for label_info in labels_data['data']['labels']:
                    label = label_info['label']
                    count = label_info['count']
                    print(f'  {label}: {count}条')
                
                return True, total_count
            else:
                print(f'❌ 获取Label分布失败: {response2.status_code}')
                return False, 0
        else:
            print(f'❌ API服务异常: {response.status_code}')
            return False, 0
    except Exception as e:
        print(f'❌ API服务连接失败: {e}')
        return False, 0

def check_specific_labels():
    """检查特定Label的数据"""
    labels_to_check = ['Material', 'Role', 'Metric']
    
    for label in labels_to_check:
        try:
            response = requests.get(f'http://localhost:8000/api/dictionary/{label}')
            if response.status_code == 200:
                data = response.json()
                count = len(data['data'])
                print(f'  {label}: {count}条')
                
                # 显示前几条数据
                if count > 0:
                    print(f'    示例数据:')
                    for i, item in enumerate(data['data'][:3]):
                        name = item.get('name', 'Unknown')
                        print(f'      {i+1}. {name}')
            else:
                print(f'  {label}: API错误 {response.status_code}')
        except Exception as e:
            print(f'  {label}: 连接失败 {e}')

def main():
    print("🔍 检查API服务状态...")
    
    success, total = check_api_status()
    
    if success:
        print(f"\n📊 重点关注缺失的Label:")
        check_specific_labels()
        
        print(f"\n✅ 当前系统状态良好，共有 {total} 条词典数据")
        print("💡 可以继续补充Material和Role类别的数据")
    else:
        print("\n❌ API服务不可用，请检查服务状态")

if __name__ == "__main__":
    main()
