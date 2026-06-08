
"""
量化模型基类
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Signal:
    """交易信号"""
    timestamp: datetime
    symbol: str
    signal_type: str  # 'buy', 'sell', 'hold'
    confidence: float  # 0-1
    reason: str
    metadata: Dict[str, Any] = None


@dataclass
class ModelPerformance:
    """模型绩效"""
    total_trades: int = 0
    win_rate: float = 0.0
    profit_factor: float = 0.0
    sharpe_ratio: float = 0.0
    max_drawdown: float = 0.0
    annual_return: float = 0.0


class BaseQuantModel(ABC):
    """量化模型基类"""
    
    def __init__(self, name: str, version: str = "1.0"):
        self.name = name
        self.version = version
        self.performance = ModelPerformance()
        self.is_trained = False
    
    @abstractmethod
    def generate_signals(self, data: Dict[str, Any]) -&gt; List[Signal]:
        """
        生成交易信号
        
        Args:
            data: 输入数据
            
        Returns:
            信号列表
        """
        pass
    
    @abstractmethod
    def train(self, training_data: Dict[str, Any]):
        """
        训练模型
        
        Args:
            training_data: 训练数据
        """
        pass
    
    @abstractmethod
    def backtest(self, backtest_data: Dict[str, Any]) -&gt; ModelPerformance:
        """
        回测模型
        
        Args:
            backtest_data: 回测数据
            
        Returns:
            绩效指标
        """
        pass
    
    def get_info(self) -&gt; Dict[str, Any]:
        """获取模型信息"""
        return {
            'name': self.name,
            'version': self.version,
            'is_trained': self.is_trained,
            'performance': self.performance.__dict__
        }

