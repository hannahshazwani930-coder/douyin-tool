import streamlit as st
from openai import OpenAI
import os

# --- 1. 收费门槛 (极简版) ---
# 只有输入正确密码才能看到后面的工具
# 这里的密码是 888888，你可以自己改
password = st.sidebar.text_input("🔑 请输入会员密码解锁", type="password")
if password != "888888":
    st.title("🔒 付费工具演示版")
    st.warning("这是内部提效工具，请输入密码后使用。")
    st.info("如需获取密码，请联系作者微信：XXX (此处写你的联系方式)")
    st.stop() # 密码不对，停止运行下面的代码

# --- 2. 核心功能代码 ---
# 从环境变量获取 API Key (为了安全，不要直接把Key写在代码里)
# 如果本地运行报错，请确保你设置了环境变量，或者临时在这里填入 Key
api_key = os.environ.get("DEEPSEEK_API_KEY") 
base_url = "https://api.deepseek.com"

if not api_key:
    st.error("❌ 未检测到 API Key，请在 Render 后台配置环境变量！")
    st.stop()

client = OpenAI(api_key=api_key, base_url=base_url)

def generate_script(title, summary, mood):
    prompt = f"""
    你是一个抖音口播博主。请根据剧情：{summary}，
    结合情绪：{mood}，写一个推书/推剧短视频文案。
    要求：开头3秒必须有反转，多用口语，结尾留悬念。
    """
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI 报错：{e}"

# --- 3. 页面布局 ---
st.title("🚀 爆款文案生成器 (VIP版)")

title = st.text_input("剧名/书名")
mood = st.selectbox("情绪基调", ["震惊", "愤怒", "感动", "爽文"])
summary = st.text_area("剧情简介", height=150)

if st.button("生成文案"):
    if not title or not summary:
        st.warning("请填写完整信息")
    else:
        with st.spinner("AI 正在思考..."):
            result = generate_script(title, summary, mood)
            st.success("生成成功！")
            st.text_area("结果", value=result, height=300)