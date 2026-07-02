"""
MeGold Crypto Notify Bot
─────────────────────────
Bot tự động gửi thông báo giá vàng & crypto qua Telegram.
Lịch gửi: 09:00, 13:00, 19:00, 23:00 (giờ Việt Nam)

Sử dụng:
    python main.py          # Chạy bot với lịch tự động
    python main.py --now    # Gửi 1 tin nhắn ngay lập tức (test)
"""

import sys
import time
import logging
from datetime import datetime

# Đảm bảo in emoji ra console Windows không bị lỗi encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass # Dự phòng cho các phiên bản python cũ không có reconfigure


import schedule
import pytz

from config import SCHEDULE_HOURS, TIMEZONE, BOT_TOKEN
from price_fetcher import fetch_all_prices
from message_builder import build_message
from telegram_sender import send_message

# ─── Logging Setup ──────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("MeGoldBot")


def job():
    """Task chính: lấy giá → format → gửi Telegram."""
    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)
    logger.info(f"🚀 Bắt đầu lấy dữ liệu giá ({now.strftime('%H:%M %d/%m/%Y')})...")

    # 1. Lấy tất cả giá
    prices = fetch_all_prices()

    # 2. Kiểm tra có dữ liệu không
    has_data = any(v is not None for v in prices.values())
    if not has_data:
        logger.error("❌ Không có dữ liệu nào. Bỏ qua lần gửi này.")
        # Vẫn gửi thông báo lỗi
        send_message("⚠️ <b>MeGold Bot</b>: Không thể lấy dữ liệu giá từ tất cả nguồn. Vui lòng kiểm tra kết nối mạng.")
        return

    # 3. Build tin nhắn
    message = build_message(prices)
    logger.info(f"📝 Tin nhắn đã tạo ({len(message)} ký tự)")

    # 4. Gửi Telegram
    success = send_message(message)
    if success:
        logger.info("✅ Hoàn tất gửi thông báo!")
    else:
        logger.error("❌ Gửi thông báo thất bại!")


def setup_schedule():
    """Đặt lịch gửi thông báo theo các khung giờ trong config."""
    for hour in SCHEDULE_HOURS:
        schedule.every().day.at(hour, TIMEZONE).do(job)
        logger.info(f"📅 Đã lên lịch gửi lúc {hour} ({TIMEZONE})")


def validate_config():
    """Kiểm tra cấu hình trước khi chạy."""
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or not BOT_TOKEN:
        logger.error("❌ Chưa cấu hình BOT_TOKEN!")
        logger.error("   Cách 1: Set biến môi trường TELEGRAM_BOT_TOKEN")
        logger.error("   Cách 2: Sửa trực tiếp trong config.py")
        return False
    return True


def main():
    print("=" * 50)
    print("  🤖 MeGold Crypto Notify Bot")
    print("  📊 Vàng XAUUSD | BTC | ETH | BTMC")
    print("=" * 50)
    print()

    # Kiểm tra cấu hình
    if not validate_config():
        sys.exit(1)

    # Chế độ test: gửi ngay
    if "--now" in sys.argv:
        logger.info("🔧 Chế độ test: gửi tin nhắn ngay...")
        job()
        return

    # Chế độ chạy lịch
    setup_schedule()

    logger.info("")
    logger.info("🟢 Bot đang chạy! Nhấn Ctrl+C để dừng.")
    logger.info(f"📅 Lịch gửi: {', '.join(SCHEDULE_HOURS)} ({TIMEZONE})")
    logger.info("")

    try:
        while True:
            schedule.run_pending()
            time.sleep(30)  # Kiểm tra mỗi 30 giây
    except KeyboardInterrupt:
        logger.info("\n🔴 Bot đã dừng.")


if __name__ == "__main__":
    main()
