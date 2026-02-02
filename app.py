import streamlit as st
from openai import OpenAI
import time
from concurrent.futures import ThreadPoolExecutor 

# ==========================================
# 0. 核心配置
# ==========================================
st.set_page_config(
    page_title="抖音爆款工场 Pro", 
    layout="wide",
    page_icon="💠",
    initial_sidebar_state="expanded"
)

# 注入 CSS：极致 UI 美化版
st.markdown("""
<style>
    /* 1. 全局字体与背景 */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    .stApp { 
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; 
        background-color: #f8fafc; /* 极简冷灰背景 */
    }
    
    /* 2. 布局容器：90% 宽度 + 悬浮白纸效果 */
    div.block-container {
        max-width: 90% !important;
        min-width: 90% !important;
        background-color: #ffffff;
        padding: 3rem !important;
        margin: 2rem auto !important;
        border-radius: 16px;
        box-shadow: 0 10px 40px -10px rgba(0,0,0,0.05); /* 更柔和的高级阴影 */
    }

    /* 3. 侧边栏：磨砂质感 */
    [data-testid="stSidebar"] { 
        background-color: #ffffff; 
        border-right: 1px solid #f1f5f9; 
    }
    
    /* 4. 工作台卡片：增加顶部高亮条 */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 24px;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    /* 鼠标悬停时卡片微微上浮 */
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: #cbd5e1;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }
    
    /* 5. 标题美化 */
    h1 { 
        color: #0f172a; 
        font-weight: 800 !important; 
        letter-spacing: -0.02em; 
        margin-bottom: 1.5rem !important;
    }
    h2, h3 { color: #334155; font-weight: 700 !important; }
    
    /* 6. 按钮极致美化 🔥 */
    
    /* (A) 通用按钮形态 */
    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
        font-size: 14px;
        height: 40px;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* (B) 次级按钮（清空/单条生成）：平时是高级灰，鼠标放上去变蓝 */
    div.stButton > button:not([kind="primary"]) {
        background-color: #f1f5f9; /* 浅灰底 */
        color: #475569;            /* 深灰字 */
        border: 1px solid transparent;
    }
    div.stButton > button:not([kind="primary"]):hover {
        background-color: #e0f2fe; /* 淡蓝底 */
        color: #0284c7;            /* 亮蓝字 */
        border-color: #bae6fd;     /* 蓝边框 */
        transform: translateY(-1px);
    }

    /* (C) 主按钮（一键并发）：极光蓝渐变 */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        border: none;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3); /* 弥散光影 */
    }
    div.stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4);
        transform: translateY(-1px);
    }
    div.stButton > button[kind="primary"]:active {
        transform: translateY(0);
    }

    /* 7. 输入框：聚焦光晕 */
    .stTextArea textarea, .stTextInput input {
        border-radius: 8px;
        border: 1px solid #cbd5e1;
        background-color: #f8fafc;
        transition: border 0.2s, box-shadow 0.2s;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        background-color: #ffffff;
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15); /* 蓝色柔光 */
    }

    /* 8. 空状态占位符（右侧等待区）美化 🔥 */
    .empty-state-box {
        height: 200px;
        background-image: repeating-linear-gradient(45deg, #f8fafc 25%, transparent 25%, transparent 75%, #f8fafc 75%, #f8fafc), repeating-linear-gradient(45deg, #f8fafc 25%, #ffffff 25%, #ffffff 75%, #f8fafc 75%, #f8fafc);
        background-position: 0 0, 10px 10px;
        background-size: 20px 20px;
        border: 2px dashed #e2e8f0;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #94a3b8;
        font-weight: 500;
        flex-direction: column;
        gap: 10px;
    }

    /* 登录框间距 */
    .login-spacer { height: 10vh; }
    
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. 登录与安全系统
# ==========================================

PASSWORD = "taoge888"

def clear_text_callback(key):
    if key in st.session_state:
        st.session_state[key] = ""

@st.cache_resource
def get_login_cache():
    return {}

def get_remote_ip():
    try:
        from streamlit.web.server.websocket_headers import _get_websocket_headers
        headers = _get_websocket_headers()
        return headers.get("X-Forwarded-For", headers.get("Remote-Addr", "unknown_ip"))
    except:
        return "unknown_ip"

def check_login():
    if st.session_state.get('is_logged_in', False):
        return True

    user_ip = get_remote_ip()
    current_time = time.time()
    login_cache = get_login_cache()
    
    if user_ip in login_cache and (current_time - login_cache[user_ip] < 172800):
        st.session_state['is_logged_in'] = True 
        return True 
        
    login_placeholder = st.empty()
    with login_placeholder.container():
        st.markdown("<div class='login-spacer'></div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 1.5, 1])
        with c2:
            st.markdown("<h2 style='text-align: center; margin-bottom: 20px;'>💠 爆款工场 Pro</h2>", unsafe_allow_html=True)
            st.info("🔒 系统已加密，获取密码请联系微信：TG777188", icon="🔑")
            
            with st.form("login_form"):
                pwd = st.text_input("请输入会员密码", type="password", placeholder="******")
                st.markdown("<br>", unsafe_allow_html=True)
                submitted = st.form_submit_button("🚀 立即解锁", type="primary", use_container_width=True)
            
            if submitted:
                if pwd == PASSWORD:
                    login_cache[user_ip] = current_time 
                    st.session_state['is_logged_in'] = True 
                    st.success("✅ 验证成功！")
                    time.sleep(0.5)
                    login_placeholder.empty()
                    st.rerun()
                else:
                    st.error("❌ 密码错误")
    return False

if not check_login():
    st.stop()

# ==========================================
# 2. API 配置
# ==========================================

try:
    api_key = st.secrets["DEEPSEEK_API_KEY"]
except:
    st.error("❌ 未检测到 DEEPSEEK_API_KEY，请在后台 Secrets 中配置。")
    st.stop()

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

# ==========================================
# 3. 功能模块
# ==========================================

# --- A. 文案改写 ---
def page_rewrite():
    st.markdown("## ⚡ 爆款文案改写中台")
    st.caption("AI 驱动的五路并发架构 | 40秒黄金完播率模型")
    st.markdown("---")

    if 'results' not in st.session_state:
        st.session_state['results'] = {}
        
    def rewrite_logic(content):
        if not content or len(content.strip()) < 5: return "⚠️ 内容过短"
        prompt = f"""
        你是一个抖音千万粉的口播博主。
        【原始素材】：{content}
        【任务】：清洗数据，改写为原创爆款文案。
        【公式】：黄金3秒开头 + 中间情绪饱满说人话 + 结尾强引导。
        【输出】：直接输出文案，200字左右。
        """
        try:
            res = client.chat.completions.create(
                model="deepseek-chat", messages=[{"role": "user", "content": prompt}], temperature=1.3
            )
            return res.choices[0].message.content
        except Exception as e: return f"Error: {e}"

    # 总控台
    col_main, col_tips = st.columns([1, 2])
    with col_main:
        if st.button("🚀 一键并发执行 (5路全开)", type="primary", use_container_width=True):
            tasks, indices = [], []
            for i in range(1, 6):
                text = st.session_state.get(f"input_{i}", "")
                if text.strip():
                    tasks.append(text)
                    indices.append(i)
            
            if not tasks:
                st.toast("⚠️ 请先输入文案", icon="🛑")
            else:
                with st.status("☁️ 云端计算中...", expanded=True) as status:
                    with ThreadPoolExecutor(max_workers=5) as executor:
                        results_list = list(executor.map(rewrite_logic, tasks))
                    for idx, res in zip(indices, results_list):
                        st.session_state['results'][idx] = res
                    status.update(label="✅ 完成！", state="complete", expanded=False)
                    st.rerun()
    with col_tips:
        st.info("💡 操作指南：将不同文案粘贴到下方 1-5 号窗口，点击左侧 **【蓝色按钮】** 同时处理。", icon="📝")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # 5个工作台
    for i in range(1, 6):
        with st.container(border=True):
            st.markdown(f"#### 🎬 工作台 #{i}")
            c1, c2 = st.columns([1, 1], gap="large")
            
            # 左侧：输入区
            with c1:
                input_key = f"input_{i}"
                st.text_area("原始文案", height=200, key=input_key, label_visibility="collapsed", placeholder="💡在此按 Ctrl+V 粘贴提取的文案...")
                
                b1, b2 = st.columns([1, 2.5])
                # 次级按钮
                b1.button("🗑️ 清空", key=f"clr_{i}", on_click=clear_text_callback, args=(input_key,), use_container_width=True)
                # 次级按钮
                if b2.button(f"⚡ 仅生成 #{i}", key=f"btn_{i}", use_container_width=True):
                    val = st.session_state.get(input_key, "")
                    if val:
                        with st.spinner("生成中..."):
                            st.session_state['results'][i] = rewrite_logic(val)
                            st.rerun()
            
            # 右侧：结果区 (美化后的空状态)
            with c2:
                res_val = st.session_state['results'].get(i, "")
                if res_val:
                    st.code(res_val, language='text')
                    st.toast(f"#{i} 已生成，可复制", icon="🎉")
                else:
                    # 使用 HTML/CSS 渲染美观的空状态
                    st.markdown("""
                    <div class="empty-state-box">
                        <div style="font-size: 24px;">⏳</div>
                        <div>等待指令...</div>
                        <div style="font-size: 12px; color: #cbd5e1;">Input content to generate</div>
                    </div>
                    """, unsafe_allow_html=True)

# --- B. 别名创建 ---
def page_alias_creation():
    st.markdown("## 🎭 剧名别名生成")
    st.caption("防屏蔽 | 矩阵分发专用")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        original_name = st.text_input("🎬 原剧名/原书名", placeholder="例如：霸道总裁爱上我")
    with col2:
        count = st.slider("生成数量", 5, 20, 10)
    
    tags = st.multiselect("🏷️ 强化元素", ["高甜", "复仇", "逆袭", "悬疑", "虐恋", "豪门"], default=["逆袭", "高甜"])
    
    if st.button("🚀 生成别名", type="primary", use_container_width=True):
        if not original_name:
            st.toast("请输入原名", icon="🛑")
        else:
            prompt = f"""
            请将《{original_name}》改写为{count}个推广别名。
            策略：加入“{'、'.join(tags)}”元素，去原名化，直击痛点。
            输出：只输出别名列表，一行一个。
            """
            try:
                with st.spinner("生成中..."):
                    res = client.chat.completions.create(
                        model="deepseek-chat", messages=[{"role": "user", "content": prompt}], temperature=1.4
                    )
                    st.session_state['alias_result'] = res.choices[0].message.content
            except Exception as e: st.error(f"Error: {e}")

    if 'alias_result' in st.session_state:
        st.info("💡 点击右上角图标复制", icon="📋")
        st.code(st.session_state['alias_result'], language='text')

# --- C. 账号起名 ---
def page_naming():
    st.markdown("## 🏷️ 账号/IP 起名大师")
    st.markdown("---")
    
    c1, c2 = st.columns(2)
    with c1:
        niche = st.selectbox("🎯 赛道", ["短剧", "小说", "口播", "情感", "带货"])
    with c2:
        style = st.selectbox("🎨 风格", ["高冷", "搞笑", "文艺", "粗暴", "反差"])
    keywords = st.text_input("🔑 关键词 (选填)")
    
    if st.button("🎲 生成名字", type="primary", use_container_width=True):
        prompt = f"为【{niche}】赛道生成10个{style}风格账号名，含关键词：{keywords}。格式：名字+解释。"
        try:
            with st.spinner("生成中..."):
                res = client.chat.completions.create(
                    model="deepseek-chat", messages=[{"role": "user", "content": prompt}], temperature=1.5
                )
                st.session_state['naming_result'] = res.choices[0].message.content
        except Exception as e: st.error(str(e))

    if 'naming_result' in st.session_state:
        st.code(st.session_state['naming_result'], language='text')

# --- D. 个人中心 ---
def page_account():
    st.markdown("## 👤 我的账户")
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.metric("会员状态", "VIP 专业版", delta="永久激活")
            st.text_input("绑定 IP", value=get_remote_ip(), disabled=True)
    with col2:
        with st.container(border=True):
            st.markdown("#### 💬 联系客服")
            st.markdown("**微信 ID**: `TG777188`")

# ==========================================
# 4. 侧边栏导航
# ==========================================

with st.sidebar:
    st.markdown("### 💠 爆款工场 Pro")
    st.markdown(f"<small>IP: {get_remote_ip()}</small>", unsafe_allow_html=True)
    st.markdown("---")
    
    menu_option = st.radio(
        "导航",
        ["📝 文案改写", "🎭 创建别名", "🏷️ 账号起名", "👤 我的账户"],
        index=0, label_visibility="collapsed"
    )
    
    st.markdown("---")
    with st.container(border=True):
        st.info("已升级至 Pro 内核，速度提升 500%。", icon="🚀")

if menu_option == "📝 文案改写": page_rewrite()
elif menu_option == "🎭 创建别名": page_alias_creation()
elif menu_option == "🏷️ 账号起名": page_naming()
elif menu_option == "👤 我的账户": page_account()
