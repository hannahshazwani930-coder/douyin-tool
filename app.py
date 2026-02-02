import streamlit as st
import sqlite3
import datetime
import uuid
import hashlib
import random
import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import streamlit.components.v1 as components 

# ==========================================
# 0. 核心配置 & 数据库初始化
# ==========================================
st.set_page_config(
    page_title="抖音爆款工场 Pro", 
    layout="wide",
    page_icon="💠",
    initial_sidebar_state="expanded"
)

# 🔑 管理员专属手机号 (请修改为你自己的手机号)
ADMIN_PHONE = "13800000000" 

# 数据库文件
DB_FILE = 'saas_data.db'

def init_db():
    """初始化多表数据库"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # 1. 用户表
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (phone TEXT PRIMARY KEY, 
                  password_hash TEXT, 
                  register_time TIMESTAMP,
                  last_login_ip TEXT,
                  last_login_time TIMESTAMP)''')
                  
    # 2. 卡密表 (增加 user_phone 字段，绑定用户)
    c.execute('''CREATE TABLE IF NOT EXISTS access_codes
                 (code TEXT PRIMARY KEY, 
                  duration_days INTEGER, 
                  activated_at TIMESTAMP, 
                  expire_at TIMESTAMP, 
                  status TEXT,
                  create_time TIMESTAMP,
                  bind_user TEXT)''') # bind_user: 绑定的手机号
    
    # 3. 反馈表
    c.execute('''CREATE TABLE IF NOT EXISTS feedbacks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_phone TEXT,
                  content TEXT,
                  reply TEXT,
                  create_time TIMESTAMP,
                  status TEXT)''') # status: pending, replied
                  
    conn.commit()
    conn.close()

init_db()

# --- 工具函数 ---

def hash_password(password):
    """密码加密"""
    return hashlib.sha256(password.encode()).hexdigest()

def get_remote_ip():
    """获取用户 IP"""
    try:
        from streamlit.web.server.websocket_headers import _get_websocket_headers
        headers = _get_websocket_headers()
        return headers.get("X-Forwarded-For", headers.get("Remote-Addr", "unknown_ip"))
    except:
        return "unknown_ip"

def send_mock_sms(phone):
    """模拟发送短信验证码"""
    code = str(random.randint(1000, 9999))
    # 真实场景这里会调用阿里云/腾讯云 API
    return code

# --- 业务逻辑函数 ---

def register_user(phone, password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (phone, password_hash, register_time) VALUES (?, ?, ?)", 
                  (phone, hash_password(password), datetime.datetime.now()))
        conn.commit()
        return True, "注册成功"
    except sqlite3.IntegrityError:
        return False, "该手机号已注册"
    finally:
        conn.close()

def login_user(phone, password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE phone=?", (phone,))
    row = c.fetchone()
    conn.close()
    
    if row and row[0] == hash_password(password):
        # 更新登录 IP
        update_login_ip(phone)
        return True, "登录成功"
    return False, "手机号或密码错误"

def update_login_ip(phone):
    ip = get_remote_ip()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE users SET last_login_ip=?, last_login_time=? WHERE phone=?", (ip, datetime.datetime.now(), phone))
    conn.commit()
    conn.close()

def reset_password(phone, new_password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE users SET password_hash=? WHERE phone=?", (hash_password(new_password), phone))
    if c.rowcount > 0:
        conn.commit(); conn.close()
        return True, "密码重置成功"
    conn.close()
    return False, "手机号未注册"

def check_ip_auto_login():
    """尝试通过 IP 自动登录 (简易版)"""
    ip = get_remote_ip()
    if ip == "unknown_ip": return None
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # 查找最近 7 天内使用该 IP 登录的用户
    seven_days_ago = datetime.datetime.now() - datetime.timedelta(days=7)
    c.execute("SELECT phone FROM users WHERE last_login_ip=? AND last_login_time > ?", (ip, seven_days_ago))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def activate_code(user_phone, code):
    """激活卡密并绑定到用户"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM access_codes WHERE code=?", (code,))
    row = c.fetchone()
    
    if not row:
        conn.close(); return False, "❌ 卡密不存在"
    
    status = row[4]
    
    if status == 'unused':
        duration = row[1]
        now = datetime.datetime.now()
        expire_date = now + datetime.timedelta(days=duration)
        # 激活并绑定
        c.execute("UPDATE access_codes SET status='active', activated_at=?, expire_at=?, bind_user=? WHERE code=?", 
                  (now, expire_date, user_phone, code))
        conn.commit(); conn.close()
        return True, f"✅ 激活成功！增加了 {duration} 天权限"
    else:
        conn.close(); return False, "⛔ 卡密已被使用或过期"

