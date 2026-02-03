# views/home.py
import streamlit as st
from utils import render_cta_wechat, render_home_project_card

def view_home():
    # 顶部欢迎语
    st.markdown("### 👋 欢迎来到抖音爆款工场 Pro")
    st.markdown("这里是您的全能创作工作台，请从左侧选择功能开始工作。", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # --- 核心项目切片 (Requirement 3) ---
    st.markdown("<div style='margin-bottom:15px; font-weight:600; color:#64748b;'>🔥 热门变现项目</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(render_home_project_card(
            "🤖", "御灵 AI 矩阵",
            "基于大模型的全自动矩阵托管系统。支持多账号批量发布、AI自动回复与粉丝互动，实现无人值守的流量变现。",
            "自动化 / 矩阵营销"
        ), unsafe_allow_html=True)
        
    with col2:
        st.markdown(render_home_project_card(
            "👥", "素人 KOC 孵化",
            "从零打造素人IP，提供全套人设定位、脚本库与拍摄指导。连接品牌方资源，实现快速商单变现。",
            "IP孵化 / 商单资源"
        ), unsafe_allow_html=True)
        
    with col3:
        st.markdown(render_home_project_card(
            "🌏", "文娱出海变现",
            "TikTok 短剧与游戏推广出海项目。提供海外热门素材、翻译工具及本地化运营策略，赚取美金收益。",
            "TikTok / 跨境电商"
        ), unsafe_allow_html=True)
        
    # --- 底部领取资料 (Requirement 3) ---
    # 调用 utils 里的高级 CTA 组件
    render_cta_wechat("W7774X")
