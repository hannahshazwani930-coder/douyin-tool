# views/rewrite.py
import streamlit as st
from utils import load_isolated_css

def view_rewrite():
    # 🔒 锁定：强制加载 rewrite 专用独立样式
    load_isolated_css("rewrite")
    
    # 1. 顶部标题
    st.markdown("""
        <div class="flowing-header">
            <h1 style='margin:0; color:white;'>📝 文案改写</h1>
            <p style='margin:10px 0 0 0; opacity:0.9;'>AI 智能重构，让每一行字都具备传播力</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 2. 创作控制台
    with st.container():
        st.markdown('<div class="creation-console">', unsafe_allow_html=True)
        
        st.markdown('<span class="custom-label">输入原始内容</span>', unsafe_allow_html=True)
        source_text = st.text_area("source", placeholder="请粘贴您想要改写的文案...", height=150, label_visibility="collapsed")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<span class="custom-label">改写风格</span>', unsafe_allow_html=True)
            style = st.selectbox("style", ["爆款标题党", "走心深度感", "专业严谨风", "幽默吐槽类"], label_visibility="collapsed")
        
        with col2:
            st.markdown('<span class="custom-label">目标平台</span>', unsafe_allow_html=True)
            platform = st.selectbox("platform", ["抖音", "小红书", "视频号", "公众号"], label_visibility="collapsed")
            
        if st.button("🚀 开始 AI 改写", use_container_width=True):
            if source_text:
                with st.spinner("正在重构文案..."):
                    # 这里是您的 AI 逻辑处理处
                    st.success("改写完成！")
                    st.text_area("结果", value=f"【{style}风格】改写后的样本文案...", height=150)
            else:
                st.warning("请先输入内容")
                
        st.markdown('</div>', unsafe_allow_html=True)