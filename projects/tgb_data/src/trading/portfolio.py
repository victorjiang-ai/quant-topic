
"""
组合管理 - 多模型信号融合、仓位管理
"""
from typing import Dict, List, Optional
from datetime import datetime
from collections import defaultdict

from ..models.base_model import Signal
from ..models.theme_model import ThemeModel
from ..models.board_model import BoardModel
from ..models.news_model import NewsModel
from ..models.price_volume_model import PriceVolumeModel


class SignalAggregator:
    """信号聚合器 - 融合多个模型的信号"""
    
    def __init__(self):
        self.model_weights: Dict[str, float] = {
            'theme_model': 0.3,
            'board_model': 0.25,
            'news_model': 0.2,
            'price_volume_model': 0.25
        }
    
    def aggregate_signals(self, signals_by_model: Dict[str, List[Signal]]) -&gt; List[Dict]:
        """
        聚合多个模型的信号
        
        Args:
            signals_by_model: {模型名: 信号列表}
            
        Returns:
            聚合后的信号列表
        """
        # 按股票分组
        symbol_signals = defaultdict(list)
        
        for model_name, signals in signals_by_model.items():
            weight = self.model_weights.get(model_name, 0.1)
            for signal in signals:
                symbol_signals[signal.symbol].append({
                    'signal': signal,
                    'model': model_name,
                    'weight': weight
                })
        
        # 计算每个股票的综合信号
        aggregated = []
        for symbol, sig_list in symbol_signals.items():
            buy_score = 0.0
            sell_score = 0.0
            supporting_models = []
            
            for sig_info in sig_list:
                signal = sig_info['signal']
                weight = sig_info['weight']
                
                if signal.signal_type == 'buy':
                    buy_score += signal.confidence * weight
                elif signal.signal_type == 'sell':
                    sell_score += signal.confidence * weight
                
                supporting_models.append({
                    'model': sig_info['model'],
                    'signal_type': signal.signal_type,
                    'confidence': signal.confidence,
                    'reason': signal.reason
                })
            
            # 决定最终信号
            final_signal = None
            if buy_score &gt; 0.3 and buy_score &gt; sell_score:
                final_signal = {
                    'symbol': symbol,
                    'signal_type': 'buy',
                    'score': buy_score,
                    'supporting_models': supporting_models
                }
            elif sell_score &gt; 0.3 and sell_score &gt; buy_score:
                final_signal = {
                    'symbol': symbol,
                    'signal_type': 'sell',
                    'score': sell_score,
                    'supporting_models': supporting_models
                }
            
            if final_signal:
                aggregated.append(final_signal)
        
        # 按分数排序
        aggregated.sort(key=lambda x: -x['score'])
        return aggregated


class PositionManager:
    """仓位管理器"""
    
    def __init__(self, initial_capital: float = 1000000.0,
                 max_position_pct: float = 0.2,
                 max_total_positions: int = 10):
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.max_position_pct = max_position_pct  # 单标的最大仓位比例
        self.max_total_positions = max_total_positions  # 最大持仓数
        self.positions: Dict[str, Dict] = {}  # {symbol: position_info}
    
    def calculate_position_size(self, signal: Dict, current_price: float) -&gt; Optional[Dict]:
        """
        计算建议仓位
        
        Args:
            signal: 聚合信号
            current_price: 当前价格
            
        Returns:
            仓位建议
        """
        # 检查持仓限制
        if len(self.positions) &gt;= self.max_total_positions:
            return None
        
        # 计算最大可用资金
        max_position_value = self.current_capital * self.max_position_pct
        
        # 根据信号分数调整
        confidence = signal['score']
        position_value = max_position_value * confidence
        
        # 计算股数（取整）
        position_size = int(position_value / current_price / 100) * 100  # 一手100股
        
        if position_size == 0:
            return None
        
        return {
            'symbol': signal['symbol'],
            'size': position_size,
            'value': position_size * current_price,
            'confidence': confidence
        }
    
    def update_position(self, symbol: str, size: float, price: float):
        """更新持仓"""
        if size == 0:
            if symbol in self.positions:
                # 平仓
                pos = self.positions.pop(symbol)
                self.current_capital += pos['size'] * price
        else:
            if symbol in self.positions:
                # 加仓/减仓
                pos = self.positions[symbol]
                size_change = size - pos['size']
                self.current_capital -= size_change * price
                pos['size'] = size
                pos['avg_price'] = (pos['avg_price'] * pos['size'] + price * size_change) / size
            else:
                # 新建仓
                self.positions[symbol] = {
                    'size': size,
                    'avg_price': price
                }
                self.current_capital -= size * price
    
    def get_portfolio_value(self, current_prices: Dict[str, float]) -&gt; float:
        """计算组合总价值"""
        position_value = 0.0
        for symbol, pos in self.positions.items():
            if symbol in current_prices:
                position_value += pos['size'] * current_prices[symbol]
        return self.current_capital + position_value


class QuantTradingSystem:
    """量化交易系统 - 整合所有模块"""
    
    def __init__(self):
        self.theme_model = ThemeModel()
        self.board_model = BoardModel()
        self.news_model = NewsModel()
        self.price_volume_model = PriceVolumeModel()
        self.signal_aggregator = SignalAggregator()
        self.position_manager = PositionManager()
    
    def generate_all_signals(self, market_data: Dict = None) -&gt; List[Dict]:
        """
        生成所有模型的信号并聚合
        
        Args:
            market_data: 市场数据
            
        Returns:
            聚合后的信号列表
        """
        signals_by_model = {}
        
        # 各模型生成信号
        signals_by_model['theme_model'] = self.theme_model.generate_signals(market_data or {})
        signals_by_model['board_model'] = self.board_model.generate_signals(market_data or {})
        signals_by_model['news_model'] = self.news_model.generate_signals(market_data or {})
        signals_by_model['price_volume_model'] = self.price_volume_model.generate_signals(market_data or {})
        
        # 聚合信号
        aggregated = self.signal_aggregator.aggregate_signals(signals_by_model)
        return aggregated

