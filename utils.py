# utils.py
import streamlit as st
import os

def load_isolated_css(page_name):
    """
    🔐 核心隔离加载器
    逻辑：只加载 base.css 和 指定页面的 .css
    """
    # 1. 加载基础样式
    base_path = os.path.join("styles", "base.css")
    if os.path.exists(base_path):
        with open(base_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # 2. 加载页面特定样式 (绝对隔离)
    page_css_path = os.path.join("styles", f"{page_name}.css")
    if os.path.exists(page_css_path):
        with open(page_css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        # 如果文件不存在，静默处理，不报错，不影响其他页面
        pass

# ... 保留您原有的 render_sidebar_user_card 等工具函数 ...
