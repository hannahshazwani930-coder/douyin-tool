# views/poster.py
import streamlit as st
from utils import load_isolated_css

def view_poster():
    # 🔒 锁定：强制加载海报页专用隔离样式
    load_isolated_css("poster")
    
    # 1. 页面标题
    st.markdown("""
        <div class="poster-header">
            <h1 style='margin:0; color:white;'>🎨 海报生成器</h1>
            <p style='margin:5px 0 0 0; opacity:0.9;'>专业级爆款视频封面，一键合成锁定风格</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 2. 交互控制区
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.markdown('<div class="poster-container">', unsafe_allow_html=True)
        st.subheader("🛠️ 配置参数")
        
        bg_image = st.file_uploader("上传背景底图", type=['png', 'jpg', 'jpeg'])
        title_text = st.text_input("主标题文字", placeholder="例如：月入过万的秘密")
        font_color = st.color_picker("文字颜色", "#FFFFFF")
        font_size = st.slider("文字大小", 20, 100, 50)
        
        if st.button("🚀 开始合成海报", use_container_width=True):
            st.toast("正在调用渲染引擎...")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_right:
        st.subheader("🖼️ 实时预览")
        # 这里是样式的“物理锁定”体现，预览框由 CSS 强制定义
        st.markdown(f"""
            <div class="preview-box">
                <div style="color:{font_color}; font-size:{font_size}px; font-weight:bold; text-align:center;">
                    {title_text if title_text else "预览文字将在此处显示"}
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.caption("注：预览效果受 styles/poster.css 锁定控制。")
