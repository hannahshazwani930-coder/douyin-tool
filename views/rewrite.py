# views/rewrite.py
import streamlit as st
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from utils import render_copy_btn
from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL

# --- 🎨 注入灵魂 CSS (悬浮极光 + 高对比度版) ---
def load_immersive_css():
    st.markdown("""
    <style>
        /* 1. 全局容器调整 */
        div.block-container {
            max-width: 1400px !important;
            padding-top: 20px !important; /* 顶部留一点空隙 */
            padding-left: 40px !important;
            padding-right: 40px !important;
            padding-bottom: 50px !important;
        }
        
        /* 2. 悬浮极光 Banner (更轻盈、两边留白) */
        .immersive-header {
            background: linear-gradient(120deg, #3b82f6 0%, #2563eb 100%); /* 亮蓝色系 */
            border-radius: 24px; /* 整体圆角 */
            padding: 40px 20px;
            color: white; text-align: center;
            margin-bottom: 30px; /* 与下方 Tab 分离 */
            box-shadow: 0 10px 30px -10px rgba(37, 99, 235, 0.4);
            position: relative;
        }
        .header-title { 
            font-size: 32px; font-weight: 800; letter-spacing: -0.5px; margin-bottom: 8px; 
            text-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .header-sub { 
            font-size: 15px; opacity: 0.9; font-weight: 500; 
            background: rgba(255,255,255,0.15); padding: 5px 15px; border-radius: 20px; 
            display: inline-block; border: 1px solid rgba(255,255,255,0.2);
        }

        /* 3. Tab 切换栏 (下移、独立) */
        .stTabs { margin-top: 0px; } /* 恢复正常位置 */
        div[data-baseweb="tab-list"] { 
            justify-content: center; gap: 20px; border: none !important; 
            background: white; padding: 8px; border-radius: 100px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05); width: fit-content; 
            margin: 0 auto 30px auto; border: 1px solid #f1f5f9;
        }
        div[data-baseweb="tab"] {
            background-color: transparent !important;
            border-radius: 50px !important; padding: 10px 35px !important;
            border: none !important; color: #64748b !important; 
            font-weight: 600 !important; font-size: 15px !important;
        }
        div[data-baseweb="tab"][aria-selected="true"] {
            background: #eff6ff !important; color: #2563eb !important;
            box-shadow: none !important; /* 扁平化高亮 */
        }

        /* 4. 工作区白卡 */
        .glass-card {
            background: white; border-radius: 24px; padding: 40px;
            box-shadow: 0 10px 30px -5px rgba(0,0,0,0.03); border: 1px solid #e2e8f0;
        }

        /* 5. 输入框高对比度优化 */
        .input-header { 
            font-size: 14px; font-weight: 700; color: #1e293b; margin-bottom: 12px; 
            display: flex; align-items: center; gap: 8px; 
        }
        
        /* 核心修改：输入框背景加深，与白底区分 */
        .stTextArea textarea {
            background-color: #f8fafc !important; /* 明显的灰底 */
            border: 1px solid #cbd5e1 !important; /* 加深边框 */
            border-radius: 12px;
            padding: 15px; font-size: 15px; line-height: 1.6;
            color: #334155;
        }
        .stTextArea textarea:focus { 
            background-color: #ffffff !important; /* 聚焦变白 */
            border-color: #3b82f6 !important; 
            box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1) !important; 
        }
        /* 去除 Streamlit label 的空隙 */
        div[data-testid="stMarkdownContainer"] p { margin-bottom: 0px; }

        /* 6. 按钮样式 */
        div.stButton button[kind="primary"] {
            width: 100%; height: 45px; 
            background: linear-gradient(90deg, #2563eb, #3b82f6) !important;
            border-radius: 10px !important; font-size: 15px !important;
            box-shadow: 0 5px 15px rgba(37, 99, 235, 0.2) !important;
        }
        div.stButton button[kind="primary"]:hover { 
            transform: translateY(-2px); box-shadow: 0 8px 20px rgba(37, 99, 235, 0.3) !important; 
        }

        /* 7. 转化提示条 */
        .conversion-tip {
            margin-top: 15px; background: #ecfdf5; border: 1px solid #a7f3d0;
            color: #065f46; padding: 10px 15px; border-radius: 8px; font-size: 13px;
            display: flex; align-items: center; gap: 10px;
        }

        /* 隐藏 Header 留白 */
        header { display: none !important; }
        .stApp { background-color: #f8fafc; }
    </style>
    """, unsafe_allow_html=True)

