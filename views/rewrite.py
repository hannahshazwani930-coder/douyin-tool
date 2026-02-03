# views/rewrite.py
import streamlit as st
from utils import render_copy_btn

def view_rewrite():
    # 1. 顶部头图 (复刻首页风格)
    st.markdown("""
    <div class="rewrite-header">
        <div class="rw-title">智能文案改写</div>
        <div class="rw-sub">深度去重 · 情感润色 · 爆款逻辑重构</div>
    </div>
    """, unsafe_allow_html=True)

    # 2. 独立工作台设计
    st.markdown('<div class="rewrite-console">', unsafe_allow_html=True)
    
    # 左右分栏：左侧配置与输入，右侧结果
    col_left, col_right = st.columns(2, gap="large")
    
    with col_left:
        st.markdown("##### 📝 输入您的文案")
        text_input = st.text_area("Original Text", height=300, placeholder="在此粘贴需要改写的文案...", label_visibility="collapsed")
        
        # 选项区域 (两列)
        c1, c2 = st.columns(2)
        with c1:
            tone = st.selectbox("改写风格", ["🔥 爆款吸睛", "🤝 亲切口语", "🎓 专业干货", "🤣 幽默搞笑"])
        with c2:
            model = st.selectbox("AI模型", ["DeepSeek V3 (推荐)", "GPT-4o (增强)"])
            
        # 提交按钮 (Primary样式)
        if st.button("✨ 立即一键改写", type="primary", use_container_width=True):
            if not text_input:
                st.toast("⚠️ 请先输入文案")
            else:
                # 模拟处理
                with st.spinner("AI 正在重构文案..."):
                    import time
                    time.sleep(1) # 模拟耗时
                    st.session_state['rewrite_res'] = f"【{tone}】改写结果：\n\n(AI生成的优化文案将显示在这里...)\n\n我们为您优化了开篇的吸引力，并调整了情绪节奏。"
                    st.rerun()

    with col_right:
        st.markdown("##### 🚀 改写结果")
        res = st.session_state.get('rewrite_res', '')
        
        # 结果展示框 (只读)
        st.text_area("Result Text", value=res, height=300, label_visibility="collapsed", disabled=False)
        
        # 底部复制功能
        if res:
            render_copy_btn(res, "copy_res_btn")
        else:
            st.info("👈 在左侧输入文案并点击生成，结果将显示在这里。")

    st.markdown('</div>', unsafe_allow_html=True)
