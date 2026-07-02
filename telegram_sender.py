"""
Module gửi tin nhắn qua Telegram Bot API.
Hỗ trợ retry logic khi gửi thất bại.
"""

import time
import requests
import logging
from config import BOT_TOKEN, CHAT_ID, RETRY_COUNT, RETRY_DELAY

logger = logging.getLogger(__name__)

TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


def send_message(text, parse_mode="HTML"):
    """
    Gửi tin nhắn đến Telegram chat.
    Args:
        text: Nội dung tin nhắn
        parse_mode: "HTML" hoặc "Markdown"
    Returns:
        bool: True nếu gửi thành công
    """
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True
    }

    for attempt in range(1, RETRY_COUNT + 1):
        try:
            response = requests.post(TELEGRAM_API_URL, json=payload, timeout=15)
            result = response.json()

            if result.get("ok"):
                logger.info("✅ Gửi tin nhắn Telegram thành công!")
                return True
            else:
                error_desc = result.get("description", "Unknown error")
                logger.error(f"❌ Telegram API error: {error_desc}")

                # Nếu lỗi do token sai hoặc chat_id sai, không retry
                if response.status_code in (401, 403, 404):
                    logger.error("Lỗi xác thực hoặc chat_id không hợp lệ. Dừng retry.")
                    return False

        except requests.RequestException as e:
            logger.error(f"❌ Lỗi kết nối Telegram (lần {attempt}/{RETRY_COUNT}): {e}")

        if attempt < RETRY_COUNT:
            logger.info(f"⏳ Thử lại sau {RETRY_DELAY}s...")
            time.sleep(RETRY_DELAY)

    logger.error(f"❌ Gửi tin nhắn thất bại sau {RETRY_COUNT} lần thử!")
    return False
