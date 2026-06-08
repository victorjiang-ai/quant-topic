"""
日期工具模块
提供日期处理相关功能
"""

from datetime import datetime, timedelta, date
from typing import List, Tuple


class DateUtils:
    """日期工具类"""
    
    @staticmethod
    def get_previous_day(ref_date: date = None) -> date:
        """
        获取前一天日期
        
        Args:
            ref_date: 参考日期，默认为今天
            
        Returns:
            前一天日期
        """
        if ref_date is None:
            ref_date = date.today()
        return ref_date - timedelta(days=1)
    
    @staticmethod
    def get_weekend_dates(ref_date: date = None) -> Tuple[date, date, date]:
        """
        获取周末日期范围（周五到周日）
        
        Args:
            ref_date: 参考日期，默认为今天
            
        Returns:
            (周五, 周六, 周日) 元组
        """
        if ref_date is None:
            ref_date = date.today()
        
        weekday = ref_date.weekday()
        
        if weekday == 5:
            saturday = ref_date
            sunday = ref_date + timedelta(days=1)
            friday = ref_date - timedelta(days=1)
        elif weekday == 6:
            sunday = ref_date
            saturday = ref_date - timedelta(days=1)
            friday = ref_date - timedelta(days=2)
        else:
            days_until_friday = (weekday - 4) % 7
            if days_until_friday == 0 and weekday == 4:
                friday = ref_date
            else:
                friday = ref_date - timedelta(days=(days_until_friday if days_until_friday > 0 else 7))
            saturday = friday + timedelta(days=1)
            sunday = friday + timedelta(days=2)
        
        return friday, saturday, sunday
    
    @staticmethod
    def format_date(date_obj: date, format_str: str = "%Y-%m-%d") -> str:
        """
        格式化日期
        
        Args:
            date_obj: 日期对象
            format_str: 格式字符串
            
        Returns:
            格式化后的日期字符串
        """
        return date_obj.strftime(format_str)
    
    @staticmethod
    def parse_date(date_str: str, format_str: str = "%Y-%m-%d") -> date:
        """
        解析日期字符串
        
        Args:
            date_str: 日期字符串
            format_str: 格式字符串
            
        Returns:
            日期对象
        """
        return datetime.strptime(date_str, format_str).date()
    
    @staticmethod
    def is_weekend(ref_date: date = None) -> bool:
        """
        判断是否为周末
        
        Args:
            ref_date: 参考日期，默认为今天
            
        Returns:
            是否为周末
        """
        if ref_date is None:
            ref_date = date.today()
        
        weekday = ref_date.weekday()
        return weekday in [5, 6]
    
    @staticmethod
    def is_weekday(ref_date: date = None) -> bool:
        """
        判断是否为工作日
        
        Args:
            ref_date: 参考日期，默认为今天
            
        Returns:
            是否为工作日
        """
        return not DateUtils.is_weekend(ref_date)
    
    @staticmethod
    def get_date_range(start_date: date, end_date: date) -> List[date]:
        """
        获取日期范围内的所有日期
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            日期列表
        """
        dates = []
        current = start_date
        while current <= end_date:
            dates.append(current)
            current += timedelta(days=1)
        return dates
    
    @staticmethod
    def get_previous_weekday(ref_date: date = None) -> date:
        """
        获取前一个工作日
        
        Args:
            ref_date: 参考日期，默认为今天
            
        Returns:
            前一个工作日
        """
        if ref_date is None:
            ref_date = date.today()
        
        current = ref_date - timedelta(days=1)
        while current.weekday() in [5, 6]:
            current -= timedelta(days=1)
        
        return current
    
    @staticmethod
    def get_chinese_weekday(ref_date: date = None) -> str:
        """
        获取中文星期几
        
        Args:
            ref_date: 参考日期，默认为今天
            
        Returns:
            中文星期几
        """
        if ref_date is None:
            ref_date = date.today()
        
        weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
        return weekdays[ref_date.weekday()]
    
    @staticmethod
    def get_timestamp() -> str:
        """
        获取当前时间戳字符串
        
        Returns:
            时间戳字符串
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
