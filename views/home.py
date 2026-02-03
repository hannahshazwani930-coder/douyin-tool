# views/home.py
import streamlit as st
import streamlit.components.v1 as components
from database import get_active_announcements

def view_home():
    # 1. 沉浸式极光头图
    st.markdown("""
    <div class="flowing-header">
        <div class="header-title">抖音爆款工场 Pro</div>
        <div class="header-sub">全流程 AI 创作工作台 · 赋能内容生产 · 连接商业变现</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. 悬浮中控台容器
    st.markdown('<div class="creation-console">', unsafe_allow_html=True)
    
    # === A. 核心功能区 (悬浮微交互卡片) ===
    st.markdown('<div class="section-label">🚀 核心创作引擎</div>', unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4, gap="medium")
    
    features = [
        ("📝", "文案改写", "深度去重 爆款逻辑", "📝 文案改写"),
        ("💡", "爆款选题", "全网挖掘 流量风向", "💡 爆款选题"),
        ("🎨", "海报生成", "封面设计 点击飙升", "🎨 海报生成"),
        ("🏷️", "账号起名", "玄学好名 易记吸粉", "🏷️ 账号起名"),
    ]
    
    for i, (icon, title, desc, target) in enumerate(features):
        with [c1, c2, c3, c4][i]:
            # 渲染卡片视觉
            st.markdown(f"""
            <div class="feature-card-pro">
                <div class="feat-icon">{icon}</div>
                <div class="feat-title">{title}</div>
                <div class="feat-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 隐形点击层
            if st.button(f"nav_home_{i}", key=f"feat_btn_{i}", use_container_width=True):
                st.session_state['nav_menu_selection'] = target
                st.rerun()

    # === B. 系统公告 (悬浮长条 + 滚动播放) ===
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    
    anns = get_active_announcements()
    ann_text = "   |   ".join([f"📅 {str(time)[5:10]} {content}" for content, time in anns]) if anns else "暂无最新系统公告，请留意后续更新。"
    
    # 使用 marquee 滚动效果 (CSS 动画在 utils.py 中定义)
    st.markdown(f"""
    <div class="news-container">
        <div class="news-icon">📢</div>
        <div class="news-scroller">{ann_text}   |   {ann_text}   |   {ann_text}</div>
    </div>
    """, unsafe_allow_html=True)

    # === C. 热门变现任务 (带复制功能徽章) ===
    st.markdown('<div class="section-label">🔥 热门变现项目</div>', unsafe_allow_html=True)
    
    p1, p2, p3 = st.columns(3, gap="medium")
    
    # 项目数据: (图标, 标题, 描述)
    projects = [
        ("🤖", "御灵 AI 协同", "人机协同创作工作流。专注于漫次元、动态漫及拟真人视频制作，大幅降低制作门槛。"),
        ("👥", "素人 KOC 孵化", "从零打造素人IP，提供全套人设定位、脚本库与拍摄指导，连接品牌方资源变现。"),
        ("🌏", "文娱出海变现", "TikTok 短剧与游戏推广出海项目。提供海外热门素材、翻译工具及本地化运营策略。")
    ]
    
    # 注入 JS 脚本 (用于复制)
    copy_script = """
    <script>
    function copyWechat() {
        navigator.clipboard.writeText('W7774X').then(function() {
            alert('✅ 微信 W7774X 已复制！\\n请添加微信并备注【资料】领取内部白皮书。');
        }, function(err) {
            console.error('复制失败: ', err);
        });
    }
    </script>
    """
    components.html(copy_script, height=0) # 隐形注入
    
    for i, (icon, title, desc) in enumerate(projects):
        with [p1, p2, p3][i]:
            # 使用 parent.document... 调用上面注入的函数比较麻烦，
            # 简单粗暴点：直接在 onclick 里写 navigator.clipboard (需 HTTPS 或 localhost)
            # 或者利用 utils.py 里已有的 render_copy_btn 逻辑
            
            # 这里我们用最稳妥的纯 HTML 渲染，onclick 直接触发
            st.markdown(f"""
            <div class="monetize-card">
                <div class="mon-head">
                    <span style="font-size:24px;">{icon}</span>
                    <span class="mon-title">{title}</span>
                </div>
                <div class="mon-desc">{desc}</div>
                
                <div class="wechat-badge" onclick="navigator.clipboard.writeText('W7774X'); alert('✅ 微信 W7774X 已复制！')">
                    <span style="font-size:14px;">💬</span>
                    <span>W7774X</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True) # End Console
