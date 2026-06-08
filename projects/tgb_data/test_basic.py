#!/usr/bin/env python3
"""
测试脚本 - 用于快速验证项目功能
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.utils.config_loader import ConfigLoader
from src.utils.date_utils import DateUtils
from src.collectors.content_processor import ContentProcessor
from src.outputs.local_output import LocalOutput
from datetime import date

def test_basic_functions():
    """测试基本功能"""
    print("=" * 60)
    print("TGB量化数据采集系统 - 基础功能测试")
    print("=" * 60)
    
    # 测试1: 配置加载
    print("\n1️⃣ 测试配置加载...")
    try:
        config = ConfigLoader()
        bloggers = config.get_enabled_bloggers()
        print(f"   ✅ 成功加载 {len(bloggers)} 位博主")
        for blogger in bloggers[:3]:
            print(f"      - {blogger.get('name')} ({blogger.get('platform')})")
    except Exception as e:
        print(f"   ❌ 配置加载失败: {e}")
        return False
    
    # 测试2: 日期工具
    print("\n2️⃣ 测试日期工具...")
    try:
        date_utils = DateUtils()
        today = date.today()
        yesterday = date_utils.get_previous_day(today)
        print(f"   ✅ 日期工具正常")
        print(f"      - 今天: {date_utils.format_date(today)}")
        print(f"      - 昨天: {date_utils.format_date(yesterday)}")
        print(f"      - 是周末? {date_utils.is_weekend(today)}")
    except Exception as e:
        print(f"   ❌ 日期工具失败: {e}")
        return False
    
    # 测试3: 内容处理器
    print("\n3️⃣ 测试内容处理器...")
    try:
        processor = ContentProcessor()
        
        # 测试数据
        test_content = """
        今天股市震荡，建议关注银行股和科技股。
        市场情绪偏积极，看好后续走势。
        注意控制仓位，不要追高。
        """
        
        summary = processor.generate_summary(test_content, max_length=50)
        keywords = processor.extract_keywords(test_content)
        sentiment = processor.analyze_sentiment(test_content)
        
        print(f"   ✅ 内容处理正常")
        print(f"      - 总结: {summary}")
        print(f"      - 关键词: {keywords}")
        print(f"      - 情感: {sentiment['sentiment']}")
    except Exception as e:
        print(f"   ❌ 内容处理失败: {e}")
        return False
    
    # 测试4: 本地输出
    print("\n4️⃣ 测试本地输出...")
    try:
        output = LocalOutput()
        
        # 创建模拟数据
        test_contents = [
            {
                "blogger_id": "blogger_001",
                "blogger_name": "测试博主A",
                "platform": "weibo",
                "title": "市场分析",
                "original_content": "今天股市震荡上行，建议关注新能源板块",
                "publish_time": "2024-05-17 10:00:00",
                "read_count": 1000,
                "like_count": 50,
                "tags": ["技术分析"],
                "summary": "关注新能源板块",
                "keywords": ["股市", "新能源"],
                "sentiment": {"sentiment": "positive"}
            },
            {
                "blogger_id": "blogger_002",
                "blogger_name": "测试博主B",
                "platform": "xueqiu",
                "title": "投资建议",
                "original_content": "市场风险较大，注意控制仓位",
                "publish_time": "2024-05-17 14:00:00",
                "read_count": 500,
                "like_count": 30,
                "tags": ["风险控制"],
                "summary": "注意风险控制",
                "keywords": ["风险", "仓位"],
                "sentiment": {"sentiment": "neutral"}
            }
        ]
        
        # 保存测试数据
        test_date = "2024-05-17"
        blogger_data = output._group_by_blogger(test_contents)
        saved_path = output.save_collection(test_date, test_contents, blogger_data)
        
        print(f"   ✅ 本地输出正常")
        print(f"      - 文件已保存: {saved_path}")
        
        # 检查文件是否存在
        if Path(saved_path).exists():
            print(f"      - 文件验证: 存在 ✓")
        else:
            print(f"      - 文件验证: 不存在 ✗")
            return False
            
    except Exception as e:
        print(f"   ❌ 本地输出失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 60)
    print("🎉 所有基础功能测试通过！")
    print("=" * 60)
    print("\n📁 项目已成功搭建，可以使用以下命令：")
    print("   - 查看帮助: python3 main.py --help")
    print("   - 完整运行: python3 main.py --mode full")
    print("   - 仅采集:   python3 main.py --mode daily")
    print("\n📖 详细文档请查看: QUICKSTART.md")
    return True

if __name__ == "__main__":
    success = test_basic_functions()
    sys.exit(0 if success else 1)
