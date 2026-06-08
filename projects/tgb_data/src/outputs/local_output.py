"""
本地文件输出模块
负责将内容输出到本地文件系统
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
from jinja2 import Template


class LocalOutput:
    """本地文件输出器"""
    
    def __init__(self, base_path: str = None):
        """
        初始化本地输出器
        
        Args:
            base_path: 基础路径
        """
        if base_path is None:
            self.base_path = Path(__file__).parent.parent.parent
        else:
            self.base_path = Path(base_path)
        
        self.collections_dir = self.base_path / 'collections'
        self.reports_dir = self.base_path / 'reports'
        self.templates_dir = self.base_path / 'templates'
    
    def ensure_directories(self):
        """确保输出目录存在"""
        self.collections_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
    
    def load_template(self, template_name: str) -> Template:
        """
        加载模版
        
        Args:
            template_name: 模版名称
            
        Returns:
            Jinja2模版对象
        """
        template_path = self.templates_dir / template_name
        with open(template_path, 'r', encoding='utf-8') as f:
            return Template(f.read(), autoescape=False)
    
    def save_collection(self, date: str, contents: List[Dict[str, Any]], 
                       blogger_data: List[Dict[str, Any]] = None) -> str:
        """
        保存博主原文合集
        
        Args:
            date: 日期字符串
            contents: 内容列表
            blogger_data: 博主数据
            
        Returns:
            保存的文件路径
        """
        self.ensure_directories()
        
        try:
            template = self.load_template('collection_template.md')
        except FileNotFoundError:
            return self._save_collection_fallback(date, contents, blogger_data)
        
        date_dir = self.collections_dir / date
        date_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = date_dir / 'collection.md'
        
        template_vars = {
            'date': date,
            'blogger_count': len(set(c.get('blogger_id') for c in contents)),
            'posts_count': len(contents),
            'generation_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'bloggers': self._group_by_blogger(contents) if blogger_data is None else blogger_data,
            'contents': contents
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(template.render(**template_vars))
        
        self._save_json_data(date_dir / 'collection_data.json', {
            'date': date,
            'contents': contents,
            'blogger_data': blogger_data,
            'generated_at': datetime.now().isoformat()
        })
        
        return str(output_file)
    
    def save_report(self, date: str, report_data: Dict[str, Any], 
                   report_type: str = 'daily') -> str:
        """
        保存复盘报告
        
        Args:
            date: 日期字符串
            report_data: 报告数据
            report_type: 报告类型
            
        Returns:
            保存的文件路径
        """
        self.ensure_directories()
        
        try:
            template = self.load_template('report_template.md')
        except FileNotFoundError:
            return self._save_report_fallback(date, report_data, report_type)
        
        date_dir = self.reports_dir / date
        date_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = date_dir / f'{report_type}_report.md'
        
        template_vars = {
            'date': date,
            'report_type': report_type,
            'generation_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            **report_data
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(template.render(**template_vars))
        
        self._save_json_data(date_dir / f'{report_type}_report_data.json', {
            'date': date,
            'report_type': report_type,
            'data': report_data,
            'generated_at': datetime.now().isoformat()
        })
        
        return str(output_file)
    
    def _group_by_blogger(self, contents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        按博主分组内容
        
        Args:
            contents: 内容列表
            
        Returns:
            按博主分组的数据
        """
        blogger_groups = {}
        
        for content in contents:
            blogger_id = content.get('blogger_id')
            if blogger_id not in blogger_groups:
                blogger_groups[blogger_id] = {
                    'id': blogger_id,
                    'name': content.get('blogger_name', 'Unknown'),
                    'platform': content.get('platform', 'unknown'),
                    'tags': content.get('tags', []),
                    'description': '',
                    'posts': [],
                    'post_count': 0
                }
            
            blogger_groups[blogger_id]['posts'].append({
                'title': content.get('title', ''),
                'summary': content.get('summary', ''),
                'original_content': content.get('original_content', ''),
                'publish_time': content.get('publish_time', ''),
                'read_count': content.get('read_count', 0),
                'like_count': content.get('like_count', 0),
                'keywords': content.get('keywords', [])
            })
            blogger_groups[blogger_id]['post_count'] += 1
        
        return list(blogger_groups.values())
    
    def _save_json_data(self, file_path: Path, data: Dict[str, Any]):
        """
        保存JSON数据
        
        Args:
            file_path: 文件路径
            data: 要保存的数据
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _save_collection_fallback(self, date: str, contents: List[Dict[str, Any]], 
                                  blogger_data: List[Dict[str, Any]] = None) -> str:
        """
        保存合集的备用方法（当模版不存在时）
        
        Args:
            date: 日期
            contents: 内容
            blogger_data: 博主数据
            
        Returns:
            保存的文件路径
        """
        date_dir = self.collections_dir / date
        date_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = date_dir / 'collection.md'
        
        lines = [f"# {date} 博主原文合集\n"]
        lines.append(f"\n## 概要\n")
        lines.append(f"- 日期: {date}\n")
        lines.append(f"- 博主数量: {len(set(c.get('blogger_id') for c in contents))}\n")
        lines.append(f"- 文章数量: {len(contents)}\n")
        lines.append(f"- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        grouped = self._group_by_blogger(contents)
        for blogger in grouped:
            lines.append(f"\n## {blogger['name']}\n")
            lines.append(f"- 平台: {blogger['platform']}\n")
            lines.append(f"- 标签: {', '.join(blogger['tags'])}\n")
            lines.append(f"- 文章数量: {blogger['post_count']}\n")
            
            for i, post in enumerate(blogger['posts'], 1):
                lines.append(f"\n### {i}. {post['title']}\n")
                lines.append(f"- 发布时间: {post['publish_time']}\n")
                lines.append(f"\n**简要总结:**\n{post['summary']}\n")
                lines.append(f"\n**博主原文:**\n{post['original_content']}\n")
                lines.append("---\n")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        self._save_json_data(date_dir / 'collection_data.json', {
            'date': date,
            'contents': contents,
            'generated_at': datetime.now().isoformat()
        })
        
        return str(output_file)
    
    def _save_report_fallback(self, date: str, report_data: Dict[str, Any], 
                            report_type: str = 'daily') -> str:
        """
        保存报告的备用方法（当模版不存在时）
        
        Args:
            date: 日期
            report_data: 报告数据
            report_type: 报告类型
            
        Returns:
            保存的文件路径
        """
        date_dir = self.reports_dir / date
        date_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = date_dir / f'{report_type}_report.md'
        
        lines = [f"# {date} {report_type}复盘报告\n\n"]
        lines.append(f"## 报告概要\n")
        lines.append(f"- 日期: {date}\n")
        lines.append(f"- 类型: {report_type}\n")
        lines.append(f"- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        if 'overall_summary' in report_data:
            lines.append(f"## 总体概述\n{report_data['overall_summary']}\n\n")
        
        if 'key_points' in report_data:
            lines.append(f"## 核心观点\n")
            for i, point in enumerate(report_data['key_points'], 1):
                lines.append(f"\n### {i}. {point.get('category', '观点')}\n")
                lines.append(f"来源: {point.get('source', '未知')}\n")
                lines.append(f"{point.get('content', '')}\n")
        
        if 'recommendations' in report_data:
            lines.append(f"\n## 投资建议\n{report_data['recommendations']}\n\n")
        
        if 'risk_warnings' in report_data and report_data['risk_warnings']:
            lines.append(f"\n## 风险提示\n")
            for warning in report_data['risk_warnings']:
                lines.append(f"- ⚠️ {warning}\n")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        self._save_json_data(date_dir / f'{report_type}_report_data.json', {
            'date': date,
            'report_type': report_type,
            'data': report_data,
            'generated_at': datetime.now().isoformat()
        })
        
        return str(output_file)
    
    def list_collections(self) -> List[str]:
        """
        列出所有合集
        
        Returns:
            合集日期列表
        """
        if not self.collections_dir.exists():
            return []
        
        return sorted([d.name for d in self.collections_dir.iterdir() if d.is_dir()])
    
    def list_reports(self) -> List[str]:
        """
        列出所有报告
        
        Returns:
            报告日期列表
        """
        if not self.reports_dir.exists():
            return []
        
        return sorted([d.name for d in self.reports_dir.iterdir() if d.is_dir()])
    
    def get_collection_path(self, date: str) -> str:
        """
        获取指定日期的合集路径
        
        Args:
            date: 日期字符串
            
        Returns:
            合集Markdown文件路径
        """
        return str(self.collections_dir / date / 'collection.md')
    
    def get_report_path(self, date: str, report_type: str = 'daily') -> str:
        """
        获取指定日期的报告路径
        
        Args:
            date: 日期字符串
            report_type: 报告类型
            
        Returns:
            报告Markdown文件路径
        """
        return str(self.reports_dir / date / f'{report_type}_report.md')
