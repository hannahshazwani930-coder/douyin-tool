# views/home.py
import streamlit as st
from utils import load_isolated_css

def view_home():
    # 🔒 锁定：强制加载首页专用 CSS 隔离文件
    load_isolated_css("home")
    
    # 1. 顶部横幅
    st.markdown("""
        <div class="home-header-card">
            <div class="header-title">欢迎使用 抖音爆款工场</div>
            <div class="header-sub">系统已进入“模块化隔离”锁定状态，所有格式均已独立存储。</div>
        </div>
    """, unsafe_allow_html=True)
    
    # 2. 项目展示区 (替代原有的 render_project_card 函数)
    st.markdown('<div class="section-label">推荐工具箱</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    # 模拟原来的项目卡片
    card_html = """
    <div class="feature-card-pro">
        <div class="feat-icon">{icon}</div>
        <div class="feat-title">{title}</div>
        <div class="feat-desc">{desc}</div>
        <div style="margin-top:10px; font-size:12px; color:#2563eb; font-weight:600;">点击侧边栏开始使用</div>
    </div>
    """

    with col1:
        st.markdown(card_html.format(icon="🏷️", title="账号起名", desc="智能匹配行业属性，生成高辨识度 ID"), unsafe_allow_html=True)
    
    with col2:
        st.markdown(card_html.format(icon="🎨", title="海报生成", desc="专业级封面模板，提升视频点击率"), unsafe_allow_html=True)
