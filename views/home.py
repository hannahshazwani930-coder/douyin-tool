# views/home.py
import streamlit as st
from utils import render_page_banner, render_feature_card_home, render_home_project_card, render_cta_wechat
from database import get_active_announcements

def view_home():
    # 1. 顶部大气切片
    render_page_banner("抖音爆款工场 Pro", "全流程 AI 创作工作台，赋能内容生产，连接商业变现。")
    
    # 2. 核心功能区 (切片 + 跳转)
    st.markdown('<div class="section-header">🚀 核心功能</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    
    # 定义功能数据
    features = [
        ("📝", "文案改写", "深度去重，爆款逻辑重写"),
        ("💡", "爆款选题", "挖掘全网最热流量话题"),
        ("🎨", "海报生成", "一键生成专业级封面图"),
        ("🏷️", "账号起名", "玄学+营销学高能起名"),
    ]
    
    # 渲染卡片和按钮
    for i, (icon, title, desc) in enumerate(features):
        with [c1, c2, c3, c4][i]:
            st.markdown(render_feature_card_home(icon, title, desc), unsafe_allow_html=True)
            if st.button(f"立即使用", key=f"home_btn_{i}", use_container_width=True):
                st.session_state['nav_menu_selection'] = title # 设置跳转目标
                st.rerun() # 刷新页面触发跳转
    
    # 3. 热门变现项目 (修正文案)
    st.markdown('<div class="section-header">🔥 热门变现项目</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
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
        
    # 4. 资料领取 & 公告 (分区切片)
    c_left, c_right = st.columns([1.5, 1])
    
    with c_left:
        st.markdown('<div class="section-header">🎁 内部福利</div>', unsafe_allow_html=True)
        render_cta_wechat("W7774X")
        
    with c_right:
        st.markdown('<div class="section-header">📢 系统公告</div>', unsafe_allow_html=True)
        anns = get_active_announcements()
        if anns:
            for content, time in anns:
                st.markdown(f"""
                <div class="ann-card">
                    <span>📅 {str(time)[:10]}</span>
                    <span>{content}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("暂无最新公告")
