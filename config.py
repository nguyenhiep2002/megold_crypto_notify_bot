"""
Cấu hình cho Telegram Bot thông báo giá vàng & crypto.
Bot Token được đọc từ biến môi trường TELEGRAM_BOT_TOKEN để bảo mật.
"""

import os

# ─── Telegram ───────────────────────────────────────────────
# Lấy token từ biến môi trường, hoặc đặt trực tiếp tại đây (không khuyến khích)
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8993073008:AAHGIzpENTypcbBCCe_HGQWafp-aNMGoCEk")
CHAT_ID = "1493207727"

# ─── Lịch gửi thông báo ────────────────────────────────────
# Các khung giờ gửi thông báo (theo giờ Việt Nam)
SCHEDULE_HOURS = ["09:00", "13:00", "19:00", "23:00"]
TIMEZONE = "Asia/Ho_Chi_Minh"

# ─── API Endpoints ──────────────────────────────────────────
XAUUSD_API = "https://forex-data-feed.swissquote.com/public-quotes/bboquotes/instrument/XAU/USD"
CRYPTO_API = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true"
BTMC_9999_API = "https://www.vang.today/api/prices?type=BT9999NTT"
BTMC_SJC_API = "https://www.vang.today/api/prices?type=BTSJC"

# ─── Request Settings ───────────────────────────────────────
REQUEST_TIMEOUT = 15  # seconds
RETRY_COUNT = 3
RETRY_DELAY = 5  # seconds between retries
