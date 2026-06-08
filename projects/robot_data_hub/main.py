#!/usr/bin/env python3
"""
机器人题材数据中心 - 主程序入口
采集多平台内容，输出到飞书多维表格
"""
import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from src.config_loader import ConfigLoader
from src.platform_collector import PlatformCollectorHub
from src.content_processor import ContentProcessor
from src.feishu_output import OutputHub


def main(target_date=None):
    """主流程"""
    print("=" * 60)
    print("      机器人题材数据中心")
    print("=" * 60)

    # 1. 初始化配置
    config_loader = ConfigLoader()

    # 2. 初始化采集器
    collector_hub = PlatformCollectorHub(config_loader)

    # 3. 采集内容
    all_items = collector_hub.collect_all(target_date)

    # 4. 处理和分析内容
    processor = ContentProcessor(config_loader)
    analysis = processor.process(all_items)

    # 5. 导出数据
    output_hub = OutputHub(config_loader)
    output_hub.export_all(all_items, analysis)

    print("\n" + "=" * 60)
    print("✓ 流程执行完成！")
    print("=" * 60)


if __name__ == "__main__":
    target_date = None
    if len(sys.argv) > 1:
        target_date = sys.argv[1]
    main(target_date)
