"""
采集模块初始化文件
"""

from .blogger_collector import BloggerCollector
from .content_processor import ContentProcessor

__all__ = ['BloggerCollector', 'ContentProcessor']
