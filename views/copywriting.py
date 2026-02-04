# views/copywriting.py
import streamlit as st

def view_copywriting():
    st.markdown("### ✍️ 文案创作中心")
    st.write("DeepSeek 高质量改文引擎已就绪")
    
    with st.container(border=True):
        text_input = st.text_area("输入原始文案", height=200)
        if st.button("开始 AI 重构", type="primary"):
            st.info("正在调用 DeepSeek-V3 接口...")
