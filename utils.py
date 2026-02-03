import streamlit as st
import streamlit.components.v1 as components
import os

def load_isolated_css(page_name):
    """🔐 核心隔离加载器"""
    # 加载基础
    base_path = os.path.join("styles", "base.css")
    if os.path.exists(base_path):
        with open(base_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # 加载页面特定样式
    page_css_path = os.path.join("styles", f"{page_name}.css")
    if os.path.exists(page_css_path):
        with open(page_css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def render_wechat_pill(title, wx_id):
    """渲染微信领取组件"""
    html = f"""
    <div style="padding:10px; background:#f0f2f6; border-radius:10px; text-align:center;">
        <small>{title}</small><br><b>微信：{wx_id}</b>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
