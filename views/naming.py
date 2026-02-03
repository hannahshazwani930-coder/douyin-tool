# views/naming.py
import streamlit as st
from utils import load_isolated_css

def view_naming():
    # 🔒 锁定：加载起名页专用隔离样式
    load_isolated_css("naming")
    
    # 1. 页面头部
    st.markdown("""
        <div class="naming-header">
            <h1 style='margin:0; color:white;'>🏷️ 账号起名工具</h1>
            <p style='margin:10px 0 0 0; opacity:0.9;'>基于行业调性与传播算法，定制您的爆款 ID</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 2. 控制台
    with st.container():
        st.markdown('<div class="control-card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            keyword = st.text_input("🎯 核心关键词", placeholder="例如：美妆、职场、探店")
            style = st.selectbox("🎭 起名风格", ["专业权威型", "幽默接地气", "文艺治愈系", "高端极简风"])
            
        with col2:
            target = st.text_input("👥 目标人群", placeholder="例如：大学生、宝妈、老板")
            length = st.select_slider("📏 名字长度限制", options=["短(2-4字)", "中(4-6字)", "长(6字以上)"], value="中(4-6字)")
            
        if st.button("🚀 开始 AI 智能起名", use_container_width=True):
            if keyword:
                with st.spinner("AI 正在深度检索爆款词库..."):
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    st.markdown('<h4 style="margin-top:0; color:#065f46;">✨ 推荐起名方案</h4>', unsafe_allow_html=True)
                    
                    # 模拟生成结果
                    names = [f"{keyword}小百科", f"最懂{target}的{keyword}", f"阿{keyword}说{target}"]
                    for name in names:
                        st.markdown(f'<div class="name-item"><span>{name}</span><small style="color:#10b981;">爆款潜力 98%</small></div>', unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("请输入关键词后再尝试")
        
        st.markdown('</div>', unsafe_allow_html=True)
