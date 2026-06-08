"""
飞书文档输出模块
负责将内容输出到飞书文档
"""

import subprocess
import json
from typing import Dict, Any, List, Optional
from datetime import datetime


class FeishuOutput:
    """飞书文档输出器"""
    
    def __init__(self, wiki_folder: str = "Quant/Tgb_data"):
        """
        初始化飞书输出器
        
        Args:
            wiki_folder: 飞书文档中的目标文件夹路径
        """
        self.wiki_folder = wiki_folder
        self.collection_folder = f"{wiki_folder}/博主原文合集"
        self.report_folder = f"{wiki_folder}/复盘报告"
    
    def _run_lark_command(self, command: List[str]) -> tuple[bool, str]:
        """
        运行lark-cli命令
        
        Args:
            command: 命令列表
            
        Returns:
            (成功标志, 输出信息)
        """
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, result.stderr
        except Exception as e:
            return False, str(e)
    
    def create_collection_doc(self, date: str, contents: List[Dict[str, Any]], 
                             blogger_data: List[Dict[str, Any]] = None) -> Optional[str]:
        """
        创建博主原文合集飞书文档
        
        Args:
            date: 日期字符串
            contents: 内容列表
            blogger_data: 博主数据
            
        Returns:
            创建的文档token，失败返回None
        """
        doc_content = self._generate_collection_content(date, contents, blogger_data)
        
        command = [
            'lark-cli', 'docs', '+create',
            '--title', f'{date} 博主原文合集',
            '--content', doc_content,
            '--folder', self.collection_folder,
            '--format', 'markdown'
        ]
        
        success, output = self._run_lark_command(command)
        
        if success:
            try:
                result = json.loads(output)
                return result.get('data', {}).get('doc', {}).get('token')
            except:
                return output.strip()
        else:
            print(f"创建飞书合集文档失败: {output}")
            return None
    
    def create_report_doc(self, date: str, report_data: Dict[str, Any], 
                         report_type: str = 'daily') -> Optional[str]:
        """
        创建复盘报告飞书文档
        
        Args:
            date: 日期字符串
            report_data: 报告数据
            report_type: 报告类型
            
        Returns:
            创建的文档token，失败返回None
        """
        doc_content = self._generate_report_content(date, report_data, report_type)
        
        command = [
            'lark-cli', 'docs', '+create',
            '--title', f'{date} {report_type}复盘报告',
            '--content', doc_content,
            '--folder', self.report_folder,
            '--format', 'markdown'
        ]
        
        success, output = self._run_lark_command(command)
        
        if success:
            try:
                result = json.loads(output)
                return result.get('data', {}).get('doc', {}).get('token')
            except:
                return output.strip()
        else:
            print(f"创建飞书报告文档失败: {output}")
            return None
    
    def _generate_collection_content(self, date: str, contents: List[Dict[str, Any]], 
                                   blogger_data: List[Dict[str, Any]] = None) -> str:
        """
        生成合集文档内容
        
        Args:
            date: 日期
            contents: 内容列表
            blogger_data: 博主数据
            
        Returns:
            Markdown格式的内容
        """
        lines = [f"# {date} 博主原文合集\n"]
        lines.append(f"\n## 采集概要\n")
        lines.append(f"- **采集日期**: {date}\n")
        lines.append(f"- **博主数量**: {len(set(c.get('blogger_id') for c in contents))}\n")
        lines.append(f"- **文章总数**: {len(contents)}\n")
        lines.append(f"- **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        blogger_groups = self._group_by_blogger(contents)
        
        for blogger in blogger_groups:
            lines.append(f"\n---\n")
            lines.append(f"## {blogger['name']}\n")
            lines.append(f"\n**平台**: {blogger['platform']}  ")
            lines.append(f"**标签**: {', '.join(blogger['tags'])}  ")
            lines.append(f"**文章数**: {len(blogger['posts'])}\n")
            
            for i, post in enumerate(blogger['posts'], 1):
                lines.append(f"\n### {i}. {post['title']}\n")
                lines.append(f"\n**发布时间**: {post['publish_time']}  ")
                lines.append(f"**阅读量**: {post.get('read_count', 0)}  ")
                lines.append(f"**点赞数**: {post.get('like_count', 0)}\n")
                
                if post.get('summary'):
                    lines.append(f"\n**简要总结**:\n{post['summary']}\n")
                
                if post.get('original_content'):
                    lines.append(f"\n**博主原文**:\n{post['original_content']}\n")
        
        lines.append(f"\n---\n")
        lines.append(f"\n*本报告由 TGB 量化数据采集系统自动生成*\n")
        
        return ''.join(lines)
    
    def _generate_report_content(self, date: str, report_data: Dict[str, Any], 
                                report_type: str = 'daily') -> str:
        """
        生成报告文档内容
        
        Args:
            date: 日期
            report_data: 报告数据
            report_type: 报告类型
            
        Returns:
            Markdown格式的内容
        """
        lines = [f"# {date} {report_type}复盘报告\n"]
        lines.append(f"\n## 报告概要\n")
        lines.append(f"- **报告日期**: {date}\n")
        lines.append(f"- **报告类型**: {report_type}\n")
        lines.append(f"- **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        if 'overall_summary' in report_data:
            lines.append(f"\n## 总体概述\n")
            lines.append(f"{report_data['overall_summary']}\n")
        
        if 'sentiment_analysis' in report_data:
            lines.append(f"\n## 市场情绪\n")
            lines.append(f"{report_data['sentiment_analysis']}\n")
        
        if 'key_points' in report_data and report_data['key_points']:
            lines.append(f"\n## 核心观点\n")
            for i, point in enumerate(report_data['key_points'], 1):
                lines.append(f"\n### {i}. {point.get('category', '观点')}\n")
                lines.append(f"\n**来源**: {point.get('source', '未知')}  ")
                lines.append(f"**时间**: {point.get('publish_time', '')}\n")
                lines.append(f"\n{point.get('content', '')}\n")
                if point.get('keywords'):
                    lines.append(f"\n**关键词**: {', '.join(point['keywords'])}\n")
        
        if 'buy_signals' in report_data and report_data['buy_signals']:
            lines.append(f"\n## 买入信号\n")
            for signal in report_data['buy_signals']:
                lines.append(f"- 📈 {signal}\n")
        
        if 'sell_signals' in report_data and report_data['sell_signals']:
            lines.append(f"\n## 卖出信号\n")
            for signal in report_data['sell_signals']:
                lines.append(f"- 📉 {signal}\n")
        
        if 'risk_warnings' in report_data and report_data['risk_warnings']:
            lines.append(f"\n## 风险提示\n")
            for warning in report_data['risk_warnings']:
                lines.append(f"- ⚠️ {warning}\n")
        
        if 'recommendations' in report_data:
            lines.append(f"\n## 投资建议\n")
            lines.append(f"{report_data['recommendations']}\n")
        
        lines.append(f"\n---\n")
        lines.append(f"\n*本报告仅供参考，不构成投资建议*\n")
        lines.append(f"*市场有风险，投资需谨慎*\n")
        lines.append(f"*本报告由 TGB 量化数据采集系统自动生成*\n")
        
        return ''.join(lines)
    
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
                    'posts': []
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
        
        return list(blogger_groups.values())
    
    def upload_local_file(self, local_file_path: str, 
                         folder: str = None) -> Optional[str]:
        """
        上传本地文件到飞书
        
        Args:
            local_file_path: 本地文件路径
            folder: 目标文件夹
            
        Returns:
            上传后的文件URL，失败返回None
        """
        if folder is None:
            folder = self.collection_folder
        
        command = [
            'lark-cli', 'drive', 'upload',
            '--file', local_file_path,
            '--folder', folder
        ]
        
        success, output = self._run_lark_command(command)
        
        if success:
            try:
                result = json.loads(output)
                return result.get('data', {}).get('file', {}).get('token')
            except:
                return output.strip()
        else:
            print(f"上传文件到飞书失败: {output}")
            return None
    
    def create_folder(self, folder_name: str, parent_folder: str = None) -> bool:
        """
        创建飞书文件夹
        
        Args:
            folder_name: 文件夹名称
            parent_folder: 父文件夹路径
            
        Returns:
            是否创建成功
        """
        if parent_folder:
            folder_path = f"{parent_folder}/{folder_name}"
        else:
            folder_path = folder_name
        
        command = [
            'lark-cli', 'drive', 'folder', 'create',
            '--name', folder_name,
            '--parent-folder', parent_folder or ''
        ]
        
        success, output = self._run_lark_command(command)
        
        if not success:
            print(f"创建飞书文件夹失败: {output}")
        
        return success
