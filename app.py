import streamlit as st
from openai import OpenAI

# --- 1. 密钥配置 (依然要去 Secrets 里填好 DEEPSEEK_API_KEY) ---
try:
    api_key = st.secrets["DEEPSEEK_API_KEY"]
except:
    st.error("请先在 Settings -> Secrets 里填入 DEEPSEEK_API_KEY")
    st.stop()

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

# --- 2. 核心：爆款改写逻辑 ---
def rewrite_viral_script(content):
    prompt = f"""
    你是一个抖音千万粉的口播博主，最擅长把别人的文案改成“原创爆款”。
    
    【原始素材】：
    {content}
    
    【你的任务】：
    请对上述素材进行“洗稿”和“升维”，必须遵守以下“爆款公式”：
    1. **黄金3秒钩子**：开头必须用一句反直觉、引发焦虑或极度好奇的话。（例如：“千万别再...”、“我这辈子最后悔的...”），严禁使用“大家好”！
    2. **说人话**：把所有书面语改成大白话，多用短句。语气要像在跟闺蜜/兄弟聊天，带点情绪（惊讶、生气、无奈）。
    3. **情绪递进**：中间要有反转，或者痛点刺激。
    4. **结尾引导**：最后必须引导点赞或评论（例如：“如果是你，你会怎么做？评论区告诉我”）。
    
    【输出格式】：
    直接输出改写后的文案，不要任何解释。字数控制在200字左右，适合40秒口播。
    """
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=1.3, # 稍微调高创造性，避免查重
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"生成出错：{e}"

# --- 3. 极简页面布局 ---
st.set_page_config(page_title="🔥 爆款洗稿机", layout="wide")

st.title("⚡️ 抖音爆款文案 · 暴力改写版")
st.markdown("把别人的爆款文案/分享链接文字粘贴在左边，右边直接出原创脚本。")

col1, col2 = st.columns(2)

with col1:
    st.header("1️⃣ 丢素材 (支持批量)")
    # 允许用户输入一大段文本
    raw_text = st.text_area("直接粘贴复制来的文案 (每条素材中间空一行)", height=500, placeholder="粘贴示例：\n\n链接1的文案...\n\n---\n\n链接2的文案...")
    
    start_btn = st.button("🚀 开始暴力改写", type="primary")

with col2:
    st.header("2️⃣ 拿结果")
    if start_btn and raw_text:
        # 简单按空行分割，支持一次改写多条
        scripts = raw_text.split('\n\n') 
        
        for i, script in enumerate(scripts):
            if len(script.strip()) > 5: # 过滤掉太短的空行
                with st.spinner(f"正在改写第 {i+1} 条..."):
                    new_script = rewrite_viral_script(script)
                    st.success(f"✅ 第 {i+1} 条改写完成")
                    st.text_area(f"文案 #{i+1}", value=new_script, height=200)
                    st.markdown("---")
    elif start_btn:
        st.warning("你还没粘贴素材呢！")
