import streamlit as st
from openai import OpenAI
from utils import render_copy_btn

def view_naming():
    st.markdown("### 🏷️ 账号/IP 起名大师")
    st.caption("AI 结合玄学与算法，为你定制最吸粉的账号 ID")
    
    c1, c2 = st.columns(2)
    with c1: niche = st.selectbox("🎯 赛道", ["短剧", "小说", "口播", "情感", "带货", "Vlog"])
    with c2: style = st.selectbox("🎨 风格", ["高冷", "搞笑", "文艺", "粗暴", "反差", "玄学"])
    keywords = st.text_input("🔑 关键词 (选填)", placeholder="例如：暴富、逆袭、清醒...")
    
    if st.button("🎲 生成名字", type="primary", use_container_width=True):
        api_key = st.secrets.get("DEEPSEEK_API_KEY", "")
        if not api_key: st.error("请配置 API Key")
        else:
            client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
            prompt = f"为【{niche}】赛道生成10个{style}风格账号名，含关键词：{keywords}。格式：1. 名字+解释。"
            try:
                with st.spinner("生成中..."):
                    res = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}], temperature=1.5)
                    st.session_state['naming_result'] = res.choices[0].message.content
            except Exception as e: st.error(str(e))
            
    if 'naming_result' in st.session_state:
        st.text_area("结果", value=st.session_state['naming_result'], height=400)
        render_copy_btn(st.session_state['naming_result'], "naming_res_copy")