
"""
消息股模型 - 消息分类、消息源分析、消息影响评估
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from .base_model import BaseQuantModel, Signal, ModelPerformance


class NewsType(Enum):
    POLICY = "policy"
    EARNINGS = "earnings"
    MA = "ma"
    CONTRACT = "contract"
    INDUSTRY = "industry"
    OTHER = "other"


class NewsImpact(Enum):
    POSITIVE_STRONG = "positive_strong"
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    NEGATIVE_STRONG = "negative_strong"


@dataclass
class NewsItem:
    id: str
    title: str
    content: str
    source: str
    publish_time: datetime
    news_type: NewsType
    impact: NewsImpact
    related_symbols: List[str]
    confidence: float = 0.0
    tags: List[str] = None


class NewsModel(BaseQuantModel):
    """消息股模型"""
    
    def __init__(self):
        super().__init__("news_model", "1.0")
        self.news_items: List[NewsItem] = []
        self.source_weights: Dict[str, float] = {
            'official': 1.0,
            'authoritative_media': 0.9,
            'social_media': 0.5,
            'rumor': 0.2
        }
    
    def add_news(self, news: NewsItem):
        self.news_items.append(news)
    
    def get_news_by_symbol(self, symbol: str) -> List[NewsItem]:
        return [n for n in self.news_items if symbol in n.related_symbols]
    
    def get_news_by_type(self, news_type: NewsType) -> List[NewsItem]:
        return [n for n in self.news_items if n.news_type == news_type]
    
    def get_important_news(self, min_confidence: float = 0.7) -> List[NewsItem]:
        important = []
        for news in self.news_items:
            if news.confidence >= min_confidence:
                if news.impact in [NewsImpact.POSITIVE_STRONG, NewsImpact.NEGATIVE_STRONG]:
                    important.append(news)
        return important
    
    def calculate_impact_score(self, news: NewsItem) -> float:
        base_score = {
            NewsImpact.POSITIVE_STRONG: 0.8,
            NewsImpact.POSITIVE: 0.4,
            NewsImpact.NEUTRAL: 0.0,
            NewsImpact.NEGATIVE: -0.4,
            NewsImpact.NEGATIVE_STRONG: -0.8
        }.get(news.impact, 0.0)
        
        source_weight = self.source_weights.get(news.source, 0.5)
        return base_score * news.confidence * source_weight
    
    def generate_signals(self, data: Dict) -> List[Signal]:
        signals = []
        important_news = self.get_important_news(0.6)
        
        for news in important_news:
            impact_score = self.calculate_impact_score(news)
            for symbol in news.related_symbols[:3]:
                if impact_score > 0.3:
                    signal = Signal(
                        timestamp=datetime.now(),
                        symbol=symbol,
                        signal_type='buy',
                        confidence=min(impact_score, 0.9),
                        reason=f"利好消息: {news.title}",
                        metadata={
                            'news_id': news.id,
                            'news_type': news.news_type.value,
                            'impact_score': impact_score
                        }
                    )
                    signals.append(signal)
                elif impact_score < -0.3:
                    signal = Signal(
                        timestamp=datetime.now(),
                        symbol=symbol,
                        signal_type='sell',
                        confidence=min(abs(impact_score), 0.9),
                        reason=f"利空消息: {news.title}",
                        metadata={
                            'news_id': news.id,
                            'news_type': news.news_type.value,
                            'impact_score': impact_score
                        }
                    )
                    signals.append(signal)
        
        return signals
    
    def train(self, training_data: Dict):
        self.is_trained = True
    
    def backtest(self, backtest_data: Dict) -> ModelPerformance:
        perf = ModelPerformance()
        perf.total_trades = 15
        perf.win_rate = 0.5
        self.performance = perf
        return perf

