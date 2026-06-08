# TGB量化数据采集系统 - 快速入门指南

## ✅ 项目创建完成

项目已成功创建在：`/Users/victorjiang/Documents/Software/quant_data/projects/tgb_data`

## 📁 项目结构

```
projects/tgb_data/
├── config/                    # 配置目录
│   ├── bloggers.yaml         # ⭐ 博主列表（可独立修改）
│   ├── templates.yaml        # 模版路径配置
│   └── settings.yaml         # 全局设置
├── templates/                 # 模版目录
│   ├── collection_template.md  # 博主原文合集模版
│   └── report_template.md    # 复盘报告模版
├── src/                       # 源代码
│   ├── collectors/           # 采集模块
│   ├── outputs/              # 输出模块
│   └── utils/                # 工具模块
├── scripts/                   # 脚本目录
│   └── daily_run.sh         # 自动化运行脚本
└── main.py                   # 主程序入口
```

## 🎯 核心功能

### 1. 博主原文采集
- 支持多平台：微博、微信公众号、雪球等
- 自动总结内容要点
- 提取关键词和交易信号
- 情感分析（积极/消极/中性）

### 2. 复盘报告生成
- 每日复盘报告
- 周末汇总报告
- 核心观点汇总
- 交易信号提取
- 投资建议

### 3. 双端输出
- **本地文件**：`/Users/victorjiang/projects/tgb_data/`
  - `collections/{日期}/` - 博主原文合集
  - `reports/{日期}/` - 复盘报告
- **飞书文档**：`Quant/Tgb_data/`
  - `博主原文合集/` - 飞书合集文档
  - `复盘报告/` - 飞书报告文档

## 🚀 快速开始

### 第一步：配置博主列表

编辑 `config/bloggers.yaml`：

```yaml
bloggers:
  - id: blogger_001
    name: "你的博主名称"
    platform: "weibo"  # 可选: weibo, wechat, xueqiu
    url: "博主主页URL"
    tags:
      - "技术分析"
      - "短线"
    enabled: true
```

### 第二步：安装依赖

```bash
cd /Users/victorjiang/Documents/Software/quant_data/projects/tgb_data
pip3 install -r requirements.txt
```

### 第三步：测试运行

```bash
# 查看帮助
python3 main.py --help

# 手动运行一次
python3 main.py --mode full
```

### 第四步：配置飞书（可选）

如果需要同步到飞书文档，需要安装并配置 lark-cli：

```bash
# 安装 lark-cli
npm install -g @larksuite/oapi-sdk-cli

# 认证
lark-cli auth login
```

## 📝 使用方法

### 命令行使用

```bash
# 运行完整工作流（采集 + 报告）
python3 main.py --mode full

# 仅采集博主内容
python3 main.py --mode daily

# 仅生成报告
python3 main.py --mode report

# 周末采集（周五到周日）
python3 main.py --mode weekend

# 指定日期
python3 main.py --mode full --date 2024-01-15
```

### 自动化运行

#### 方法一：使用 Shell 脚本

```bash
# 直接运行
./scripts/daily_run.sh

# 手动触发特定模式
./scripts/daily_run.sh daily
./scripts/daily_run.sh weekend
./scripts/daily_run.sh full
```

#### 方法二：添加到 crontab（定时任务）

```bash
# 编辑 crontab
crontab -e

# 添加以下内容（每天早上8点自动运行）
0 8 * * * cd /Users/victorjiang/Documents/Software/quant_data/projects/tgb_data && /usr/bin/python3 main.py --mode full >> logs/cron.log 2>&1

# 保存并退出
```

#### 方法三：使用 launchd（macOS）

创建 `~/Library/LaunchAgents/com.tgb.quant.plist`：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.tgb.quant</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/victorjiang/Documents/Software/quant_data/projects/tgb_data/main.py</string>
        <string>--mode</string>
        <string>full</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>8</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
</dict>
</plist>
```

加载定时任务：
```bash
launchctl load ~/Library/LaunchAgents/com.tgb.quant.plist
```

## ⚙️ 配置说明

### 博主配置 (bloggers.yaml)

这是最常用的配置文件，可独立修改：

```yaml
bloggers:
  - id: blogger_001                    # 博主ID（唯一）
    name: "博主昵称"                   # 博主显示名称
    platform: "weibo"                  # 平台类型
    url: "https://weibo.com/u/xxx"    # 博主主页
    tags: ["技术分析", "短线"]         # 标签分类
    enabled: true                     # 是否启用
    description: "简介"                # 博主简介
```

### 全局设置 (settings.yaml)

```yaml
logging:
  level: "INFO"      # 日志级别
  file: "logs/..."    # 日志文件

output:
  local:
    enabled: true    # 是否启用本地输出
  feishu:
    enabled: true    # 是否启用飞书输出

automation:
  daily_run_time: "08:00"  # 每日运行时间
  weekend:
    include_friday: true   # 周五纳入周末采集
    include_saturday: false
    include_sunday: true
```

### 模版配置

如果需要自定义输出格式，编辑 `templates/` 目录下的模版文件。

## 📊 输出示例

### 博主原文合集

会生成包含以下内容的 Markdown 文件：
- 采集概要（日期、博主数、文章数）
- 按博主分组的内容
- 每篇文章的：标题、发布时间、简要总结、原文内容

### 复盘报告

会生成包含以下内容的 Markdown 文件：
- 报告概要
- 市场情绪分析
- 核心观点汇总
- 交易信号（买入/卖出）
- 风险提示
- 投资建议

## 🔧 扩展开发

### 添加新平台支持

在 `src/collectors/blogger_collector.py` 中添加采集方法：

```python
def _collect_new_platform(self, blogger, target_date):
    # 实现新平台的采集逻辑
    # 返回格式：[{title, content, publish_time, ...}, ...]
    pass
```

### 自定义内容处理

在 `src/collectors/content_processor.py` 中扩展：
- 新的关键词识别
- 自定义情感分析
- 特定行业的交易信号

## ❓ 常见问题

### Q: 如何添加新的博主？
A: 编辑 `config/bloggers.yaml`，添加新的博主配置即可。

### Q: 飞书文档没有生成？
A: 检查：
1. 是否安装了 lark-cli
2. 是否完成了认证（`lark-cli auth login`）
3. 查看日志中的错误信息

### Q: 如何查看运行日志？
A: 日志默认输出到控制台，也可以查看 `logs/` 目录下的日志文件。

### Q: 如何停止自动化任务？
A: 如果使用 crontab，运行 `crontab -e` 删除对应行；如果使用 launchd，运行 `launchctl unload ~/Library/LaunchAgents/com.tgb.quant.plist`

## 📝 注意事项

1. 本系统仅供参考，不构成投资建议
2. 市场有风险，投资需谨慎
3. 建议定期备份配置文件
4. 保持依赖包更新

## 🎉 初始化完成！

现在你可以：
1. 配置你的博主列表
2. 运行一次测试
3. 设置定时任务实现自动化

祝你投资顺利！💰
