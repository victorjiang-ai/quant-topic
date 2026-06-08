
"""
交易日志系统 - 记录交易、分析绩效
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import csv


@dataclass
class TradeRecord:
    """交易记录"""
    trade_id: str
    symbol: str
    symbol_name: str
    direction: str  # 'long' 做多, 'short' 做空
    entry_time: datetime
    entry_price: float
    entry_reason: str
    position_size: float  # 仓位数量
    exit_time: Optional[datetime] = None
    exit_price: Optional[float] = None
    exit_reason: Optional[str] = None
    profit_loss: Optional[float] = None
    profit_loss_pct: Optional[float] = None
    status: str = 'open'  # 'open', 'closed'
    tags: List[str] = None
    notes: str = ""
    
    def __post_init__(self):
        self.tags = self.tags or []


class TradeLogger:
    """交易日志管理器"""
    
    def __init__(self, log_dir: str = "trade_logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.trades: Dict[str, TradeRecord] = {}
        self._load_existing_trades()
    
    def _load_existing_trades(self):
        """加载已有的交易记录"""
        json_file = self.log_dir / "trades.json"
        if json_file.exists():
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for trade_data in data:
                    trade = self._dict_to_trade(trade_data)
                    self.trades[trade.trade_id] = trade
    
    def _save_trades(self):
        """保存交易记录到文件"""
        data = [self._trade_to_dict(t) for t in self.trades.values()]
        json_file = self.log_dir / "trades.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        
        # 同时保存CSV版本
        csv_file = self.log_dir / "trades.csv"
        self._save_to_csv(data, csv_file)
    
    def _trade_to_dict(self, trade: TradeRecord) -&gt; Dict:
        """交易记录转字典"""
        return {
            'trade_id': trade.trade_id,
            'symbol': trade.symbol,
            'symbol_name': trade.symbol_name,
            'direction': trade.direction,
            'entry_time': trade.entry_time,
            'entry_price': trade.entry_price,
            'entry_reason': trade.entry_reason,
            'position_size': trade.position_size,
            'exit_time': trade.exit_time,
            'exit_price': trade.exit_price,
            'exit_reason': trade.exit_reason,
            'profit_loss': trade.profit_loss,
            'profit_loss_pct': trade.profit_loss_pct,
            'status': trade.status,
            'tags': trade.tags,
            'notes': trade.notes
        }
    
    def _dict_to_trade(self, data: Dict) -&gt; TradeRecord:
        """字典转交易记录"""
        entry_time = data['entry_time']
        if isinstance(entry_time, str):
            entry_time = datetime.fromisoformat(entry_time)
        
        exit_time = data.get('exit_time')
        if exit_time and isinstance(exit_time, str):
            exit_time = datetime.fromisoformat(exit_time)
        
        return TradeRecord(
            trade_id=data['trade_id'],
            symbol=data['symbol'],
            symbol_name=data.get('symbol_name', data['symbol']),
            direction=data['direction'],
            entry_time=entry_time,
            entry_price=data['entry_price'],
            entry_reason=data['entry_reason'],
            position_size=data['position_size'],
            exit_time=exit_time,
            exit_price=data.get('exit_price'),
            exit_reason=data.get('exit_reason'),
            profit_loss=data.get('profit_loss'),
            profit_loss_pct=data.get('profit_loss_pct'),
            status=data.get('status', 'open'),
            tags=data.get('tags', []),
            notes=data.get('notes', '')
        )
    
    def _save_to_csv(self, data: List[Dict], csv_file: Path):
        """保存到CSV文件"""
        if not data:
            return
        
        with open(csv_file, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    
    def _generate_trade_id(self) -&gt; str:
        """生成交易ID"""
        return f"TRADE_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def open_trade(self, symbol: str, symbol_name: str, direction: str,
                   entry_price: float, position_size: float, entry_reason: str,
                   tags: List[str] = None) -&gt; TradeRecord:
        """
        开仓记录
        
        Args:
            symbol: 股票代码
            symbol_name: 股票名称
            direction: 方向 ('long'/'short')
            entry_price: 入场价格
            position_size: 仓位
            entry_reason: 入场理由
            tags: 标签
            
        Returns:
            交易记录
        """
        trade_id = self._generate_trade_id()
        trade = TradeRecord(
            trade_id=trade_id,
            symbol=symbol,
            symbol_name=symbol_name,
            direction=direction,
            entry_time=datetime.now(),
            entry_price=entry_price,
            entry_reason=entry_reason,
            position_size=position_size,
            status='open',
            tags=tags or []
        )
        self.trades[trade_id] = trade
        self._save_trades()
        return trade
    
    def close_trade(self, trade_id: str, exit_price: float, 
                    exit_reason: str, notes: str = "") -&gt; Optional[TradeRecord]:
        """
        平仓记录
        
        Args:
            trade_id: 交易ID
            exit_price: 平仓价格
            exit_reason: 平仓理由
            notes: 备注
            
        Returns:
            更新后的交易记录
        """
        if trade_id not in self.trades:
            return None
        
        trade = self.trades[trade_id]
        if trade.status != 'open':
            return None
        
        trade.exit_time = datetime.now()
        trade.exit_price = exit_price
        trade.exit_reason = exit_reason
        trade.notes = notes
        trade.status = 'closed'
        
        # 计算盈亏
        if trade.direction == 'long':
            profit_loss = (exit_price - trade.entry_price) * trade.position_size
            profit_loss_pct = (exit_price - trade.entry_price) / trade.entry_price * 100
        else:
            profit_loss = (trade.entry_price - exit_price) * trade.position_size
            profit_loss_pct = (trade.entry_price - exit_price) / trade.entry_price * 100
        
        trade.profit_loss = profit_loss
        trade.profit_loss_pct = profit_loss_pct
        
        self._save_trades()
        return trade
    
    def get_open_trades(self) -&gt; List[TradeRecord]:
        """获取未平仓的交易"""
        return [t for t in self.trades.values() if t.status == 'open']
    
    def get_closed_trades(self) -&gt; List[TradeRecord]:
        """获取已平仓的交易"""
        return [t for t in self.trades.values() if t.status == 'closed']
    
    def get_trades_by_symbol(self, symbol: str) -&gt; List[TradeRecord]:
        """获取某股票的所有交易"""
        return [t for t in self.trades.values() if t.symbol == symbol]
    
    def calculate_performance(self) -&gt; Dict:
        """
        计算绩效指标
        
        Returns:
            绩效统计
        """
        closed_trades = self.get_closed_trades()
        if not closed_trades:
            return {
                'total_trades': 0,
                'win_rate': 0,
                'total_profit': 0,
                'avg_profit': 0,
                'avg_profit_pct': 0,
                'max_profit': 0,
                'max_loss': 0,
                'profit_factor': 0
            }
        
        profits = [t.profit_loss for t in closed_trades if t.profit_loss is not None]
        profits_pct = [t.profit_loss_pct for t in closed_trades if t.profit_loss_pct is not None]
        
        wins = [p for p in profits if p &gt; 0]
        losses = [p for p in profits if p &lt;= 0]
        
        total_profit = sum(profits)
        total_win = sum(wins)
        total_loss = abs(sum(losses))
        
        return {
            'total_trades': len(closed_trades),
            'win_rate': len(wins) / len(closed_trades) * 100 if closed_trades else 0,
            'total_profit': total_profit,
            'avg_profit': total_profit / len(closed_trades) if closed_trades else 0,
            'avg_profit_pct': sum(profits_pct) / len(profits_pct) if profits_pct else 0,
            'max_profit': max(profits) if profits else 0,
            'max_loss': min(profits) if profits else 0,
            'profit_factor': total_win / total_loss if total_loss &gt; 0 else float('inf'),
            'avg_win': sum(wins) / len(wins) if wins else 0,
            'avg_loss': sum(losses) / len(losses) if losses else 0
        }

