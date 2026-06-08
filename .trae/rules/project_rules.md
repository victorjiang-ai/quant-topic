# Trae SOLO 项目规则 - 量化金融系统

## 项目概述

这是一个多模块量化金融系统，包含数据采集、模型分析、交易策略等核心功能。

**项目路径**: `/Users/victorjiang/Documents/Software/quant_data`
**主要子项目**:
- `projects/tgb_data/` - TGB量化数据采集系统（博主内容采集+复盘报告）

## 代码规范

### Python 代码风格
- 使用 Python 3.8+ 特性
- 类型注解：所有公共方法必须有类型注解
- 文档字符串：使用 Google 风格的 docstring
- 命名规范：
  - 类名：PascalCase (如 `ThemeModel`)
  - 函数/方法：snake_case (如 `calculate_hot_score`)
  - 常量：UPPER_SNAKE_CASE (如 `MAX_RETRY_COUNT`)
  - 私有方法：前缀下划线 (如 `_collect_weibo`)

### 文件组织
```
src/
├── __init__.py          # 导出公共接口
├── models/              # 数据模型
├── collectors/          # 数据采集
├── outputs/             # 输出处理
├── trading/             # 交易逻辑
└── utils/               # 工具函数
```

## 测试要求

### 运行测试
```bash
cd projects/tgb_data
python -m pytest test_basic.py -v
```

### 测试覆盖
- 新功能必须添加测试
- 核心模型测试覆盖率 > 80%
- 使用 pytest 框架

## Git 提交规范

### Commit Message 格式
```
<type>(<scope>): <subject>

<body>
```

**类型 (type)**:
- `feat`: 新功能
- `fix`: Bug 修复
- `refactor`: 重构
- `docs`: 文档更新
- `test`: 测试相关
- `chore`: 构建/工具

**示例**:
```
feat(theme): 添加题材热度计算算法

- 实现基于提及次数的热度评分
- 添加龙头股识别逻辑
- 支持题材关联分析
```

## 模块职责

### TGB 数据采集系统 (`projects/tgb_data/`)

**核心模块**:
- `main.py` - 主入口，工作流编排
- `src/collectors/` - 数据采集（微博、雪球等平台）
- `src/models/` - 量化模型（题材、打板、量价、消息股）
- `src/outputs/` - 输出处理（本地文件、飞书文档）
- `src/trading/` - 交易逻辑（持仓、交易日志）
- `src/utils/` - 工具函数（配置、日期处理）

**配置文件**:
- `config/bloggers.yaml` - 博主列表（可独立修改）
- `config/settings.yaml` - 全局设置
- `config/templates.yaml` - 模版配置

## 任务分配规则

### Trae SOLO 负责
✅ 单文件修改 < 200 行
✅ 明确需求的功能开发
✅ 测试用例编写
✅ Bug 修复
✅ 文档更新
✅ 数据处理脚本
✅ 配置文件修改
✅ 工具函数开发

### 需转交 Claude Code
⚠️ 架构变更
⚠️ 多模块重构
⚠️ 核心算法实现
⚠️ 性能优化
⚠️ 新系统设计

## 依赖管理

### 安装依赖
```bash
pip install -r requirements.txt
```

### 主要依赖
- `pyyaml` - 配置文件解析
- `jinja2` - 模版渲染
- `lark-cli` - 飞书 API（可选）

## 输出路径

### 本地输出
- 博主合集: `/Users/victorjiang/projects/tgb_data/collections/{date}/`
- 复盘报告: `/Users/victorjiang/projects/tgb_data/reports/{date}/`

### 飞书输出
- 文档夹: `Quant/Tgb_data/`
- 博主合集: `博主原文合集/`
- 复盘报告: `复盘报告/`

## 注意事项

1. **配置文件优先**: 修改博主列表只需编辑 `config/bloggers.yaml`
2. **飞书认证**: 使用飞书功能前需运行 `lark-cli auth login`
3. **日志查看**: 默认输出到控制台，可配置文件日志
4. **测试先行**: 修改核心逻辑前先写测试
5. **文档同步**: 修改接口时更新对应文档

## 快速命令

```bash
# 运行完整工作流
python main.py --mode full

# 仅采集
python main.py --mode daily

# 生成报告
python main.py --mode report

# 运行测试
python -m pytest test_basic.py -v
```

## 联系与协作

- **Claude Code 负责**: 架构设计、核心算法、复杂重构
- **Trae SOLO 负责**: 功能实现、测试、文档、日常维护
- **交接文档**: `docs/handover_notes.md`
- **接口契约**: `docs/module_contracts.md`