# --- DeepSeek 调用 (保持不变) ---
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

# --- 组件 ---
def render_conversion_tip():
    st.markdown("""<div class="conversion-tip"><span>💡</span><span><b>私域钩子建议：</b> 文案末尾添加“点击主页”或“领取资料”，转化率提升 30%！</span></div>""", unsafe_allow_html=True)

# --- 主视图 ---
def view_rewrite():
    load_immersive_css()
    
    # 1. 悬浮极光 Banner (两侧留白，更清爽)
    st.markdown("""
    <div class="immersive-header">
        <div class="header-title">✨ 文案改写 Pro</div>
        <div class="header-sub">DeepSeek 驱动 · 智能去重 · 爆款逻辑重构</div>
    </div>
    """, unsafe_allow_html=True)
    
    # State
    if 'rw_single_res' not in st.session_state: st.session_state.rw_single_res = ""
    if 'rw_batch_res' not in st.session_state: st.session_state.rw_batch_res = [""] * 5

    # 2. Tab 下移，作为独立控件
    tab_single, tab_batch = st.tabs(["⚡ 单条精修", "🚀 5路矩阵"])
    
    # === 单条模式 ===
    with tab_single:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        c_left, c_right = st.columns(2, gap="large")
        
        with c_left:
            st.markdown('<div class="input-header">📝 原始内容</div>', unsafe_allow_html=True)
            # 使用灰色背景输入框，与白色卡片形成对比
            content = st.text_area("in", height=400, placeholder="在此粘贴文案...", label_visibility="collapsed")
            
            st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
            
            cc1, cc2 = st.columns([1, 1.2])
            with cc1:
                style = st.selectbox("风格偏好", ["标准去重", "爆款悬疑", "情感共鸣", "硬核干货", "幽默反转"], label_visibility="collapsed")
            with cc2:
                run_single = st.button("✨ 立即改写", type="primary", use_container_width=True)
                
            if run_single:
                if content:
                    with st.spinner("AI 正在思考..."):
                        st.session_state.rw_single_res = call_deepseek_rewrite(content, style)
                else:
                    st.toast("⚠️ 请输入内容")

        with c_right:
            st.markdown('<div class="input-header">🎯 改写结果</div>', unsafe_allow_html=True)
            
            if st.session_state.rw_single_res:
                st.text_area("out", value=st.session_state.rw_single_res, height=400, label_visibility="collapsed")
                render_copy_btn(st.session_state.rw_single_res, "copy_single_v3")
                render_conversion_tip()
            else:
                # 占位图
                st.markdown("""
                <div style="height:480px; background:#f8fafc; border-radius:12px; border:2px dashed #e2e8f0; display:flex; flex-direction:column; align-items:center; justify-content:center; color:#94a3b8;">
                    <div style="font-size:48px; opacity:0.3; margin-bottom:10px;">🪄</div>
                    <div>等待生成...</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # === 矩阵模式 ===
    with tab_batch:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        top_c1, top_c2 = st.columns([3, 1])
        with top_c1:
             st.markdown("""
             <div style="display:flex; align-items:center; gap:10px; height:100%;">
                <span style="font-size:20px;">💡</span>
                <span style="color:#64748b; font-size:14px;"><b>矩阵效率模式</b>：5 个线程并发处理，独立生成，互不干扰。</span>
             </div>
             """, unsafe_allow_html=True)
        with top_c2:
            run_batch = st.button("🚀 并行启动", type="primary", use_container_width=True)
            
        st.markdown("<div style='height:25px'></div>", unsafe_allow_html=True)
        
        # 输入区
        cols = st.columns(5, gap="small")
        inputs = []
        for i, col in enumerate(cols):
            with col:
                st.markdown(f"<div class='input-header' style='justify-content:center;'>通道 {i+1}</div>", unsafe_allow_html=True)
                val = st.text_area(f"in_{i}", height=150, key=f"bi_{i}_v3", placeholder="输入...", label_visibility="collapsed")
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
                    render_copy_btn(res, f"cp_b_{i}_v3")
                else:
                    st.markdown("<div style='height:245px; background:#f8fafc; border-radius:12px; border:1px dashed #e2e8f0; display:flex; align-items:center; justify-content:center; color:#cbd5e1;'>空闲</div>", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
