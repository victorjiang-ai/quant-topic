# 模块接口契约

## 📋 概述

本文档定义了各模块之间的接口契约，确保 Claude Code 和 Trae SOLO 在协作时保持一致性。

---

## 🔧 核心模块接口

### 1. 数据采集层 (Collectors)

#### BloggerCollector

**职责**: 从各平台采集博主内容

**输入**:
```python
target_date: str  # 格式: YYYY-MM-DD
blogger_config: Dict  # 来自 config/bloggers.yaml
```

**输出**:
```python
List[Dict]  # 内容列表
[
    {
        'blogger_id': str,
        'blogger_name': str,
        'platform': str,
        'title': str,
        'content': str,
        'publish_time': str,
        'url': str,
        'tags': List[str]
    }
]
```

**接口方法**:
```python
def collect_all(self, target_date: str) -> List[Dict]
def collect_with_date_range(self, start_date: str, end_date: str) -> List[Dict]
```

**变更通知**: 修改输出格式需双方确认

---

#### ContentProcessor

**职责**: 处理采集的内容（总结、关键词、情感分析）

**输入**:
```python
contents: List[Dict]  # BloggerCollector 的输出
summary_config: Dict  # 来自 config/settings.yaml
```

**输出**:
```python
List[Dict]  # 处理后的内容
[
    {
        'blogger_id': str,
        'blogger_name': str,
        'title': str,
        'summary': str,
        'keywords': List[str],
        'sentiment': {
            'sentiment': str,  # positive/negative/neutral
            'score': float
        },
        'buy_signals': List[str],
        'sell_signals': List[str],
        'risk_warnings': List[str]
    }
]
```

**接口方法**:
```python
def process_batch(self, contents: List[Dict], config: Dict) -> List[Dict]
def process_single(self, content: Dict, config: Dict) -> Dict
```

---

### 2. 模型层 (Models)

#### BaseQuantModel

**职责**: 所有量化模型的基类

**接口定义**:
```python
class BaseQuantModel:
    def __init__(self, name: str, version: str)
    
    def generate_signals(self, data: Dict) -> List[Signal]
    def train(self, training_data: Dict)
    def backtest(self, backtest_data: Dict) -> ModelPerformance
    def save_to_file(self, filepath: str)
    def load_from_file(cls, filepath: str) -> BaseQuantModel
```

**Signal 数据结构**:
```python
@dataclass
class Signal:
    timestamp: datetime
    symbol: str
    signal_type: str  # buy/sell/hold
    confidence: float  # 0.0-1.0
    reason: str
    metadata: Dict
```

**ModelPerformance 数据结构**:
```python
@dataclass
class ModelPerformance:
    total_trades: int = 0
    win_rate: float = 0.0
    avg_return: float = 0.0
    max_drawdown: float = 0.0
    sharpe_ratio: float = 0.0
```

---

#### ThemeModel

**职责**: 题材分析、龙头识别、题材轮动

**输入**:
```python
# 题材数据
{
    'theme_id': str,
    'name': str,
    'stocks': List[str],
    'upstream': List[str],
    'downstream': List[str]
}

# 市场数据
{
    'date': str,
    'stock_prices': Dict[str, float],
    'mention_counts': Dict[str, int]
}
```

**输出**:
```python
List[Signal]  # 交易信号
```

**核心方法**:
```python
def add_theme(self, theme: Theme)
def calculate_hot_score(self, theme_id: str) -> float
def identify_leaders(self, theme_id: str) -> List[ThemeStock]
def get_hot_themes(self, top_n: int = 10) -> List[Theme]
```

**数据结构**:
```python
@dataclass
class Theme:
    id: str
    name: str
    description: str
    hot_score: float
    mention_count: int
    stocks: List[str]
    upstream: List[str]
    downstream: List[str]
    related_themes: List[str]

@dataclass
class ThemeStock:
    symbol: str
    name: str
    theme_id: str
    tier: int  # 1=龙头, 2=核心, 3=跟风
    weight: float
    is_leader: bool
```

---

#### BoardModel (打板模型)

**职责**: 打板数据分析、涨停板监测

**接口**:
```python
def analyze_board_data(self, date: str) -> Dict
def identify_board_opportunities(self) -> List[Signal]
```

**数据结构**:
```python
@dataclass
class BoardData:
    symbol: str
    board_time: datetime
    board_type: str  # first_board/second_board
    turnover_rate: float
    amount: float
```

---

#### NewsModel (消息股模型)

**职责**: 消息股分析、消息分类

