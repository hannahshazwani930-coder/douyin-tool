# views/rewrite.py
import streamlit as st

def view_rewrite():
    # 1. 顶部悬浮卡片 (移植自首页风格)
    st.markdown("""
    <div class="rewrite-header-card">
        <div class="rw-title">智能文案改写</div>
        <div class="rw-sub">深度去重 · 情感润色 · 爆款逻辑重构</div>
    </div>
    """, unsafe_allow_html=True)

    # 2. 主要操作区
    st.markdown('<div class="rewrite-console">', unsafe_allow_html=True)
    
    # 布局：左侧输入，右侧输出 (或上下布局，视宽度自动调整)
    c1, c2 = st.columns(2, gap="large")
    
    with c1:
        st.markdown("##### 📝 原文输入")
        text_input = st.text_area("请输入需要改写的文案", height=300, placeholder="在此粘贴您的原始文案...", label_visibility="collapsed")
        
        # 选项区
        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            tone = st.selectbox("改写风格", ["🔥 爆款吸睛", "🤝 亲切口语", "🎓 专业干货", "🤣 幽默搞笑"])
        with col_opt2:
            model = st.selectbox("AI模型", ["通用大模型 V4", "文案特化 V2 (推荐)"])
            
        if st.button("✨ 立即一键改写", type="primary"):
            if not text_input:
                st.warning("请先输入文案")
            else:
                st.session_state['rewrite_result'] = f"【{tone}】改写结果演示：\n\n这是基于您的输入生成的优化文案。它采用了更吸引人的开头，优化了段落结构，并添加了能够提升互动的钩子。\n\n(此处为演示输出，实际对接AI后将显示真实结果)"
    
    with c2:
        st.markdown("##### 🚀 改写结果")
        result = st.session_state.get('rewrite_result', '')
        st.text_area("改写结果", value=result, height=380, label_visibility="collapsed")
        
        # 底部操作栏
        if result:
            st.button("📋 复制结果", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)
