import streamlit as st
from database import get_setting

def view_home():
    # 公告栏逻辑
    ann_text = get_setting("announcement")
    if not ann_text: ann_text = "🎉 欢迎使用抖音爆款工场 Pro，系统已升级至 V3.0 模块化版！"
    
    st.markdown(f"""
    <div class="announcement-box">
        <span class="ann-icon">📢</span>
        <span>{ann_text}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Hero 区域
    st.markdown("""
    <div style="text-align:center; padding: 40px 20px; background:white; border-radius:20px; border:1px solid #e2e8f0; margin-bottom:30px; box-shadow:0 10px 30px -10px rgba(0,0,0,0.05);">
        <h1 style="color:#1e293b; font-size:36px; margin-bottom:10px;">抖音爆款工场 Pro</h1>
        <p style="color:#64748b; font-size:16px;">专为素人 KOC 打造的 AI 商业变现操作系统</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 卡片导航区
    c1, c2, c3, c4 = st.columns(4)
    def home_card(col, emoji, title, desc, target):
        with col:
            with st.container(border=True):
                st.markdown(f"""
                <div style="text-align:center; height:140px;">
                    <div style="font-size:40px; margin-bottom:10px;">{emoji}</div>
                    <div style="font-weight:700; color:#1e293b; font-size:16px;">{title}</div>
                    <div style="font-size:12px; color:#94a3b8; margin-top:5px; line-height:1.4;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)
                # 注意：这里使用 session_state 控制跳转，需配合 main.py 的逻辑
                if st.button("立即使用", key=f"home_btn_{title}", use_container_width=True, type="primary"):
                    st.session_state['nav_menu_selection'] = target 
                    st.rerun()

    home_card(c1, "📝", "文案改写", "5路并发洗稿<br>告别文案枯竭", "📝 文案改写")
    home_card(c2, "💡", "爆款选题", "击穿流量焦虑<br>精准击中痛点", "💡 爆款选题")
    home_card(c3, "🎨", "海报生成", "好莱坞级光影<br>极速渲染引擎", "🎨 海报生成")
    home_card(c4, "🏷️", "账号起名", "AI 算命玄学<br>赛道垂直定制", "🏷️ 账号起名")