"""
TGB量化数据采集系统 - 主程序
"""

import sys
import argparse
import logging
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.utils.config_loader import ConfigLoader
from src.utils.date_utils import DateUtils
from src.collectors.blogger_collector import BloggerCollector
from src.collectors.content_processor import ContentProcessor
from src.outputs.local_output import LocalOutput
from src.outputs.feishu_output import FeishuOutput


class QuantTgbSystem:
    """TGB量化数据采集系统主类"""
    
    def __init__(self, config_dir: str = None):
        """
        初始化系统
        
        Args:
            config_dir: 配置目录路径
        """
        self.config_loader = ConfigLoader(config_dir)
        self.date_utils = DateUtils()
        self.collector = BloggerCollector(self.config_loader)
        self.processor = ContentProcessor()
        self.local_output = LocalOutput()
        self.feishu_output = FeishuOutput()
        
        self._setup_logging()
    
    def _setup_logging(self):
        """设置日志"""
        settings = self.config_loader.load_settings()
        log_config = settings.get('logging', {})
        
        log_level = getattr(logging, log_config.get('level', 'INFO'))
        log_format = log_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        logging.basicConfig(
            level=log_level,
            format=log_format,
            handlers=[
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger(__name__)
    
    def run_daily_collection(self, target_date: str = None):
        """
        运行每日采集
        
        Args:
            target_date: 目标日期，默认为前一天
        """
        if target_date is None:
            target_date = self.date_utils.format_date(self.date_utils.get_previous_day())
        
        self.logger.info(f"开始采集 {target_date} 的博主内容")
        
        try:
            contents = self.collector.collect_all(target_date)
            self.logger.info(f"采集到 {len(contents)} 条内容")
            
            summary_config = self.config_loader.get_summary_config()
            processed_contents = self.processor.process_batch(contents, summary_config)
            self.logger.info(f"处理完成 {len(processed_contents)} 条内容")
            
            blogger_data = self.local_output._group_by_blogger(processed_contents)
            local_path = self.local_output.save_collection(target_date, processed_contents, blogger_data)
            self.logger.info(f"本地合集已保存: {local_path}")
            
            try:
                feishu_token = self.feishu_output.create_collection_doc(
                    target_date, processed_contents, blogger_data
                )
                if feishu_token:
                    self.logger.info(f"飞书合集文档已创建: {feishu_token}")
            except Exception as e:
                self.logger.warning(f"飞书文档创建失败: {e}")
            
            return {
                'success': True,
                'date': target_date,
                'content_count': len(processed_contents),
                'local_path': local_path,
                'feishu_token': feishu_token if 'feishu_token' in locals() else None
            }
            
        except Exception as e:
            self.logger.error(f"每日采集失败: {e}")
            return {
                'success': False,
                'date': target_date,
                'error': str(e)
            }
    
    def run_weekend_collection(self, ref_date: str = None):
        """
        运行周末采集
        
        Args:
            ref_date: 参考日期，默认为今天
        """
        if ref_date:
            ref = self.date_utils.parse_date(ref_date)
        else:
            ref = None
        
        friday, saturday, sunday = self.date_utils.get_weekend_dates(ref)
        start_date = self.date_utils.format_date(friday)
        end_date = self.date_utils.format_date(sunday)
        
        self.logger.info(f"开始采集周末内容: {start_date} 至 {end_date}")
        
        try:
            contents = self.collector.collect_with_date_range(start_date, end_date)
            self.logger.info(f"采集到 {len(contents)} 条内容")
            
            summary_config = self.config_loader.get_summary_config()
            processed_contents = self.processor.process_batch(contents, summary_config)
            
            blogger_data = self.local_output._group_by_blogger(processed_contents)
            local_path = self.local_output.save_collection(
                f"{start_date}_to_{end_date}",
                processed_contents,
                blogger_data
            )
            self.logger.info(f"本地合集已保存: {local_path}")
            
            try:
                feishu_token = self.feishu_output.create_collection_doc(
                    f"{start_date}至{end_date}",
                    processed_contents,
                    blogger_data
                )
                if feishu_token:
                    self.logger.info(f"飞书合集文档已创建: {feishu_token}")
            except Exception as e:
                self.logger.warning(f"飞书文档创建失败: {e}")
            
            return {
                'success': True,
                'date_range': f"{start_date}至{end_date}",
                'content_count': len(processed_contents),
                'local_path': local_path
            }
            
        except Exception as e:
            self.logger.error(f"周末采集失败: {e}")
            return {
                'success': False,
                'date_range': f"{start_date}至{end_date}",
                'error': str(e)
            }
    
    def generate_daily_report(self, target_date: str = None):
        """
        生成每日复盘报告
        
        Args:
            target_date: 目标日期，默认为前一天
        """
        if target_date is None:
            target_date = self.date_utils.format_date(self.date_utils.get_previous_day())
        
        self.logger.info(f"开始生成 {target_date} 的复盘报告")
        
        try:
            collection_path = self.local_output.get_collection_path(target_date)
            
            from src.outputs.local_output import LocalOutput
            import json
            
            data_path = Path(collection_path).parent / 'collection_data.json'
            if data_path.exists():
                with open(data_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    contents = data.get('contents', [])
            else:
                contents = []
            
            report_data = self._generate_report_data(contents)
            
            report_path = self.local_output.save_report(
                target_date,
                report_data,
                'daily'
            )
            self.logger.info(f"本地报告已保存: {report_path}")
            
            try:
                feishu_token = self.feishu_output.create_report_doc(
                    target_date,
                    report_data,
                    'daily'
                )
                if feishu_token:
                    self.logger.info(f"飞书报告文档已创建: {feishu_token}")
            except Exception as e:
                self.logger.warning(f"飞书报告创建失败: {e}")
            
            return {
                'success': True,
                'date': target_date,
                'report_path': report_path
            }
            
        except Exception as e:
            self.logger.error(f"生成复盘报告失败: {e}")
            return {
                'success': False,
                'date': target_date,
                'error': str(e)
            }
    
    def _generate_report_data(self, contents: list) -> dict:
        """
        生成报告数据
        
        Args:
            contents: 内容列表
            
        Returns:
            报告数据字典
        """
        if not contents:
            return {
                'overall_summary': '当日无采集内容',
                'blogger_count': 0,
                'content_count': 0,
                'key_points': [],
                'buy_signals': [],
                'sell_signals': [],
                'risk_warnings': [],
                'recommendations': '无内容可分析'
            }
        
        all_keywords = []
        all_buy_signals = []
        all_sell_signals = []
        all_risk_warnings = []
        key_points = []
        
        for content in contents:
            all_keywords.extend(content.get('keywords', []))
            all_buy_signals.extend(content.get('buy_signals', []))
            all_sell_signals.extend(content.get('sell_signals', []))
            all_risk_warnings.extend(content.get('risk_warnings', []))
            
            if content.get('summary'):
                key_points.append({
                    'category': content.get('blogger_name', '博主'),
                    'source': content.get('blogger_name', ''),
                    'publish_time': content.get('publish_time', ''),
                    'content': content.get('summary', ''),
                    'keywords': content.get('keywords', [])
                })
        
        blogger_count = len(set(c.get('blogger_id') for c in contents))
        
        positive_count = sum(1 for c in contents if c.get('sentiment', {}).get('sentiment') == 'positive')
        negative_count = sum(1 for c in contents if c.get('sentiment', {}).get('sentiment') == 'negative')
        
        if positive_count > negative_count:
            sentiment_analysis = "市场情绪偏积极"
        elif negative_count > positive_count:
            sentiment_analysis = "市场情绪偏谨慎"
        else:
            sentiment_analysis = "市场情绪中性"
        
        recommendations = self._generate_recommendations(
            all_buy_signals,
            all_sell_signals,
            all_risk_warnings
        )
        
        return {
            'overall_summary': f"采集了{blogger_count}位博主的{len(contents)}条内容，整体{sentiment_analysis}",
            'sentiment_analysis': sentiment_analysis,
            'blogger_count': blogger_count,
            'content_count': len(contents),
            'key_points': key_points[:10],
            'buy_signals': list(set(all_buy_signals))[:5],
            'sell_signals': list(set(all_sell_signals))[:5],
            'risk_warnings': list(set(all_risk_warnings))[:5],
            'recommendations': recommendations
        }
    
    def _generate_recommendations(self, buy_signals: list, sell_signals: list, 
                                 risk_warnings: list) -> str:
        """
        生成投资建议
        
        Args:
            buy_signals: 买入信号列表
            sell_signals: 卖出信号列表
            risk_warnings: 风险警告列表
            
        Returns:
            投资建议文本
        """
        recommendations = []
        
        if buy_signals:
            recommendations.append("近期买入信号较多，建议关注相关板块")
        
        if sell_signals:
            recommendations.append("部分博主发出卖出信号，注意获利了结")
        
        if risk_warnings:
            recommendations.append("风险提示增多，建议控制仓位")
        
        if not recommendations:
            recommendations.append("市场观点分散，建议谨慎操作，等待明确信号")
        
        return "\n".join(recommendations)
    
    def run_full_workflow(self, target_date: str = None):
        """
        运行完整工作流：采集 + 生成报告
        
        Args:
            target_date: 目标日期
        """
        self.logger.info("开始运行完整工作流")
        
        collection_result = self.run_daily_collection(target_date)
        
        if collection_result['success']:
            self.logger.info("采集完成，开始生成报告")
            report_result = self.generate_daily_report(target_date)
            
            return {
                'collection': collection_result,
                'report': report_result
            }
        else:
            self.logger.error("采集失败，跳过报告生成")
            return {
                'collection': collection_result,
                'report': None
            }


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='TGB量化数据采集系统')
    parser.add_argument('--mode', choices=['daily', 'weekend', 'full', 'report'],
                      default='full', help='运行模式')
    parser.add_argument('--date', type=str, default=None,
                      help='目标日期 (YYYY-MM-DD)')
    parser.add_argument('--config', type=str, default=None,
                      help='配置目录路径')
    
    args = parser.parse_args()
    
    system = QuantTgbSystem(args.config)
    
    if args.mode == 'daily':
        result = system.run_daily_collection(args.date)
    elif args.mode == 'weekend':
        result = system.run_weekend_collection(args.date)
    elif args.mode == 'report':
        result = system.generate_daily_report(args.date)
    else:
        result = system.run_full_workflow(args.date)
    
    print("\n执行结果:")
    print(result)


if __name__ == '__main__':
    main()
