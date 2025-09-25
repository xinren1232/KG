#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def check_latest_upload():
    # 检查最新的上传文件 - 这是一个真正的DOCX文件
    upload_id = '357d434f-3011-4732-aec6-6217392bfe3f'
    base_url = 'http://127.0.0.1:8000'

    try:
        # 获取文件信息
        response = requests.get(f'{base_url}/kg/files/{upload_id}')
        if response.status_code == 200:
            data = response.json()
            file_info = data.get('data', {})
            print(f'文件名: {file_info.get("filename", "unknown")}')
            print(f'文件大小: {file_info.get("size", "unknown")}')
            print(f'上传时间: {file_info.get("upload_time", "unknown")}')
            
            # 检查状态
            status_response = requests.get(f'{base_url}/kg/files/{upload_id}/status')
            if status_response.status_code == 200:
                status_data = status_response.json()
                current_status = status_data.get('data', {}).get('status', 'unknown')
                print(f'当前状态: {current_status}')
            
            # 如果是DOCX文件，检查解析结果
            filename = file_info.get('filename', '')
            if filename.lower().endswith('.docx'):
                print('这是一个DOCX文件！')
                
                # 获取解析结果
                preview_response = requests.get(f'{base_url}/kg/files/{upload_id}/preview')
                if preview_response.status_code == 200:
                    preview_data = preview_response.json()
                    if preview_data.get('success'):
                        raw_data = preview_data.get('data', {}).get('raw_data', [])
                        print(f'解析记录数: {len(raw_data)}')
                        if len(raw_data) == 0:
                            print('❌ 解析结果为空！')
                            
                            # 检查缓存文件
                            from pathlib import Path
                            cache_file = Path(f"api/cache/{upload_id}.json")
                            if cache_file.exists():
                                print(f'📄 检查缓存文件: {cache_file}')
                                try:
                                    with open(cache_file, 'r', encoding='utf-8') as f:
                                        cache_data = json.load(f)
                                    print(f'   缓存文件大小: {cache_file.stat().st_size} bytes')
                                    print(f'   缓存数据结构: {list(cache_data.keys())}')
                                    
                                    if 'raw_data' in cache_data:
                                        cached_raw_data = cache_data['raw_data']
                                        print(f'   缓存中的记录数: {len(cached_raw_data)}')
                                        if len(cached_raw_data) > 0:
                                            print(f'   第一条记录: {cached_raw_data[0]}')
                                    
                                except Exception as e:
                                    print(f'   ❌ 读取缓存文件失败: {e}')
                            else:
                                print('❌ 缓存文件不存在')
                        else:
                            print('✅ 解析成功')
                            for i, record in enumerate(raw_data[:3]):
                                content_type = record.get('content_type', 'unknown')
                                content = record.get('content', '')
                                print(f'  记录{i+1}: {content_type} - {content[:50]}...')
                    else:
                        print(f'❌ 解析失败: {preview_data.get("error", "未知错误")}')
                else:
                    print(f'❌ 获取解析结果失败: {preview_response.status_code}')
            else:
                print(f'这不是DOCX文件，文件类型: {filename}')
        else:
            print(f'❌ 获取文件信息失败: {response.status_code}')
            
    except Exception as e:
        print(f'❌ 检查失败: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_latest_upload()
