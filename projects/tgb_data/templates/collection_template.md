# {{ date }} 博主原文合集

## 采集概要

- **采集日期**: {{ date }}
- **博主数量**: {{ blogger_count }}
- **文章总数**: {{ posts_count }}

---

{% for blogger in bloggers %}
## {{ blogger.name }}

**平台**: {{ blogger.platform }}
**标签**: {{ blogger.tags | join(', ') }}
**描述**: {{ blogger.description }}

### 最新文章 ({{ blogger.post_count }} 篇)

{% for post in blogger.posts %}
#### {{ loop.index }}. {{ post.title }}

- **发布时间**: {{ post.publish_time }}
- **阅读量**: {{ post.read_count }}
- **点赞数**: {{ post.like_count }}

**简要总结**:
{{ post.summary }}

**博主原文**:
{{ post.original_content }}

---
{% endfor %}

{% endfor %}

---

*本报告由 TGB 量化数据采集系统自动生成*
*生成时间: {{ generation_time }}*
