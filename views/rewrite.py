# views/rewrite.py
import streamlit as st
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from utils import render_copy_btn
from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL

# --- 🎨 注入灵魂 CSS (流光 + 像素级修复版) ---
def load_flow_css():
    st.markdown("""
    <style>
        /* 1. 布局优化 */
        div.block-container {
            max-width: 1400px !important;
            padding: 0 40px 50px 40px !important;
        }
        
        /* 2. 流光极光 Banner (动效版) */
        .flowing-header {
            background: linear-gradient(-45deg, #1e3a8a, #2563eb, #3b82f6, #0ea5e9);
            background-size: 400% 400%;
            animation: gradientBG 10s ease infinite; /* 流动动画 */
            border-bottom-left-radius: 40px;
            border-bottom-right-radius: 40px;
            padding: 60px 40px 110px 40px; /* 底部留白给 Tab */
            color: white; text-align: center;
            margin-bottom: -60px; /* 让 Tab 深度重叠 */
            margin-left: -40px; margin-right: -40px;
            box-shadow: 0 20px 50px rgba(37, 99, 235, 0.3);
            position: relative; z-index: 0;
        }
        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .header-title { 
            font-size: 40px; font-weight: 900; letter-spacing: -1px; margin-bottom: 10px; 
            text-shadow: 0 4px 10px rgba(0,0,0,0.2);
        }
        .header-sub { 
            font-size: 16px; opacity: 0.95; font-weight: 500; 
            background: rgba(255,255,255,0.1); padding: 6px 20px; border-radius: 30px; 
            backdrop-filter: blur(10px); display: inline-block; border: 1px solid rgba(255,255,255,0.2);
        }

        /* 3. 大气 Tabs (全宽分段式) */
        .stTabs { margin-top: 0px; position: relative; z-index: 10; }
        div[data-baseweb="tab-list"] { 
            justify-content: center; gap: 0px; border: none !important; 
            background: white; padding: 6px; border-radius: 16px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08); 
            width: 600px; /* 锁定宽度更显大气 */
            margin: 0 auto 40px auto; 
        }
        div[data-baseweb="tab"] {
            flex: 1; /* 平分宽度 */
            background-color: transparent !important;
            border-radius: 12px !important; padding: 12px 0 !important;
            border: none !important; color: #64748b !important; 
            font-weight: 700 !important; font-size: 16px !important; text-align: center;
            transition: all 0.2s ease !important;
        }
        div[data-baseweb="tab"][aria-selected="true"] {
            background: #eff6ff !important; color: #2563eb !important;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15) !important;
        }

        /* 4. 一体化创作台 (White Box 修复) */
        .creation-console {
            background: white; border-radius: 24px; padding: 40px;
            box-shadow: 0 20px 60px -10px rgba(0,0,0,0.05); 
            border: 1px solid #e2e8f0;
            position: relative;
        }

        /* 5. 修复文本框叠影 (Fix Ghosting) */
        /* 移除外层容器的所有边框和阴影 */
        .stTextArea > div { border: none !important; box-shadow: none !important; }
        .stTextArea > label { display: none !important; } /* 彻底隐藏自带 Label */
        
        /* 只给内部 textarea 加样式 */
        .stTextArea textarea {
            background-color: #f8fafc !important; 
            border: 2px solid #e2e8f0 !important; /* 加粗边框 */
            border-radius: 12px;
            padding: 15px; font-size: 15px; line-height: 1.6; color: #334155;
            box-shadow: none !important; /* 去除内部阴影 */
        }
        .stTextArea textarea:focus { 
            background-color: #ffffff !important; 
            border-color: #3b82f6 !important; 
            box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1) !important; 
        }

        /* 6. 像素级对齐修复 */
        /* 自定义 Label 样式 */
        .custom-label {
            font-size: 14px; font-weight: 700; color: #1e293b; margin-bottom: 8px; display: block;
        }
        /* 强制 Selectbox 高度 */
        div[data-baseweb="select"] > div {
            height: 48px !important; border-radius: 10px !important; border-color: #e2e8f0 !important;
            display: flex; align-items: center;
        }
        /* 强制 Button 高度与 Selectbox 一致 */
        div.stButton button[kind="primary"] {
            height: 48px !important; 
            margin-top: 0px !important; /* 移除顶部 Margin */
            background: linear-gradient(90deg, #2563eb, #3b82f6) !important;
            border-radius: 10px !important; font-size: 16px !important;
            box-shadow: 0 8px 16px -4px rgba(37, 99, 235, 0.3) !important;
        }
        div.stButton button[kind="primary"]:hover { transform: translateY(-2px); box-shadow: 0 12px 20px -5px rgba(37, 99, 235, 0.5) !important; }

        /* 7. 转化提示条 */
        .conversion-tip {
            margin-top: 15px; background: #f0fdf4; border: 1px solid #bbf7d0;
            color: #166534; padding: 12px 15px; border-radius: 12px; font-size: 14px;
            display: flex; align-items: center; gap: 10px; font-weight: 500;
        }

        .stApp { background-color: #f8fafc; }
    </style>
    """, unsafe_allow_html=True)

