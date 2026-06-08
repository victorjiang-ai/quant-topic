# {{ date }} {{ report_type }}复盘报告

## 报告概要

- **报告日期**: {{ date }}
- **报告类型**: {{ report_type }}
- **覆盖博主数**: {{ blogger_count }}
- **覆盖内容数**: {{ content_count }}

---

## 一、总体概述

{{ overall_summary }}

---

## 二、市场情绪分析

### 2.1 整体情绪
{{ sentiment_analysis }}

### 2.2 关键情绪指标
{{ sentiment_indicators }}

---

## 三、核心观点汇总

{% for point in key_points %}
### 3.{{ loop.index }} {{ point.category }}

**观点来源**: {{ point.source }}
**发布时间**: {{ point.publish_time }}

{{ point.content }}

**关键词**: {{ point.keywords | join(', ') }}

{% endfor %}

---

## 四、交易信号

### 4.1 买入信号
{% for signal in buy_signals %}
- {{ signal }}
{% endfor %}

### 4.2 卖出信号
{% for signal in sell_signals %}
- {{ signal }}
{% endfor %}

### 4.3 风险提示
{% for warning in risk_warnings %}
- ⚠️ {{ warning }}
{% endfor %}

---

## 五、投资建议

{{ investment_recommendations }}

---

## 六、需关注博主

{% for blogger in bloggers_to_watch %}
### {{ loop.index }}. {{ blogger.name }}

{{ blogger.reason }}

{% endfor %}

---

## 七、风险提示

{{ risk_warnings_summary }}

---

*本报告仅供参考，不构成投资建议*
*市场有风险，投资需谨慎*
*本报告由 TGB 量化数据采集系统自动生成*
*生成时间: {{ generation_time }}*