def get_user_vip_status(phone):
    """查询用户的所有有效卡密，计算最大过期时间"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    now = datetime.datetime.now()
    # 查询该用户绑定的所有未过期卡密
    c.execute("SELECT expire_at FROM access_codes WHERE bind_user=? AND status='active'", (phone,))
    rows = c.fetchall()
    conn.close()
    
    if not rows:
        return False, "未开通会员"
    
    # 找出最晚的过期时间
    max_expire = None
    for r in rows:
        exp = datetime.datetime.strptime(str(r[0]).split('.')[0], '%Y-%m-%d %H:%M:%S')
        if not max_expire or exp > max_expire:
            max_expire = exp
            
    if max_expire and max_expire > now:
        days_left = (max_expire - now).days
        return True, f"VIP 有效期至：{max_expire.strftime('%Y-%m-%d')} (剩余 {days_left} 天)"
    else:
        return False, "会员已过期"

def submit_feedback(phone, content):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO feedbacks (user_phone, content, create_time, status) VALUES (?, ?, ?, ?)",
              (phone, content, datetime.datetime.now(), 'pending'))
    conn.commit(); conn.close()

# --- CSS 样式 ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    .stApp { font-family: 'Inter', sans-serif; background-color: #f8fafc; }
    
    /* 登录框美化 */
    .auth-container { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); }
    .auth-title { text-align: center; font-weight: 800; font-size: 24px; color: #1e293b; margin-bottom: 20px; }
    
    /* 通用组件美化 */
    div.block-container { max-width: 90% !important; background-color: #ffffff; padding: 3rem !important; margin: 2rem auto !important; border-radius: 16px; box-shadow: 0 10px 40px -10px rgba(0,0,0,0.05); }
    div.stButton > button[kind="primary"] { background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); border: none; color: white !important; font-weight: 600; height: 45px; border-radius: 8px; transition: transform 0.2s; }
    div.stButton > button[kind="primary"]:hover { transform: translateY(-2px); box-shadow: 0 6px 15px rgba(37, 99, 235, 0.3); }
    
    /* 验证码按钮 */
    .verify-btn { font-size: 12px; padding: 5px 10px; border-radius: 4px; background: #e2e8f0; color: #475569; border: none; cursor: pointer; }
    
    /* 反馈气泡 */
    .chat-bubble { background: #f1f5f9; padding: 10px; border-radius: 8px; margin-bottom: 8px; font-size: 14px; }
    .chat-meta { font-size: 12px; color: #94a3b8; margin-bottom: 4px; }
    
    /* 商业化组件 */
    .project-box { background-color: #f0f9ff; border: 1px solid #bae6fd; padding: 12px; border-radius: 8px; margin-bottom: 10px; }
    .project-title { font-weight: bold; color: #0369a1; font-size: 14px; }
    .project-desc { font-size: 12px; color: #334155; margin-top: 4px; }
    
    a.redirect-btn { display: flex !important; align-items: center; justify-content: center; width: 100%; height: 50px; background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); color: white !important; border-radius: 8px; text-decoration: none; font-weight: 700; box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3); }
    
    .login-spacer { height: 5vh; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. 认证中心 (登录/注册/找回)
# ==========================================

if 'user_phone' not in st.session_state:
    # 尝试自动登录
    auto_phone = check_ip_auto_login()
    if auto_phone:
        st.session_state['user_phone'] = auto_phone
        st.toast(f"欢迎回来，{auto_phone} (已自动登录)", icon="👋")
        time.sleep(1)
        st.rerun()

def auth_page():
    st.markdown("<div class='login-spacer'></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        with st.container():
            st.markdown("<div class='auth-title'>💠 爆款工场 Pro</div>", unsafe_allow_html=True)
            
            tab1, tab2, tab3 = st.tabs(["🔐 登录", "✨ 注册", "🆘 找回密码"])
            
            # --- 登录 ---
            with tab1:
                with st.form("login"):
                    phone = st.text_input("手机号", key="login_phone")
                    pwd = st.text_input("密码", type="password", key="login_pwd")
                    if st.form_submit_button("立即登录", type="primary", use_container_width=True):
                        success, msg = login_user(phone, pwd)
                        if success:
                            st.session_state['user_phone'] = phone
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
            
            # --- 注册 ---
            with tab2:
                c_col1, c_col2 = st.columns([2, 1])
                reg_phone = c_col1.text_input("手机号", key="reg_phone")
                
                # 模拟发送验证码
                if c_col2.button("获取验证码", key="get_code_reg", use_container_width=True):
                    if len(reg_phone) == 11:
                        code = send_mock_sms(reg_phone)
                        st.session_state['mock_code'] = code
                        st.toast(f"【模拟短信】验证码是：{code}", icon="📩")
                    else:
                        st.toast("请输入正确手机号", icon="⚠️")
                
                reg_code = st.text_input("验证码", key="reg_code_input", placeholder="输入刚才的验证码")
                reg_pwd = st.text_input("设置密码", type="password", key="reg_pwd")
                
                if st.button("注册账号", type="primary", use_container_width=True):
                    if st.session_state.get('mock_code') == reg_code:
                        success, msg = register_user(reg_phone, reg_pwd)
                        if success:
                            st.success("注册成功！请前往登录页登录")
                        else:
                            st.error(msg)
                    else:
                        st.error("验证码错误")

            # --- 找回密码 ---
            with tab3:
                c_col1, c_col2 = st.columns([2, 1])
                find_phone = c_col1.text_input("手机号", key="find_phone")
                if c_col2.button("获取验证码", key="get_code_find", use_container_width=True):
                    code = send_mock_sms(find_phone)
                    st.session_state['mock_code_find'] = code
                    st.toast(f"【模拟短信】验证码是：{code}", icon="📩")
                
                find_code = st.text_input("验证码", key="find_code_input")
                new_pwd = st.text_input("新密码", type="password", key="new_pwd")
                
                if st.button("重置密码", type="primary", use_container_width=True):
                    if st.session_state.get('mock_code_find') == find_code:
                        success, msg = reset_password(find_phone, new_pwd)
                        if success: st.success(msg)
                        else: st.error(msg)
                    else:
                        st.error("验证码错误")

if 'user_phone' not in st.session_state:
    auth_page()
    st.stop()

# ==========================================
# 2. 登录后的主逻辑
# ==========================================

# 获取当前用户的会员状态
CURRENT_USER = st.session_state['user_phone']
IS_ADMIN = (CURRENT_USER == ADMIN_PHONE) # 检查是否是管理员
IS_VIP, VIP_MSG = get_user_vip_status(CURRENT_USER)

# 前端 JS 复制组件
def render_hover_copy_box(text, label="点击复制"):
    safe_text = text.replace("`", "\`").replace("'", "\\'")
    html_code = f"""
    <!DOCTYPE html><html><head><style>@import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;600&display=swap');body{{margin:0;padding:0;background:transparent;font-family:'Inter',sans-serif;overflow:hidden;}}.code-box{{display:flex;align-items:center;justify-content:space-between;background-color:#f8fafc;border:1px solid #cbd5e1;border-radius:6px;padding:0 10px;height:36px;cursor:pointer;transition:all 0.2s ease;color:#1e293b;font-weight:600;font-size:13px;box-sizing:border-box;}}.code-box:hover{{border-color:#3b82f6;background-color:#ffffff;box-shadow:0 0 0 2px rgba(59,130,246,0.1);}}.hint{{font-size:12px;color:#94a3b8;font-weight:400;}}.code-box:hover .hint{{color:#3b82f6;}}.code-box.success{{background-color:#ecfdf5;border-color:#10b981;color:#065f46;}}.code-box.success .hint{{color:#059669;}}</style></head><body><div class="code-box" onclick="copyText(this)"><span id="code-content">{safe_text}</span><span class="hint" id="status-text">{label}</span></div><script>function copyText(box){{const text=`{safe_text}`;const statusText=box.querySelector("#status-text");if(navigator.clipboard&&window.isSecureContext){{navigator.clipboard.writeText(text).then(()=>{{showSuccess(box,statusText);}}).catch(err=>{{fallbackCopyText(text,box,statusText);}});}}else{{fallbackCopyText(text,box,statusText);}}}}function fallbackCopyText(text,box,statusText){{const textArea=document.createElement("textarea");textArea.value=text;textArea.style.position="fixed";textArea.style.left="-9999px";document.body.appendChild(textArea);textArea.focus();textArea.select();try{{const successful=document.execCommand('copy');if(successful)showSuccess(box,statusText);}}catch(err){{statusText.innerText="❌";}}document.body.removeChild(textArea);}}function showSuccess(box,statusText){{box.classList.add("success");const originalHint="{label}";statusText.innerText="✅ 成功";setTimeout(()=>{{box.classList.remove("success");statusText.innerText=originalHint;}},1500);}}</script></body></html>
    """
    components.html(html_code, height=40)

# --- 侧边栏 ---
with st.sidebar:
    st.markdown(f"### 👋 Hi, {CURRENT_USER}")
    
    if IS_VIP:
        st.success(VIP_MSG)
    else:
        st.error("⚠️ 未激活会员")
        with st.expander("🔑 激活卡密", expanded=True):
            code_input = st.text_input("输入卡密", type="password", key="sidebar_code")
            if st.button("激活", type="primary"):
                success, msg = activate_code(CURRENT_USER, code_input)
                if success: st.success(msg); time.sleep(1); st.rerun()
                else: st.error(msg)
                
    st.markdown("---")
    st.markdown("#### 🔥 热门搞钱项目")
    st.markdown("""<div class="project-box"><div class="project-title">📹 素人 KOC 孵化</div><div class="project-desc">真人出镜口播，红果/番茄拉新，0基础陪跑。</div></div><div class="project-box"><div class="project-title">🎨 御灵 AI 动漫</div><div class="project-desc">小说转动漫视频，端原生+版权分销，高收益。</div></div>""", unsafe_allow_html=True)
    
    st.markdown("<div class='wechat-contact'>", unsafe_allow_html=True)
    st.markdown("<div class='wechat-item'><span class='wechat-label'>💼 营销咨询:</span></div>", unsafe_allow_html=True)
    render_hover_copy_box("W7774X", "点击复制")
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='wechat-item'><span class='wechat-label'>🛠️ 技术/合作:</span></div>", unsafe_allow_html=True)
    render_hover_copy_box("TG777188", "点击复制")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 动态生成菜单
    nav_options = ["📝 文案改写", "💡 爆款选题库", "🎨 海报生成", "🏷️ 账号起名", "👤 个人中心"]
    if IS_ADMIN:
        nav_options.append("🕵️‍♂️ 管理后台")
        
    menu_option = st.radio("功能导航", nav_options, index=0, label_visibility="collapsed")
    
    st.markdown("---")
    if st.button("🚪 退出登录"):
        del st.session_state['user_phone']
        st.rerun()

# --- 权限拦截 ---
if not IS_VIP and menu_option not in ["👤 个人中心", "🕵️‍♂️ 管理后台"]:
    st.warning("⚠️ 您当前未激活会员，无法使用该功能。")
    st.info("请在左侧侧边栏输入卡密激活。")
    st.stop()

# --- A-D 功能模块 (保持业务逻辑) ---
client = OpenAI(api_key=st.secrets.get("DEEPSEEK_API_KEY", "fake_key"), base_url="https://api.deepseek.com")

def page_rewrite():
    st.markdown("## ⚡ 爆款文案改写中台")
    st.caption("AI 驱动的五路并发架构 | 40秒黄金完播率模型")
    st.markdown("---")
    if 'results' not in st.session_state: st.session_state['results'] = {}
    
    def rewrite_logic(content):
        prompt = f"你是一个抖音千万粉的口播博主。原始素材：{content}。任务：清洗数据，改写为原创爆款文案。公式：黄金3秒开头+中间情绪饱满+结尾强引导。输出：直接输出文案，不要任何markdown格式。"
        try:
            res = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}], temperature=1.3)
            return res.choices[0].message.content
        except: return "模拟生成：这是一个爆款文案示例..." # 避免无 Key 报错

    col_main, col_tips = st.columns([1, 2], gap="medium")
    with col_main:
        if st.button("🚀 一键并发执行", type="primary", use_container_width=True):
            tasks, indices = [], []
            for i in range(1, 6):
                text = st.session_state.get(f"input_{i}", "")
                if text.strip(): tasks.append(text); indices.append(i)
            if not tasks: st.toast("请输入文案", icon="🛑")
            else:
                with st.status("☁️ 云端计算中..."):
                    with ThreadPoolExecutor(max_workers=5) as executor:
                        results_list = list(executor.map(rewrite_logic, tasks))
                    for idx, res in zip(indices, results_list): st.session_state['results'][idx] = res
                    st.rerun()
    with col_tips: st.markdown("""<div class="info-box-aligned">💡 指南：粘贴文案到下方窗口，点击左侧 <b>【蓝色按钮】</b> 同时处理。</div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    for i in range(1, 6):
        with st.container(border=True):
            st.markdown(f"#### 🎬 工作台 #{i}")
            c1, c2 = st.columns([1, 1], gap="large")
            with c1: st.text_area("原始文案", height=150, key=f"input_{i}")
            with c2:
                res = st.session_state['results'].get(i, "")
                if res: st.text_area(f"结果 #{i}", value=res, height=150); render_hover_copy_box(res, "点击复制")
                else: st.caption("等待生成...")

