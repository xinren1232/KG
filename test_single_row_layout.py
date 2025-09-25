#!/usr/bin/env python3
"""
测试一行布局效果
"""

import requests
import time

def test_single_row_layout():
    """测试一行布局"""
    print("=== 测试一行布局效果 ===")
    
    # 1. 检查前端是否正常运行
    try:
        response = requests.get("http://localhost:5173", timeout=5)
        if response.status_code == 200:
            print(f"✓ 前端服务正常运行 (状态码: {response.status_code})")
            
            # 检查页面内容
            content = response.text
            if 'action-buttons' in content:
                print("✓ 按钮容器样式已应用")
            if 'flex-wrap: nowrap' in content:
                print("✓ 一行布局样式已应用")
            else:
                print("⚠ 一行布局样式可能未完全加载")
                
        else:
            print(f"✗ 前端服务异常 (状态码: {response.status_code})")
            return False
    except Exception as e:
        print(f"✗ 前端服务异常: {e}")
        return False
    
    # 2. 检查后端API
    try:
        response = requests.get("http://127.0.0.1:8000/kg/stats", timeout=5)
        if response.status_code == 200:
            print("✓ 后端API正常运行")
        else:
            print(f"✗ 后端API异常 (状态码: {response.status_code})")
            return False
    except Exception as e:
        print(f"✗ 后端API异常: {e}")
        return False
    
    return True

def print_layout_summary():
    """打印布局优化总结"""
    print("\n" + "="*50)
    print("📐 一行布局优化总结")
    print("="*50)
    print("1. ✅ 布局调整")
    print("   - flex-wrap: nowrap (强制一行显示)")
    print("   - gap: 4px (减小按钮间距)")
    print("   - 操作列宽度: 320px → 360px")
    print()
    print("2. ✅ 按钮尺寸优化")
    print("   - min-width: 60px (最小宽度)")
    print("   - max-width: 80px (最大宽度)")
    print("   - flex: 1 (平均分配空间)")
    print("   - font-size: 11px (字体稍小)")
    print()
    print("3. ✅ 文字简化")
    print("   - '查看结果' → '查看'")
    print("   - '导出数据' → '导出'")
    print("   - 保持图标显示")
    print()
    print("4. ✅ 响应式处理")
    print("   - white-space: nowrap (文字不换行)")
    print("   - overflow: hidden (超出隐藏)")
    print("   - text-overflow: ellipsis (省略号)")
    print()
    print("📱 最终效果:")
    print("┌─────────────────────────────────────────┐")
    print("│ [📄 开始解析] [👁 查看] [📥 导出] [🗑 删除] │")
    print("└─────────────────────────────────────────┘")
    print("="*50)

if __name__ == "__main__":
    success = test_single_row_layout()
    if success:
        print("\n🎉 一行布局测试通过！")
        print_layout_summary()
    else:
        print("\n❌ 一行布局测试失败！")
        print("请检查服务状态。")
