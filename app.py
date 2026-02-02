import streamlit as st
from openai import OpenAI
import pandas as pd
import requests
import json
import time

# --- 配置区 (请在 Streamlit Secrets 里填入) ---
# 需要配置: DEEPSEEK_API_KEY, FEISHU_APP_ID, FEISHU_APP_SECRET, FEISHU_APP_TOKEN, FEISHU_TABLE_ID
def get_secret(key):
    try:
        return st.secrets[key]
    except:
        return None

# 初始化 OpenAI
api_key = get_secret("DEEPSEEK_API_KEY")
if api_key:
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

# --- 飞书工具函数 ---
def get_feishu_token(app_id, app_secret):
    """获取飞书 Tenant Access Token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {"Content-Type": "application/json; charset=utf-8"}
    payload = {"app_id": app_id, "app_secret": app_secret}
    
    try:
        r = requests.post(url, headers=headers, json=payload)
        return r.json().get("tenant_access_token")
    except Exception as e:
        st.error(f"获取飞书Token失败: {e}")
        return None

def push_to_feishu(token, app_token, table_id, data_list):
    """批量写入飞书多维表格"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8"
    }
    
    # 构造符合飞书要求的记录格式
    records = []
    for item in data_list:
        records.append({
            "fields": {
                "标题": item['title'],
                "简介": item['summary'],
                "AI文案": item['script'],
                # 飞书超链接格式: { "text": "显示文字", "link": "URL" }
                "番茄验证": {"text": "🔍 查番茄", "link": f"https://fanqienovel.com/search?keyword={item['title']}"},
                "红果验证": {"text": "🔍 查红果(百度)", "link": f"https://www.baidu.com/s?wd={item['title']}+红果短剧"}
            }
        })
    
    payload = {"records": records}
    
    try:
        r = requests.post(url, headers=headers, json=payload)
        res = r.json()
        if res.get("code") == 0:
            return True, "同步成功"
        else:
            return False, f"飞书报错: {res.get('msg')}"
    except Exception as e:
        return False, str(e)

# --- AI 生成函数 ---
def generate_script(title, summary):
    if not api_key: return "未配置Key"
    prompt = f"""
    剧名/书名：{title}
    简介：{summary}
    请写一段40秒的强情绪口播文案，突出冲突和爽点，引导去番茄/红果搜索。
    """
    try:
        res = client.chat.completions.create(
            model="deepseek-chat", messages=[{"role": "user", "content": prompt}]
        )
        return res.choices[0].message.content
    except:
        return "生成失败"

# --- 页面主逻辑 ---
st.set_page_config(page_title="🔥 爆款搬运工", layout="wide")
st.title("🚀 全网爆款 -> 飞书选品库")

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ 飞书配置")
    fs_app_id = st.text_input("App ID", value=get_secret("FEISHU_APP_ID") or "")
    fs_app_secret = st.text_input("App Secret", value=get_secret("FEISHU_APP_SECRET") or "")
    fs_token = st.text_input("多维表格 Token", value=get_secret("FEISHU_APP_TOKEN") or "")
    fs_table = st.text_input("数据表 Table ID", value=get_secret("FEISHU_TABLE_ID") or "")
    
    st.info("💡 提示：这些配置最好填入 Streamlit Secrets 以免每次都要输。")

# 核心功能区
uploaded_file = st.file_uploader("上传采集好的 Excel (包含'标题'和'简介'列)", type=["xlsx"])

if uploaded_file and st.button("开始处理并同步"):
    if not (fs_app_id and fs_app_secret and fs_token and fs_table):
        st.error("❌ 请先在侧边栏填写飞书配置！")
        st.stop()
        
    df = pd.read_excel(uploaded_file)
    
    # 简单列名清洗
    title_col = next((c for c in df.columns if '标题' in c or '名' in c), None)
    summary_col = next((c for c in df.columns if '简介' in c or 'summary' in c), None)
    
    if not title_col:
        st.error("❌ 表格里没找到【标题】列")
        st.stop()
        
    results = []
    progress_bar = st.progress(0)
    status = st.empty()
    
    # 循环处理
    total = len(df)
    for i, row in df.iterrows():
        title = str(row[title_col])
        summary = str(row.get(summary_col, "暂无简介"))
        
        status.text(f"正在处理: {title} ...")
        
        # 1. AI写文案
        script = generate_script(title, summary)
        
        # 2. 存入待同步列表
        results.append({
            "title": title,
            "summary": summary,
            "script": script
        })
        
        progress_bar.progress((i + 1) / total)
    
    # 同步到飞书
    status.text("正在同步到飞书...")
    token = get_feishu_token(fs_app_id, fs_app_secret)
    if token:
        success, msg = push_to_feishu(token, fs_token, fs_table, results)
        if success:
            st.success(f"🎉 成功！已将 {len(results)} 条爆款数据推送到飞书！")
            st.balloons()
        else:
            st.error(msg)
