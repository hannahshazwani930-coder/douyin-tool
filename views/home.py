# views/home.py
import streamlit as st
from utils import render_cta_wechat
from database import get_active_announcements

def view_home():
    # 1. 悬浮岛头图 V3
    st.markdown("""
    <div class="header-card-v3">
        <div class="header-title-v3">抖音爆款工场 Pro</div>
        <div class="header-sub-v3">全流程 AI 创作工作台 · 赋能内容生产 · 连接商业变现</div>
    </div>
    """, unsafe_allow_html=True)
    
    # === A. 核心功能区 V3 ===
    st.markdown('<div class="section-title-v3">🚀 核心创作引擎</div>', unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4, gap="medium")
    
    features = [
        ("📝", "文案改写", "深度去重 爆款重构", "📝 文案改写"),
        ("💡", "爆款选题", "全网挖掘 流量风向", "💡 爆款选题"),
        ("🎨", "海报生成", "封面设计 点击飙升", "🎨 海报生成"),
        ("🏷️", "账号起名", "玄学好名 易记吸粉", "🏷️ 账号起名"),
    ]
    
    for i, (icon, title, desc, target) in enumerate(features):
        with [c1, c2, c3, c4][i]:
            # 使用新类名
            st.markdown(f"""
            <div class="feature-box-v3">
                <div class="feat-icon-v3">{icon}</div>
                <div class="feat-title-v3">{title}</div>
                <div class="feat-desc-v3">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 隐形点击
            if st.button(f"nav_home_{i}", key=f"feat_btn_{i}", use_container_width=True):
                st.session_state['nav_menu_selection'] = target
                st.rerun()

    # === B. 系统公告 V3 ===
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    anns = get_active_announcements()
    latest_ann = anns[0][0] if anns else "暂无最新系统公告，请留意后续更新。"
    
    st.markdown(f"""
    <div class="news-box-v3">
        <div class="news-tag-v3">🔔 NEW</div>
        <div class="news-text-v3">{latest_ann}</div>
    </div>
    """, unsafe_allow_html=True)

    # === C. 热门变现任务 V3 (长按钮版) ===
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-title-v3">🔥 热门变现项目</div>', unsafe_allow_html=True)
    
    p1, p2, p3 = st.columns(3, gap="medium")
    
    projects = [
        ("🤖", "御灵 AI 协同", "人机协同创作工作流。专注于漫次元、动态漫及拟真人视频制作，大幅降低制作门槛。"),
        ("👥", "素人 KOC 孵化", "从零打造素人IP，提供全套人设定位、脚本库与拍摄指导，连接品牌方资源变现。"),
        ("🌏", "文娱出海变现", "TikTok 短剧与游戏推广出海项目。提供海外热门素材、翻译工具及本地化运营策略。")
    ]
    
    for i, (icon, title, desc) in enumerate(projects):
        with [p1, p2, p3][i]:
            st.markdown(f"""
            <div class="project-card-v3">
                <div class="proj-head-v3">
                    <span class="proj-icon-v3">{icon}</span>
                    <span class="proj-title-v3">{title}</span>
                </div>
                <div class="proj-desc-v3">{desc}</div>
                
                <div class="copy-btn-v3" onclick="navigator.clipboard.writeText('W7774X'); alert('✅ 微信 W7774X 已复制！\\n请添加微信并备注【资料】领取内部白皮书。')">
                    📋 复制微信领取资料 (W7774X)
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
