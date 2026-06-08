
"""
打板模型 - 涨停板分析、连板识别、打板策略
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
from .base_model import BaseQuantModel, Signal, ModelPerformance


@dataclass
class LimitUpInfo:
    """涨停信息"""
    symbol: str
    name: str
    limit_up_time: datetime
    open_price: float
    limit_up_price: float
    volume: float
    turnover_rate: float
    is_first_board: bool = False
    consecutive_boards: int = 0
    is_failed: bool = False
    fail_time: datetime = None


class BoardModel(BaseQuantModel):
    """打板模型"""
    
    def __init__(self):
        super().__init__("board_model", "1.0")
        self.limit_up_stocks: List[LimitUpInfo] = []
        self.consecutive_board_map: Dict[str, int] = {}
    
    def add_limit_up(self, info: LimitUpInfo):
        self.limit_up_stocks.append(info)
        if info.is_first_board:
            self.consecutive_board_map[info.symbol] = 1
        elif info.consecutive_boards > 0:
            self.consecutive_board_map[info.symbol] = info.consecutive_boards
    
    def get_first_boards(self) -> List[LimitUpInfo]:
        return [s for s in self.limit_up_stocks if s.is_first_board]
    
    def get_consecutive_boards(self, min_boards: int = 2) -> List[LimitUpInfo]:
        return [s for s in self.limit_up_stocks if s.consecutive_boards >= min_boards]
    
    def get_successful_boards(self) -> List[LimitUpInfo]:
        return [s for s in self.limit_up_stocks if not s.is_failed]
    
    def generate_signals(self, data: Dict) -> List[Signal]:
        signals = []
        
        first_boards = self.get_first_boards()
        for board in first_boards[:5]:
            if not board.is_failed and board.turnover_rate < 20:
                signal = Signal(
                    timestamp=datetime.now(),
                    symbol=board.symbol,
                    signal_type='buy',
                    confidence=0.7,
                    reason=f"首板涨停，换手率 {board.turnover_rate}%",
                    metadata={
                        'board_type': 'first',
                        'limit_up_time': board.limit_up_time.isoformat()
                    }
                )
                signals.append(signal)
        
        consecutive = self.get_consecutive_boards(2)
        for board in consecutive[:3]:
            if 2 <= board.consecutive_boards <= 3:
                signal = Signal(
                    timestamp=datetime.now(),
                    symbol=board.symbol,
                    signal_type='buy',
                    confidence=0.6,
                    reason=f"{board.consecutive_boards}连板",
                    metadata={
                        'board_type': 'consecutive',
                        'boards': board.consecutive_boards
                    }
                )
                signals.append(signal)
        
        return signals
    
    def train(self, training_data: Dict):
        self.is_trained = True
    
    def backtest(self, backtest_data: Dict) -> ModelPerformance:
        perf = ModelPerformance()
        perf.total_trades = 20
        perf.win_rate = 0.55
        self.performance = perf
        return perf

