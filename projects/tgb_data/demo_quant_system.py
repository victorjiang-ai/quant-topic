
"""
量化系统演示 - 展示如何使用四大模型和交易日志
"""
from datetime import datetime, timedelta
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from src.models.theme_model import ThemeModel, Theme, ThemeStock
from src.models.board_model import BoardModel, LimitUpInfo
from src.models.news_model import NewsModel, NewsItem, NewsType, NewsImpact
from src.models.price_volume_model import PriceVolumeModel, PriceVolumeData
from src.trading.trade_log import TradeLogger
from src.trading.portfolio import QuantTradingSystem


def demo_theme_model():
    """演示题材模型"""
    print("\n" + "="*60)
    print("题材模型演示")
    print("="*60)
    
    model = ThemeModel()
    
    # 添加示例题材
    ai_theme = Theme(
        id="theme_ai",
        name="人工智能",
        description="AI大模型、算力相关",
        hot_score=85.5,
        mention_count=156,
        stocks=["000001", "600000", "300001"],
        related_themes=["theme_chip"]
    )
    model.add_theme(ai_theme)
    
    chip_theme = Theme(
        id="theme_chip",
        name="芯片半导体",
        description="国产芯片、半导体产业链",
        hot_score=72.3,
        mention_count=98
    )
    model.add_theme(chip_theme)
    
    # 添加题材股票
    model.add_theme_stock("theme_ai", ThemeStock(
        symbol="000001",
        name="AI龙头A",
        theme_id="theme_ai",
        tier=1,
        weight=0.4,
        is_leader=True
    ))
    model.add_theme_stock("theme_ai", ThemeStock(
        symbol="600000",
        name="AI股B",
        theme_id="theme_ai",
        tier=2,
        weight=0.3
    ))
    
    # 获取热门题材
    hot_themes = model.get_hot_themes(5)
    print(f"\n热门题材:")
    for t in hot_themes:
        print(f"  - {t.name}: 热度{t.hot_score:.1f}, 提及{t.mention_count}次")
    
    # 生成信号
    signals = model.generate_signals({})
    print(f"\n生成信号: {len(signals)}个")
    for s in signals[:3]:
        print(f"  - {s.symbol}: {s.signal_type} (置信度{s.confidence:.2f}) - {s.reason}")
    
    return model


def demo_board_model():
    """演示打板模型"""
    print("\n" + "="*60)
    print("打板模型演示")
    print("="*60)
    
    model = BoardModel()
    
    # 添加示例涨停
    model.add_limit_up(LimitUpInfo(
        symbol="000001",
        name="涨停股A",
        limit_up_time=datetime.now(),
        open_price=9.5,
        limit_up_price=10.45,
        volume=1000000,
        turnover_rate=5.2,
        is_first_board=True
    ))
    model.add_limit_up(LimitUpInfo(
        symbol="600000",
        name="连板股B",
        limit_up_time=datetime.now(),
        open_price=15.0,
        limit_up_price=16.5,
        volume=800000,
        turnover_rate=4.8,
        consecutive_boards=2
    ))
    
    print(f"\n首板股票: {len(model.get_first_boards())}只")
    print(f"连板股票: {len(model.get_consecutive_boards(2))}只")
    
    signals = model.generate_signals({})
    print(f"\n打板信号: {len(signals)}个")
    for s in signals:
        print(f"  - {s.symbol}: {s.signal_type} - {s.reason}")
    
    return model


def demo_news_model():
    """演示消息股模型"""
    print("\n" + "="*60)
    print("消息股模型演示")
    print("="*60)
    
    model = NewsModel()
    
    # 添加示例消息
    model.add_news(NewsItem(
        id="news_001",
        title="重大政策利好发布",
        content="国家发布重要产业政策...",
        source="official",
        publish_time=datetime.now(),
        news_type=NewsType.POLICY,
        impact=NewsImpact.POSITIVE_STRONG,
        related_symbols=["000001", "600000"],
        confidence=0.9
    ))
    model.add_news(NewsItem(
        id="news_002",
        title="公司业绩超预期",
        content="某公司发布财报...",
        source="authoritative_media",
        publish_time=datetime.now(),
        news_type=NewsType.EARNINGS,
        impact=NewsImpact.POSITIVE,
        related_symbols=["300001"],
        confidence=0.75
    ))
    
    important_news = model.get_important_news(0.6)
    print(f"\n重要消息: {len(important_news)}条")
    for n in important_news:
        print(f"  - {n.title} (影响:{n.impact.value})")
    
    signals = model.generate_signals({})
    print(f"\n消息信号: {len(signals)}个")
    for s in signals:
        print(f"  - {s.symbol}: {s.signal_type} - {s.reason}")
    
    return model


