"""
多平台内容采集器
"""
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class ContentItem:
    """内容项数据类"""
    platform: str
    platform_name: str
    title: str
    content: str
    url: str
    author: str
    publish_time: str
    views: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0


class BaseCollector:
    """基础采集器类"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = config.get("name", "unknown")
        self.keywords = config.get("keywords", [])
        self.base_url = config.get("base_url", "")

    def collect(self, target_date: Optional[str] = None, max_items: int = 50) -> List[ContentItem]:
        """采集内容（子类覆盖）"""
        raise NotImplementedError("子类需要实现此方法")


class DouyinCollector(BaseCollector):
    """抖音采集器"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)

    def collect(self, target_date: Optional[str] = None, max_items: int = 50) -> List[ContentItem]:
        """模拟采集抖音数据（实际项目需要接入真实API或爬虫）"""
        items = []
        date_str = target_date or (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        sample_titles = [
            "人形机器人最新进展！",
            "Optimus发布会预告！",
            "宇树机器人新品发布！",
            "机器人产业链分析！",
            "波士顿动力新视频！",
        ]

        for i in range(min(random.randint(5, 15), max_items)):
            keyword = random.choice(self.keywords)
            title = random.choice(sample_titles)
            content = f"这是关于{keyword}的精彩内容... {title}"
            items.append(
                ContentItem(
                    platform="douyin",
                    platform_name="抖音",
                    title=f"{title}（{keyword}）",
                    content=content,
                    url=f"{self.base_url}/search/{keyword}",
                    author=f"博主{random.randint(1000, 9999)}",
                    publish_time=f"{date_str} {random.randint(0, 23):02d}:{random.randint(0, 59):02d}",
                    views=random.randint(1000, 100000),
                    likes=random.randint(100, 10000),
                    comments=random.randint(10, 1000),
                    shares=random.randint(5, 500),
                )
            )
        return items


class XiaohongshuCollector(BaseCollector):
    """小红书采集器"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)

    def collect(self, target_date: Optional[str] = None, max_items: int = 50) -> List[ContentItem]:
        """模拟采集小红书数据"""
        items = []
        date_str = target_date or (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        sample_titles = [
            "机器人产业链投资机会！",
            "人形机器人未来展望！",
            "Optimus深度解析！",
            "机器人行业科普！",
        ]

        for i in range(min(random.randint(3, 12), max_items)):
            keyword = random.choice(self.keywords)
            title = random.choice(sample_titles)
            items.append(
                ContentItem(
                    platform="xiaohongshu",
                    platform_name="小红书",
                    title=f"{title}（{keyword}）",
                    content=f"今天聊聊{keyword}... 更多内容见正文！",
                    url=f"{self.base_url}/search/{keyword}",
                    author=f"小红薯{random.randint(1000, 9999)}",
                    publish_time=f"{date_str} {random.randint(0, 23):02d}:{random.randint(0, 59):02d}",
                    views=random.randint(500, 50000),
                    likes=random.randint(50, 5000),
                    comments=random.randint(5, 500),
                    shares=random.randint(3, 300),
                )
            )
        return items


class WeiboCollector(BaseCollector):
    """微博采集器"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)

    def collect(self, target_date: Optional[str] = None, max_items: int = 50) -> List[ContentItem]:
        """模拟采集微博数据"""
        items = []
        date_str = target_date or (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        sample_titles = [
            "【话题】#人形机器人#",
            "【热点】Optimus最新动态",
            "【分析】机器人产业链解读",
        ]

        for i in range(min(random.randint(8, 20), max_items)):
            keyword = random.choice(self.keywords)
            title = random.choice(sample_titles)
            items.append(
                ContentItem(
                    platform="weibo",
                    platform_name="微博",
                    title=f"{title} #{keyword}#",
                    content=f"这是一条关于{keyword}的微博... 更多内容见原链接！",
                    url=f"{self.base_url}/search/{keyword}",
                    author=f"大V{random.randint(1000, 9999)}",
                    publish_time=f"{date_str} {random.randint(0, 23):02d}:{random.randint(0, 59):02d}",
                    views=random.randint(10000, 500000),
                    likes=random.randint(100, 5000),
                    comments=random.randint(50, 1000),
                    shares=random.randint(20, 500),
                )
            )
        return items


class ZhihuCollector(BaseCollector):
    """知乎采集器"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)

    def collect(self, target_date: Optional[str] = None, max_items: int = 50) -> List[ContentItem]:
        """模拟采集知乎数据"""
        items = []
        date_str = target_date or (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        sample_titles = [
            "如何看待人形机器人的未来？",
            "Optimus会带来什么影响？",
            "机器人产业链投资分析！",
        ]

        for i in range(min(random.randint(4, 10), max_items)):
            keyword = random.choice(self.keywords)
            title = random.choice(sample_titles)
            items.append(
                ContentItem(
                    platform="zhihu",
                    platform_name="知乎",
                    title=f"{title}（{keyword}）",
                    content=f"谢邀！今天来聊聊{keyword}... 以下是我的分析：",
                    url=f"{self.base_url}/search?q={keyword}",
                    author=f"答主{random.randint(1000, 9999)}",
                    publish_time=f"{date_str} {random.randint(0, 23):02d}:{random.randint(0, 59):02d}",
                    views=random.randint(1000, 100000),
                    likes=random.randint(50, 2000),
                    comments=random.randint(10, 300),
                    shares=random.randint(5, 200),
                )
            )
        return items


class PlatformCollectorHub:
    """多平台采集调度中心"""

    def __init__(self, config_loader):
        self.config_loader = config_loader
        self.collectors = {}
        self._init_collectors()

    def _init_collectors(self):
        """初始化所有采集器"""
        platforms = self.config_loader.get_platforms()

        collector_classes = {
            "douyin": DouyinCollector,
            "xiaohongshu": XiaohongshuCollector,
            "weibo": WeiboCollector,
            "zhihu": ZhihuCollector,
        }

        for name, config in platforms.items():
            if name in collector_classes:
                self.collectors[name] = collector_classes[name](config)
            else:
                print(f"未找到平台 {name} 的采集器")

    def collect_all(self, target_date: Optional[str] = None) -> Dict[str, List[ContentItem]]:
        """采集所有平台"""
        results = {}
        collection_config = self.config_loader.get_collection_config()
        max_items = collection_config.get("max_items_per_platform", 50)

        for name, collector in self.collectors.items():
            print(f"正在采集 {name}...")
            items = collector.collect(target_date, max_items)
            results[name] = items
            print(f"✓ {name} 采集完成，获得 {len(items)} 条内容")

        return results

    def get_collector(self, name: str) -> Optional[BaseCollector]:
        """获取指定平台采集器"""
        return self.collectors.get(name)
