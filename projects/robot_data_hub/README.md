# 机器人题材数据中心

采集多平台（抖音、小红书、微博、知乎）关于机器人题材的内容，输出到飞书多维表格。

## 功能特点

- ✅ **多平台采集**：抖音、小红书、微博、知乎
- ✅ **内容分析**：热词提取、热度评分、简单情感分析
- ✅ **多维输出**：本地 Markdown + 飞书多维表格
- ✅ **配置驱动**：通过 YAML 配置平台关键词和输出

## 项目结构

```
robot_data_hub/
├── config/
│   └── platforms.yaml    # 平台配置
├── src/
│   ├── config_loader.py  # 配置加载
│   ├── platform_collector.py  # 多平台采集
│   ├── content_processor.py   # 内容处理分析
│   └── feishu_output.py       # 飞书多维表格导出
├── collections/           # 本地输出目录
├── main.py                # 主程序入口
└── requirements.txt       # 依赖
```

## 快速开始

### 1. 安装依赖

```bash
cd robot_data_hub
pip install -r requirements.txt
```

### 2. 运行采集

```bash
python main.py

# 指定日期
python main.py 2026-06-07
```

### 3. 配置飞书

如需连接真实飞书多维表格：

1. 运行 `lark-cli auth login` 登录
2. 在飞书中创建多维表格并配置字段
3. 更新 `config/platforms.yaml` 中的配置
4. 在 `feishu_output.py` 中接入真实 lark-cli 多维表格命令

## 飞书多维表格字段建议

创建表格时可配置以下字段：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 平台 | 单选 | 抖音/小红书/微博/知乎 |
| 标题 | 多行文本 | 内容标题 |
| 内容 | 多行文本 | 正文摘要 |
| 作者 | 文本 | 作者/博主名 |
| 发布时间 | 日期时间 | 发布时间 |
| 浏览量 | 数字 | 浏览数 |
| 点赞数 | 数字 | 点赞数 |
| 评论数 | 数字 | 评论数 |
| 原文链接 | 链接 | 链接 |
| 采集时间 | 日期时间 | 采集时间 |
| 热度分 | 数字 | 计算得出的热度分 |

## 扩展说明

当前采集器为模拟数据，如需接入真实数据：

1. 在 `platform_collector.py` 中的对应类中实现真实请求/爬虫
2. 注意遵守平台 robots.txt 规则
3. 建议使用官方 API（如微博开放平台等）
