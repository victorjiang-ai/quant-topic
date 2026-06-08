"""
内容处理模块
负责内容总结、关键词提取、情感分析等
"""

import re
from typing import List, Dict, Any, Optional
from collections import Counter


class ContentProcessor:
    """内容处理器"""
    
    def __init__(self):
        """初始化内容处理器"""
        self.finance_keywords = [
            '股票', '基金', 'A股', '港股', '美股', '上证', '深证', '创业板',
            '科创板', '北交所', '沪深300', '上证指数', '深证成指',
            '牛市', '熊市', '震荡', '回调', '反弹', '突破', '压力', '支撑',
            '买入', '卖出', '建仓', '清仓', '加仓', '减仓', '补仓',
            '涨停', '跌停', '停牌', '复牌',
            '分红', '送股', '配股', '增发', '回购',
            '财报', '业绩', '营收', '利润', '净利润', '同比增长', '环比增长',
            '行业', '板块', '概念', '题材', '龙头', '白马', '黑马',
            'PE', 'PB', 'ROE', 'EPS', '股息率',
            '基本面', '技术面', '消息面', '资金面',
            '主力', '庄家', '散户', '机构', '北向资金', '外资'
        ]
    
    def generate_summary(self, content: str, max_length: int = 200) -> str:
        """
        生成内容摘要
        
        Args:
            content: 原始内容
            max_length: 最大摘要长度
            
        Returns:
            内容摘要
        """
        if not content:
            return ''
        
        content = self._clean_content(content)
        
        if len(content) <= max_length:
            return content
        
        sentences = re.split(r'[。！？\n]', content)
        summary = ''
        
        for sentence in sentences:
            if len(summary) + len(sentence) <= max_length:
                summary += sentence + '。'
            else:
                break
        
        if not summary:
            summary = content[:max_length] + '...'
        
        return summary.strip()
    
    def extract_keywords(self, content: str, top_n: int = 5) -> List[str]:
        """
        提取关键词
        
        Args:
            content: 内容文本
            top_n: 返回前N个关键词
            
        Returns:
            关键词列表
        """
        if not content:
            return []
        
        content = self._clean_content(content)
        
        found_keywords = []
        for keyword in self.finance_keywords:
            if keyword in content:
                found_keywords.append(keyword)
        
        keyword_counts = Counter(found_keywords)
        
        return [kw for kw, _ in keyword_counts.most_common(top_n)]
    
    def analyze_sentiment(self, content: str) -> Dict[str, Any]:
        """
        简单情感分析
        
        Args:
            content: 内容文本
            
        Returns:
            情感分析结果
        """
        if not content:
            return {'sentiment': 'neutral', 'score': 0.0, 'keywords': []}
        
        positive_words = [
            '涨', '涨了', '大涨', '涨停', '盈利', '赚钱', '看好', '买入',
            '推荐', '机会', '突破', '反弹', '上升', '增长', '上升趋势'
        ]
        
        negative_words = [
            '跌', '跌了', '大跌', '跌停', '亏损', '亏钱', '看空', '卖出',
            '警告', '风险', '回调', '下跌', '下降', '减少', '下降趋势'
        ]
        
        content_lower = content.lower()
        
        pos_count = sum(1 for word in positive_words if word in content_lower)
        neg_count = sum(1 for word in negative_words if word in content_lower)
        
        total = pos_count + neg_count
        
        if total == 0:
            sentiment = 'neutral'
            score = 0.0
        elif pos_count > neg_count:
            sentiment = 'positive'
            score = pos_count / total
        elif neg_count > pos_count:
            sentiment = 'negative'
            score = -neg_count / total
        else:
            sentiment = 'neutral'
            score = 0.0
        
        return {
            'sentiment': sentiment,
            'score': score,
            'positive_count': pos_count,
            'negative_count': neg_count
        }
    
    def extract_trading_signals(self, content: str) -> Dict[str, List[str]]:
        """
        提取交易信号
        
        Args:
            content: 内容文本
            
        Returns:
            交易信号字典
        """
        signals = {
            'buy_signals': [],
            'sell_signals': [],
            'risk_warnings': []
        }
        
        buy_patterns = [
            r'建议买入',
            r'可以买入',
            r'推荐买入',
            r'买入时机',
            r'值得关注',
            r'布局机会',
            r'低吸',
            r'加仓'
        ]
        
        sell_patterns = [
            r'建议卖出',
            r'可以考虑卖出',
            r'减仓',
            r'清仓',
            r'规避',
            r'远离',
            r'注意风险'
        ]
        
        risk_patterns = [
            r'注意风险',
            r'风险提示',
            r'谨慎',
            r'风险较大',
            r'不建议',
            r'避开',
            r'风险因素'
        ]
        
        for pattern in buy_patterns:
            matches = re.findall(pattern, content)
            signals['buy_signals'].extend(matches)
        
        for pattern in sell_patterns:
            matches = re.findall(pattern, content)
            signals['sell_signals'].extend(matches)
        
        for pattern in risk_patterns:
            matches = re.findall(pattern, content)
            signals['risk_warnings'].extend(matches)
        
        signals['buy_signals'] = list(set(signals['buy_signals']))
        signals['sell_signals'] = list(set(signals['sell_signals']))
        signals['risk_warnings'] = list(set(signals['risk_warnings']))
        
        return signals
    
    def filter_finance_content(self, content: str) -> bool:
        """
        判断内容是否与金融相关
        
        Args:
            content: 内容文本
            
        Returns:
            是否与金融相关
        """
        if not content:
            return False
        
        match_count = sum(1 for keyword in self.finance_keywords if keyword in content)
        return match_count >= 2
    
    def extract_stock_codes(self, content: str) -> List[str]:
        """
        提取股票代码
        
        Args:
            content: 内容文本
            
        Returns:
            股票代码列表
        """
        pattern = r'\b\d{6}\b'
        codes = re.findall(pattern, content)
        return list(set(codes))
    
    def extract_stock_names(self, content: str) -> List[str]:
        """
        提取股票名称
        
        Args:
            content: 内容文本
            
        Returns:
            股票名称列表
        """
        names = []
        common_stocks = [
            '茅台', '宁德时代', '比亚迪', '腾讯', '阿里', '京东', '美团',
            '百度', '拼多多', '网易', '小米', '华为'
        ]
        
        for name in common_stocks:
            if name in content:
                names.append(name)
        
        return list(set(names))
    
    def process_content(self, content_item: Dict[str, Any], 
                       summary_config: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        处理单条内容
        
        Args:
            content_item: 原始内容项
            summary_config: 总结配置
            
        Returns:
            处理后的内容
        """
        if summary_config is None:
            max_length = 200
        else:
            max_length = summary_config.get('max_length', 200)
        
        original_content = content_item.get('original_content', '')
        
        summary = self.generate_summary(original_content, max_length)
        
        keywords = self.extract_keywords(original_content)
        
        sentiment = self.analyze_sentiment(original_content)
        
        signals = self.extract_trading_signals(original_content)
        
        stock_codes = self.extract_stock_codes(original_content)
        stock_names = self.extract_stock_names(original_content)
        
        processed = content_item.copy()
        processed['summary'] = summary
        processed['keywords'] = keywords
        processed['sentiment'] = sentiment
        processed['buy_signals'] = signals.get('buy_signals', [])
        processed['sell_signals'] = signals.get('sell_signals', [])
        processed['risk_warnings'] = signals.get('risk_warnings', [])
        processed['stock_codes'] = stock_codes
        processed['stock_names'] = stock_names
        
        return processed
    
    def process_batch(self, contents: List[Dict[str, Any]], 
                     summary_config: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        批量处理内容
        
        Args:
            contents: 内容列表
            summary_config: 总结配置
            
        Returns:
            处理后的内容列表
        """
        return [self.process_content(content, summary_config) for content in contents]
    
    def _clean_content(self, content: str) -> str:
        """
        清理内容文本
        
        Args:
            content: 原始内容
            
        Returns:
            清理后的内容
        """
        content = re.sub(r'http[s]?://\S+', '', content)
        content = re.sub(r'@\S+', '', content)
        content = re.sub(r'#\S+#', '', content)
        content = re.sub(r'\s+', ' ', content)
        content = content.strip()
        
        return content