def page_poster_gen():
    st.markdown("## 🎨 AI 智能海报改图 (专业版)")
    st.info("💡 提示：为了提供更稳定的算力支持，海报改图功能已升级至 **小提大作 独立站**。")
    with st.container(border=True):
        st.markdown("### 🚀 前往 小提大作 专业版控制台")
        c1, c2 = st.columns([1, 1.5], gap="large")
        with c1:
            st.markdown("##### 第 1 步：复制专属邀请码")
            render_hover_copy_box("5yzMbpxn", "点击复制")
        with c2:
            st.markdown("##### 第 2 步：前往生成")
            st.markdown("""<a href="https://aixtdz.com/" target="_blank" class="redirect-btn">🚀 立即前往 小提大作 生成海报</a>""", unsafe_allow_html=True)

# --- F. 个人中心 (含反馈) ---
def page_account():
    st.markdown("## 👤 个人中心")
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["💳 账户信息", "💬 需求反馈"])
    
    with tab1:
        st.metric("登录账号", CURRENT_USER)
        st.metric("会员状态", "VIP" if IS_VIP else "未激活", delta="有效" if IS_VIP else "无权限")
        st.caption(VIP_MSG)
        
        st.markdown("#### 🔑 卡密激活")
        code = st.text_input("输入新卡密", placeholder="VIP-XXXXXX")
        if st.button("激活 / 续费", type="primary"):
            success, msg = activate_code(CURRENT_USER, code)
            if success: st.success(msg); time.sleep(1); st.rerun()
            else: st.error(msg)

    with tab2:
        st.info("💡 觉得哪里不好用？或者想要什么新功能？请留言，管理员后台可见。")
        fb_content = st.text_area("留言内容", height=100)
        if st.button("提交反馈"):
            if len(fb_content) > 5:
                submit_feedback(CURRENT_USER, fb_content)
                st.success("✅ 反馈已提交，我们会尽快处理！")
            else:
                st.warning("请多写几个字吧~")
        
        # 显示历史反馈
        st.markdown("#### 📜 我的反馈历史")
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT content, reply, create_time FROM feedbacks WHERE user_phone=? ORDER BY create_time DESC", (CURRENT_USER,))
        rows = c.fetchall()
        conn.close()
        
        if rows:
            for content, reply, ctime in rows:
                with st.container(border=True):
                    st.markdown(f"<div class='chat-meta'>📅 {ctime}</div>", unsafe_allow_html=True)
                    st.markdown(f"**我**: {content}")
                    if reply:
                        st.markdown(f"**管理员回复**: <span style='color:#059669'>{reply}</span>", unsafe_allow_html=True)
                    else:
                        st.caption("⏳ 等待回复...")
        else:
            st.caption("暂无反馈记录")

