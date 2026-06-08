"""
内容处理器与分析模块
"""
import re
from typing import Dict, Any, List
from collections import Counter
from datetime import datetime
from .platform_collector import ContentItem


class ContentAnalyzer:
    """内容分析器"""

    def __init__(self, config_loader):
        self.config_loader = config_loader
        self.analysis_config = config_loader.get_analysis_config()
        # 简单的情感分析词库
        self.positive_words = [
            "好", "赞", "棒", "优秀", "牛逼", "看好", "上涨", "利好",
            "突破", "增长", "成功", "机遇", "希望", "看好", "推荐",
        ]
        self.negative_words = [
            "差", "烂", "糟", "坑", "失败", "下跌", "利空", "风险",
            "担忧", "危机", "崩溃", "问题", "失望", "不看好", "糟糕",
        ]

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """简单情感分析"""
        if not self.analysis_config.get("sentiment_analysis", True):
            return {"sentiment": "neutral", "score": 0}

        text_lower = text.lower()
        positive_count = sum(1 for word in self.positive_words if word in text_lower)
        negative_count = sum(1 for word in self.negative_words if word in text_lower)

        total = positive_count + negative_count
        if total == 0:
            sentiment = "neutral"
            score = 0
        else:
            score = (positive_count - negative_count) / total
            if score > 0.1:
                sentiment = "positive"
            elif score < -0.1:
                sentiment = "negative"
            else:
                sentiment = "neutral"

        return {
            "sentiment": sentiment,
            "score": score,
            "positive_count": positive_count,
            "negative_count": negative_count,
        }

    def extract_hot_keywords(self, items: List[ContentItem]) -> List[str]:
        """提取热词"""
        if not self.analysis_config.get("hot_keywords_extraction", True):
            return []

        all_text = ""
        for item in items:
            all_text += " " + item.title + " " + item.content

        words = re.findall(r"[\u4e00-\u9fa5]+", all_text)
        filtered = [word for word in words if len(word) >= 2]
        counter = Counter(filtered)
        hot_words = [word for word, count in counter.most_common(20)]
        return hot_words

    def calculate_hot_score(self, item: ContentItem) -> float:
        """计算内容热度分"""
        score = 0
        if item.views:
            score += item.views * 0.1
        if item.likes:
            score += item.likes * 1
        if item.comments:
            score += item.comments * 3
        if item.shares:
            score += item.shares * 5
        return score

    def analyze_collection(self, all_items: Dict[str, List[ContentItem]]) -> Dict[str, Any]:
        """分析所有采集内容"""
        all_items_flat = []
        platform_stats = {}

        for platform, items in all_items.items():
            all_items_flat.extend(items)
            platform_stats[platform] = {
                "count": len(items),
                "total_views": sum(i.views for i in items),
                "total_likes": sum(i.likes for i in items),
                "total_comments": sum(i.comments for i in items),
            }

        hot_keywords = self.extract_hot_keywords(all_items_flat)

        # 按热度排序
        all_items_flat.sort(
            key=lambda x: self.calculate_hot_score(x), reverse=True
        )

        sentiment_summary = {
            "positive": 0,
            "negative": 0,
            "neutral": 0,
        }
        for item in all_items_flat[:100]:
            sent = self.analyze_sentiment(item.content)
            sentiment_summary[sent["sentiment"]] += 1

        return {
            "platform_stats": platform_stats,
            "hot_keywords": hot_keywords,
            "total_count": len(all_items_flat),
            "top_hot_items": all_items_flat[:10],
            "sentiment_summary": sentiment_summary,
        }


class ContentProcessor:
    """内容处理器"""

    def __init__(self, config_loader):
        self.config_loader = config_loader
        self.analyzer = ContentAnalyzer(config_loader)

    def process(self, all_items: Dict[str, List[ContentItem]]) -> Dict[str, Any]:
        """处理和分析所有内容"""
        print("正在处理和分析内容...")

        analysis_result = self.analyzer.analyze_collection(all_items)

        print(f"✓ 分析完成！总内容数：{analysis_result['total_count']}")
        print(f"✓ 平台统计：{analysis_result['platform_stats']}")

        return analysis_result
