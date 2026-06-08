# TGB量化数据采集系统

用于采集关注博主原文并生成复盘报告的量化系统。

## 项目结构

```
projects/tgb_data/
├── config/                    # 配置目录
│   ├── bloggers.yaml         # 博主列表配置
│   ├── templates.yaml        # 模版路径配置
│   └── settings.yaml         # 全局设置
├── templates/                 # 模版目录
│   ├── collection_template.md # 博主原文合集模版
│   └── report_template.md    # 复盘报告模版
├── src/                       # 源代码
│   ├── collectors/           # 采集模块
│   ├── outputs/              # 输出模块
│   └── utils/                # 工具模块
├── scripts/                  # 脚本目录
│   └── daily_run.sh         # 自动化运行脚本
└── main.py                   # 主程序入口
```

## 功能特性

1. **博主原文采集**: 支持微博、微信公众号、雪球等平台
2. **内容处理**: 自动总结、关键词提取、情感分析
3. **复盘报告**: 生成每日/周末复盘报告，辅助炒股决策
4. **双端输出**: 支持本地文件保存和飞书文档同步
5. **自动化运行**: 支持定时任务自动执行

## 安装依赖

```bash
pip install pyyaml jinja2
```

## 使用方法

### 命令行使用

```bash
# 运行完整工作流（采集+报告）
python main.py --mode full

# 仅采集
python main.py --mode daily

# 仅生成报告
python main.py --mode report

# 周末采集
python main.py --mode weekend

# 指定日期
python main.py --mode full --date 2024-01-15
```

### 自动化运行

```bash
# 添加到 crontab
# 每天早上8点自动运行
0 8 * * * /Users/victorjiang/Documents/Software/quant_data/projects/tgb_data/scripts/daily_run.sh daily >> /Users/victorjiang/Documents/Software/quant_data/projects/tgb_data/logs/cron.log 2>&1
```

## 配置说明

### 博主配置 (config/bloggers.yaml)

```yaml
bloggers:
  - id: blogger_001
    name: "博主名称"
    platform: "weibo"  # weibo/wechat/xueqiu
    url: "https://..."
    tags: ["技术分析", "短线"]
    enabled: true
```

### 模版配置 (config/templates.yaml)

定义输出文件的模版和路径。

### 全局设置 (config/settings.yaml)

包括日志配置、输出配置、自动化配置等。

## 输出目录

- **本地**: `/Users/victorjiang/projects/tgb_data/`
  - `collections/{date}/` - 博主原文合集
  - `reports/{date}/` - 复盘报告

- **飞书**: `Quant/Tgb_data/`
  - `博主原文合集/` - 飞书合集文档
  - `复盘报告/` - 飞书报告文档

## 开发说明

### 扩展新平台

在 `src/collectors/blogger_collector.py` 中添加新的采集方法：

```python
def _collect_new_platform(self, blogger, target_date):
    # 实现新平台的采集逻辑
    pass
```

### 自定义报告模版

编辑 `templates/report_template.md` 文件，使用 Jinja2 语法自定义报告格式。

## 注意事项

1. 首次使用需要配置博主列表
2. 飞书功能需要安装 lark-cli 并完成认证
3. 建议定期备份配置文件
4. 仅供参考，不构成投资建议

## 版本

Version: 1.0.0
Author: Victor
