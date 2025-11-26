import os
import feedparser
import requests
import datetime
from openai import OpenAI

# ======================================================
import os  # 确保导入了 os 模块
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
# 引入 requests 库 (如果没有引入，记得在文件最上面写 import requests)
import requests
import feedparser

def get_game_news():
    """获取 Epic 资讯 (国内镜像直连版)"""
    
    # 目标：RSSHub 的国内镜像源 (Epic 喜加一)
    # 这个源通常在国内可以直接访问，不需要梯子
    rss_url = "https://rsshub.rssforever.com/epicgames/freegames"
    
    print("👻 正在连接 Epic 镜像源 (直连模式)...")

    # 伪装头
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    try:
        # 1. timeout 改成 30 秒
        # 2. verify=False 关闭证书验证 (防止报错)
        # 3. 去掉了 proxies 参数，尝试直连
        response = requests.get(rss_url, headers=headers, timeout=30, verify=False)
        
        if response.status_code != 200:
             print(f"❌ 请求失败，状态码: {response.status_code}")
             return []

        feed = feedparser.parse(response.content)

        if len(feed.entries) == 0:
            print("❌ 获取成功但内容为空。")
            return []
            
        print(f"✅ 成功拿到 {len(feed.entries)} 条游戏资讯！")
        
        # ... (下面的数据处理逻辑不用变) ...
        news_data = []
        for entry in feed.entries[:3]:
             title = entry.title
             link = entry.link
             # 这里的 summary 处理可能需要根据 RSSHub 的格式微调，先保持原样试试
             summary = entry.summary if 'summary' in entry else ""
             summary = summary.replace("<p>", "").replace("</p>", "").replace("&nbsp;", "")
             news_data.append(f"🎮 {title}\n🔗 {link}\n📝 {summary[:100]}...") 
        
        return news_data

    except Exception as e:
        print(f"❌ 依然报错: {e}")
        print("💡 绝望建议：如果还不行，请用浏览器打开上面的 rss_url 看看能不能开？")
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
    “你是一个挑剔的懂规矩、极其谨慎的游戏省钱博主。
我会给你最新的 GamerPower 游戏限免简讯。
请执行以下逻辑：
筛选： 只保留 'Epic Games Store' 或 'Steam' 平台的完整游戏 (Full Game) 免费信息。
过滤： 如果是 DLC、皮肤(Skin)、试玩版(Demo) 或者不知名的小平台（比如 Itch.io），直接忽略，不要输出任何内容。
撰写文案： 如果发现了符合条件的 Epic/Steam 喜加一，请写一篇小红书文案：
标签： #喜加一  #游戏推荐
请根据我提供的游戏信息，写一篇小红书文案。
⚠️ 核心禁忌（绝对不能犯）：
严禁出现 ‘链接’、‘网址’、‘点击领取’、‘访问官网’、‘Epic Games Store’ (全名) 等字眼。
严禁引导 用户跳出小红书APP。
✅ 必须执行的‘黑话’策略：
把 ‘Epic’ 称为 ‘E宝’ 或 ‘那个E开头的平台’。
把 ‘Steam’ 称为 ‘G胖家’ 或 ‘蒸汽平台’。
领取方式要写： ‘懂的都懂’ 或 ‘老地方见’ 或 ‘直接去E宝看一眼就有’。
文案结构：
标题： 只有Emoji和游戏名，比如 ‘🤫嘘！E宝这周送《[游戏名]》了！’
正文：
第一段：直接夸游戏好玩在哪（原本要几十块，现在0圆）。
第二段：强调截止时间（手慢无）。
结尾：‘关注我，每周提醒，不错过任何一个大作！’
请确保文案看起来像是一个真实玩家在分享喜悦，而不是在发广告。”
    
    新闻素材：
    {combined_content}
    """

    try:
        completion = client.chat.completions.create(
            # 👇 关键修改：换成了 32k 模型，容量更大
            model="moonshot-v1-32k", 
            messages=[
                {"role": "system", "content": "你是挑剔的游戏省钱博主。"},
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
    raw_news = get_game_news()
    if raw_news:
        summary = generate_briefing(raw_news)
        if summary:
            summary = summary.replace("```html", "").replace("```", "")
            push_to_wechat(summary)
            print("\n--- 预览内容 ---\n", summary)