def demo_price_volume_model():
    """演示量价模型"""
    print("\n" + "="*60)
    print("量价模型演示")
    print("="*60)
    
    model = PriceVolumeModel()
    
    # 添加示例价格数据
    base_date = datetime.now() - timedelta(days=40)
    base_price = 10.0
    
    for i in range(40):
        # 模拟一些价格波动
        import random
        price_change = random.uniform(-0.03, 0.03)
        price = base_price * (1 + price_change) ** i
        
        model.add_price_data("000001", PriceVolumeData(
            symbol="000001",
            timestamp=base_date + timedelta(days=i),
            open=price * 0.995,
            high=price * 1.02,
            low=price * 0.98,
            close=price,
            volume=1000000
        ))
    
    # 计算技术指标
    sma_5 = model.calculate_sma("000001", 5)
    sma_20 = model.calculate_sma("000001", 20)
    rsi = model.calculate_rsi("000001")
    macd = model.calculate_macd("000001")
    
    print(f"\n技术指标计算:")
    print(f"  - MA5: 最新{sma_5[-1]:.2f}" if sma_5 else "  - MA5: 数据不足")
    print(f"  - MA20: 最新{sma_20[-1]:.2f}" if sma_20 else "  - MA20: 数据不足")
    print(f"  - RSI: 最新{rsi[-1]:.1f}" if rsi else "  - RSI: 数据不足")
    print(f"  - MACD: 信号点{len(macd['signal'])}个")
    
    signals = model.generate_signals({})
    print(f"\n量价信号: {len(signals)}个")
    for s in signals:
        print(f"  - {s.symbol}: {s.signal_type} - {s.reason}")
    
    return model


def demo_trade_log():
    """演示交易日志"""
    print("\n" + "="*60)
    print("交易日志演示")
    print("="*60)
    
    logger = TradeLogger(log_dir="demo_trade_logs")
    
    # 开仓
    trade1 = logger.open_trade(
        symbol="000001",
        symbol_name="测试股票A",
        direction="long",
        entry_price=10.5,
        position_size=1000,
        entry_reason="技术突破 + 题材利好",
        tags=["demo", "test"]
    )
    print(f"\n开仓: {trade1.symbol} @ {trade1.entry_price}")
    
    trade2 = logger.open_trade(
        symbol="600000",
        symbol_name="测试股票B",
        direction="long",
        entry_price=15.2,
        position_size=500,
        entry_reason="消息刺激",
        tags=["demo"]
    )
    print(f"开仓: {trade2.symbol} @ {trade2.entry_price}")
    
    # 平仓1
    closed = logger.close_trade(
        trade_id=trade1.trade_id,
        exit_price=11.8,
        exit_reason="达到止盈目标",
        notes="这笔交易很顺利"
    )
    if closed:
        print(f"\n平仓: {closed.symbol}, 盈亏: {closed.profit_loss:.2f} ({closed.profit_loss_pct:.2f}%)")
    
    # 计算绩效
    perf = logger.calculate_performance()
    print(f"\n绩效统计:")
    print(f"  - 总交易: {perf['total_trades']}")
    print(f"  - 胜率: {perf['win_rate']:.1f}%")
    print(f"  - 总盈亏: {perf['total_profit']:.2f}")
    print(f"  - 盈亏比: {perf['profit_factor']:.2f}")
    
    return logger


def demo_full_system():
    """演示完整量化系统"""
    print("\n" + "="*60)
    print("完整量化系统演示")
    print("="*60)
    
    system = QuantTradingSystem()
    
    # 先给模型添加一些测试数据
    # 1. 题材模型
    ai_theme = Theme(
        id="theme_ai",
        name="人工智能",
        description="AI大模型、算力相关",
        hot_score=85.5,
        mention_count=156,
        stocks=["000001"]
    )
    system.theme_model.add_theme(ai_theme)
    system.theme_model.add_theme_stock("theme_ai", ThemeStock(
        symbol="000001",
        name="AI龙头",
        theme_id="theme_ai",
        tier=1,
        weight=0.4,
        is_leader=True
    ))
    
    # 2. 打板模型
    system.board_model.add_limit_up(LimitUpInfo(
        symbol="000001",
        name="AI龙头",
        limit_up_time=datetime.now(),
        open_price=9.5,
        limit_up_price=10.45,
        volume=1000000,
        turnover_rate=5.2,
        is_first_board=True
    ))
    
    # 3. 消息模型
    system.news_model.add_news(NewsItem(
        id="news_001",
        title="AI重大突破",
        content="...",
        source="official",
        publish_time=datetime.now(),
        news_type=NewsType.POLICY,
        impact=NewsImpact.POSITIVE_STRONG,
        related_symbols=["000001"],
        confidence=0.9
    ))
    
    # 4. 量价模型 - 添加足够的数据
    base_date = datetime.now() - timedelta(days=40)
    for i in range(40):
        import random
        price = 10.0 * (1 + random.uniform(-0.02, 0.02)) ** i
        system.price_volume_model.add_price_data("000001", PriceVolumeData(
            symbol="000001",
            timestamp=base_date + timedelta(days=i),
            open=price * 0.995,
            high=price * 1.02,
            low=price * 0.98,
            close=price,
            volume=1000000
        ))
    
    # 生成聚合信号
    signals = system.generate_all_signals()
    
    print(f"\n聚合信号 (按分数排序):")
    for i, sig in enumerate(signals[:5], 1):
        print(f"\n{i}. {sig['symbol']} - {sig['signal_type'].upper()} (分数: {sig['score']:.3f})")
        print(f"   支持模型: {[m['model'] for m in sig['supporting_models']]}")
    
    return system


def main():
    """主函数 - 运行所有演示"""
    print("="*60)
    print("AI量化创业系统 - 半月冲刺演示")
    print("="*60)
    
    # 运行各模块演示
    demo_theme_model()
    demo_board_model()
    demo_news_model()
    demo_price_volume_model()
    demo_trade_log()
    demo_full_system()
    
    print("\n" + "="*60)
    print("演示完成！")
    print("="*60)


if __name__ == "__main__":
    main()

