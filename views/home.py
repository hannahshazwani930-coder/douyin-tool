# views/home.py
import streamlit as st
from utils import render_home_project_card, render_cta_wechat
from database import get_active_announcements

def view_home():
    # 1. 背景融合式大标题 (Requirement 2)
    st.markdown("""
    <div class="home-header-text">
        <div class="home-h1">抖音爆款工场 Pro</div>
        <div class="home-sub">全流程 AI 创作工作台 · 赋能内容生产 · 连接商业变现</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. 核心功能区 (Requirement 1, 2, 5)
    # 使用 container 包裹，CSS 会将其渲染为白色大卡片
    with st.container():
        st.markdown('<div class="section-card"><div class="section-header">🚀 核心功能</div>', unsafe_allow_html=True)
        
        # 布局：4个大按钮直接点击跳转
        c1, c2, c3, c4 = st.columns(4)
        
        # 技巧：在 Button 的 label 中写入换行符来模拟 Title + Desc
        # 注意：具体的样式由 utils.py 中的 CSS 强制控制
        with c1:
            if st.button("📝 文案改写\n深度去重 爆款逻辑", use_container_width=True):
                st.session_state['nav_menu_selection'] = "📝 文案改写"
                st.rerun()
        with c2:
            if st.button("💡 爆款选题\n挖掘全网 最热流量", use_container_width=True):
                st.session_state['nav_menu_selection'] = "💡 爆款选题"
                st.rerun()
        with c3:
            if st.button("🎨 海报生成\n一键生成 专业封面", use_container_width=True):
                st.session_state['nav_menu_selection'] = "🎨 海报生成"
                st.rerun()
        with c4:
            if st.button("🏷️ 账号起名\n玄学起名 易记好听", use_container_width=True):
                st.session_state['nav_menu_selection'] = "🏷️ 账号起名"
                st.rerun()
                
        st.markdown('</div>', unsafe_allow_html=True) # 闭合 section-card

    # 3. 热门变现项目 (Requirement 5 分区归类)
    with st.container():
        st.markdown('<div class="section-card"><div class="section-header">🔥 热门变现项目</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(render_home_project_card(
                "🤖", "御灵 AI 协同",
                "人机协同创作工作流。专注于漫次元、动态漫及拟真人视频制作，一键生成高质量动漫内容。",
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
        st.markdown('</div>', unsafe_allow_html=True)

    # 4. 资料与公告 (Requirement 5)
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        c_left, c_right = st.columns([1.5, 1], gap="large")
        
        with c_left:
            st.markdown('<div class="section-header">🎁 内部福利</div>', unsafe_allow_html=True)
            # 修复阴影切边问题 (utils里已加margin)
            render_cta_wechat("W7774X")
            
        with c_right:
            st.markdown('<div class="section-header">📢 系统公告</div>', unsafe_allow_html=True)
            anns = get_active_announcements()
            if anns:
                for content, time in anns:
                    st.markdown(f"""
                    <div class="ann-card">
                        <span style="font-weight:700; white-space:nowrap;">📅 {str(time)[5:10]}</span>
                        <span style="line-height:1.4;">{content}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("暂无最新公告")
        st.markdown('</div>', unsafe_allow_html=True)
