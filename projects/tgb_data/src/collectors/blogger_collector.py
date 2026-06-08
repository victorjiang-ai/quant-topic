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
        
        这个方法需要接入实际的微博API或爬虫逻辑
        目前返回模拟数据
        
        Args:
            url: 微博用户URL
            target_date: 目标日期
            
        Returns:
            微博帖子列表
        """
        return []
    
    def _fetch_wechat_articles(self, account: str, 
                              target_date: str = None) -> List[Dict[str, Any]]:
        """
        获取微信公众号文章
        
        这个方法需要接入实际的微信公众号API或爬虫逻辑
        目前返回模拟数据
        
        Args:
            account: 微信公众号账号
            target_date: 目标日期
            
        Returns:
            文章列表
        """
        return []
    
    def _fetch_xueqiu_posts(self, url: str, 
                           target_date: str = None) -> List[Dict[str, Any]]:
        """
        获取雪球帖子
        
        这个方法需要接入实际的雪球API或爬虫逻辑
        目前返回模拟数据
        
        Args:
            url: 雪球用户URL
            target_date: 目标日期
            
        Returns:
            雪球帖子列表
        """
        return []
    
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
