#!/bin/bash

echo "========================================="
echo "  Engine Logs 分析工具"
echo "========================================="
echo ""

if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3，请先安装 Python3"
    exit 1
fi

echo "正在安装依赖..."
pip3 install -r requirements.txt

echo ""
echo "正在启动应用..."
echo "应用将在 http://localhost:5000 运行"
echo "按 Ctrl+C 停止服务"
echo ""

python3 app.py
