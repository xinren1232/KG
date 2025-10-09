#!/usr/bin/env python3
import requests

def test_api():
    try:
        r = requests.get('http://localhost:8000/health')
        print(f'API状态: {r.status_code}')
        if r.status_code == 200:
            print('✅ API正常运行')
            return True
        else:
            print('❌ API响应异常')
            return False
    except Exception as e:
        print(f'❌ API连接失败: {e}')
        return False

if __name__ == "__main__":
    test_api()
