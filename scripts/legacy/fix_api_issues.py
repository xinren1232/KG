#!/usr/bin/env python3
"""
检查和修复API调用问题
"""

import os
import re
from pathlib import Path

def check_api_calls(file_path):
    """检查文件中的API调用"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找API调用
        api_calls = []
        
        # 查找 api.methodName() 调用
        api_pattern = r'api\.([a-zA-Z][a-zA-Z0-9]*)\s*\('
        matches = re.finditer(api_pattern, content)
        
        for match in matches:
            method_name = match.group(1)
            line_num = content[:match.start()].count('\n') + 1
            
            # 获取调用的上下文
            lines = content.split('\n')
            context_start = max(0, line_num - 2)
            context_end = min(len(lines), line_num + 2)
            context = '\n'.join(lines[context_start:context_end])
            
            api_calls.append({
                'method': method_name,
                'line': line_num,
                'context': context
            })
        
        return {
            'file': file_path,
            'api_calls': api_calls
        }
    
    except Exception as e:
        return {
            'file': file_path,
            'error': str(e)
        }

def check_api_definitions():
    """检查API定义"""
    api_file = Path("apps/web/src/api/index.js")
    if not api_file.exists():
        return []
    
    try:
        with open(api_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找API方法定义
        method_pattern = r'([a-zA-Z][a-zA-Z0-9]*)\s*\([^)]*\)\s*\{'
        matches = re.finditer(method_pattern, content)
        
        defined_methods = []
        for match in matches:
            method_name = match.group(1)
            if method_name not in ['use', 'config', 'interceptors']:  # 排除axios内置方法
                defined_methods.append(method_name)
        
        return defined_methods
    
    except Exception as e:
        print(f"❌ 检查API定义失败: {e}")
        return []

def main():
    """主函数"""
    print("🔍 检查API调用问题...")
    
    # 获取已定义的API方法
    defined_methods = check_api_definitions()
    print(f"📋 已定义的API方法: {defined_methods}")
    
    # 检查主要组件的API调用
    files_to_check = [
        "apps/web/src/views/SystemManagement.vue",
        "apps/web/src/views/GraphVisualization.vue",
        "apps/web/src/views/DictionaryManagement.vue",
        "apps/web/src/components/system/DataSourceManagement.vue",
        "apps/web/src/components/system/MonitoringManagement.vue"
    ]
    
    issues_found = []
    
    for file_path in files_to_check:
        file_path_obj = Path(file_path)
        if file_path_obj.exists():
            result = check_api_calls(file_path_obj)
            
            if 'error' in result:
                print(f"❌ {file_path}: {result['error']}")
                continue
            
            print(f"\n📄 {file_path_obj.name}")
            
            if result['api_calls']:
                for call in result['api_calls']:
                    method = call['method']
                    line = call['line']
                    
                    if method in defined_methods:
                        print(f"  ✅ 第{line}行: api.{method}() - 方法存在")
                    else:
                        print(f"  ⚠️  第{line}行: api.{method}() - 方法不存在")
                        issues_found.append({
                            'file': file_path,
                            'method': method,
                            'line': line,
                            'context': call['context']
                        })
            else:
                print(f"  📝 无API调用")
    
    # 报告问题
    if issues_found:
        print(f"\n⚠️  发现 {len(issues_found)} 个API调用问题:")
        for issue in issues_found:
            print(f"\n📁 文件: {issue['file']}")
            print(f"🔍 第{issue['line']}行: api.{issue['method']}()")
            print(f"📝 上下文:")
            print(f"```")
            print(issue['context'])
            print(f"```")
    else:
        print(f"\n✅ 未发现API调用问题")
    
    # 检查常见的undefined问题
    print(f"\n🔧 检查常见的undefined问题...")
    
    # 检查可能导致undefined的模式
    undefined_patterns = [
        r'api\.\w+\(\s*undefined',  # api.method(undefined)
        r'api\.\w+\([^)]*undefined',  # api.method(param, undefined)
        r'await\s+api\.\w+\(\s*\)',  # await api.method() 没有参数但需要参数
    ]
    
    for file_path in files_to_check:
        file_path_obj = Path(file_path)
        if file_path_obj.exists():
            try:
                with open(file_path_obj, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for pattern in undefined_patterns:
                    matches = re.finditer(pattern, content)
                    for match in matches:
                        line_num = content[:match.start()].count('\n') + 1
                        print(f"⚠️  {file_path_obj.name} 第{line_num}行: 可能的undefined问题")
                        print(f"   {match.group()}")
            
            except Exception as e:
                print(f"❌ 检查 {file_path} 失败: {e}")
    
    print(f"\n💡 建议:")
    print(f"  1. 确保所有API调用的方法都在 api/index.js 中定义")
    print(f"  2. 检查API调用时传递的参数是否正确")
    print(f"  3. 添加错误处理来捕获API调用失败")
    print(f"  4. 使用浏览器开发者工具查看网络请求详情")

if __name__ == "__main__":
    main()
