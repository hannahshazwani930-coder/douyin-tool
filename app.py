import streamlit as st
from openai import OpenAI
import time
from concurrent.futures import ThreadPoolExecutor 

# ==========================================
# 🎨 0. 全局 UI 配置
# ==========================================
st.set_page_config(page_title="抖音爆款工场 Pro", layout="wide", page_icon="💠")

# 注入 CSS
st.markdown("""
<style>
    .stApp { font-family: 'PingFang SC', 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    [data-testid="stSidebar"] { background-color: #f0f2f6; border-right: 1px solid #e0e0e0; }
    h1, h2, h3 { color: #2C3E50; font-weight: 700 !important; }
    div.stButton > button { border-radius: 8px; font-weight: 600; transition: all 0.3s; }
    .stCode { font-size: 1.1em; }
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        background-color: white;
        padding: 20px;
    }
    @media (prefers-color-scheme: dark) {
        [data-testid="stVerticalBlockBorderWrapper"] { background-color: #262730; }
        [data-testid="stSidebar"] { background-color: #1e1e1e; border-right: 1px solid #333; }
        h1, h2, h3 { color: #eee; }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 🔐 1. 登录与安全系统 (修复核心)
# ==========================================

PASSWORD = "taoge888"

def clear_text_callback(key):
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
    # 1. 优先检查本地 Session 状态 (最快)
    if st.session_state.get('is_logged_in', False):
        return True

    user_ip = get_remote_ip()
    current_time = time.time()
    login_cache = get_login_cache()
    
    # 2. 检查 IP 缓存 (48小时免密)
    if user_ip in login_cache and (current_time - login_cache[user_ip] < 172800):
        st.session_state['is_logged_in'] = True 
        return True 
        
    # --- 登录界面 (使用占位符清空模式) ---
    login_container = st.empty() # 创建一个占位符
    
    with login_container.container():
        st.markdown("<br><br><br>", unsafe_allow_html=True) 
        c1, c2, c3 = st.columns([1, 1.5, 1])
        with c2:
            with st.container(border=True):
                st.markdown("<h2 style='text-align: center;'>💠 爆款工场 Pro</h2>", unsafe_allow_html=True)
                st.info("🔑 获取密码请联系微信：TG777188", icon="💬")
                
                # 表单逻辑
                with st.form("login_form"):
                    pwd = st.text_input("请输入会员密码", type="password")
                    # 这里的按钮只是提交表单
                    submitted = st.form_submit_button("🚀 立即解锁", type="primary", use_container_width=True)
                
                # 逻辑判断放在表单外面或紧接着表单
                if submitted:
                    if pwd == PASSWORD:
                        # 1. 记录状态
                        login_cache[user_ip] = current_time 
                        st.session_state['is_logged_in'] = True 
                        # 2. 提示成功
                        st.success("✅ 验证成功！正在进入系统...")
                        # 3. 清空登录界面
                        login_container.empty()
                        # 4. 强制刷新
                        st.rerun()
                    else:
                        st.error("❌ 密码错误，请重试")
    
    # 如果没登录，返回 False，程序会在下面停止
    return False

# 🛑 如果未登录，直接停止后续代码运行
if not check_login():
    st.stop()

# ==========================================
# ⚙️ 2. API 配置
# ==========================================

try:
    api_key = st.secrets["DEEPSEEK_API_KEY"]
except:
    st.error("⚠️ 请先在 Settings -> Secrets 里配置 DEEPSEEK_API_KEY")
    st.stop()

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

# ==========================================
# 🧩 3. 功能模块函数化
# ==========================================

# --- 功能 A: 文案改写 ---
def page_rewrite():
    st.markdown("## ⚡ 爆款文案改写中台")
    st.caption("五路并发架构 | 自动清洗杂质 | 40秒黄金完播率模型")
    
    if 'results' not in st.session_state:
        st.session_state['results'] = {}
        
    def rewrite_logic(content):
        if not content or len(content.strip()) < 5: return "⚠️ 内容太短"
        prompt = f"""
        你是一个抖音千万粉的口播博主。
        【原始素材】：{content}
        【任务】：清洗数据，暴力改写为原创爆款文案。
        【公式】：黄金3秒开头（反直觉/焦虑）+ 中间说人话（情绪饱满）+ 结尾强引导。
        【输出】：直接输出文案，200字左右。
        """
        try:
            res = client.chat.completions.create(
                model="deepseek-chat", messages=[{"role": "user", "content": prompt}], temperature=1.3
            )
            return res.choices[0].message.content
        except Exception as e: return f"Error: {e}"

    with st.container(border=True):
        col_main, col_tips = st.columns([1, 3])
        with col_main:
            if st.button("🚀 一键并发执行 (提速500%)", type="primary", use_container_width=True):
                tasks, indices = [], []
                for i in range(1, 6):
                    text = st.session_state.get(f"input_{i}", "")
                    if text.strip():
                        tasks.append(text)
                        indices.append(i)
                
                if not tasks:
                    st.toast("请先在下方输入素材", icon="⚠️")
                else:
                    with st.status("正在进行云端计算...", expanded=True) as status:
                        with ThreadPoolExecutor(max_workers=5) as executor:
                            results_list = list(executor.map(rewrite_logic, tasks))
                        for idx, res in zip(indices, results_list):
                            st.session_state['results'][idx] = res
                        status.update(label="✅ 生成完毕", state="complete", expanded=False)
                        st.rerun()
        with col_tips:
            st.markdown("*💡 提示：将不同视频的提取文案粘贴到下方窗口，点击左侧按钮同时生成。*")

    st.markdown("<br>", unsafe_allow_html=True)
    for i in range(1, 6):
        with st.container(border=True):
            st.markdown(f"**🎬 工作台 #{i}**")
            c1, c2 = st.columns([1, 1], gap="large")
            with c1:
                input_key = f"input_{i}"
                st.text_area("输入", height=150, key=input_key, label_visibility="collapsed", placeholder="按 Ctrl+V 粘贴...")
                b1, b2 = st.columns([1, 3])
                b1.button("🗑️", key=f"clr_{i}", on_click=clear_text_callback, args=(input_key,), use_container_width=True, help="清空")
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
                    st.info("等待生成...", icon="⏳")

# --- 功能 B: 别名创建 ---
def page_alias_creation():
    st.markdown("## 🎭 剧名别名生成")
    st.caption("为短剧/小说生成高转化率的推广别名，防屏蔽、增点击、做矩阵。")
    
    with st.container(border=True):
        c1, c2 = st.columns([2, 1])
        with c1:
            original_name = st.text_input("🎬 原剧名/原书名", placeholder="例如：霸道总裁爱上我")
        with c2:
            count = st.slider("生成数量", min_value=5, max_value=20, value=10)
            
        tags = st.multiselect("🏷️ 强化元素 (可多选)", ["高甜", "复仇", "逆袭", "悬疑", "虐恋", "豪门"], default=["逆袭", "高甜"])
        
        if st.button("🚀 生成推广别名", type="primary", use_container_width=True):
            if not original_name:
                st.toast("请先输入原名！", icon="🛑")
            else:
                tag_str = "、".join(tags)
                prompt = f"""
                你是一个短剧/小说推广专家。请将原名《{original_name}》改写为 {count} 个用于“拉新推广”的爆款别名。
                策略：加入“{tag_str}”元素，去原名化，直击下沉市场痛点。
                只输出别名列表，一行一个，不要带序号。
                """
                try:
                    with st.spinner("正在构思爆款别名..."):
                        res = client.chat.completions.create(
                            model="deepseek-chat", messages=[{"role": "user", "content": prompt}], temperature=1.4
                        )
                        st.session_state['alias_result'] = res.choices[0].message.content
                except Exception as e:
                    st.error(str(e))

    if 'alias_result' in st.session_state:
        st.markdown("### ✨ 推荐别名列表")
        st.info("💡 提示：这些名字专为“拉新”设计，点击右上角复制，直接用于视频标题或评论区引导。")
        st.code(st.session_state['alias_result'], language='text')

# --- 功能 C: 账号起名 ---
def page_naming():
    st.markdown("## 🏷️ 爆款账号/IP 起名大师")
    st.caption("基于平台算法逻辑，生成高辨识度、易记忆、带人设的名称。")
    
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            niche = st.selectbox("🎯 赛道/领域", ["短剧推广", "小说推文", "口播知识", "情感鸡汤", "带货测评", "其他"])
        with c2:
            style = st.selectbox("🎨 风格偏好", ["高冷专业风", "接地气/搞笑", "文艺有内涵", "简单粗暴", "神秘反差"])
            
        keywords = st.text_input("🔑 核心关键词 (选填)", placeholder="输入你想包含的字...")
        
        if st.button("🎲 生成 10 个爆款名", type="primary", use_container_width=True):
            prompt = f"""
            请为【{niche}】赛道的账号生成10个爆款名字。
            风格：{style}。包含关键词：{keywords}。
            要求：记忆点强，符合平台调性。
            输出格式：名字 + 一句话解释。
            """
            try:
                with st.spinner("正在头脑风暴中..."):
                    res = client.chat.completions.create(
                        model="deepseek-chat", messages=[{"role": "user", "content": prompt}], temperature=1.5
                    )
                    st.session_state['naming_result'] = res.choices[0].message.content
            except Exception as e:
                st.error(str(e))

    if 'naming_result' in st.session_state:
        st.markdown("### ✨ 生成结果")
        st.code(st.session_state['naming_result'], language='text')

# --- 功能 D: 个人中心 ---
def page_account():
    st.markdown("## 👤 我的账户")
    with st.container(border=True):
        st.metric("当前状态", "VIP 会员", delta="已激活")
        st.text_input("绑定 IP", value=get_remote_ip(), disabled=True)
        st.markdown("---")
        st.markdown("**专属客服微信**：`TG777188`")
        st.caption("如需续费或增加并发额度，请联系客服。")

# ==========================================
# 🧭 4. 侧边栏导航与主控逻辑
# ==========================================

with st.sidebar:
    st.markdown("### 💠 爆款工场 Pro")
    st.markdown(f"<small>IP: {get_remote_ip()}</small>", unsafe_allow_html=True)
    st.markdown("---")
    
    menu_option = st.radio(
        "功能导航",
        ["📝 文案改写", "🎭 创建别名", "🏷️ 账号起名", "👤 我的账户"],
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    with st.container(border=True):
        st.markdown("#### 📢 公告")
        st.caption("新增功能：\n✨ 剧名/书名智能改写\n✨ 一键生成推广矩阵名")

# 路由分发
if menu_option == "📝 文案改写":
    page_rewrite()
elif menu_option == "🎭 创建别名":
    page_alias_creation()
elif menu_option == "🏷️ 账号起名":
    page_naming()
elif menu_option == "👤 我的账户":
    page_account()
