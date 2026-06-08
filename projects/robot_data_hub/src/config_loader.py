"""
配置加载器
"""
import os
import yaml
from pathlib import Path
from typing import Dict, Any, List


class ConfigLoader:
    """配置加载器"""

    def __init__(self, config_dir: str = None):
        if config_dir is None:
            self.config_dir = Path(__file__).parent.parent / "config"
        else:
            self.config_dir = Path(config_dir)

        self._platforms_config = None

    def load_platforms_config(self) -> Dict[str, Any]:
        """加载平台配置"""
        if self._platforms_config is None:
            config_file = self.config_dir / "platforms.yaml"
            with open(config_file, "r", encoding="utf-8") as f:
                self._platforms_config = yaml.safe_load(f)
        return self._platforms_config

    def get_platforms(self) -> Dict[str, Dict[str, Any]]:
        """获取所有启用的平台配置"""
        config = self.load_platforms_config()
        platforms = config.get("platforms", {})
        return {k: v for k, v in platforms.items() if v.get("enabled", False)}

    def get_keywords(self, platform: str) -> List[str]:
        """获取指定平台的关键词"""
        config = self.load_platforms_config()
        return config.get("platforms", {}).get(platform, {}).get("keywords", [])

    def get_collection_config(self) -> Dict[str, Any]:
        """获取采集配置"""
        config = self.load_platforms_config()
        return config.get("collection", {})

    def get_output_config(self) -> Dict[str, Any]:
        """获取输出配置"""
        config = self.load_platforms_config()
        return config.get("output", {})

    def get_analysis_config(self) -> Dict[str, Any]:
        """获取分析配置"""
        config = self.load_platforms_config()
        return config.get("analysis", {})
