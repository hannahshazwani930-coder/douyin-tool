# views/rewrite.py
import streamlit as st
from utils import render_copy_btn

def view_rewrite():
    # 1. 顶部悬浮头图 (复刻首页风格)
    st.markdown("""
    <div class="rewrite-header-card">
        <div class="rw-title">智能文案改写</div>
        <div class="rw-sub">深度去重 · 情感润色 · 爆款逻辑重构</div>
    </div>
    """, unsafe_allow_html=True)

    # 2. 主要工作台 (整齐的白底容器)
    st.markdown('<div class="rewrite-workstation">', unsafe_allow_html=True)
    
    # 左右分栏布局：左侧输入设置，右侧结果
    col_left, col_right = st.columns(2, gap="large")
    
    with col_left:
        st.markdown("##### 📝 输入原文")
        text_input = st.text_area("Original Text", height=300, placeholder="请在此粘贴需要改写的文案...", label_visibility="collapsed")
        
        # 选项行
        c1, c2 = st.columns(2)
        with c1:
            tone = st.selectbox("改写风格", ["🔥 爆款吸睛", "🤝 亲切口语", "🎓 专业干货", "🤣 幽默搞笑"])
        with c2:
            model = st.selectbox("AI模型", ["DeepSeek V3 (推荐)", "GPT-4o (增强)"])
            
        # 提交按钮
        if st.button("✨ 立即一键改写", type="primary", use_container_width=True):
            if not text_input:
                st.toast("⚠️ 请先输入文案")
            else:
                # 模拟加载
                with st.spinner("AI 正在重构文案..."):
                    import time
                    time.sleep(1) # 模拟耗时
                    st.session_state['rewrite_res'] = f"【{tone}】改写结果：\n\n(这里是AI生成的文案内容...)\n\n针对您的输入，我们优化了开篇3秒的完播率设计，并增强了互动引导。"
                    st.rerun()

    with col_right:
        st.markdown("##### 🚀 改写结果")
        res = st.session_state.get('rewrite_res', '')
        
        # 结果展示框 (只读)
        st.text_area("Result Text", value=res, height=300, label_visibility="collapsed", disabled=False)
        
        # 底部操作
        if res:
            render_copy_btn(res, "copy_res_btn")
        else:
            st.info("👈 在左侧输入并点击生成，结果将显示在这里。")

    st.markdown('</div>', unsafe_allow_html=True)