# --- G. 管理员后台 ---
def page_admin():
    st.markdown("## 🕵️‍♂️ 超级管理后台")
    st.caption(f"当前管理员: {CURRENT_USER}")
    
    tab_code, tab_user, tab_fb = st.tabs(["🎫 卡密管理", "👥 用户管理", "💬 反馈处理"])
    
    # 1. 卡密生成
    with tab_code:
        c1, c2 = st.columns(2)
        with c1:
            qty = st.number_input("生成数量", 1, 100, 10)
            days = st.number_input("有效天数", 1, 365, 30)
            if st.button("⚡ 批量生成卡密", type="primary"):
                conn = sqlite3.connect(DB_FILE)
                c = conn.cursor()
                now = datetime.datetime.now()
                new_codes = []
                for _ in range(qty):
                    code = "VIP-" + str(uuid.uuid4())[:8].upper()
                    c.execute("INSERT INTO access_codes (code, duration_days, status, create_time) VALUES (?, ?, ?, ?)", 
                              (code, days, 'unused', now))
                    new_codes.append(code)
                conn.commit(); conn.close()
                st.success(f"成功生成 {qty} 个卡密！")
        
        # 展示/导出
        conn = sqlite3.connect(DB_FILE)
        df_codes = pd.read_sql_query("SELECT code, duration_days, status, bind_user, create_time FROM access_codes ORDER BY create_time DESC", conn)
        conn.close()
        st.dataframe(df_codes, use_container_width=True)
        csv = df_codes.to_csv(index=False).encode('utf-8')
        st.download_button("📥 导出所有卡密 (CSV)", csv, "vip_codes.csv", "text/csv")

    # 2. 用户查看
    with tab_user:
        conn = sqlite3.connect(DB_FILE)
        df_users = pd.read_sql_query("SELECT phone, register_time, last_login_time, last_login_ip FROM users ORDER BY register_time DESC", conn)
        conn.close()
        st.metric("总注册用户", len(df_users))
        st.dataframe(df_users, use_container_width=True)

    # 3. 反馈回复
    with tab_fb:
        conn = sqlite3.connect(DB_FILE)
        # 获取所有未回复
        pending = pd.read_sql_query("SELECT id, user_phone, content, create_time FROM feedbacks WHERE status='pending'", conn)
        conn.close()
        
        if not pending.empty:
            for index, row in pending.iterrows():
                with st.container(border=True):
                    st.write(f"用户: **{row['user_phone']}** | 时间: {row['create_time']}")
                    st.info(row['content'])
                    reply_text = st.text_input(f"回复内容 #{row['id']}", key=f"reply_{row['id']}")
                    if st.button(f"发送回复 #{row['id']}", key=f"btn_reply_{row['id']}"):
                        conn = sqlite3.connect(DB_FILE)
                        c = conn.cursor()
                        c.execute("UPDATE feedbacks SET reply=?, status='replied' WHERE id=?", (reply_text, row['id']))
                        conn.commit(); conn.close()
                        st.success("已回复！")
                        st.rerun()
        else:
            st.success("🎉 所有反馈都已处理完毕！")

# --- 路由分发 ---
if menu_option == "📝 文案改写": page_rewrite()
elif menu_option == "🎨 海报生成": page_poster_gen()
elif menu_option == "👤 个人中心": page_account()
elif menu_option == "🕵️‍♂️ 管理后台": page_admin()
else: st.info("功能开发中...")import streamlit as st
from openai import OpenAI
import time
from concurrent.futures import ThreadPoolExecutor
import streamlit.components.v1 as components 
import sqlite3
import datetime
import uuid
import pandas as pd # 引入 Pandas 用于表格展示和导出

# ==========================================
# 0. 核心配置 & 数据库初始化
# ==========================================
st.set_page_config(
    page_title="抖音爆款工场 Pro", 
    layout="wide",
    page_icon="💠",
    initial_sidebar_state="expanded"
)

# --- 数据库操作 ---
DB_FILE = 'users.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # 增加 create_time 字段记录创建时间，方便排序
    c.execute('''CREATE TABLE IF NOT EXISTS access_codes
                 (code TEXT PRIMARY KEY, 
                  duration_days INTEGER, 
                  activated_at TIMESTAMP, 
                  expire_at TIMESTAMP, 
                  status TEXT,
                  create_time TIMESTAMP)''')
    
    # 检查是否存在 create_time 列 (兼容旧版本数据库)
    c.execute("PRAGMA table_info(access_codes)")
    columns = [info[1] for info in c.fetchall()]
    if 'create_time' not in columns:
        c.execute("ALTER TABLE access_codes ADD COLUMN create_time TIMESTAMP")
        
    conn.commit()
    conn.close()

init_db()

