#!/usr/bin/env python3
"""
检查Vue组件的方法暴露情况，修复Vue警告
"""

import os
import re
from pathlib import Path

def check_vue_component(file_path):
    """检查单个Vue组件的方法暴露情况"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找模板中使用的方法
        template_methods = set()
        template_match = re.search(r'<template>(.*?)</template>', content, re.DOTALL)
        if template_match:
            template_content = template_match.group(1)
            # 查找@click事件
            click_methods = re.findall(r'@click="([^"(]+)', template_content)
            template_methods.update(click_methods)
            
            # 查找其他方法调用
            method_calls = re.findall(r'\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', template_content)
            template_methods.update(method_calls)
        
        # 查找setup函数中定义的方法
        setup_methods = set()
        setup_match = re.search(r'setup\(\)\s*\{(.*?)return\s*\{(.*?)\}', content, re.DOTALL)
        if setup_match:
            setup_content = setup_match.group(1)
            return_content = setup_match.group(2)
            
            # 查找const方法定义
            const_methods = re.findall(r'const\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(?:async\s+)?\(', setup_content)
            setup_methods.update(const_methods)
            
            # 查找return中暴露的方法
            exposed_methods = set()
            # 移除注释和换行，然后查找方法名
            clean_return = re.sub(r'//.*?\n', '', return_content)
            clean_return = re.sub(r'\s+', ' ', clean_return)
            method_names = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)(?:\s*,|\s*$)', clean_return)
            exposed_methods.update(method_names)
            
            # 检查缺失的方法
            missing_methods = template_methods - exposed_methods
            unused_methods = setup_methods - template_methods - exposed_methods
            
            return {
                'file': file_path,
                'template_methods': template_methods,
                'setup_methods': setup_methods,
                'exposed_methods': exposed_methods,
                'missing_methods': missing_methods,
                'unused_methods': unused_methods
            }
    
    except Exception as e:
        return {
            'file': file_path,
            'error': str(e)
        }

def main():
    """主函数"""
    print("🔍 检查Vue组件方法暴露情况...")
    
    # 检查系统管理组件
    system_components_dir = Path("apps/web/src/components/system")
    if system_components_dir.exists():
        print(f"\n📁 检查目录: {system_components_dir}")
        
        for vue_file in system_components_dir.glob("*.vue"):
            result = check_vue_component(vue_file)
            
            if 'error' in result:
                print(f"❌ {vue_file.name}: {result['error']}")
                continue
            
            print(f"\n📄 {vue_file.name}")
            print(f"  模板中使用的方法: {result['template_methods']}")
            print(f"  setup中定义的方法: {result['setup_methods']}")
            print(f"  return中暴露的方法: {result['exposed_methods']}")
            
            if result['missing_methods']:
                print(f"  ⚠️  缺失暴露的方法: {result['missing_methods']}")
            
            if result['unused_methods']:
                print(f"  💡 未使用的方法: {result['unused_methods']}")
            
            if not result['missing_methods'] and not result['unused_methods']:
                print(f"  ✅ 方法暴露正常")
    
    # 检查主要视图组件
    views_dir = Path("apps/web/src/views")
    if views_dir.exists():
        print(f"\n📁 检查目录: {views_dir}")
        
        # 只检查几个主要的组件
        main_views = ['SystemManagement.vue', 'GraphVisualization.vue', 'DictionaryManagement.vue']
        
        for view_name in main_views:
            view_file = views_dir / view_name
            if view_file.exists():
                result = check_vue_component(view_file)
                
                if 'error' in result:
                    print(f"❌ {view_name}: {result['error']}")
                    continue
                
                print(f"\n📄 {view_name}")
                if result['missing_methods']:
                    print(f"  ⚠️  缺失暴露的方法: {result['missing_methods']}")
                else:
                    print(f"  ✅ 方法暴露正常")

if __name__ == "__main__":
    main()
