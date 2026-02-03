# views/admin.py
import streamlit as st
from utils import load_isolated_css

def view_admin():
    load_isolated_css("admin") # 🔒 锁定样式
    
    st.markdown("### 🕵️‍♂️ 系统管理后台")
    
    # 模拟数据统计
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="stat-card"><small>总用户数</small><div class="stat-value">1,280</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stat-card"><small>今日注册</small><div class="stat-value">42</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="stat-card"><small>激活卡密数</small><div class="stat-value">856</div></div>', unsafe_allow_html=True)
    
    st.write("")
    tab1, tab2 = st.tabs(["🎫 卡密管理", "📢 系统公告"])
    with tab1:
        st.button("➕ 生成新卡密")
        st.table({"卡密": ["VIP-888", "VIP-999"], "天数": [30, 365], "状态": ["未使用", "已使用"]})
