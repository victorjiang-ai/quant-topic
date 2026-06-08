#!/bin/bash

# TGB量化数据采集系统 - 自动化运行脚本
# 用于定时执行每日采集和报告生成

# 配置区域
PROJECT_DIR="/Users/victorjiang/Documents/Software/quant_data/projects/tgb_data"
PYTHON_PATH="/usr/bin/python3"
LOG_FILE="$PROJECT_DIR/logs/automation.log"

# 创建日志目录
mkdir -p "$PROJECT_DIR/logs"

# 日志函数
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 切换到项目目录
cd "$PROJECT_DIR"

# 检查Python环境
if [ ! -f "$PYTHON_PATH" ]; then
    PYTHON_PATH="python3"
fi

# 检查依赖
check_dependencies() {
    log_message "检查依赖包..."
    
    $PYTHON_PATH -c "import yaml" 2>/dev/null
    if [ $? -ne 0 ]; then
        log_message "缺少 pyyaml，正在安装..."
        pip3 install pyyaml
    fi
    
    $PYTHON_PATH -c "import jinja2" 2>/dev/null
    if [ $? -ne 0 ]; then
        log_message "缺少 jinja2，正在安装..."
        pip3 install jinja2
    fi
}

# 获取当前日期信息
get_day_info() {
    DAY_OF_WEEK=$(date +%u)  # 1=Monday, 7=Sunday
    
    if [ $DAY_OF_WEEK -eq 6 ]; then
        echo "saturday"
    elif [ $DAY_OF_WEEK -eq 7 ]; then
        echo "sunday"
    elif [ $DAY_OF_WEEK -eq 5 ]; then
        echo "friday"
    else
        echo "weekday"
    fi
}

# 运行每日采集
run_daily_collection() {
    log_message "=== 开始每日采集 ==="
    $PYTHON_PATH "$PROJECT_DIR/main.py" --mode daily --date "$1"
    log_message "=== 每日采集完成 ==="
}

# 运行周末采集
run_weekend_collection() {
    log_message "=== 开始周末采集 ==="
    $PYTHON_PATH "$PROJECT_DIR/main.py" --mode weekend
    log_message "=== 周末采集完成 ==="
}

# 运行报告生成
run_report_generation() {
    log_message "=== 开始生成报告 ==="
    $PYTHON_PATH "$PROJECT_DIR/main.py" --mode report --date "$1"
    log_message "=== 报告生成完成 ==="
}

# 运行完整流程
run_full_workflow() {
    log_message "=== 开始完整工作流 ==="
    $PYTHON_PATH "$PROJECT_DIR/main.py" --mode full --date "$1"
    log_message "=== 完整工作流完成 ==="
}

# 主流程
main() {
    log_message "=========================================="
    log_message "TGB量化数据采集系统自动化运行"
    log_message "=========================================="
    
    check_dependencies
    
    DAY_TYPE=$(get_day_info)
    log_message "今天是: $DAY_TYPE"
    
    case $DAY_TYPE in
        "weekday")
            log_message "执行工作日流程"
            TARGET_DATE=$(date -v-1d +%Y-%m-%d)
            run_full_workflow "$TARGET_DATE"
            ;;
        "friday")
            log_message "执行周五流程（含周末预览）"
            TARGET_DATE=$(date +%Y-%m-%d)
            run_full_workflow "$TARGET_DATE"
            ;;
        "saturday")
            log_message "执行周六流程（周末汇总）"
            run_weekend_collection
            ;;
        "sunday")
            log_message "执行周日流程（周末汇总）"
            run_weekend_collection
            ;;
        *)
            log_message "执行默认流程"
            TARGET_DATE=$(date -v-1d +%Y-%m-%d)
            run_full_workflow "$TARGET_DATE"
            ;;
    esac
    
    log_message "=========================================="
    log_message "自动化运行结束"
    log_message "=========================================="
}

# 命令行参数处理
case $1 in
    "daily")
        log_message "执行每日采集"
        run_daily_collection "$(date -v-1d +%Y-%m-%d)"
        ;;
    "weekend")
        log_message "执行周末采集"
        run_weekend_collection
        ;;
    "report")
        log_message "生成报告"
        run_report_generation "$(date -v-1d +%Y-%m-%d)"
        ;;
    "full")
        log_message "执行完整工作流"
        run_full_workflow "$(date -v-1d +%Y-%m-%d)"
        ;;
    *)
        main
        ;;
esac
