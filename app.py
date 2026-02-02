import streamlit as st
from openai import OpenAI

# --- 1. 密钥配置 ---
try:
    api_key = st.secrets["DEEPSEEK_API_KEY"]
except:
    st.error("请先在 Settings -> Secrets 里填入 DEEPSEEK_API_KEY")
    st.stop()

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

# --- 2. 核心：爆款改写逻辑 (保持不变) ---
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
    4. **结尾引导**：最后必须引导点赞或评论。
    
    【输出格式】：
    直接输出改写后的文案，不要任何解释。字数控制在200字左右。
    """
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=1.3, 
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"生成出错：{e}"

# --- 3. 页面布局 (已改为双窗口模式) ---
st.set_page_config(page_title="🔥 双管齐下改写机", layout="wide")

st.title("⚡️ 抖音爆款文案 · 双窗口独立版")

# 创建左右两列：左边输入，右边输出
col1, col2 = st.columns([1, 1]) # 1:1 比例

with col1:
    st.header("1️⃣ 丢素材 (输入)")
    
    # --- 窗口 A ---
    st.subheader("📝 素材 A")
    # height=300 让窗口默认变得很高
    input_a = st.text_area("粘贴第1个文案/链接内容", height=300, key="input_a", placeholder="在这里粘贴文案 A...")
    
    st.markdown("---") # 分割线
    
    # --- 窗口 B ---
    st.subheader("📝 素材 B")
    input_b = st.text_area("粘贴第2个文案/链接内容", height=300, key="input_b", placeholder="在这里粘贴文案 B...")
    
    # 按钮放在最下面
    start_btn = st.button("🚀 同时改写 A 和 B", type="primary", use_container_width=True)

with col2:
    st.header("2️⃣ 拿结果 (输出)")
    
    if start_btn:
        # 既然是分开的，我们就分别处理
        if not input_a and not input_b:
            st.warning("⚠️ 两个窗口都是空的，你没给我素材呀！")
        
        # 处理 A
        if input_a:
            with st.spinner("正在改写素材 A..."):
                res_a = rewrite_viral_script(input_a)
                st.success("✅ 素材 A 改写完成")
                st.text_area("🔥 爆款文案 A (直接复制)", value=res_a, height=250)
        
        # 如果 A 和 B 都有，加个分割线好看点
        if input_a and input_b:
            st.markdown("---")
            
        # 处理 B
        if input_b:
            with st.spinner("正在改写素材 B..."):
                res_b = rewrite_viral_script(input_b)
                st.success("✅ 素材 B 改写完成")
                st.text_area("🔥 爆款文案 B (直接复制)", value=res_b, height=250)
