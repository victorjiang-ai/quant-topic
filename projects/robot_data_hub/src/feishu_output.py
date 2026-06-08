"""
飞书多维表格输出模块
"""
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
from .platform_collector import ContentItem
import subprocess


class FeishuBitableExporter:
    """飞书多维表格导出器"""

    def __init__(self, config_loader):
        self.config_loader = config_loader
        self.output_config = config_loader.get_output_config()
        self.feishu_config = self.output_config.get("feishu", {})
        self.base_app_token = self.feishu_config.get("base_app_token", "")
        self.table_name = self.feishu_config.get("table_name", "舆情采集")

    def export_to_feishu(self, all_items: Dict[str, List[ContentItem]], analysis: Dict[str, Any]) -> bool:
        """
        导出到飞书多维表格（使用 lark-cli 命令）
        注意：实际项目中需要配置 lark-cli 并先创建多维表格
        """
        if not self.feishu_config.get("enabled", True):
            print("飞书输出未启用")
            return False

        print("✓ 提示：飞书多维表格同步功能已准备")
        print(f"  - 知识库 App Token: {self.base_app_token}")
        print(f"  - 目标表格: {self.table_name}")
        print("\n  使用 lark-cli 多维表格功能需要先完成：")
        print("  1. lark-cli auth login 登录")
        print("  2. 在飞书中创建多维表格并获取 table_id")
        print("  3. 在 config 中配置 table_id")
        print("\n  以下是本模块生成的数据示例：")

        # 生成示例输出，展示要写入的数据格式
        self._print_sample_data(all_items)
        return True

    def _print_sample_data(self, all_items: Dict[str, List[ContentItem]]):
        """打印示例数据"""
        all_items_flat = []
        for items in all_items.values():
            all_items_flat.extend(items)

        print("\n  前 5 条内容数据示例：")
        for i, item in enumerate(all_items_flat[:5], 1):
            print(f"\n  内容 {i}:")
            print(f"    - 平台: {item.platform_name}")
            print(f"    - 标题: {item.title}")
            print(f"    - 作者: {item.author}")
            print(f"    - 时间: {item.publish_time}")
            print(f"    - 浏览: {item.views}, 点赞: {item.likes}, 评论: {item.comments}")


class LocalExporter:
    """本地文件导出器"""

    def __init__(self, config_loader):
        self.config_loader = config_loader
        self.output_config = config_loader.get_output_config()
        self.local_config = self.output_config.get("local", {})
        self.output_dir = Path(self.local_config.get("directory", "./collections"))
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export_to_local(self, all_items: Dict[str, List[ContentItem]], analysis: Dict[str, Any]) -> bool:
        """导出到本地文件"""
        if not self.local_config.get("enabled", True):
            print("本地输出未启用")
            return False

        date_str = datetime.now().strftime("%Y-%m-%d")

        # 1. 导出各平台原始数据
        for platform, items in all_items.items():
            file_path = self.output_dir / f"{date_str}_{platform}_raw.md"
            self._export_platform_to_md(file_path, platform, items)

        # 2. 导出分析报告
        summary_path = self.output_dir / f"{date_str}_analysis_summary.md"
        self._export_analysis_to_md(summary_path, analysis)

        print(f"✓ 本地文件已导出到：{self.output_dir.absolute()}")
        return True

    def _export_platform_to_md(self, file_path: Path, platform: str, items: List[ContentItem]):
        """导出单个平台到 Markdown"""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"# {platform} 采集内容\n\n")
            f.write(f"采集时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"内容数量: {len(items)}\n\n")
            f.write("---\n\n")

            for i, item in enumerate(items, 1):
                f.write(f"## {i}. {item.title}\n\n")
                f.write(f"- **作者**: {item.author}\n")
                f.write(f"- **发布时间**: {item.publish_time}\n")
                f.write(f"- **数据**: 浏览 {item.views} / 点赞 {item.likes} / 评论 {item.comments}\n")
                f.write(f"- **链接**: {item.url}\n\n")
                f.write(f"**内容**: {item.content}\n\n")
                f.write("---\n\n")

    def _export_analysis_to_md(self, file_path: Path, analysis: Dict[str, Any]):
        """导出分析报告"""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("# 内容分析报告\n\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"总内容数: {analysis['total_count']}\n\n")

            f.write("## 平台统计\n\n")
            for platform, stats in analysis["platform_stats"].items():
                f.write(f"### {platform}\n")
                f.write(f"- 内容数: {stats['count']}\n")
                f.write(f"- 总浏览: {stats['total_views']}\n")
                f.write(f"- 总点赞: {stats['total_likes']}\n\n")

            f.write("## 热词\n\n")
            f.write(", ".join(analysis["hot_keywords"]) + "\n\n")

            f.write("## TOP 10 热门内容\n\n")
            for i, item in enumerate(analysis["top_hot_items"], 1):
                f.write(f"{i}. [{item.platform_name}] {item.title} (浏览:{item.views})\n")


class OutputHub:
    """输出调度中心"""

    def __init__(self, config_loader):
        self.config_loader = config_loader
        self.feishu_exporter = FeishuBitableExporter(config_loader)
        self.local_exporter = LocalExporter(config_loader)

    def export_all(self, all_items: Dict[str, List[ContentItem]], analysis: Dict[str, Any]):
        """导出所有输出"""
        print("\n--- 正在导出数据 ---")

        self.local_exporter.export_to_local(all_items, analysis)
        self.feishu_exporter.export_to_feishu(all_items, analysis)

        print("✓ 导出流程完成")
