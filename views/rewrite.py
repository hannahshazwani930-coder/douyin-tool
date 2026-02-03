import streamlit as st
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor
from utils import render_copy_btn

def view_rewrite():
    st.markdown("### 📝 爆款文案改写")
    st.caption("基于 DeepSeek V3 模型，智能清洗重组文案结构")
    
    api_key = st.secrets.get("DEEPSEEK_API_KEY", "")
    client = None
    if api_key:
        try: client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        except: pass
    
    if not client: st.warning("⚠️ 未配置 API Key，系统将运行在演示模式")

    def process_text(text):
        if not client: return "【演示模式】请配置 API Key。\n模拟结果：这是改写后的爆款文案..."
        if len(text) < 5: return "❌ 文案太短"
        try:
            prompt = f"你是一个抖音千万粉博主。请将以下文案改写为爆款口播文案，要求：黄金3秒开头，情绪饱满，结尾强引导。原文：{text}"
            res = client.chat.completions.create(model="deepseek-chat", messages=[{"role":"user", "content":prompt}], temperature=1.3)
            return res.choices[0].message.content
        except Exception as e: return f"API Error: {str(e)}"

    c1, c2 = st.columns([1, 2])
    with c1:
        st.info("💡 提示：将竞品文案粘贴在下方，点击按钮批量生成。")
        if st.button("🚀 5路并发执行", type="primary", use_container_width=True):
            inputs = [st.session_state.get(f"in_{i}", "") for i in range(1,6)]
            valid_inputs = [(i+1, txt) for i, txt in enumerate(inputs) if txt.strip()]
            
            if not valid_inputs: st.toast("请至少输入一条文案")
            else:
                with st.status("正在极速改写中...", expanded=True):
                    with ThreadPoolExecutor(max_workers=5) as executor:
                        futures = {executor.submit(process_text, txt): idx for idx, txt in valid_inputs}
                        for future in futures:
                            idx = futures[future]
                            st.session_state[f"out_{idx}"] = future.result()
                    st.rerun()

    for i in range(1, 6):
        with st.container(border=True):
            st.markdown(f"**工作台 #{i}**")
            col_in, col_out = st.columns([1, 1], gap="medium")
            with col_in:
                st.text_area(f"原始文案 #{i}", key=f"in_{i}", height=150, placeholder="粘贴文案...", label_visibility="collapsed")
            with col_out:
                res = st.session_state.get(f"out_{i}", "")
                if res:
                    st.text_area(f"结果 #{i}", value=res, height=150, key=f"area_out_{i}", label_visibility="collapsed")
                    render_copy_btn(res, f"cp_{i}")
                else:
                    st.markdown("<div style='height:150px; display:flex; align-items:center; justify-content:center; color:#cbd5e1; border:1px dashed #e2e8f0; border-radius:8px;'>等待生成...</div>", unsafe_allow_html=True)