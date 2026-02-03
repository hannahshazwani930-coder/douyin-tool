# views/rewrite.py
import streamlit as st
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from utils import render_copy_btn
from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL

# --- 🎨 注入灵魂 CSS (修正版) ---
def load_immersive_css():
    st.markdown("""
    <style>
        /* 1. 布局优化：不再无脑全屏，而是宽幅居中，留出呼吸感 */
        div.block-container {
            max-width: 1400px !important; /* 限制最大宽幅，防止在大屏太散 */
            padding-top: 0 !important;
            padding-left: 40px !important; /* 左右留白 */
            padding-right: 40px !important;
            padding-bottom: 50px !important;
        }
        
        /* 2. 极光通栏 (修复斜角问题 -> 改为底部大圆角) */
        .immersive-header {
            background: linear-gradient(180deg, #0f172a 0%, #1e293b 60%, #3b82f6 100%);
            padding: 60px 40px 100px 40px; /* 底部多留白给 Tab */
            color: white; text-align: center;
            margin-bottom: -50px; /* 让 Tab 往上叠 */
            margin-left: -40px; margin-right: -40px; /* 抵消掉 padding 实现通栏 */
            border-bottom-left-radius: 40px; /* 优雅的圆角 */
            border-bottom-right-radius: 40px;
            box-shadow: 0 20px 50px -10px rgba(15, 23, 42, 0.5);
            position: relative; z-index: 0;
        }
        .header-title { font-size: 38px; font-weight: 800; letter-spacing: -0.5px; margin-bottom: 15px; text-shadow: 0 5px 15px rgba(0,0,0,0.3); }
        .header-sub { font-size: 16px; opacity: 0.95; font-weight: 400; background: rgba(255,255,255,0.15); padding: 6px 20px; border-radius: 30px; backdrop-filter: blur(10px); display: inline-block; border: 1px solid rgba(255,255,255,0.1); }

        /* 3. 魔改 Tab -> 悬浮岛式切换栏 */
        .stTabs { 
            margin-top: -30px; 
            position: relative; z-index: 10;
        }
        div[data-baseweb="tab-list"] { 
            justify-content: center; gap: 20px; border: none !important; 
            background: rgba(255,255,255,0.9); padding: 10px; border-radius: 100px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1); width: fit-content; margin: 0 auto 40px auto; /* 居中且下留白 */
            backdrop-filter: blur(20px);
        }
        div[data-baseweb="tab"] {
            background-color: transparent !important;
            border-radius: 50px !important; padding: 12px 40px !important; /* 加宽按钮 */
            border: none !important; box-shadow: none !important;
            color: #64748b !important; font-weight: 600 !important; font-size: 16px !important;
            transition: all 0.3s ease !important;
        }
        /* 选中状态 */
        div[data-baseweb="tab"][aria-selected="true"] {
            background: #2563eb !important; color: white !important;
            box-shadow: 0 5px 15px rgba(37, 99, 235, 0.4) !important;
        }

        /* 4. 工作区容器 */
        .glass-card {
            background: white; border-radius: 24px; padding: 40px; /* 内部留白加大 */
            box-shadow: 0 20px 40px -10px rgba(0,0,0,0.05); border: 1px solid #f1f5f9;
        }

        /* 5. 输入框美化 (增加顶部标题条) */
        .input-header { font-size: 14px; font-weight: 700; color: #334155; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; }
        .stTextArea textarea {
            background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 16px;
            padding: 20px; font-size: 15px; line-height: 1.6;
        }
        .stTextArea textarea:focus { background: white; border-color: #3b82f6; box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1); }

        /* 6. 转化提示条 */
        .conversion-tip {
            margin-top: 15px; background: #ecfdf5; border: 1px solid #a7f3d0;
            color: #065f46; padding: 12px 15px; border-radius: 12px; font-size: 13px;
            display: flex; align-items: center; gap: 10px; animation: fadeIn 0.5s ease;
        }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }

        /* 去除 Streamlit 默认顶部空白 */
        .stApp { background-color: #f8fafc; }
        
        /* 针对页面按钮的优化 */
        div.stButton button[kind="primary"] {
            width: 100%; height: 50px; background: linear-gradient(90deg, #2563eb, #3b82f6) !important;
            border-radius: 12px !important; font-size: 16px !important; letter-spacing: 1px;
            box-shadow: 0 10px 20px -5px rgba(37, 99, 235, 0.3) !important;
        }
        div.stButton button[kind="primary"]:hover { transform: translateY(-2px); box-shadow: 0 15px 25px -5px rgba(37, 99, 235, 0.5) !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DeepSeek 调用 ---
def call_deepseek_rewrite(content, style_prompt):
    if not DEEPSEEK_API_KEY or "sk-" not in DEEPSEEK_API_KEY:
        return "❌ 配置错误：请在 config.py 中填入正确的 DEEPSEEK_API_KEY"

    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    system_prompt = f"""
    你是由抖音爆款工场开发的顶级文案专家。请对用户输入的文案进行【{style_prompt}】方向的改写。
    核心要求：1.深度去重；2.语言更有网感和穿透力；3.适当使用emoji增加视觉留存；4.直接输出结果，不要废话。
    """
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": content}],
        "temperature": 1.3, "stream": False
    }
    try:
        response = requests.post(f"{DEEPSEEK_BASE_URL}/chat/completions", headers=headers, json=data, timeout=60)
        if response.status_code == 200: return response.json()['choices'][0]['message']['content']
        else: return f"❌ API 报错: {response.status_code} - {response.text}"
    except Exception as e: return f"❌ 网络错误: {str(e)}"

# --- 转化提示条组件 ---
def render_conversion_tip():
    st.markdown("""
    <div class="conversion-tip">
        <span style="font-size:18px;">💡</span>
        <span><b>增长黑客建议：</b> 试着在文案末尾添加“领取资料”或“点击主页”的钩子，私域转化率平均可提升 30%！</span>
    </div>
    """, unsafe_allow_html=True)

# --- 主视图 ---
def view_rewrite():
    load_immersive_css()
    
    # 1. 极光通栏 Header (底部平滑圆角，无斜角)
    st.markdown("""
    <div class="immersive-header">
        <div class="header-title">✨ 文案改写 Pro</div>
        <div class="header-sub">DeepSeek V3 深度驱动 · 全网去重 · 爆款逻辑重构</div>
    </div>
    """, unsafe_allow_html=True)
    
    # State Init
    if 'rw_single_res' not in st.session_state: st.session_state.rw_single_res = ""
    if 'rw_batch_res' not in st.session_state: st.session_state.rw_batch_res = [""] * 5

    # 2. 悬浮岛式 Tab 切换
    tab_single, tab_batch = st.tabs(["⚡ 单条精修模式", "🚀 5路矩阵模式"])
    
    # === 模式 A: 单条精修 ===
    with tab_single:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        # 左右双栏布局 (加宽间距)
        c_left, c_right = st.columns(2, gap="large")
        
        # 左侧：输入与操作
        with c_left:
            st.markdown('<div class="input-header">📝 原始内容输入</div>', unsafe_allow_html=True)
            content = st.text_area("in", height=400, placeholder="在此粘贴文案...", label_visibility="collapsed")
            
            st.markdown("<div style='height:25px'></div>", unsafe_allow_html=True)
            
            # 风格选择 + 按钮
            cc1, cc2 = st.columns([1, 1.2])
            with cc1:
                style = st.selectbox("风格偏好", ["标准去重", "爆款悬疑", "情感共鸣", "硬核干货", "幽默反转"], label_visibility="collapsed")
            with cc2:
                run_single = st.button("✨ 立即生成爆款", type="primary", use_container_width=True)
                
            if run_single:
                if content:
                    with st.spinner("DeepSeek 正在重构逻辑..."):
                        st.session_state.rw_single_res = call_deepseek_rewrite(content, style)
                else:
                    st.toast("⚠️ 内容不能为空")

        # 右侧：结果展示
        with c_right:
            st.markdown('<div class="input-header">🎯 AI 改写结果</div>', unsafe_allow_html=True)
            
            if st.session_state.rw_single_res:
                st.text_area("out", value=st.session_state.rw_single_res, height=400, label_visibility="collapsed")
                
                # 底部工具栏 + 转化提示
                render_copy_btn(st.session_state.rw_single_res, "copy_single_fix")
                render_conversion_tip() # 新增提示条
            else:
                st.markdown("""
                <div style="height:480px; background:#f8fafc; border-radius:16px; border:2px dashed #e2e8f0; display:flex; flex-direction:column; align-items:center; justify-content:center; color:#94a3b8;">
                    <div style="font-size:56px; margin-bottom:20px; opacity:0.3;">🪄</div>
                    <div style="font-size:16px; font-weight:500;">等待 AI 施展魔法...</div>
                    <div style="font-size:13px; opacity:0.7; margin-top:5px;">请在左侧输入文案并点击生成</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # === 模式 B: 5路矩阵 ===
    with tab_batch:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        # 顶部操作条
        top_c1, top_c2 = st.columns([3, 1])
        with top_c1:
             st.markdown("""
             <div style="display:flex; align-items:center; gap:10px; height:100%;">
                <span style="font-size:20px;">💡</span>
                <span style="color:#64748b; font-size:14px;">矩阵模式：同时调用 5 个并发线程，独立处理，效率提升 500%</span>
             </div>
             """, unsafe_allow_html=True)
        with top_c2:
            run_batch = st.button("🚀 并行启动", type="primary", use_container_width=True)
            
        st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
        
        # 5列输入
        cols = st.columns(5, gap="medium")
        inputs = []
        for i, col in enumerate(cols):
            with col:
                st.markdown(f"<div class='input-header'>通道 {i+1}</div>", unsafe_allow_html=True)
                val = st.text_area(f"in_{i}", height=180, key=f"bi_{i}_fix", placeholder="输入...", label_visibility="collapsed")
                inputs.append(val)
        
        # 5列输出
        if run_batch:
            valid = [(i, t) for i, t in enumerate(inputs) if t.strip()]
            if valid:
                status = st.status(f"正在并行处理 {len(valid)} 个任务...", expanded=True)
                with ThreadPoolExecutor(max_workers=5) as ex:
                    f_map = {ex.submit(call_deepseek_rewrite, t, "标准去重"): i for i, t in valid}
                    for f in f_map:
                        try:
                            st.session_state.rw_batch_res[f_map[f]] = f.result()
                        except:
                            st.session_state.rw_batch_res[f_map[f]] = "Error"
                status.update(label="✅ 完成", state="complete", expanded=False)
        
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        
        res_cols = st.columns(5, gap="medium")
        for i, col in enumerate(res_cols):
            with col:
                res = st.session_state.rw_batch_res[i]
                if res:
                    st.text_area(f"out_{i}", value=res, height=250, label_visibility="collapsed")
                    render_copy_btn(res, f"cp_b_{i}_fix")
                    if i == 0: # 仅在第一个显示提示，避免重复
                         st.markdown("""<div style="font-size:12px; color:#059669; margin-top:5px;">💡 记得加私域钩子</div>""", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='height:250px; background:#f8fafc; border-radius:12px; border:1px dashed #e2e8f0; display:flex; align-items:center; justify-content:center; color:#cbd5e1;'>空闲</div>", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
