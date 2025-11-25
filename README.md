# 🤖 AI-News-Briefing | 全自动 AI 科技早报

> **基于 LLM 的零成本自动化情报系统**  
> **A Zero-cost Automated Intelligence System powered by Large Language Models**

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-Automated-green)
![LLM](https://img.shields.io/badge/Model-Kimi_(Moonshot)-purple)
![License](https://img.shields.io/badge/License-MIT-orange)

---

## 📖 Introduction | 项目简介

In the era of information explosion, filtering noise is more important than acquiring data.
**AI-News-Briefing** is a serverless automated bot designed for efficiency. It runs entirely on the cloud, automatically capturing the latest technological trends every morning, using the powerful **Kimi (Moonshot AI)** model for deep summarization and analysis, and pushing the "essence" directly to your WeChat. No server required, zero maintenance costs.

在信息爆炸的时代，过滤噪音比获取数据更重要。
**AI-News-Briefing** 是一个为效率而生的无服务器（Serverless）自动化机器人。它完全运行在云端，每天清晨自动捕获最新的科技动态，利用强大的 **Kimi（Moonshot AI）** 模型进行深度总结与分析，并将“精华”直接推送到你的微信。无需服务器，零维护成本，开箱即用。

---

## ✨ Features | 核心特性

- **🌐 Multi-source Aggregation (多源情报聚合)**  
  Automatically fetches data from mainstream tech RSS feeds (e.g., 36Kr, TechCrunch) to ensure information timeliness.  
  自动抓取主流科技媒体 RSS 源（如 36Kr），确保情报的时效性。

- **🧠 Deep AI Insight (深度 AI 洞察)**  
  Powered by the **Kimi LLM**, it doesn't just truncate text; it acts as a professional editor to summarize, comment, and organize content into HTML-formatted briefings.  
  接入 **Kimi 大模型**，拒绝简单的文本截断。它像一位专业主编，对新闻进行深度总结、犀利点评，并整理成排版精美的 HTML 简报。

- **☁️ Cloud-Native Automation (云端自动巡航)**  
  Leveraging **GitHub Actions**, the script runs on a scheduled cron job (UTC 0:00 / Beijing 8:00). No local computer needed.  
  依托 **GitHub Actions** 实现完全的云端托管，每天北京时间早 8 点准时自动运行，无需本地挂机。

- **📱 Instant Notification (多渠道直达)**  
  Integrated with **PushPlus**, delivering the briefing directly to WeChat.  
  集成 **PushPlus** 推送服务，早报直达微信，不错过任何重要信息。

---

## 🛠️ Tech Stack | 技术栈

- **Core Logic:** Python 3.9
- **LLM API:** OpenAI SDK (Connecting to Moonshot/Kimi)
- **Data Fetching:** Feedparser
- **CI/CD:** GitHub Actions
- **Notification:** PushPlus API

---

## 🚀 How to Use | 如何使用

You can deploy your own AI bot in 3 steps without writing any code.  
你只需三步，无需编写任何代码，即可部署属于你的 AI 机器人。

### 1. Fork this Repository (Fork 本项目)
Click the `Fork` button in the upper right corner to copy this project to your GitHub account.  
点击右上角的 `Fork` 按钮，将本项目复制到你的 GitHub 账号下。

### 2. Configure Secrets (配置密钥)
Go to `Settings` -> `Secrets and variables` -> `Actions` -> `New repository secret`. Add the following two secrets:  
进入项目的 `Settings` -> `Secrets and variables` -> `Actions` -> `New repository secret`，添加以下两个变量：

| Secret Name | Description | How to get |
| :--- | :--- | :--- |
| `KIMI_API_KEY` | Your Kimi API Key | [Moonshot Platform](https://platform.moonshot.cn/) |
| `PUSH_PLUS_TOKEN` | Your PushPlus Token | [PushPlus Official](http://www.pushplus.plus/) |

### 3. Enable Actions (激活自动化)
Go to the `Actions` tab, enable workflows if asked. You can manually trigger it once to test (`Run workflow`), or wait for the automatic schedule (8:00 AM Beijing Time).  
进入 `Actions` 页面，如果提示禁止，请点击启用。你可以手动点击 `Run workflow` 测试一次，或等待每天早 8 点自动运行。

---

## ⚠️ Disclaimer | 免责声明

- This project is for learning and research purposes only.  
- Please comply with the Terms of Service of the relevant APIs (Kimi, 36Kr, PushPlus).  
- The author is not responsible for any copyright disputes caused by the content fetched.  

- 本项目仅供学习和研究使用。
- 请遵守相关 API（Kimi, 36Kr, PushPlus）的服务条款。
- 抓取的内容版权归原作者所有，本项目不承担任何版权纠纷责任。

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/rongjiedu0-code">溶解度</a>
</p>
