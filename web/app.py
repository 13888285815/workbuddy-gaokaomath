"""高考数学试卷 Web 浏览器 - Flask 后端"""

import os
import json
from pathlib import Path
from flask import Flask, jsonify, send_file, render_template

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent  # workbuddy-gaokaomath 根目录
PDF_DIRS = ["普通高考", "春季高考"]


def build_tree():
    """构建完整目录树 JSON"""
    tree = []
    for category in PDF_DIRS:
        cat_path = BASE_DIR / category
        if not cat_path.is_dir():
            continue
        cat_node = {
            "name": category,
            "type": "category",
            "children": [],
            "count": 0,
        }
        years = sorted(
            [d for d in cat_path.iterdir() if d.is_dir()],
            key=lambda x: x.name,
            reverse=True,
        )
        for year_dir in years:
            pdfs = sorted(
                [f for f in year_dir.iterdir() if f.suffix.lower() == ".pdf"],
                key=lambda x: x.stem,
            )
            year_node = {
                "name": year_dir.name,
                "type": "year",
                "children": [],
                "count": len(pdfs),
            }
            for pdf in pdfs:
                rel_path = str(pdf.relative_to(BASE_DIR))
                year_node["children"].append({
                    "name": pdf.name,
                    "type": "file",
                    "path": rel_path,
                })
            cat_node["children"].append(year_node)
            cat_node["count"] += len(pdfs)
        tree.append(cat_node)
    return tree


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/tree")
def api_tree():
    tree = build_tree()
    return jsonify(tree)


@app.route("/api/pdf/<path:subpath>")
def api_pdf(subpath):
    """提供 PDF 文件流"""
    file_path = BASE_DIR / subpath
    if not file_path.exists() or file_path.suffix.lower() != ".pdf":
        return "Not Found", 404
    return send_file(str(file_path), mimetype="application/pdf")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
