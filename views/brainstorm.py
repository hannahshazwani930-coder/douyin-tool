# views/brainstorm.py
import streamlit as st
from utils import load_isolated_css

def view_brainstorm():
    load_isolated_css("brainstorm") # 🔒 锁定选题页专属样式
    
    st.markdown('<div class="page-header">💡 爆款选题</div>', unsafe_allow_html=True)
    st.info("正在实时追踪当前全网热门话题...")
    
    # 简单的选题列表逻辑
    topics = ["2026年AI行业预测", "普通人如何抓住短视频红利", "职场避坑指南"]
    for t in topics:
        with st.expander(f"📌 选题：{t}"):
            st.write("建议拍摄方向：对比法、反转法...")