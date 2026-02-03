import streamlit as st
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor
from utils import render_copy_btn

def view_rewrite():
    # 1. 顶部悬浮卡片 (移植自首页风格)
    st.markdown("""
    <div class="rewrite-header-card">
        <div class="rw-title">智能文案改写</div>
        <div class="rw-sub">深度去重 · 情感润色 · 爆款逻辑重构</div>
    </div>
    """, unsafe_allow_html=True)

    # 2. 主要操作区 (白色悬浮台)
    st.markdown('<div class="rewrite-console">', unsafe_allow_html=True)
    
    # 顶部控制栏
    c1, c2, c3 = st.columns([2, 2, 1], gap="medium")
    with c1:
        tone = st.selectbox("改写风格", ["🔥 爆款吸睛", "🤝 亲切口语", "🎓 专业干货", "🤣 幽默搞笑"], label_visibility="visible")
    with c2:
        model_ver = st.selectbox("AI模型版本", ["DeepSeek V3 (推荐)", "GPT-4o (增强)"], label_visibility="visible")
    with c3:
        st.markdown("<div style='height: 28px'></div>", unsafe_allow_html=True) # 占位对齐
        # 预留给未来的高级设置按钮
    
    st.markdown("---") # 分割线

    # 左右分栏布局
    col_input, col_output = st.columns(2, gap="large")
    
    with col_input:
        st.markdown("##### 📝 原文输入")
        text_input = st.text_area("Original", height=350, placeholder="在此粘贴您的原始文案...", label_visibility="collapsed")
        
        # 提交按钮
        if st.button("✨ 立即一键改写", type="primary", use_container_width=True):
            if not text_input:
                st.toast("⚠️ 请先输入文案")
            else:
                # 模拟处理逻辑 (保留原接口结构)
                with st.spinner("AI 正在深度思考重构文案..."):
                    # 这里接入真实的 API 逻辑
                    # 暂时用模拟数据展示 UI 效果
                    import time
                    time.sleep(1) 
                    st.session_state['rewrite_result'] = f"【{tone}】版本改写结果：\n\n(这里是AI生成的高质量文案...)\n\n针对您的输入内容，我们优化了开头的前3秒黄金点，增强了情绪价值，并在结尾添加了强引导指令。建议配合快节奏BGM食用。"
                    st.rerun()

    with col_output:
        st.markdown("##### 🚀 改写结果")
        result = st.session_state.get('rewrite_result', '')
        
        # 结果显示区 (只读)
        st.text_area("Result", value=result, height=350, label_visibility="collapsed", disabled=False)
        
        # 底部复制栏
        if result:
            render_copy_btn(result, "rewrite_res_btn")
        else:
            st.info("👈 在左侧输入文案并点击生成，结果将显示在这里。")

    st.markdown('</div>', unsafe_allow_html=True) # End Console
