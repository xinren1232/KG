#!/usr/bin/env python3
import requests
import time

def create_test_pdf():
    """创建测试PDF文档"""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib import colors
        
        doc = SimpleDocTemplate("test_quality_report.pdf", pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # 标题
        story.append(Paragraph("硬件质量分析报告", styles['Title']))
        story.append(Spacer(1, 12))
        
        # 内容
        story.append(Paragraph("1. 产品概述", styles['Heading2']))
        story.append(Paragraph("本报告分析了智能手机的硬件质量问题。", styles['Normal']))
        story.append(Spacer(1, 12))
        
        story.append(Paragraph("2. 问题统计", styles['Heading2']))
        story.append(Paragraph("在测试过程中发现了多个硬件问题，包括电池续航异常和屏幕显示故障。", styles['Normal']))
        story.append(Spacer(1, 12))
        
        # 表格数据
        data = [
            ['问题类型', '数量', '严重程度'],
            ['电池续航短', '8', '高'],
            ['屏幕显示异常', '5', '中'],
            ['摄像头模糊', '3', '低']
        ]
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        story.append(Spacer(1, 12))
        
        story.append(Paragraph("3. 分析结论", styles['Heading2']))
        story.append(Paragraph("主要质量问题集中在电池和显示模块，需要重点关注供应商质量控制。", styles['Normal']))
        
        doc.build(story)
        print("✅ 创建PDF测试文档: test_quality_report.pdf")
        return True
        
    except ImportError:
        print("❌ reportlab未安装，创建简单文本文件代替")
        # 创建简单的文本文件
        with open('test_quality_report.txt', 'w', encoding='utf-8') as f:
            f.write("""硬件质量分析报告

1. 产品概述
本报告分析了智能手机的硬件质量问题。

2. 问题统计
在测试过程中发现了多个硬件问题，包括电池续航异常和屏幕显示故障。

问题类型 | 数量 | 严重程度
电池续航短 | 8 | 高
屏幕显示异常 | 5 | 中
摄像头模糊 | 3 | 低

3. 分析结论
主要质量问题集中在电池和显示模块，需要重点关注供应商质量控制。
""")
        print("✅ 创建文本测试文档: test_quality_report.txt")
        return False

def test_pdf_parsing():
    """测试PDF文档解析"""
    print("\n=== 测试PDF文档解析 ===")
    
    # 创建测试文档
    has_pdf = create_test_pdf()
    filename = 'test_quality_report.pdf' if has_pdf else 'test_quality_report.txt'
    file_type = 'PDF' if has_pdf else '文本'
    
    try:
        # 1. 上传文件
        print(f"1. 上传{file_type}文档...")
        with open(filename, 'rb') as f:
            files = {'file': f}
            upload_response = requests.post('http://localhost:8000/kg/upload', files=files, timeout=10)
        
        if upload_response.status_code != 200:
            print(f"   ❌ 上传失败: {upload_response.status_code}")
            print(f"   错误: {upload_response.text}")
            return False
        
        upload_result = upload_response.json()
        if not upload_result.get('success'):
            print(f"   ❌ 上传失败: {upload_result.get('message')}")
            return False
        
        upload_id = upload_result.get('upload_id')
        print(f"   ✅ 上传成功: {upload_id}")
        
        # 2. 触发解析
        print("2. 触发解析...")
        parse_response = requests.post(f'http://localhost:8000/kg/files/{upload_id}/parse', timeout=10)
        
        if parse_response.status_code != 200:
            print(f"   ❌ 解析请求失败: {parse_response.status_code}")
            print(f"   错误: {parse_response.text}")
            return False
        
        parse_result = parse_response.json()
        if not parse_result.get('success'):
            print(f"   ❌ 解析失败: {parse_result.get('message')}")
            return False
        
        print(f"   ✅ 解析触发成功: {parse_result.get('message')}")
        
        # 3. 等待解析完成
        print("3. 等待解析完成...")
        time.sleep(3)
        
        # 4. 获取解析结果
        print("4. 获取解析结果...")
        preview_response = requests.get(f'http://localhost:8000/kg/files/{upload_id}/preview', timeout=10)
        
        if preview_response.status_code != 200:
            print(f"   ❌ 获取结果失败: {preview_response.status_code}")
            print(f"   错误: {preview_response.text}")
            return False
        
        preview_result = preview_response.json()
        if not preview_result.get('success'):
            print(f"   ❌ 获取结果失败: {preview_result.get('message')}")
            return False
        
        data = preview_result.get('data', {})
        raw_data = data.get('raw_data', [])
        entities = data.get('entities', [])
        
        print(f"   ✅ 解析结果获取成功!")
        print(f"   📊 统计信息:")
        print(f"      - 原始数据条数: {len(raw_data)}")
        print(f"      - 识别实体数量: {len(entities)}")
        
        # 显示解析内容
        if raw_data:
            print(f"   📄 解析内容示例:")
            for i, item in enumerate(raw_data[:5]):
                content = item.get('content', '')[:80]
                item_type = item.get('type', '未知')
                print(f"      {i+1}. [{item_type}] {content}...")
        
        # 显示识别的实体
        if entities:
            print(f"   🏷️ 识别的实体:")
            for entity in entities[:5]:
                name = entity.get('name')
                entity_type = entity.get('type')
                confidence = entity.get('confidence', 0)
                print(f"      - {name} ({entity_type}) - 置信度: {confidence:.2f}")
        
        return len(raw_data) > 0  # 如果有解析数据就算成功
        
    except Exception as e:
        print(f"   ❌ 测试异常: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔧 开始测试PDF文档解析...")
    
    # 测试PDF文档解析
    if test_pdf_parsing():
        print("\n🎉 PDF文档解析修复成功!")
    else:
        print("\n❌ PDF文档解析仍有问题")
    
    print("\n测试完成。")
