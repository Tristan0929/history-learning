# -*- coding: utf-8 -*-
"""
历史学习助手 · 后端(极简转发)
作用:把前端请求转发给 DeepSeek 等 OpenAI 兼容服务商,解决浏览器直连的跨域(CORS)问题。
- 不存储、不记录用户的 API Key(仅在本次请求内用于转发)。
- 密钥来源:优先用前端传来的 key;若前端没传,则用环境变量 DEEPSEEK_API_KEY(可选)。
"""
import os
import json
import requests
from flask import Flask, request, Response, send_from_directory

app = Flask(__name__, static_folder=".", static_url_path="")


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True, silent=True) or {}
    base = (data.get("base") or "https://api.deepseek.com").rstrip("/")
    model = data.get("model") or "deepseek-v4-flash"
    messages = data.get("messages") or []
    key = data.get("key") or os.environ.get("DEEPSEEK_API_KEY", "")

    if not key:
        return Response(
            json.dumps({"error": "缺少 API Key(请在网页右上角⚙设置中填写)"}, ensure_ascii=False),
            status=400, mimetype="application/json",
        )

    payload = {
        "model": model,
        "messages": messages,
        "stream": True,
        "temperature": float(data.get("temperature", 0.4)),
    }

    try:
        upstream = requests.post(
            base + "/chat/completions",
            headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
            json=payload, stream=True, timeout=300,
        )
    except requests.RequestException as e:
        return Response(
            json.dumps({"error": "无法连接服务商:" + str(e)}, ensure_ascii=False),
            status=502, mimetype="application/json",
        )

    def generate():
        for chunk in upstream.iter_content(chunk_size=None):
            if chunk:
                yield chunk

    ctype = upstream.headers.get("Content-Type", "text/event-stream")
    return Response(generate(), status=upstream.status_code, content_type=ctype)


@app.route("/healthz")
def healthz():
    return "ok"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
