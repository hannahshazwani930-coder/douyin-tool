# views/home.py
import streamlit as st
from utils import render_cta_wechat, render_home_project_card, render_feature_nav_card
from database import get_active_announcements

def view_home():
    st.markdown("### 👋 欢迎使用抖音爆款工场 Pro")
    
    # 1. 功能展示区 (Requirement 4)
    st.markdown("<div style='margin-bottom:10px; font-weight:600; color:#64748b;'>🚀 核心功能</div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: 
        st.markdown(render_feature_nav_card("📝", "文案改写"), unsafe_allow_html=True)
    with c2:
        st.markdown(render_feature_nav_card("💡", "爆款选题"), unsafe_allow_html=True)
    with c3:
        st.markdown(render_feature_nav_card("🎨", "海报生成"), unsafe_allow_html=True)
    with c4:
        st.markdown(render_feature_nav_card("🏷️", "账号起名"), unsafe_allow_html=True)
        
    st.markdown("---")
    
    # 2. 热门变现项目
    st.markdown("<div style='margin-bottom:15px; font-weight:600; color:#64748b;'>🔥 热门变现项目</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    # Requirement 3: 修正御灵AI介绍
    with col1:
        st.markdown(render_home_project_card(
            "🤖", "御灵 AI 协同",
            "人机协同创作工作流。专注于漫次元、动态漫及拟真人视频制作，一键生成高质量动漫内容，赋能二次元赛道变现。",
            "AI动漫 / 人机协同"
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
        
    # 3. 领取资料 (Requirement 5)
    render_cta_wechat("W7774X")
    
    # 4. 公告区 (Requirement 5)
    st.markdown("<div style='margin-top:30px; margin-bottom:10px; font-weight:600; color:#64748b;'>📢 系统公告</div>", unsafe_allow_html=True)
    anns = get_active_announcements()
    if anns:
        for ann in anns:
            content, time = ann
            st.info(f"**[{str(time)[:10]}]** {content}")
    else:
        st.caption("暂无最新公告")
