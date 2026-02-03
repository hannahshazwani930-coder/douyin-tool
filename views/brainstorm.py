# views/brainstorm.py
import streamlit as st
from utils import load_isolated_css

def view_brainstorm():
    # 🔒 锁定：加载选题页专属样式
    load_isolated_css("brainstorm")
    
    st.markdown("""
        <div class="page-header">
            <h1 style='margin:0; color:#1e293b;'>💡 爆款选题</h1>
            <p style='margin:5px 0 0 0; color:#64748b;'>实时追踪全网流量高地，挖掘最具传播力的创作方向</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 创作容器
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("行业赛道", ["知识干货", "剧情反转", "美妆穿搭", "美食探店"])
        with col2:
            st.selectbox("目标人群", ["职场人士", "大学生", "宝妈", "创业者"])
            
        if st.button("🔥 生成深度选题方案", use_container_width=True):
            st.divider()
            st.success("已为您生成 3 个高转化潜力选题：")
            st.info("1. **对比法**：XX行业不为人知的内幕 vs 表面光鲜")
            st.info("2. **清单法**：普通人入局XX必看的 5 个建议")
            st.info("3. **反直觉**：为什么你越努力在XX，反而越赚不到钱？")
        st.markdown('</div>', unsafe_allow_html=True)
