import streamlit as st
from openai import OpenAI
import time
from concurrent.futures import ThreadPoolExecutor 

# ==========================================
# 🎨 0. 企业级 UI/UX 配置 (修复版)
# ==========================================
st.set_page_config(
    page_title="抖音爆款工场 Pro", 
    layout="wide",
    page_icon="💠",
    initial_sidebar_state="expanded"
)

# 注入 CSS：黄金比例布局 + 现代化 SaaS 风格
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    .stApp {
        font-family: 'Inter', 'PingFang SC', 'Helvetica Neue', sans-serif;
        background-color: #f8f9fa;
    }

    /* 黄金比例布局控制 */
    [data-testid="stAppViewContainer"] > .main > .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 5rem;
        margin-left: auto;
        margin-right: auto;
    }

    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #eaeaea;
        box-shadow: 2px 0 10px rgba(0,0,0,0.02);
    }
    
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff;
        border: 1px solid #eeeeee;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
        padding: 24px;
    }
    
    h1 {
        font-weight: 800 !important;
        background: -webkit-linear-gradient(45deg, #2C3E50, #4CA1AF);
        -webkit-