def check_code(code):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM access_codes WHERE code=?", (code,))
    row = c.fetchone()
    
    if not row:
        conn.close()
        return False, "❌ 卡密不存在"
    
    # row结构: 0:code, 1:duration, 2:activated_at, 3:expire_at, 4:status, 5:create_time
    duration, activated_at, expire_at, status = row[1], row[2], row[3], row[4]
    now = datetime.datetime.now()
    
    if status == 'unused':
        expire_date = now + datetime.timedelta(days=duration)
        c.execute("UPDATE access_codes SET status='active', activated_at=?, expire_at=? WHERE code=?", (now, expire_date, code))
        conn.commit(); conn.close()
        return True, f"✅ 激活成功！有效期至：{expire_date.strftime('%Y-%m-%d')}"
    elif status == 'active':
        expire_date = datetime.datetime.strptime(str(expire_at).split('.')[0], '%Y-%m-%d %H:%M:%S')
        if now > expire_date:
            c.execute("UPDATE access_codes SET status='expired' WHERE code=?", (code,))
            conn.commit(); conn.close()
            return False, "⛔ 卡密已过期"
        else:
            days_left = (expire_date - now).days
            conn.close()
            return True, f"✅ VIP 生效中 (剩余 {days_left} 天)"
    else:
        conn.close()
        return False, "⛔ 卡密已过期"

