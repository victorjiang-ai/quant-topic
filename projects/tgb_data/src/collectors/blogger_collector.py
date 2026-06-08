"""
博主采集模块
负责从不同平台采集博主内容
"""

import re
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from ..utils.config_loader import ConfigLoader
from ..utils.date_utils import DateUtils


class BloggerCollector:
    """博主内容采集器"""
    
    def __init__(self, config_loader: ConfigLoader = None):
        """
        初始化采集器
        
        Args:
            config_loader: 配置加载器实例
        """
        self.config_loader = config_loader or ConfigLoader()
        self.date_utils = DateUtils()
    
    def collect_all(self, target_date: str = None) -> List[Dict[str, Any]]:
        """
        采集所有博主的内容
        
        Args:
            target_date: 目标日期，格式 YYYY-MM-DD，默认为前一天
            
        Returns:
            所有博主的内容列表
        """
        bloggers = self.config_loader.get_enabled_bloggers()
        all_contents = []
        
        for blogger in bloggers:
            contents = self.collect_blogger(blogger, target_date)
            all_contents.extend(contents)
        
        return all_contents
    
    def collect_blogger(self, blogger: Dict[str, Any], 
                       target_date: str = None) -> List[Dict[str, Any]]:
        """
        采集单个博主的内容
        
        Args:
            blogger: 博主信息
            target_date: 目标日期
            
        Returns:
            博主内容列表
        """
        platform = blogger.get('platform', '').lower()
        
        if platform == 'weibo':
            return self._collect_weibo(blogger, target_date)
        elif platform == 'wechat':
            return self._collect_wechat(blogger, target_date)
        elif platform == 'xueqiu':
            return self._collect_xueqiu(blogger, target_date)
        else:
            return self._collect_generic(blogger, target_date)
    
    def _collect_weibo(self, blogger: Dict[str, Any], 
                      target_date: str = None) -> List[Dict[str, Any]]:
        """
        采集微博内容
        
        Args:
            blogger: 博主信息
            target_date: 目标日期
            
        Returns:
            微博内容列表
        """
        url = blogger.get('url', '')
        
        posts = self._fetch_weibo_posts(url, target_date)
        
        return [{
            'blogger_id': blogger.get('id'),
            'blogger_name': blogger.get('name'),
            'platform': 'weibo',
            'title': post.get('title', f"微博_{post.get('id', '')}"),
            'original_content': post.get('content', ''),
            'publish_time': post.get('created_at', ''),
            'read_count': post.get('read_count', 0),
            'like_count': post.get('like_count', 0),
            'url': url,
            'tags': blogger.get('tags', [])
        } for post in posts]
    
    def _collect_wechat(self, blogger: Dict[str, Any], 
                      target_date: str = None) -> List[Dict[str, Any]]:
        """
        采集微信公众号内容
        
        Args:
            blogger: 博主信息
            target_date: 目标日期
            
        Returns:
            微信公众号内容列表
        """
        account = blogger.get('account', '')
        
        articles = self._fetch_wechat_articles(account, target_date)
        
        return [{
            'blogger_id': blogger.get('id'),
            'blogger_name': blogger.get('name'),
            'platform': 'wechat',
            'title': article.get('title', ''),
            'original_content': article.get('content', ''),
            'publish_time': article.get('publish_time', ''),
            'read_count': article.get('read_count', 0),
            'like_count': article.get('like_count', 0),
            'url': article.get('url', ''),
            'digest': article.get('digest', ''),
            'tags': blogger.get('tags', [])
        } for article in articles]
    
    def _collect_xueqiu(self, blogger: Dict[str, Any], 
                      target_date: str = None) -> List[Dict[str, Any]]:
        """
        采集雪球内容
        
        Args:
            blogger: 博主信息
            target_date: 目标日期
            
        Returns:
            雪球内容列表
        """
        url = blogger.get('url', '')
        
        posts = self._fetch_xueqiu_posts(url, target_date)
        
        return [{
            'blogger_id': blogger.get('id'),
            'blogger_name': blogger.get('name'),
            'platform': 'xueqiu',
            'title': post.get('title', f"雪球_{post.get('id', '')}"),
            'original_content': post.get('content', ''),
            'publish_time': post.get('created_at', ''),
            'read_count': post.get('view_count', 0),
            'comment_count': post.get('comment_count', 0),
            'like_count': post.get('like_count', 0),
            'url': url,
            'tags': blogger.get('tags', [])
        } for post in posts]
    
    def _collect_generic(self, blogger: Dict[str, Any], 
                        target_date: str = None) -> List[Dict[str, Any]]:
        """
        采集通用平台内容
        
        Args:
            blogger: 博主信息
            target_date: 目标日期
            
        Returns:
            内容列表
        """
        return [{
            'blogger_id': blogger.get('id'),
            'blogger_name': blogger.get('name'),
            'platform': blogger.get('platform', 'unknown'),
            'title': '',
            'original_content': '',
            'publish_time': target_date or datetime.now().strftime('%Y-%m-%d'),
            'read_count': 0,
            'like_count': 0,
            'url': blogger.get('url', ''),
            'tags': blogger.get('tags', []),
            'note': '请配置具体的平台采集逻辑'
        }]
    
    def _fetch_weibo_posts(self, url: str, target_date: str = None) -> List[Dict[str, Any]]:
        """
        获取微博帖子
        
        目前返回高质量的示例数据，方便系统测试
        实际生产可接入微博API或爬虫
        
        Args:
            url: 微博用户URL
            target_date: 目标日期
            
        Returns:
            微博帖子列表
        """
        import random
        from datetime import datetime, timedelta
        
        date_str = target_date or (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        sample_posts = [
            {
                'id': 'wb_001',
                'title': f'市场分析{date_str}：创业板突破压力位',
                'content': '''今日创业板强势反弹，突破了2000点的关键压力位。
从技术面看，MACD金叉，KDJ指标也显示超卖后的反弹信号。
建议关注科技板块，尤其是人工智能和半导体产业链的相关标的。
关注龙头：宁德时代、比亚迪、昆仑万维。''',
                'created_at': f'{date_str} 09:15:00',
                'read_count': random.randint(10000, 50000),
                'like_count': random.randint(500, 2000)
            },
            {
                'id': 'wb_002',
                'title': '题材轮动观察：新能源汽车产业链',
                'content': '''今天新能源汽车板块表现抢眼，整车厂和锂电池材料都有不错的涨幅。
从资金流向看，北向资金持续流入宁德时代、比亚迪。
技术面上，板块指数站上5日线，建议重点关注。
关注：宁德时代、比亚迪、赣锋锂业。''',
                'created_at': f'{date_str} 10:30:00',
                'read_count': random.randint(8000, 30000),
                'like_count': random.randint(300, 1000)
            },
            {
                'id': 'wb_003',
                'title': '风险提示：注意短期回调风险',
                'content': '''虽然今日市场表现不错，但仍需注意风险。
从历史规律看，连续上涨后往往会有回调整固。
建议控制仓位，不要追高。耐心等待更好的买点。''',
                'created_at': f'{date_str} 14:45:00',
                'read_count': random.randint(5000, 20000),
                'like_count': random.randint(200, 800)
            }
        ]
        
        return sample_posts
    
    def _fetch_wechat_articles(self, account: str, 
                              target_date: str = None) -> List[Dict[str, Any]]:
        """
        获取微信公众号文章
        
        目前返回高质量的示例数据，方便系统测试
        实际生产可接入公众号API或第三方服务
        
        Args:
            account: 微信公众号账号
            target_date: 目标日期
            
        Returns:
            文章列表
        """
        import random
        from datetime import datetime, timedelta
        
        date_str = target_date or (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        sample_articles = [
            {
                'id': 'wx_001',
                'title': '2026年A股投资策略：科技为王',
                'content': '''2026年的投资主线仍然是科技创新。
从政策面看，国家大力支持人工智能、半导体、新能源等战略新兴产业。
从基本面看，相关公司的业绩增长确定性高。
从估值看，经过调整后，很多优质标的已经具备投资价值。
建议重点布局：人工智能、半导体、新能源汽车、创新药。''',
                'publish_time': f'{date_str} 08:00:00',
                'read_count': random.randint(20000, 100000),
                'like_count': random.randint(1000, 5000),
                'digest': '2026年投资策略分析，科技板块有望成为全年主线。',
                'url': ''
            },
            {
                'id': 'wx_002',
                'title': '深度分析：半导体产业链投资机会',
                'content': '''半导体产业链包括：
1. 上游：设备、材料
2. 中游：设计、制造、封测
3. 下游：应用端（AI、消费电子、汽车电子）
推荐关注：北方华创、中微公司、中芯国际、长电科技。
建议采用分批建仓策略，不要一次性买入。''',
                'publish_time': f'{date_str} 12:30:00',
                'read_count': random.randint(15000, 60000),
                'like_count': random.randint(800, 3000),
                'digest': '半导体产业链深度分析，细分领域投资机会梳理。',
                'url': ''
            }
        ]
        
        return sample_articles
    
    def _fetch_xueqiu_posts(self, url: str, 
                           target_date: str = None) -> List[Dict[str, Any]]:
        """
        获取雪球帖子
        
        目前返回高质量的示例数据，方便系统测试
        实际生产可接入雪球API或爬虫
        
        Args:
            url: 雪球用户URL
            target_date: 目标日期
            
        Returns:
            雪球帖子列表
        """
        import random
        from datetime import datetime, timedelta
        
        date_str = target_date or (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        sample_posts = [
            {
                'id': 'xq_001',
                'title': '实盘记录：今日买入宁德时代',
                'content': '''今日实盘操作：
- 买入宁德时代 300股，成本价 165.50元
- 逻辑：新能源汽车景气度回升，公司基本面优秀

后续计划：如果回调到160元继续加仓，目标看180-200元。
止损位：150元。''',
                'created_at': f'{date_str} 10:00:00',
                'view_count': random.randint(5000, 20000),
                'comment_count': random.randint(100, 500),
                'like_count': random.randint(200, 1000)
            },
            {
                'id': 'xq_002',
                'title': '财报解读：贵州茅台2026Q1',
                'content': '''贵州茅台公布2026年一季报：
- 营收 368亿元，同比+18.5%
- 净利润 172亿元，同比+19.2%
- 毛利率 92.1%，保持稳定

点评：业绩符合预期，公司基本面稳健。
作为A股核心资产，适合长期持有。
当前PE 35倍，处于历史合理区间。''',
                'created_at': f'{date_str} 15:30:00',
                'view_count': random.randint(8000, 30000),
                'comment_count': random.randint(200, 800),
                'like_count': random.randint(500, 2000)
            },
            {
                'id': 'xq_003',
                'title': '市场观点：当前市场处于什么位置？',
                'content': '''从几个维度分析当前市场：
1. 估值：上证综指PE 12倍，处于历史30%分位
2. 情绪：市场情绪中性偏谨慎
3. 资金：北向资金持续流入

结论：当前是布局优质股票的好时机。
建议：分批买入，控制仓位在5-7成。
重点方向：消费、医药、科技。''',
                'created_at': f'{date_str} 20:45:00',
                'view_count': random.randint(10000, 40000),
                'comment_count': random.randint(300, 1000),
                'like_count': random.randint(1000, 3000)
            }
        ]
        
        return sample_posts
    
    def collect_with_date_range(self, start_date: str, 
                                end_date: str) -> List[Dict[str, Any]]:
        """
        按日期范围采集所有博主内容
        
        Args:
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            
        Returns:
            所有内容列表
        """
        start = self.date_utils.parse_date(start_date)
        end = self.date_utils.parse_date(end_date)
        dates = self.date_utils.get_date_range(start, end)
        
        all_contents = []
        for d in dates:
            date_str = self.date_utils.format_date(d)
            contents = self.collect_all(date_str)
            all_contents.extend(contents)
        
        return all_contents
    
    def collect_weekend(self, ref_date: str = None) -> List[Dict[str, Any]]:
        """
        采集周末内容
        
        Args:
            ref_date: 参考日期，默认为今天
            
        Returns:
            周末所有内容
        """
        if ref_date:
            ref = self.date_utils.parse_date(ref_date)
        else:
            ref = None
        
        friday, saturday, sunday = self.date_utils.get_weekend_dates(ref)
        
        return self.collect_with_date_range(
            self.date_utils.format_date(friday),
            self.date_utils.format_date(sunday)
        )
