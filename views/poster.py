# views/poster.py
import streamlit as st
from utils import load_isolated_css

def view_poster():
    load_isolated_css("poster") # 🔒 锁定海报页专属样式
    
    st.markdown('<div class="page-header">🎨 海报生成</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.file_uploader("上传背景图")
    with col2:
        st.text_input("主标题文案")
        st.color_picker("字体颜色", "#FFFFFF")
        
    st.button("🖼️ 一键生成海报", use_container_width=True)