# views/rewrite.py
import streamlit as st
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from utils import render_copy_btn, render_conversion_tip, inject_css
from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL

def call_deepseek_rewrite(content, style_prompt):
    if not DEEPSEEK_API_KEY or "sk-" not in DEEPSEEK_API_KEY:
        return "❌ 配置错误：请在 config.py 中填入正确的 DEEPSEEK_API_KEY"
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    system_prompt = f"""你是由抖音爆款工场开发的顶级文案专家。请对用户输入的文案进行【{style_prompt}】方向的改写。核心要求：1.深度去重；2.语言更有网感；3.适当使用emoji；4.直接输出结果。"""
    data = {"model": "deepseek-chat", "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": content}], "temperature": 1.3, "stream": False}
    try:
        response = requests.post(f"{DEEPSEEK_BASE_URL}/chat/completions", headers=headers, json=data, timeout=60)
        if response.status_code == 200: return response.json()['choices'][0]['message']['content']
        else: return f"❌ API 报错: {response.status_code} - {response.text}"
    except Exception as e: return f"❌ 网络错误: {str(e)}"

def view_rewrite():
    inject_css() 
    
    # 1. 悬浮流光 Header (动效)
    st.markdown("""
    <div class="flowing-header">
        <div class="header-title">✨ 文案改写 Pro</div>
        <div class="header-sub">DeepSeek V3 深度驱动 · 智能矩阵 · 爆款逻辑重构</div>
    </div>
    """, unsafe_allow_html=True)
    
    # State
    if 'rewrite_mode' not in st.session_state: st.session_state.rewrite_mode = "single"
    if 'rw_single_res' not in st.session_state: st.session_state.rw_single_res = ""
    if 'rw_batch_res' not in st.session_state: st.session_state.rw_batch_res = [""] * 5

    # 2. 悬浮切换按钮 (独立于白卡之上，更显大气)
    # 使用 columns 居中
    c_l, c_m1, c_m2, c_r = st.columns([2, 1.2, 1.2, 2])
    
    with c_m1:
        # 选中时用 Primary (渐变蓝)，未选中 Secondary (白底灰字)
        type_s = "primary" if st.session_state.rewrite_mode == "single" else "secondary"
        if st.button("⚡ 单条精修", key="sw_single", type=type_s, use_container_width=True):
            st.session_state.rewrite_mode = "single"
            st.rerun()
            
    with c_m2:
        type_m = "primary" if st.session_state.rewrite_mode == "matrix" else "secondary"
        if st.button("🚀 5路矩阵", key="sw_matrix", type=type_m, use_container_width=True):
            st.session_state.rewrite_mode = "matrix"
            st.rerun()

    # 3. 一体化创作控制台 (所有内容镶嵌其中)
    st.markdown('<div class="creation-console">', unsafe_allow_html=True)

    # === 模式 A: 单条精修 ===
    if st.session_state.rewrite_mode == "single":
        c_left, c_right = st.columns(2, gap="large")
        
        with c_left:
            st.markdown('<div class="custom-label" style="text-align:left">📝 原始内容</div>', unsafe_allow_html=True)
            # 这里的输入框现在没有叠影，背景为淡灰
            content = st.text_area("in", height=400, placeholder="在此粘贴文案...", label_visibility="collapsed")
            
            st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
            
            # 底部绝对对齐
            cc1, cc2 = st.columns([1, 1])
            with cc1:
                st.markdown('<div class="custom-label" style="text-align:left; margin-bottom:5px;">风格偏好</div>', unsafe_allow_html=True)
                style = st.selectbox("style_s", ["标准去重", "爆款悬疑", "情感共鸣", "硬核干货", "幽默反转"], label_visibility="collapsed")
            with cc2:
                # 这是一个空白占位，强制把按钮向下推，与 Selectbox 底部对齐
                st.markdown('<div class="custom-label" style="opacity:0">&nbsp;</div>', unsafe_allow_html=True)
                run_single = st.button("✨ 立即改写", type="primary", use_container_width=True)
                
            if run_single:
                if content:
                    with st.spinner("AI 正在重构..."):
                        st.session_state.rw_single_res = call_deepseek_rewrite(content, style)
                else:
                    st.toast("⚠️ 内容不能为空")

        with c_right:
            st.markdown('<div class="custom-label" style="text-align:left">🎯 改写结果</div>', unsafe_allow_html=True)
            if st.session_state.rw_single_res:
                st.text_area("out", value=st.session_state.rw_single_res, height=400, label_visibility="collapsed")
                st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
                render_copy_btn(st.session_state.rw_single_res, "copy_s_v6")
                render_conversion_tip()
            else:
                st.markdown("""
                <div style="height:485px; background:#f8fafc; border-radius:12px; border:2px dashed #e2e8f0; display:flex; flex-direction:column; align-items:center; justify-content:center; color:#94a3b8;">
                    <div style="font-size:48px; opacity:0.3; margin-bottom:10px;">🪄</div>
                    <div>等待 AI 施展魔法...</div>
                </div>
                """, unsafe_allow_html=True)

    # === 模式 B: 5路矩阵 ===
    else:
        # 顶部对齐：左侧文字 vs 右侧按钮
        top_c1, top_c2 = st.columns([3, 1])
        
        with top_c1:
             # 使用 Flex 布局的 info-box 实现垂直居中
             st.markdown("""
             <div class="info-box">
                <span style="font-size:20px;">💡</span>
                <span style="font-weight:600;">矩阵效率模式：开启 5 个并发线程，独立处理，互不干扰。</span>
             </div>
             """, unsafe_allow_html=True)
             
        with top_c2:
            # 按钮高度已强制 CSS 为 48px，与 info-box 一致
            run_batch = st.button("🚀 并行启动", type="primary", use_container_width=True)
            
        st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
        
        # 5列输入
        cols = st.columns(5, gap="small")
        inputs = []
        for i, col in enumerate(cols):
            with col:
                st.markdown(f"<div class='custom-label' style='text-align:center'>通道 {i+1}</div>", unsafe_allow_html=True)
                val = st.text_area(f"in_{i}", height=150, key=f"bi_{i}_v6", placeholder="输入...", label_visibility="collapsed")
                inputs.append(val)
        
        # 逻辑
        if run_batch:
            valid = [(i, t) for i, t in enumerate(inputs) if t.strip()]
            if valid:
                status = st.status(f"并行处理 {len(valid)} 个任务...", expanded=True)
                with ThreadPoolExecutor(max_workers=5) as ex:
                    f_map = {ex.submit(call_deepseek_rewrite, t, "标准去重"): i for i, t in valid}
                    for f in f_map:
                        try: st.session_state.rw_batch_res[f_map[f]] = f.result()
                        except: st.session_state.rw_batch_res[f_map[f]] = "Error"
                status.update(label="✅ 完成", state="complete", expanded=False)
        
        st.markdown("<div style='height:20px; border-bottom:1px solid #f1f5f9; margin-bottom:20px;'></div>", unsafe_allow_html=True)
        
        # 输出区
        res_cols = st.columns(5, gap="small")
        for i, col in enumerate(res_cols):
            with col:
                res = st.session_state.rw_batch_res[i]
                if res:
                    st.text_area(f"out_{i}", value=res, height=200, label_visibility="collapsed")
                    render_copy_btn(res, f"cp_b_{i}_v6")
                else:
                    st.markdown("<div style='height:245px; background:#f8fafc; border-radius:12px; border:1px dashed #e2e8f0; display:flex; align-items:center; justify-content:center; color:#cbd5e1;'>空闲</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True) # End creation-console