**接口**:
```python
def classify_news(self, news_data: Dict) -> str
def generate_news_signals(self) -> List[Signal]
```

**数据结构**:
```python
@dataclass
class NewsItem:
    source: str
    content: str
    timestamp: datetime
    category: str  # insider/official/rumor
    confidence: float
```

---

#### PriceVolumeModel (量价模型)

**职责**: 技术指标分析、量价关系

**接口**:
```python
def calculate_indicators(self, price_data: Dict) -> Dict
def generate_pv_signals(self) -> List[Signal]
```

**数据结构**:
```python
@dataclass
class TechnicalIndicators:
    ma5: float
    ma10: float
    ma20: float
    rsi: float
    macd: Dict
    volume_ratio: float
```

---

### 3. 输出层 (Outputs)

#### LocalOutput

**职责**: 本地文件保存

**输入**:
```python
target_date: str
processed_contents: List[Dict]
blogger_data: Dict
```

**输出**:
```python
{
    'success': bool,
    'path': str  # 文件路径
}
```

**接口方法**:
```python
def save_collection(self, target_date: str, contents: List[Dict], blogger_data: Dict) -> str
def save_report(self, target_date: str, report_data: Dict, report_type: str) -> str
def get_collection_path(self, target_date: str) -> str
```

---

#### FeishuOutput

**职责**: 飞书文档同步

**输入**:
```python
target_date: str
processed_contents: List[Dict]
blogger_data: Dict
```

**输出**:
```python
{
    'success': bool,
    'token': str  # 飞书文档 token
}
```

**接口方法**:
```python
def create_collection_doc(self, target_date: str, contents: List[Dict], blogger_data: Dict) -> str
def create_report_doc(self, target_date: str, report_data: Dict, report_type: str) -> str
```

**依赖**: 需要安装并认证 `lark-cli`

---

### 4. 交易层 (Trading)

#### Portfolio

**职责**: 持仓管理

**接口**:
```python
def add_position(self, symbol: str, shares: int, price: float)
def remove_position(self, symbol: str)
def get_position(self, symbol: str) -> Position
def calculate_total_value(self) -> float
```

**数据结构**:
```python
@dataclass
class Position:
    symbol: str
    shares: int
    avg_cost: float
    current_price: float
    profit_loss: float
```

---

#### TradeLog

**职责**: 交易日志记录

**接口**:
```python
def log_trade(self, trade: Trade)
def get_trades(self, date: str) -> List[Trade]
def calculate_statistics(self) -> Dict
```

**数据结构**:
```python
@dataclass
class Trade:
    timestamp: datetime
    symbol: str
    action: str  # buy/sell
    shares: int
    price: float
    reason: str
```

---

### 5. 工具层 (Utils)

#### ConfigLoader

**职责**: 配置文件加载

**接口**:
```python
def load_bloggers(self) -> List[Dict]
def load_settings(self) -> Dict
def load_templates(self) -> Dict
def get_summary_config(self) -> Dict
```

---

#### DateUtils

**职责**: 日期处理

**接口**:
```python
def get_previous_day(self) -> date
def get_weekend_dates(self, ref_date: date = None) -> Tuple[date, date, date]
def format_date(self, date: date) -> str
def parse_date(self, date_str: str) -> date
```

---

## 🔄 数据流向

```
采集流程:
BloggerCollector → ContentProcessor → LocalOutput/FeishuOutput

模型流程:
数据输入 → Model.generate_signals() → Signal输出

交易流程:
Signal → Portfolio → TradeLog
```

---

## ⚠️ 变更管理

### 接口变更规则

1. **新增字段**: 可以自由添加，不影响现有功能
2. **修改字段**: 需双方确认，确保向后兼容
3. **删除字段**: 需双方确认，更新所有依赖模块

### 变更通知流程

1. 在 `docs/handover_notes.md` 中记录变更
2. 更新本文档
3. 通知相关模块负责人
4. 测试验证

---

## 📝 版本控制

### 当前版本

- **数据采集**: v1.0.0
- **题材模型**: v1.0.0
- **打板模型**: v0.1.0
- **消息股模型**: v0.1.0
- **量价模型**: v0.1.0

### 版本升级规则

- **主版本**: 架构变更、接口不兼容
- **次版本**: 新增功能、向后兼容
- **修订版本**: Bug 修复、小改进

---

## 🧪 测试契约

### 单元测试要求

每个模块必须提供:
- 输入验证测试
- 输出格式测试
- 边界条件测试
- 异常处理测试

### 集成测试要求

- 模块间数据流测试
- 端到端工作流测试
- 性能测试

---

**最后更新**: 2026-06-08