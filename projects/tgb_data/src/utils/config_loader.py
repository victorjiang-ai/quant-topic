"""
配置加载器模块
负责加载和管理项目配置
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, List


class ConfigLoader:
    """配置加载器类"""
    
    def __init__(self, config_dir: str = None):
        """
        初始化配置加载器
        
        Args:
            config_dir: 配置文件目录路径，默认为项目根目录下的config
        """
        if config_dir is None:
            self.config_dir = Path(__file__).parent.parent.parent / 'config'
        else:
            self.config_dir = Path(config_dir)
        
        self._bloggers_config = None
        self._templates_config = None
        self._settings_config = None
    
    def load_bloggers(self) -> List[Dict[str, Any]]:
        """
        加载博主列表配置
        
        Returns:
            博主列表
        """
        if self._bloggers_config is None:
            config_file = self.config_dir / 'bloggers.yaml'
            with open(config_file, 'r', encoding='utf-8') as f:
                self._bloggers_config = yaml.safe_load(f)
        
        return self._bloggers_config.get('bloggers', [])
    
    def get_enabled_bloggers(self) -> List[Dict[str, Any]]:
        """
        获取所有已启用的博主
        
        Returns:
            已启用的博主列表
        """
        bloggers = self.load_bloggers()
        return [b for b in bloggers if b.get('enabled', True)]
    
    def load_templates_config(self) -> Dict[str, Any]:
        """
        加载模版配置
        
        Returns:
            模版配置字典
        """
        if self._templates_config is None:
            config_file = self.config_dir / 'templates.yaml'
            with open(config_file, 'r', encoding='utf-8') as f:
                self._templates_config = yaml.safe_load(f)
        
        return self._templates_config
    
    def load_settings(self) -> Dict[str, Any]:
        """
        加载全局设置
        
        Returns:
            全局设置字典
        """
        if self._settings_config is None:
            config_file = self.config_dir / 'settings.yaml'
            with open(config_file, 'r', encoding='utf-8') as f:
                self._settings_config = yaml.safe_load(f)
        
        return self._settings_config
    
    def get_output_paths(self) -> Dict[str, str]:
        """
        获取输出路径配置
        
        Returns:
            输出路径配置字典
        """
        templates_config = self.load_templates_config()
        return templates_config.get('paths', {})
    
    def get_collection_config(self) -> Dict[str, Any]:
        """
        获取采集配置
        
        Returns:
            采集配置字典
        """
        bloggers_config = self.load_bloggers()
        return bloggers_config.get('collection', {})
    
    def get_summary_config(self) -> Dict[str, Any]:
        """
        获取总结配置
        
        Returns:
            总结配置字典
        """
        bloggers_config = self.load_bloggers()
        return bloggers_config.get('summary', {})
    
    def update_blogger(self, blogger_id: str, updates: Dict[str, Any]) -> bool:
        """
        更新博主配置
        
        Args:
            blogger_id: 博主ID
            updates: 要更新的字段和值
            
        Returns:
            是否更新成功
        """
        bloggers = self.load_bloggers()
        
        for blogger in bloggers:
            if blogger.get('id') == blogger_id:
                blogger.update(updates)
                config_file = self.config_dir / 'bloggers.yaml'
                with open(config_file, 'w', encoding='utf-8') as f:
                    yaml.dump(self._bloggers_config, f, allow_unicode=True, default_flow_style=False)
                return True
        
        return False
    
    def add_blogger(self, blogger: Dict[str, Any]) -> bool:
        """
        添加新博主
        
        Args:
            blogger: 博主信息字典
            
        Returns:
            是否添加成功
        """
        if self._bloggers_config is None:
            self.load_bloggers()
        
        if 'bloggers' not in self._bloggers_config:
            self._bloggers_config['bloggers'] = []
        
        self._bloggers_config['bloggers'].append(blogger)
        
        config_file = self.config_dir / 'bloggers.yaml'
        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.dump(self._bloggers_config, f, allow_unicode=True, default_flow_style=False)
        
        return True
    
    def remove_blogger(self, blogger_id: str) -> bool:
        """
        删除博主
        
        Args:
            blogger_id: 博主ID
            
        Returns:
            是否删除成功
        """
        if self._bloggers_config is None:
            self.load_bloggers()
        
        original_length = len(self._bloggers_config.get('bloggers', []))
        self._bloggers_config['bloggers'] = [
            b for b in self._bloggers_config.get('bloggers', [])
            if b.get('id') != blogger_id
        ]
        
        if len(self._bloggers_config['bloggers']) < original_length:
            config_file = self.config_dir / 'bloggers.yaml'
            with open(config_file, 'w', encoding='utf-8') as f:
                yaml.dump(self._bloggers_config, f, allow_unicode=True, default_flow_style=False)
            return True
        
        return False