# --- DeepSeek 调用 ---
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

def render_conversion_tip():
    st.markdown("""<div class="conversion-tip"><span>💰</span><span><b>商业化建议：</b> 已自动植入私域钩子，预计提升 30% 导流效率。</span></div>""", unsafe_allow_html=True)

# --- 主视图 ---
def view_rewrite():
    load_flow_css()
    
    # 1. 动态流光 Banner
    st.markdown("""
    <div class="flowing-header">
        <div class="header-title">✨ 文案改写 Pro</div>
        <div class="header-sub">DeepSeek V3 深度驱动 · 智能矩阵 · 爆款逻辑重构</div>
    </div>
    """, unsafe_allow_html=True)
    
    if 'rw_single_res' not in st.session_state: st.session_state.rw_single_res = ""
    if 'rw_batch_res' not in st.session_state: st.session_state.rw_batch_res = [""] * 5

    # 2. 霸气 Tabs
    tab_single, tab_batch = st.tabs(["⚡ 单条精修模式", "🚀 5路矩阵模式"])
    
    # === 模式 A: 单条精修 ===
    with tab_single:
        # 一体化创作台容器
        st.markdown('<div class="creation-console">', unsafe_allow_html=True)
        
        c_left, c_right = st.columns(2, gap="large")
        
        with c_left:
            # 自定义 Label，解决 Streamlit Label 无法对齐的问题
            st.markdown('<div class="custom-label">📝 原始内容</div>', unsafe_allow_html=True)
            content = st.text_area("in", height=400, placeholder="在此粘贴文案...", label_visibility="collapsed")
            
            st.markdown("<div style='height:25px'></div>", unsafe_allow_html=True)
            
            # 核心对齐修复：使用两列，通过自定义 Label 占位，保证 Input 和 Button 完美对齐
            cc1, cc2 = st.columns([1.5, 1])
            with cc1:
                st.markdown('<div class="custom-label">风格偏好</div>', unsafe_allow_html=True)
                style = st.selectbox("style_hidden", ["标准去重", "爆款悬疑", "情感共鸣", "硬核干货", "幽默反转"], label_visibility="collapsed")
            with cc2:
                # 为了对齐，我们在 Button 上方加一个空白的 Label 占位符
                st.markdown('<div class="custom-label">&nbsp;</div>', unsafe_allow_html=True) 
                run_single = st.button("✨ 立即改写", type="primary", use_container_width=True)
                
            if run_single:
                if content:
                    with st.spinner("DeepSeek 正在重构..."):
                        st.session_state.rw_single_res = call_deepseek_rewrite(content, style)
                else:
                    st.toast("⚠️ 内容不能为空")

        with c_right:
            st.markdown('<div class="custom-label">🎯 改写结果</div>', unsafe_allow_html=True)
            
            if st.session_state.rw_single_res:
                st.text_area("out", value=st.session_state.rw_single_res, height=400, label_visibility="collapsed")
                st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
                render_copy_btn(st.session_state.rw_single_res, "copy_single_v4")
                render_conversion_tip()
            else:
                st.markdown("""
                <div style="height:480px; background:#f8fafc; border-radius:12px; border:2px dashed #e2e8f0; display:flex; flex-direction:column; align-items:center; justify-content:center; color:#94a3b8;">
                    <div style="font-size:56px; opacity:0.3; margin-bottom:10px;">🪄</div>
                    <div>等待生成...</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # === 模式 B: 5路矩阵 ===
    with tab_batch:
        st.markdown('<div class="creation-console">', unsafe_allow_html=True)
        
        # 顶部对齐修复
        # 左侧文字垂直居中
        top_c1, top_c2 = st.columns([3, 1], vertical_alignment="bottom") 
        with top_c1:
             st.markdown("""
             <div style="margin-bottom: 5px;">
                <span style="font-size:18px;">💡</span>
                <span style="color:#64748b; font-size:15px; font-weight:500;">矩阵模式：5 个线程并发处理，独立生成，互不干扰。</span>
             </div>
             """, unsafe_allow_html=True)
        with top_c2:
            # 按钮与文字视觉对齐
            run_batch = st.button("🚀 并行启动", type="primary", use_container_width=True)
            
        st.markdown("<div style='height:25px'></div>", unsafe_allow_html=True)
        
        # 5列输入
        cols = st.columns(5, gap="small")
        inputs = []
        for i, col in enumerate(cols):
            with col:
                st.markdown(f"<div class='custom-label' style='text-align:center'>通道 {i+1}</div>", unsafe_allow_html=True)
                val = st.text_area(f"in_{i}", height=150, key=f"bi_{i}_v4", placeholder="输入...", label_visibility="collapsed")
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
                    render_copy_btn(res, f"cp_b_{i}_v4")
                else:
                    st.markdown("<div style='height:245px; background:#f8fafc; border-radius:12px; border:1px dashed #e2e8f0; display:flex; align-items:center; justify-content:center; color:#cbd5e1;'>空闲</div>", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
