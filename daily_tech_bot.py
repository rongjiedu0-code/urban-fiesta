import os
import feedparser
import requests
import datetime
from openai import OpenAI

# =========================================================
# 👇 用户配置区域
# =========================================================
# import os  # 确保导入了 os 模块
# ... 其他导入 ...

# =========================================================
# 👇 修改部分：不再硬编码，而是从系统环境变量里读取
# =========================================================

# 获取 Kimi 的 Key (如果你最后用的是 Kimi)
# os.environ.get("变量名") 的意思是：去系统里找这个名字的变量，找不到就报错
KIMI_API_KEY = os.environ.get("KIMI_API_KEY")

# 获取 PushPlus Token
PUSH_PLUS_TOKEN = os.environ.get("PUSH_PLUS_TOKEN")

# 检查一下是否获取成功（调试用，GitHub日志里能看到，但不会泄露Key）
if not KIMI_API_KEY:
    print("❌ 错误：未找到 KIMI_API_KEY，请检查 GitHub Secrets 设置！")
if not PUSH_PLUS_TOKEN:
    print("❌ 错误：未找到 PUSH_PLUS_TOKEN，请检查 GitHub Secrets 设置！")

# =========================================================
# 下面的代码保持不变...

# =========================================================

def get_36kr_news():
    """从 36Kr RSS 获取新闻"""
    rss_url = "https://36kr.com/feed"
    print("📡 正在连接 36Kr RSS 源...")
    
    try:
        feed = feedparser.parse(rss_url)
        if len(feed.entries) == 0:
            print("❌ 获取失败，可能是网络问题。")
            return []
        
        news_data = []
        # 获取前 5 条 (减少一条，防止太长)
        for entry in feed.entries[:5]: 
            title = entry.title
            link = entry.link
            summary = entry.summary if 'summary' in entry else ""
            
            # --- ✂️ 关键修改：强制瘦身 ---
            # 去除 HTML 标签
            summary = summary.replace("<p>", "").replace("</p>", "").replace("&nbsp;", "")
            # 如果摘要超过 800 字，强制截断，只取前 800 字
            if len(summary) > 800:
                summary = summary[:800] + "..."
            # ---------------------------

            news_data.append(f"【标题】{title}\n【摘要】{summary}\n【链接】{link}")
            
        print(f"✅ 成功抓取 {len(news_data)} 条新闻。")
        return news_data
    except Exception as e:
        print(f"⚠️ RSS 抓取错误: {e}")
        return []

def generate_briefing(news_list):
    """调用 Kimi 生成早报"""
    if not news_list:
        return None

    print("🌙 正在呼叫 Kimi (32k大内存版) 进行总结...")
    
    client = OpenAI(
        api_key=KIMI_API_KEY,
        base_url="https://api.moonshot.cn/v1",
    )

    combined_content = "\n\n".join(news_list)
    
    prompt = f"""
    你是一位专业的科技新闻主编。
    请根据以下 36Kr 的新闻资讯，写一份“每日科技早报”。

    要求：
    1. 风格犀利、简洁，有商业洞察力。
    2. **必须输出 HTML 格式**（方便微信显示），但不要用 ```html 代码块包裹。
    3. 结构：
       - <h3>📅 今日科技风向</h3> (一句话总结)
       - <ul>
       - <li><b>新闻标题</b>：一句话核心摘要 <a href="链接">点击阅读</a></li>
       - </ul>
       - <p><i>(主编点评：挑选最重要的一条新闻进行简短点评)</i></p>
    
    新闻素材：
    {combined_content}
    """

    try:
        completion = client.chat.completions.create(
            # 👇 关键修改：换成了 32k 模型，容量更大
            model="moonshot-v1-32k", 
            messages=[
                {"role": "system", "content": "你是专业的科技新闻助手。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )
        
        result = completion.choices[0].message.content
        print("✅ Kimi 写作完成！")
        return result

    except Exception as e:
        print(f"❌ Kimi 调用失败: {e}")
        return None

def push_to_wechat(content):
    """推送到 PushPlus"""
    if not content:
        return

    print("🚀 正在推送到微信...")
    url = "http://www.pushplus.plus/send"
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    
    data = {
        "token": PUSH_PLUS_TOKEN,
        "title": f"科技早报 ({date_str})",
        "content": content,
        "template": "html"
    }
    
    try:
        resp = requests.post(url, json=data)
        if resp.json().get('code') == 200:
            print("🎉 推送成功！快看微信！")
        else:
            print(f"⚠️ 推送失败: {resp.text}")
    except Exception as e:
        print(f"⚠️ 网络错误: {e}")

if __name__ == "__main__":
    raw_news = get_36kr_news()
    if raw_news:
        summary = generate_briefing(raw_news)
        if summary:
            summary = summary.replace("```html", "").replace("```", "")
            push_to_wechat(summary)
            print("\n--- 预览内容 ---\n", summary)
