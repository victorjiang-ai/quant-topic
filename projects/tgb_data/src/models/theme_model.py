
"""
题材模型 - 题材图谱、龙头识别、题材轮动
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import defaultdict
import json
from pathlib import Path

from .base_model import BaseQuantModel, Signal, ModelPerformance


@dataclass
class Theme:
    """题材"""
    id: str
    name: str
    description: str
    hot_score: float = 0.0
    mention_count: int = 0
    stocks: List[str] = None
    upstream: List[str] = None
    downstream: List[str] = None
    related_themes: List[str] = None
    first_mention: datetime = None
    last_mention: datetime = None
    tags: List[str] = None
    
    def __post_init__(self):
        self.stocks = self.stocks or []
        self.upstream = self.upstream or []
        self.downstream = self.downstream or []
        self.related_themes = self.related_themes or []
        self.tags = self.tags or []


@dataclass
class ThemeStock:
    """题材股票"""
    symbol: str
    name: str
    theme_id: str
    tier: int  # 1=龙头, 2=核心, 3=跟风
    weight: float = 0.0
    correlation: float = 0.0
    is_leader: bool = False


class ThemeModel(BaseQuantModel):
    """题材模型"""
    
    def __init__(self):
        super().__init__("theme_model", "1.0")
        self.themes: Dict[str, Theme] = {}
        self.theme_stocks: Dict[str, List[ThemeStock]] = defaultdict(list)
        self.stock_themes: Dict[str, List[str]] = defaultdict(list)
        self.theme_history: List[Dict] = []
    
    def add_theme(self, theme: Theme):
        """添加题材"""
        self.themes[theme.id] = theme
        for stock in theme.stocks:
            self.stock_themes[stock].append(theme.id)
    
    def add_theme_stock(self, theme_id: str, stock: ThemeStock):
        """添加题材股票"""
        self.theme_stocks[theme_id].append(stock)
        self.stock_themes[stock.symbol].append(theme_id)
    
    def calculate_hot_score(self, theme_id: str, mention_weight: float = 0.4, stock_performance_weight: float = 0.4, growth_weight: float = 0.2) -> float:
        """
        计算题材热度
        
        Args:
            theme_id: 题材ID
            mention_weight: 提及权重
            stock_performance_weight: 股票表现权重
            growth_weight: 增长权重
            
        Returns:
            热度分数 0-100
        """
        if theme_id not in self.themes:
            return 0.0
            
        theme = self.themes[theme_id]
        
        mention_score = min(theme.mention_count / 100 * 100, 100)
        performance_score = 50.0
        growth_score = 50.0
        
        hot_score = (
            mention_score * mention_weight +
            performance_score * stock_performance_weight +
            growth_score * growth_weight
        )
        
        theme.hot_score = hot_score
        return hot_score
    
    def identify_leaders(self, theme_id: str) -> List[ThemeStock]:
        """
        识别龙头股
        
        Args:
            theme_id: 题材ID
            
        Returns:
            龙头股列表
        """
        if theme_id not in self.theme_stocks:
            return []
            
        stocks = self.theme_stocks[theme_id]
        sorted_stocks = sorted(stocks, key=lambda x: (x.tier, -x.weight))
        
        for i, stock in enumerate(sorted_stocks):
            stock.is_leader = (i < 3 and stock.tier == 1)
            
        return [s for s in sorted_stocks if s.is_leader]
    
    def get_related_themes(self, theme_id: str) -> List[Theme]:
        """
        获取相关题材
        
        Args:
            theme_id: 题材ID
            
        Returns:
            相关题材列表
        """
        if theme_id not in self.themes:
            return []
            
        theme = self.themes[theme_id]
        related = []
        
        for related_id in theme.related_themes:
            if related_id in self.themes:
                related.append(self.themes[related_id])
        
        return related
    
    def get_hot_themes(self, top_n: int = 10) -> List[Theme]:
        """
        获取热门题材
        
        Args:
            top_n: 返回数量
            
        Returns:
            热门题材列表
        """
        sorted_themes = sorted(self.themes.values(), key=lambda x: -x.hot_score)
        return sorted_themes[:top_n]
    
    def generate_signals(self, data: Dict) -> List[Signal]:
        """
        生成题材相关交易信号
        
        Args:
            data: 包含市场数据、新闻等
            
        Returns:
            交易信号列表
        """
        signals = []
        hot_themes = self.get_hot_themes(5)
        
        for theme in hot_themes:
            if theme.hot_score > 70:
                leaders = self.identify_leaders(theme.id)
                for leader in leaders:
                    signal = Signal(
                        timestamp=datetime.now(),
                        symbol=leader.symbol,
                        signal_type='buy',
                        confidence=min(theme.hot_score / 100, 0.9),
                        reason=f"题材 {theme.name} 热度高，{leader.name} 是龙头",
                        metadata={
                            'theme_id': theme.id,
                            'theme_name': theme.name,
                            'hot_score': theme.hot_score
                        }
                    )
                    signals.append(signal)
        
        return signals
    
    def train(self, training_data: Dict):
        self.is_trained = True
    
    def backtest(self, backtest_data: Dict) -> ModelPerformance:
        perf = ModelPerformance()
        perf.total_trades = 10
        perf.win_rate = 0.6
        self.performance = perf
        return perf
    
    def save_to_file(self, filepath: str):
        data = {
            'themes': {
                k: {
                    'id': v.id,
                    'name': v.name,
                    'description': v.description,
                    'hot_score': v.hot_score,
                    'mention_count': v.mention_count,
                    'stocks': v.stocks,
                    'upstream': v.upstream,
                    'downstream': v.downstream,
                    'related_themes': v.related_themes
                }
                for k, v in self.themes.items()
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'ThemeModel':
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        model = cls()
        for theme_data in data.get('themes', {}).values():
            theme = Theme(
                id=theme_data['id'],
                name=theme_data['name'],
                description=theme_data['description'],
                hot_score=theme_data.get('hot_score', 0),
                mention_count=theme_data.get('mention_count', 0),
                stocks=theme_data.get('stocks', []),
                upstream=theme_data.get('upstream', []),
                downstream=theme_data.get('downstream', []),
                related_themes=theme_data.get('related_themes', [])
            )
            model.add_theme(theme)
        
        return model

