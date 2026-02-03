# config.py
import os

# ==========================================
# 全局配置常量
# ==========================================

# 🔑 管理员账号信息
ADMIN_ACCOUNT = "13065080569" 
ADMIN_INIT_PASSWORD = "ltren777188" 

# 🎁 裂变与奖励配置
GLOBAL_INVITE_CODE = "VIP888" 
REWARD_DAYS_NEW_USER = 3  
REWARD_DAYS_REFERRER = 3  

# 💾 数据库路径
DB_FILE = 'saas_data_final_v3.db'

# 🛠️ 第三方 API 配置 (从 secrets 获取，这里做备用)
DEEPSEEK_BASE_URL = "https://api.deepseek.com"