#!/usr/bin/env python3
"""
系统测试脚本 - 验证整个采集和分析流程
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.utils.config_loader import ConfigLoader
from src.collectors.blogger_collector import BloggerCollector
from src.collectors.content_processor import ContentProcessor
from src.outputs.local_output import LocalOutput
from datetime import datetime

print("=" * 60)
print("TGB量化采集系统 - 完整流程测试")
print("=" * 60)

# 1. 测试配置加载
print("\n[1/5] 测试配置加载...")
config_loader = ConfigLoader()
bloggers = config_loader.get_enabled_bloggers()
print(f"✓ 加载到 {len(bloggers)} 位博主")
for b in bloggers:
    print(f"  - {b.get('name')} ({b.get('platform')})")

# 2. 测试采集器
print("\n[2/5] 测试内容采集...")
collector = BloggerCollector(config_loader)
target_date = datetime.now().strftime('%Y-%m-%d')
contents = collector.collect_all(target_date)
print(f"✓ 采集到 {len(contents)} 条内容")

# 3. 测试内容处理
print("\n[3/5] 测试内容处理...")
processor = ContentProcessor()
summary_config = config_loader.get_summary_config()
processed_contents = processor.process_batch(contents, summary_config)
print(f"✓ 处理完成 {len(processed_contents)} 条内容")

if processed_contents:
    first = processed_contents[0]
    print(f"\n  示例内容：")
    print(f"  - 标题: {first.get('title', 'N/A')}")
    print(f"  - 摘要: {first.get('summary', 'N/A')[:80]}...")
    print(f"  - 关键词: {first.get('keywords', [])}")
    print(f"  - 情感: {first.get('sentiment', {}).get('sentiment', 'N/A')}")

# 4. 测试本地输出
print("\n[4/5] 测试本地输出...")
local_output = LocalOutput()
blogger_data = local_output._group_by_blogger(processed_contents)
collection_path = local_output.save_collection(target_date, processed_contents, blogger_data)
print(f"✓ 合集已保存: {collection_path}")

# 5. 测试报告生成
print("\n[5/5] 测试报告生成...")
from main import QuantTgbSystem
system = QuantTgbSystem()
result = system.generate_daily_report(target_date)

if result and result.get('success'):
    print(f"✓ 报告已生成: {result.get('report_path')}")
else:
    print(f"✓ 报告生成完成")

print("\n" + "=" * 60)
print("✓ 系统测试完成！")
print("=" * 60)
