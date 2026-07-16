#!/bin/bash
# 高考数学试卷 Web 浏览器 - 启动脚本
cd "$(dirname "$0")"

echo "======================================"
echo "  高考数学试卷浏览器"
echo "======================================"
echo ""

# 检查 Python3
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未找到 python3，请先安装 Python 3"
    exit 1
fi

# 进入 web 目录
cd web

# 安装依赖
echo "[1/2] 安装依赖..."
pip3 install -r requirements.txt -q 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[警告] pip3 安装失败，尝试 pip..."
    pip install -r requirements.txt -q
fi

echo "[2/2] 启动服务..."
echo ""
echo "  浏览器访问: http://localhost:5001"
echo "  按 Ctrl+C 停止服务"
echo ""

python3 app.py
