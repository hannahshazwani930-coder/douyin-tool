# config.py
import streamlit as st

# 1. 管理员账号配置
ADMIN_ACCOUNT = st.secrets.get("ADMIN_ACCOUNT", "13800138000")
ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "admin123456")

# 2. 注册与邀请逻辑配置
DEFAULT_INVITE_CODE = "888888"
REWARD_DAYS_NEW_USER = 3
REWARD_DAYS_REFERRER = 7

# 3. 应用视觉配置
APP_NAME = "抖音爆款工场 Pro"
APP_ICON = "💠"
STYLE_DIR = "styles"

# 4. 数据库文件名
DB_FILE = "system_data.db"
