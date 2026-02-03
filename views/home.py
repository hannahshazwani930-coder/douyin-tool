# views/home.py
import streamlit as st
from utils import load_isolated_css

def view_home():
    # 🔒 锁定：强制加载独立样式文件，实现格式锁定
    load_isolated_css("home")
    
    # --- 页面内容开始 ---
    # 顶部横幅 (样式已由 home.css 锁定)
    st.markdown("""
        <div class="home-header-card">
            <div class="header-title">抖音爆款工场 Pro</div>
            <div class="header-sub">模块化版本：格式已独立并锁定</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-label">创作中心</div>', unsafe_allow_html=True)
    
    # 使用原生 Streamlit 组件代替被删除的旧 utils 组件
    col1, col2 = st.columns(2)
    with col1:
        st.info("💡 **爆款选题**\n\n追踪实时热点，挖掘流量高地。")
        st.button("进入选题", key="home_brainstorm", use_container_width=True)
    with col2:
        st.success("🎨 **海报生成**\n\n专业模板，一键生成高点击率封面。")
        st.button("开始制作", key="home_poster", use_container_width=True)
