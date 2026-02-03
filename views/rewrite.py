# views/rewrite.py
import streamlit as st
import time
from utils import render_copy_btn, render_page_banner

def view_rewrite():
    render_page_banner("文案改写 Pro", "支持单条精修与批量矩阵生成，深度学习爆款逻辑，全网去重。")
    
    # 初始化 session_state 防止刷新丢失
    if 'rewrite_single_res' not in st.session_state:
        st.session_state.rewrite_single_res = ""
    if 'rewrite_batch_res' not in st.session_state:
        st.session_state.rewrite_batch_res = [""] * 5

    tab_single, tab_batch = st.tabs(["⚡ 单条精修模式", "🚀 5路并行模式 (矩阵)"])
    
    # --- 单条模式 ---
    with tab_single:
        with st.container(border=True):
            content = st.text_area("输入文案", height=150, placeholder="粘贴需要改写的文案...")
            
            if st.button("开始改写 (单条)", type="primary", use_container_width=True):
                if content:
                    res_container = st.empty()
                    # 模拟专业处理流程
                    with st.status("AI 智能处理中...", expanded=True) as status:
                        st.write("🔍 正在分析文案语义...")
                        time.sleep(0.8)
                        st.write("🌪️ 进行深度去重与逻辑重构...")
                        time.sleep(1)
                        st.write("✨ 润色生成中...")
                        time.sleep(0.5)
                        status.update(label="✅ 改写完成", state="complete", expanded=False)
                    
                    # 生成结果并存入 State
                    simulated_res = f"【改写优化版】\n{content}\n\n(这里是模拟的高质量改写结果，实际部署时请对接大模型API)"
                    st.session_state.rewrite_single_res = simulated_res
                else:
                    st.warning("请先输入文案")
            
            # 显示结果 (从 State 读取)
            if st.session_state.rewrite_single_res:
                st.text_area("改写结果", value=st.session_state.rewrite_single_res, height=200)
                render_copy_btn(st.session_state.rewrite_single_res, "single_copy_btn")

    # --- 并行模式 ---
    with tab_batch:
        st.info("💡 并行模式：同时调用 5 个 AI 线程处理，互不干扰，效率提升 500%。")
        
        # 5个输入框
        inputs = []
        cols = st.columns(5)
        for i, col in enumerate(cols):
            with col:
                st.markdown(f"**任务 {i+1}**")
                val = st.text_area(f"文案 {i+1}", height=120, key=f"batch_in_{i}", label_visibility="collapsed")
                inputs.append(val)
        
        if st.button("🚀 立即并行改写", type="primary", use_container_width=True):
            if any(inputs):
                with st.status("正在启动 5 路并行计算...", expanded=True) as status:
                    progress_bar = st.progress(0)
                    for pct in range(100):
                        time.sleep(0.02)
                        progress_bar.progress(pct + 1)
                    status.update(label="✅ 所有任务处理完毕", state="complete", expanded=False)
                
                # 生成结果并存入 State
                for i, inp in enumerate(inputs):
                    if inp:
                        st.session_state.rewrite_batch_res[i] = f"【并行改写-{i+1}】\n{inp[:15]}... (优化版)"
                    else:
                        st.session_state.rewrite_batch_res[i] = ""
            else:
                st.warning("请至少输入一条文案")

        # 展示 5 路结果
        if any(st.session_state.rewrite_batch_res):
            st.markdown("---")
            st.markdown("#### 🎯 并行处理结果")
            res_cols = st.columns(5)
            for i, col in enumerate(res_cols):
                with col:
                    if st.session_state.rewrite_batch_res[i]:
                        st.success(f"任务 {i+1} 完成")
                        st.text_area(f"结果 {i+1}", value=st.session_state.rewrite_batch_res[i], height=150)
                        render_copy_btn(st.session_state.rewrite_batch_res[i], f"batch_res_{i}")
                    else:
                        st.caption(f"任务 {i+1} 空闲")
