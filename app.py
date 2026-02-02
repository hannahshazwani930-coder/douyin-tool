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

# 注入 CSS：90% 自适应流体布局
st.markdown("""
<style>
    /* 1. 全局背景 */
    .stApp { 
        font-family: 'Helvetica Neue', Arial, sans-serif; 
        background-color: #f0f2f5; 
    }
    
    /* 🔥 核心修改：宽度设置为 90% 🔥 */
    div.block-container {
        max-width: 90% !important;     /* 强制占满 90% */
        min-width: 90% !important;     /* 保证不缩得太小 */
        background-color: #ffffff;     
        padding: 3rem !important;      
        margin: 2rem auto !important;  /* 上下留白，左右自动居中 */
        border-radius: 12px;           
        box-shadow: 0 4px 20px rgba(0,0,0,0.08); 
    }

    /* 2. 侧边栏 */
    [data-testid="stSidebar"] { 
        background-color: #ffffff; 
        border-right: 1px solid #e0e0e0; 
    }
    
    /* 3. 内部卡片 (工作台) */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #f8f9fa; 
        border: 1px solid #eaeaea; 
        border-radius: 10px; 
        padding: 20px;
    }
    
    /* 4. 标题 */
    h1 { color: #1a202c; font-weight: 800 !important; text-align: center; margin-bottom: 30px !important;}
    h2, h3 { color: #2d3748; font-weight: 700 !important; }
    
    /* 5. 按钮美化 - 蓝色系 */
    div.stButton > button {
        border-radius: 6px; 
        font-weight: 600; 
        border: none; 
        height: 42px; 
        transition: all 0.2s;
    }
    div.stButton > button:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    
    /* 主按钮：科技蓝渐变 */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #3182ce 0%, #2b6cb0 100%);
        border: none;
    }

    /* 6. 输入框 */
    .stTextArea textarea, .stTextInput input {
        border-radius: 6px; 
        border: 1px solid #e2e8f0; 
        background-color: #ffffff;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #3182ce;
        box-shadow: 0 0 0 2px rgba(49, 130, 206, 0.2);
    }
    
    /* 7. 登录框垂直间距 */
    .login-spacer { height: 5vh; }
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
            with c1:
                input_key = f"input_{i}"
                st.text_area("原始文案", height=180, key=input_key, label_visibility="collapsed", placeholder="按 Ctrl+V 粘贴...")
                b1, b2 = st.columns([1, 3])
                b1.button("🗑️", key=f"clr_{i}", on_click=clear_text_callback, args=(input_key,), use_container_width=True)
                if b2.button(f"⚡ 仅生成 #{i}", key=f"btn_{i}", use_container_width=True):
                    val = st.session_state.get(input_key, "")
                    if val:
                        with st.spinner("生成中..."):
                            st.session_state['results'][i] = rewrite_logic(val)
                            st.rerun()
            with c2:
                res_val = st.session_state['results'].get(i, "")
                if res_val:
                    st.code(res_val, language='text')
                    st.toast(f"#{i} 已生成，可复制", icon="🎉")
                else:
                    st.markdown("<div style='color:#ccc; text-align:center; line-height:180px;'>等待生成...</div>", unsafe_allow_html=True)

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
