import streamlit as st
from openai import OpenAI
import time
from concurrent.futures import ThreadPoolExecutor 

# ==========================================
# 🎨 0. 核心配置 (修复版)
# ==========================================
st.set_page_config(
    page_title="抖音爆款工场 Pro", 
    layout="wide",
    page_icon="💠",
    initial_sidebar_state="expanded"
)

# 将 CSS 样式单独定义，防止语法错误
CUSTOM_CSS = """
<style>
    .stApp { font-family: 'Helvetica Neue', Arial, sans-serif; background-color: #f8f9fa; }
    
    /* 黄金比例布局限制 */
    [data-testid="stAppViewContainer"] > .main > .block-container {
        max-width: 1200px; padding-top: 2rem; padding-bottom: 5rem;
        margin-left: auto; margin-right: auto;
    }
    
    /* 侧边栏与卡片美化 */
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #eaeaea; }
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff; border: 1px solid #eeeeee;
        border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.03);
        padding: 24px;
    }
    
    /* 标题与按钮 */
    h1 { color: #2C3E50; font-weight: 800 !important; }
    div.stButton > button {
        border-radius: 8px; font-weight