# --- CSS 样式 ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    .stApp { font-family: 'Inter', sans-serif; background-color: #f8fafc; }
    
    /* 容器美化 */
    div.block-container { max-width: 90% !important; min-width: 90% !important; background-color: #ffffff; padding: 3rem !important; margin: 2rem auto !important; border-radius: 16px; box-shadow: 0 10px 40px -10px rgba(0,0,0,0.05); }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #f1f5f9; }
    [data-testid="stVerticalBlockBorderWrapper"] { background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 24px; transition: all 0.3s ease; }
    [data-testid="stVerticalBlockBorderWrapper"]:hover { border-color: #cbd5e1; box-shadow: 0 4px 12px rgba(0,0,0,0.03); }
    h1 { color: #0f172a !important; font-weight: 800 !important; margin-bottom: 1.5rem !important; }
    .stMarkdown p, label { color: #475569 !important; }
    
    /* 统一按钮高度 */
    div.stButton > button { border-radius: 8px !important; font-weight: 600 !important; height: 50px !important; transition: all 0.2s !important; }
    div.stButton > button:not([kind="primary"]) { background-color: #f1f5f9; color: #475569 !important; border: 1px solid transparent; }
    div.stButton > button:not([kind="primary"]):hover { background-color: #e0f2fe; color: #0284c7 !important; border-color: #bae6fd; }
    div.stButton > button[kind="primary"] { background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3); border: none; color: #ffffff !important; }
    div.stButton > button[kind="primary"]:hover { box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4); transform: translateY(-1px); }
    
    /* 输入框 */
    .stTextArea textarea, .stTextInput input, .stNumberInput input { border-radius: 8px; border: 1px solid #cbd5e1; background-color: #f8fafc !important; color: #1e293b !important; caret-color: #2563eb; font-weight: 500; }
    .stTextArea textarea:focus, .stTextInput input:focus, .stNumberInput input:focus { background-color: #ffffff !important; border-color: #3b82f6; box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15); }
    
    /* 商业化组件 */
    .project-box { background-color: #f0f9ff; border: 1px solid #bae6fd; padding: 12px; border-radius: 8px; margin-bottom: 10px; }
    .project-title { font-weight: bold; color: #0369a1; font-size: 14px; }
    .project-desc { font-size: 12px; color: #334155; margin-top: 4px; }
    .wechat-contact { margin-top: 20px; padding-top: 15px; border-top: 1px solid #e2e8f0; }
    .wechat-item { display: flex; align-items: center; justify-content: space-between; font-size: 13px; color: #475569; margin-bottom: 8px; }
    .wechat-label { font-weight: 600; }
    
    /* 后台统计卡片 */
    .stat-card { background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 15px; text-align: center; }
    .stat-value { font-size: 24px; font-weight: 800; color: #2563eb; }
    .stat-label { font-size: 12px; color: #64748b; margin-top: 5px; }

    /* 跳转按钮 */
    a.redirect-btn { display: flex !important; align-items: center; justify-content: center; width: 100%; height: 52px !important; background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); color: white !important; padding: 0 !important; border-radius: 8px; text-decoration: none; font-size: 16px; font-weight: 700; margin-top: 0px !important; box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3); transition: transform 0.2s; border: 1px solid #7c3aed; }
    a.redirect-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(139, 92, 246, 0.4); }
    
    .login-spacer { height: 10vh; }
    .empty-state-box { height: 200px; background-image: repeating-linear-gradient(45deg, #f8fafc 25%, transparent 25%, transparent 75%, #f8fafc 75%, #f8fafc), repeating-linear-gradient(45deg, #f8fafc 25%, #ffffff 25%, #ffffff 75%, #f8fafc 75%, #f8fafc); background-size: 20px 20px; border: 2px dashed #e2e8f0; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #94a3b8; font-weight: 500; flex-direction: column; gap: 10px; }
    .tutorial-box { background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; margin-top: 25px; }
    .tutorial-step { display: flex; align-items: center; margin-bottom: 15px; font-size: 15px; color: #334155; line-height: 1.5; }
    .step-num { background-color: #e0f2fe; color: #0284c7; font-weight: bold; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 12px; flex-shrink: 0; }
    .info-box-aligned { height: 50px !important; background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; color: #1e40af; display: flex; align-items: center; padding: 0 16px; font-size: 14px; font-weight: 500; width: 100%; box-sizing: border-box; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# ⚡ 前端组件 (复制功能)
# ==========================================
def render_copy_button_html(text, unique_key):
    safe_text = text.replace("`", "\`").replace("${", "\${").replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')
    html_code = f"""
    <!DOCTYPE html><html><head><style>@import url('https://fonts.googleapis.com/css2?family=Inter:wght@600&display=swap');body{{margin:0;padding:0;background:transparent;overflow:hidden;}}.copy-btn{{width:100%;height:42px;background:linear-gradient(135deg,#2563eb 0%,#1d4ed8 100%);color:white;border:none;border-radius:8px;font-family:'Inter',sans-serif;font-weight:600;font-size:14px;cursor:pointer;box-shadow:0 4px 12px rgba(37,99,235,0.3);transition:all 0.2s ease;display:flex;align-items:center;justify-content:center;gap:8px;}}.copy-btn:hover{{box-shadow:0 6px 16px rgba(37,99,235,0.4);transform:translateY(-1px);}}.copy-btn:active{{transform:translateY(0);background:#1d4ed8;}}.copy-btn.success{{background:linear-gradient(135deg,#10b981 0%,#059669 100%);box-shadow:0 4px 12px rgba(16,185,129,0.3);}}</style></head><body><button class="copy-btn" onclick="copyText(this)"><span>📋 一键复制纯文本</span></button><script>function copyText(btn){{const text=`{safe_text}`;if(navigator.clipboard&&window.isSecureContext){{navigator.clipboard.writeText(text).then(()=>{{showSuccess(btn);}}).catch(err=>{{fallbackCopyText(text,btn);}});}}else{{fallbackCopyText(text,btn);}}}}function fallbackCopyText(text,btn){{const textArea=document.createElement("textarea");textArea.value=text;textArea.style.position="fixed";textArea.style.left="-9999px";document.body.appendChild(textArea);textArea.focus();textArea.select();try{{const successful=document.execCommand('copy');if(successful)showSuccess(btn);}}catch(err){{btn.innerText="❌";}}document.body.removeChild(textArea);}}function showSuccess(btn){{const originalText=btn.innerHTML;btn.innerHTML="<span>✅ 复制成功！</span>";btn.classList.add("success");setTimeout(()=>{{btn.innerHTML=originalText;btn.classList.remove("success");}},2000);}}</script></body></html>
    """
    components.html(html_code, height=50)

def render_hover_copy_box(text, label="点击复制"):
    safe_text = text.replace("`", "\`").replace("${", "\${").replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')
    html_code = f"""
    <!DOCTYPE html><html><head><style>@import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;600&display=swap');body{{margin:0;padding:0;background:transparent;font-family:'Inter',sans-serif;overflow:hidden;}}.code-box{{display:flex;align-items:center;justify-content:space-between;background-color:#f8fafc;border:1px solid #cbd5e1;border-radius:6px;padding:0 10px;height:36px;cursor:pointer;transition:all 0.2s ease;color:#1e293b;font-weight:600;font-size:13px;box-sizing:border-box;}}.code-box:hover{{border-color:#3b82f6;background-color:#ffffff;box-shadow:0 0 0 2px rgba(59,130,246,0.1);}}.hint{{font-size:12px;color:#94a3b8;font-weight:400;}}.code-box:hover .hint{{color:#3b82f6;}}.code-box.success{{background-color:#ecfdf5;border-color:#10b981;color:#065f46;}}.code-box.success .hint{{color:#059669;}}</style></head><body><div class="code-box" onclick="copyText(this)"><span id="code-content">{safe_text}</span><span class="hint" id="status-text">{label}</span></div><script>function copyText(box){{const text=`{safe_text}`;const statusText=box.querySelector("#status-text");if(navigator.clipboard&&window.isSecureContext){{navigator.clipboard.writeText(text).then(()=>{{showSuccess(box,statusText);}}).catch(err=>{{fallbackCopyText(text,box,statusText);}});}}else{{fallbackCopyText(text,box,statusText);}}}}function fallbackCopyText(text,box,statusText){{const textArea=document.createElement("textarea");textArea.value=text;textArea.style.position="fixed";textArea.style.left="-9999px";document.body.appendChild(textArea);textArea.focus();textArea.select();try{{const successful=document.execCommand('copy');if(successful)showSuccess(box,statusText);}}catch(err){{statusText.innerText="❌";}}document.body.removeChild(textArea);}}function showSuccess(box,statusText){{box.classList.add("success");const originalHint="{label}";statusText.innerText="✅ 成功";setTimeout(()=>{{box.classList.remove("success");statusText.innerText=originalHint;}},1500);}}</script></body></html>
    """
    components.html(html_code, height=40)

# ==========================================
# 1. 登录与安全系统 (使用数据库)
# ==========================================
def clear_text_callback(key):
    if key in st.session_state: st.session_state[key] = ""

@st.cache_resource
def get_login_cache(): return {}

def get_remote_ip():
    try:
        from streamlit.web.server.websocket_headers import _get_websocket_headers
        headers = _get_websocket_headers()
        return headers.get("X-Forwarded-For", headers.get("Remote-Addr", "unknown_ip"))
    except: return "unknown_ip"

def check_login():
    if st.session_state.get('is_logged_in', False): return True
    
    login_placeholder = st.empty()
    with login_placeholder.container():
        st.markdown("<div class='login-spacer'></div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 1.5, 1])
        with c2:
            st.markdown("<h2 style='text-align: center; margin-bottom: 20px;'>💠 爆款工场 Pro</h2>", unsafe_allow_html=True)
            st.info("🔒 商业授权系统 | 请输入月卡/季卡卡密", icon="🔑")
            
            with st.form("login_form"):
                user_code = st.text_input("请输入卡密 (Access Code)", placeholder="例如：VIP-XXXXXXXX", type="password")
                st.markdown("<br>", unsafe_allow_html=True)
                submitted = st.form_submit_button("🚀 立即激活/登录", type="primary", use_container_width=True)
            
            if submitted:
                valid, msg = check_code(user_code.strip())
                if valid:
                    st.session_state['is_logged_in'] = True 
                    st.session_state['user_code'] = user_code.strip()
                    st.success(msg)
                    time.sleep(1)
                    login_placeholder.empty()
                    st.rerun()
                else:
                    st.error(msg)
    return False

if not check_login(): st.stop()

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
        prompt = f"""你是一个抖音千万粉的口播博主。原始素材：{content}。任务：清洗数据，改写为原创爆款文案。公式：黄金3秒开头+中间情绪饱满+结尾强引导。输出：直接输出文案，不要任何markdown格式。"""
        try:
            res = client.chat.completions.create(
                model="deepseek-chat", messages=[{"role": "user", "content": prompt}], temperature=1.3
            )
            return res.choices[0].message.content
        except Exception as e: return f"Error: {e}"

    col_main, col_tips = st.columns([1, 2], gap="medium")
    with col_main:
        if st.button("🚀 一键并发执行 (5路全开)", type="primary", use_container_width=True):
            tasks, indices = [], []
            for i in range(1, 6):
                text = st.session_state.get(f"input_{i}", "")
                if text.strip(): tasks.append(text); indices.append(i)
            if not tasks: st.toast("⚠️ 请先输入文案", icon="🛑")
            else:
                with st.status("☁️ 云端计算中...", expanded=True) as status:
                    with ThreadPoolExecutor(max_workers=5) as executor:
                        results_list = list(executor.map(rewrite_logic, tasks))
                    for idx, res in zip(indices, results_list): st.session_state['results'][idx] = res
                    status.update(label="✅ 完成！", state="complete", expanded=False); st.rerun()
    with col_tips:
        st.markdown("""<div class="info-box-aligned">💡 指南：粘贴文案到下方窗口，点击左侧 <b>【蓝色按钮】</b> 同时处理。</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    for i in range(1, 6):
        with st.container(border=True):
            st.markdown(f"#### 🎬 工作台 #{i}")
            c1, c2 = st.columns([1, 1], gap="large")
            with c1:
                input_key = f"input_{i}"
                st.text_area("原始文案", height=200, key=input_key, label_visibility="collapsed", placeholder="💡在此按 Ctrl+V 粘贴提取的文案...")
                b1, b2 = st.columns([1, 2.5])
                b1.button("🗑️ 清空", key=f"clr_{i}", on_click=clear_text_callback, args=(input_key,), use_container_width=True)
                if b2.button(f"⚡ 仅生成 #{i}", key=f"btn_{i}", use_container_width=True):
                    val = st.session_state.get(input_key, "")
                    if val:
                        with st.spinner("生成中..."): st.session_state['results'][i] = rewrite_logic(val); st.rerun()
            with c2:
                res_val = st.session_state['results'].get(i, "")
                if res_val:
                    st.text_area(f"结果 #{i}", value=res_val, height=200, label_visibility="collapsed", key=f"res_area_{i}")
                    render_copy_button_html(res_val, f"copy_btn_{i}")
                    st.markdown("""<div style="margin-top: 10px; padding: 10px; background: #fff1f2; border-radius: 8px; border: 1px solid #fecdd3; font-size: 13px; color: #be123c;">🔥 <b>文案搞定了，不会拍？</b> <br>领取《素人KOC爆款出镜SOP》，教你对着镜头自然说话！<br><span style="color:#e11d48;font-weight:bold;">👉 复制左侧微信 W7774X 免费领</span></div>""", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='empty-state-box'><div style='font-size: 24px;'>⏳</div><div>等待指令...</div><div style='font-size: 12px; color: #94a3b8;'>Input content to generate</div></div>", unsafe_allow_html=True)

# --- B. 别名创建 ---
def page_alias_creation():
    st.markdown("## 🎭 剧名别名生成"); st.markdown("---")
    c1, c2 = st.columns([2, 1])
    with c1: original_name = st.text_input("🎬 原剧名/原书名", placeholder="例如：霸道总裁爱上我")
    with c2: count = st.slider("生成数量", 5, 20, 10)
    tags = st.multiselect("🏷️ 强化元素", ["高甜", "复仇", "逆袭", "悬疑", "虐恋", "豪门"], default=["逆袭", "高甜"])
    if st.button("🚀 生成别名", type="primary", use_container_width=True):
        if not original_name: st.toast("请输入原名", icon="🛑")
        else:
            prompt = f"请将《{original_name}》改写为{count}个推广别名。策略：加入“{'、'.join(tags)}”元素，去原名化，直击痛点。输出：只输出别名列表，一行一个，纯文本。"
            try:
                with st.spinner("生成中..."):
                    res = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}], temperature=1.4)
                    st.session_state['alias_result'] = res.choices[0].message.content
            except Exception as e: st.error(f"Error: {e}")
    if 'alias_result' in st.session_state:
        res_text = st.session_state['alias_result']
        st.info("👇 别名列表已生成，点击下方按钮一键复制", icon="📋")
        st.text_area("结果", value=res_text, height=300, label_visibility="collapsed")
        render_copy_button_html(res_text, "alias_copy_btn")

# --- C. 账号起名 ---
def page_naming():
    st.markdown("## 🏷️ 账号/IP 起名大师"); st.markdown("---")
    c1, c2 = st.columns(2)
    with c1: niche = st.selectbox("🎯 赛道", ["短剧", "小说", "口播", "情感", "带货"])
    with c2: style = st.selectbox("🎨 风格", ["高冷", "搞笑", "文艺", "粗暴", "反差"])
    keywords = st.text_input("🔑 关键词 (选填)")
    if st.button("🎲 生成名字", type="primary", use_container_width=True):
        prompt = f"为【{niche}】赛道生成10个{style}风格账号名，含关键词：{keywords}。格式：名字+解释。"
        try:
            with st.spinner("生成中..."):
                res = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}], temperature=1.5)
                st.session_state['naming_result'] = res.choices[0].message.content
        except Exception as e: st.error(str(e))
    if 'naming_result' in st.session_state:
        res_text = st.session_state['naming_result']
        st.text_area("结果", value=res_text, height=400, label_visibility="collapsed")
        render_copy_button_html(res_text, "name_copy_btn")

# --- D. 选题灵感库 ---
def page_brainstorm():
    st.markdown("## 💡 爆款选题灵感库"); st.markdown("---")
    with st.container(border=True):
        c1, c2 = st.columns([3, 1])
        with c1: topic = st.text_input("🔍 输入你的赛道/关键词", placeholder="例如：职场、美妆、减肥、副业...")
        with c2: st.write(""); st.write(""); generate_btn = st.button("🧠 帮我想选题", type="primary", use_container_width=True)
    if generate_btn and topic:
        prompt = f"我是做【{topic}】领域的。现在文案枯竭，请帮我生成 10 个绝对会火的爆款选题。要求：1. 必须反直觉，打破认知。2. 必须直击痛点，引发焦虑或强烈好奇。3. 格式：标题：xxxx | 钩子：xxxx"
        try:
            with st.spinner("AI 正在疯狂头脑风暴..."):
                res = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}], temperature=1.5)
                st.session_state['brainstorm_result'] = res.choices[0].message.content
        except Exception as e: st.error(str(e))
    if 'brainstorm_result' in st.session_state:
        res_text = st.session_state['brainstorm_result']
        st.text_area("灵感列表", value=res_text, height=400, label_visibility="collapsed")
        render_copy_button_html(res_text, "brain_copy_btn")

# --- E. 海报生成 ---
def page_poster_gen():
    st.markdown("## 🎨 AI 智能海报改图 (专业版)"); st.info("💡 提示：为了提供更稳定的算力支持，海报改图功能已升级至 **小提大作 独立站**。")
    with st.container(border=True):
        st.markdown("### 🚀 前往 小提大作 专业版控制台")
        c1, c2 = st.columns([1, 1.5], gap="large")
        with c1: st.markdown("##### 第 1 步：复制专属邀请码"); st.caption("注册时填写，可获赠额外算力点数"); render_hover_copy_box("5yzMbpxn", "点击复制")
        with c2: st.markdown("##### 第 2 步：前往生成"); st.caption("点击下方按钮跳转"); st.markdown("""<a href="https://aixtdz.com/" target="_blank" class="redirect-btn">🚀 立即前往 小提大作 生成海报</a>""", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("""<div style="padding: 10px; background: #f0f9ff; border-radius: 8px; border: 1px solid #bae6fd; display: flex; align-items: center; justify-content: space-between;"><div><span style="font-size: 18px;">💡</span><span style="color: #0369a1; font-weight: bold; margin-left: 5px;">想让海报动起来？做动漫视频赚收益？</span><div style="font-size: 12px; color: #64748b; margin-top: 2px;">了解【御灵AI】动漫视频变现玩法，红果/番茄拉新 + 版权分销。</div></div><a href="#" style="background: #0284c7; color: white; padding: 6px 12px; border-radius: 6px; text-decoration: none; font-size: 13px; font-weight: bold;">联系左侧客服</a></div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("#### 📖 新手保姆级改图教程"); st.markdown("""<div class="tutorial-box"><div class="tutorial-step"><div class="step-num">1</div><div>注册登录后，点击 <b>“创建自由画布”</b></div></div><div class="tutorial-step"><div class="step-num">2</div><div>根据提示 <b>双击</b> 或者 <b>右键点击</b> 空白处，选择 <b>“图生图”</b></div></div><div class="tutorial-step"><div class="step-num">3</div><div>点击组件上的 <b>“+”</b> 号，上传你需要修改的 <b>原剧海报</b></div></div><div class="tutorial-step"><div class="step-num">4</div><div>点击 <b>右边边框</b>，在下方输入指令（点击右上角复制）：</div></div></div>""", unsafe_allow_html=True)
        st.code("将原图剧名：原剧名\n改为：[你的新剧名]", language="text")

# --- G. 管理员后台 ---
def page_admin():
    # 简单的管理员鉴权 (这里为了演示，直接校验 session，实际可加二次密码)
    st.markdown("## 🕵️‍♂️ 超级管理后台")
    st.caption("仅限管理员访问 | 卡密生成与数据统计")
    
    # 1. 登录
    pwd = st.text_input("请输入管理员密码", type="password")
    if pwd == "admin888": # 默认密码
        # 2. 数据统计
        conn = sqlite3.connect(DB_FILE)
        df = pd.read_sql_query("SELECT * FROM access_codes ORDER BY create_time DESC", conn)
        conn.close()
        
        c1, c2, c3 = st.columns(3)
        c1.markdown(f"<div class='stat-card'><div class='stat-value'>{len(df)}</div><div class='stat-label'>总卡密数</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-card'><div class='stat-value'>{len(df[df['status']=='active'])}</div><div class='stat-label'>已激活/使用中</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-card'><div class='stat-value'>{len(df[df['status']=='unused'])}</div><div class='stat-label'>未使用库存</div></div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 3. 批量生成
        with st.container(border=True):
            st.markdown("#### ⚡ 批量生成卡密")
            cc1, cc2, cc3 = st.columns(3)
            with cc1: qty = st.number_input("生成数量", 1, 500, 10)
            with cc2: days = st.number_input("有效天数", 1, 365, 30)
            with cc3: 
                st.write("")
                st.write("")
                if st.button("🚀 立即生成", type="primary", use_container_width=True):
                    new_codes = []
                    conn = sqlite3.connect(DB_FILE)
                    c = conn.cursor()
                    now = datetime.datetime.now()
                    for _ in range(qty):
                        code = "VIP-" + str(uuid.uuid4())[:8].upper()
                        c.execute("INSERT INTO access_codes (code, duration_days, status, create_time) VALUES (?, ?, ?, ?)", (code, days, 'unused', now))
                        new_codes.append([code, days, 'unused'])
                    conn.commit()
                    conn.close()
                    st.success(f"成功生成 {qty} 个卡密！")
                    st.rerun()

        # 4. 数据展示与导出
        st.markdown("#### 📋 卡密明细 (支持下载)")
        st.dataframe(df, use_container_width=True)
        
        # 导出 CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(label="📥 下载所有数据 (CSV)", data=csv, file_name="vip_codes_export.csv", mime="text/csv", type="primary")
    else:
        if pwd: st.error("密码错误")

# --- F. 个人中心 ---
def page_account():
    st.markdown("## 👤 我的账户"); st.markdown("---")
    valid, msg = check_code(st.session_state.get('user_code'))
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.metric("会员状态", "VIP 正式版", delta="生效中" if valid else "已过期")
            st.text_input("当前卡密", value=st.session_state.get('user_code'), disabled=True)
            st.caption(msg)
    with col2:
        with st.container(border=True):
            st.markdown("#### 💬 遇到问题？")
            st.markdown("请联系技术支持微信：`TG777188`")

# ==========================================
# 4. 侧边栏导航
# ==========================================
with st.sidebar:
    st.markdown("### 💠 爆款工场 Pro")
    if st.session_state.get('is_logged_in'):
        valid, msg = check_code(st.session_state.get('user_code'))
        if valid: st.success(msg)
        else: st.error("卡密已失效")
    st.markdown("---")
    st.markdown("#### 🔥 热门搞钱项目")
    st.markdown("""<div class="project-box"><div class="project-title">📹 素人 KOC 孵化</div><div class="project-desc">真人出镜口播，红果/番茄拉新，0基础陪跑。</div></div><div class="project-box"><div class="project-title">🎨 御灵 AI 动漫</div><div class="project-desc">小说转动漫视频，端原生+版权分销，高收益。</div></div>""", unsafe_allow_html=True)
    
    st.markdown("<div class='wechat-contact'>", unsafe_allow_html=True)
    st.markdown("<div class='wechat-item'><span class='wechat-label'>💼 营销咨询:</span></div>", unsafe_allow_html=True)
    render_hover_copy_box("W7774X", "点击复制")
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='wechat-item'><span class='wechat-label'>🛠️ 技术/合作:</span></div>", unsafe_allow_html=True)
    render_hover_copy_box("TG777188", "点击复制")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    menu_option = st.radio("功能导航", ["📝 文案改写", "💡 爆款选题库", "🎨 海报生成", "🏷️ 账号起名", "👤 我的账户", "🕵️‍♂️ 管理后台"], index=0, label_visibility="collapsed")

if menu_option == "📝 文案改写": page_rewrite()
elif menu_option == "💡 爆款选题库": page_brainstorm()
elif menu_option == "🎨 海报生成": page_poster_gen()
elif menu_option == "🏷️ 账号起名": page_naming()
elif menu_option == "👤 我的账户": page_account()
elif menu_option == "🕵️‍♂️ 管理后台": page_admin()

