# 历史学习助手 · 部署说明

一个整合了五个历史学习工具(章节笔记 / 材料题陪练 / 中外贯通 / 小论文陪练 / 辨析检查)的网页应用。
前端是单个 `index.html`;后端 `app.py` 是一个极简转发服务,用来解决浏览器直连大模型的跨域(CORS)问题,并让网站可以公开部署。

- 默认接入 **DeepSeek**(可在网页里切换 OpenAI / Kimi / 智谱 / 自定义)。
- **API Key 不会被服务器存储或记录**,仅在每次请求中用于转发。
- 支持流式回复、五色批注渲染、一键导出美观 PDF。

---

## 一、文件说明

| 文件 | 作用 |
| --- | --- |
| `index.html` | 前端页面(全部界面与逻辑) |
| `app.py` | 后端转发服务(Flask) |
| `requirements.txt` | Python 依赖 |
| `render.yaml` | Render 部署配置(可选,自动化用) |
| `.gitignore` | Git 忽略项 |

---

## 二、本地先跑一遍(可选,建议先测)

需要电脑装了 Python 3.10+。在本文件夹里打开终端:

```bash
pip install -r requirements.txt
python app.py
```

然后浏览器打开 `http://localhost:5000` ,右上角 ⚙ 设置里填入你的 DeepSeek API Key 即可使用。

---

## 三、部署到 GitHub + Render(公开网站)

### 第 1 步:把代码放到 GitHub

1. 登录 <https://github.com> → 右上角 **+** → **New repository**。
2. 仓库名填 `history-study-helper`(随意),选 **Public**,不要勾选 "Add a README"(我们已有),点 **Create repository**。
3. 在新仓库页点 **uploading an existing file**(或 Add file → Upload files)。
4. 把本文件夹里的 **全部文件**(`index.html`、`app.py`、`requirements.txt`、`render.yaml`、`.gitignore`、`README.md`)拖进去,点 **Commit changes**。

### 第 2 步:在 Render 上部署

1. 登录 <https://dashboard.render.com> → **New +** → **Web Service**。
2. 连接你的 GitHub 账号,选择刚才那个仓库。
3. 关键设置(如果 Render 没自动读取 `render.yaml`,就手动填):
   - **Language / Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --timeout 300 --workers 1 --threads 8`
   - **Instance Type**: `Free`
4. 点 **Create Web Service**,等几分钟构建完成。
5. 部署好后会得到一个网址(形如 `https://history-study-helper.onrender.com`),打开它,在 ⚙ 设置里填 Key 即可对外使用。

### (可选)让所有访问者共用你的密钥

如果你想让别人不填 Key 也能用(**费用由你承担,注意成本与滥用风险**):
在 Render 服务的 **Environment** 里新增变量 `DEEPSEEK_API_KEY` = 你的密钥。
不设置时,默认每个访问者用自己填的 Key。

---

## 四、几点如实说明

- **免费版 Render 会休眠**:超过约 15 分钟无访问会休眠,下次打开需等约 30 秒冷启动,属正常现象。
- **准确性**:AI 可能记错史实且语气自信。本工具已内置"依据教材、不确定要标注"等约束,但硬史实请以教材为准;最佳用法是先自己想/写,再让它检查。
- **成本**:DeepSeek 价格很低,个人使用通常每月几毛到几块钱;若开放给很多人共用你的 Key,请留意用量。
