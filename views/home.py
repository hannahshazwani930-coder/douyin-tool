# views/home.py
import streamlit as st
from utils import render_home_project_card, render_cta_wechat, render_feature_card_home
from database import get_active_announcements

def view_home():
    # 1. 顶部：流光极光 Header
    # 注意：样式已由 main.py 加载，这里只负责渲染 HTML 结构
    st.markdown("""
    <div class="flowing-header">
        <div class="header-title">抖音爆款工场 Pro</div>
        <div class="header-sub">全流程 AI 创作工作台 · 赋能内容生产 · 连接商业变现</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. 核心内容区：一体化白卡 (Creation Console)
    # CSS 中已设置负边距，使其向上覆盖 Header 底部，消除白框
    st.markdown('<div class="creation-console">', unsafe_allow_html=True)
    
    # --- A. 核心功能导航 ---
    st.markdown('<div class="custom-label" style="font-size:18px; margin-bottom:20px; border-left:4px solid #3b82f6; padding-left:10px;">🚀 核心功能</div>', unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4, gap="medium")
    
    # 定义功能数据 (Icon, 标题, 描述, 对应侧边栏的完整名称)
    # 🔴 关键：target_menu 必须与 main.py 中的 menu_opts 完全一致(含Emoji)
    features = [
        ("📝", "文案改写", "深度去重 爆款逻辑", "📝 文案改写"),
        ("💡", "爆款选题", "挖掘全网 最热流量", "💡 爆款选题"),
        ("🎨", "海报生成", "一键生成 专业封面", "🎨 海报生成"),
        ("🏷️", "账号起名", "玄学起名 易记好听", "🏷️ 账号起名"),
    ]
    
    # 渲染功能入口
    for i, (icon, title, desc, target_menu) in enumerate(features):
        with [c1, c2, c3, c4][i]:
            # 1. 渲染视觉卡片 (HTML)
            st.markdown(render_feature_card_home(icon, title, desc), unsafe_allow_html=True)
            
            # 2. 渲染隐形跳转按钮 (覆盖在卡片之上)
            # key 用于区分不同按钮，避免 Streamlit 报错
            if st.button(f"立即使用 {title}", key=f"home_nav_btn_{i}", use_container_width=True):
                st.session_state['nav_menu_selection'] = target_menu
                st.rerun()

    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

    # --- B. 热门变现项目 (保留所有详细文案) ---
    st.markdown('<div class="custom-label" style="font-size:18px; margin-bottom:20px; border-left:4px solid #f59e0b; padding-left:10px;">🔥 热门变现项目</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.markdown(render_home_project_card(
            "🤖", "御灵 AI 协同",
            "人机协同创作工作流。专注于漫次元、动态漫及拟真人视频制作，一键生成高质量动漫内容，大幅降低制作门槛。",
            "AI动漫 / 人机协同"
        ), unsafe_allow_html=True)
        
    with col2:
        st.markdown(render_home_project_card(
            "👥", "素人 KOC 孵化",
            "从零打造素人IP，提供全套人设定位、脚本库与拍摄指导。连接品牌方资源，实现快速商单变现与私域引流。",
            "IP孵化 / 商单资源"
        ), unsafe_allow_html=True)
        
    with col3:
        st.markdown(render_home_project_card(
            "🌏", "文娱出海变现",
            "TikTok 短剧与游戏推广出海项目。提供海外热门素材、翻译工具及本地化运营策略，赚取美金收益。",
            "TikTok / 跨境电商"
        ), unsafe_allow_html=True)
        
    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

    # --- C. 底部：福利与公告 ---
    c_left, c_right = st.columns([1.5, 1], gap="large")
    
    with c_left:
        st.markdown('<div class="custom-label" style="font-size:18px; margin-bottom:15px; border-left:4px solid #10b981; padding-left:10px;">🎁 内部福利</div>', unsafe_allow_html=True)
        render_cta_wechat("W7774X")
        
    with c_right:
        st.markdown('<div class="custom-label" style="font-size:18px; margin-bottom:15px; border-left:4px solid #ef4444; padding-left:10px;">📢 系统公告</div>', unsafe_allow_html=True)
        # 获取数据库中的公告
        anns = get_active_announcements()
        if anns:
            for content, time_val in anns:
                # 格式化时间显示
                date_str = str(time_val)[5:10] # 只取 MM-DD
                st.markdown(f"""
                <div class="ann-card">
                    <span style="font-weight:700; white-space:nowrap; color:#ea580c;">📅 {date_str}</span>
                    <span style="line-height:1.4; color:#7c2d12;">{content}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("暂无最新公告")

    # 闭合控制台卡片
    st.markdown('</div>', unsafe_allow_html=True)
