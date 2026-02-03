# views/naming.py
import streamlit as st
from utils import load_isolated_css

def view_naming():
    load_isolated_css("naming") # 🔒 锁定命名页专属样式
    
    st.markdown('<div class="page-header">🏷️ 账号起名</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        keyword = st.text_input("输入核心关键词（如：美食、穿搭）")
        target = st.selectbox("受众群体", ["宝妈", "职场新人", "学生", "高净值人群"])
        
        if st.button("✨ 生成爆款账号名", use_container_width=True):
            st.success(f"根据“{keyword}”为“{target}”生成的起名建议如下...")
        st.markdown('</div>', unsafe_allow_html=True)