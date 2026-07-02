"""
Module format tin nhắn Telegram với emoji và layout đẹp.
Sử dụng HTML parse mode cho Telegram.
"""

from datetime import datetime
import pytz
from config import TIMEZONE


def format_number(value, decimal_places=2):
    """Format số với dấu phân cách hàng nghìn."""
    if value is None:
        return "N/A"
    try:
        if isinstance(value, str):
            # Xử lý chuỗi có thể chứa dấu phẩy
            value = float(value.replace(",", ""))
        return f"{value:,.{decimal_places}f}"
    except (ValueError, TypeError):
        return str(value)


def format_change(change):
    """Format % thay đổi 24h với mũi tên lên/xuống."""
    if change is None or change == 0:
        return ""
    try:
        change = float(change)
        arrow = "🟢" if change >= 0 else "🔴"
        sign = "+" if change >= 0 else ""
        return f" {arrow} {sign}{change:.2f}%"
    except (ValueError, TypeError):
        return ""


def build_message(prices):
    """
    Xây dựng tin nhắn thông báo từ dữ liệu giá.
    Args:
        prices: dict từ fetch_all_prices()
    Returns:
        str: Tin nhắn HTML cho Telegram
    """
    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)
    time_str = now.strftime("%H:%M - %d/%m/%Y")

    lines = []

    # ═══ Header ═══
    lines.append("📊 <b>BẢNG GIÁ THỊ TRƯỜNG</b>")
    lines.append(f"🕐 <i>{time_str}</i>")
    lines.append("")

    # ═══ XAUUSD ═══
    lines.append("━━━ 🌍 <b>VÀNG THẾ GIỚI</b> ━━━")
    xau = prices.get("xauusd")
    if xau:
        lines.append(f"🥇 XAUUSD: <b>{format_number(xau['bid'])} USDT</b> / oz")
        lines.append(f"    Bid: {format_number(xau['bid'])} | Ask: {format_number(xau['ask'])} USDT")
        lines.append(f"    Spread: {format_number(xau['spread'])} USDT")
    else:
        lines.append("⚠️ <i>Không lấy được giá XAUUSD</i>")
    lines.append("")

    # ═══ Crypto ═══
    lines.append("━━━ 💰 <b>CRYPTO</b> ━━━")
    crypto = prices.get("crypto")
    if crypto:
        if "btc" in crypto:
            btc = crypto["btc"]
            change_str = format_change(btc.get("change_24h"))
            lines.append(f"₿ BTC: <b>{format_number(btc['usd'])} USDT</b>{change_str}")

        if "eth" in crypto:
            eth = crypto["eth"]
            change_str = format_change(eth.get("change_24h"))
            lines.append(f"⟠ ETH: <b>{format_number(eth['usd'])} USDT</b>{change_str}")
    else:
        lines.append("⚠️ <i>Không lấy được giá Crypto</i>")
    lines.append("")

    # ═══ Vàng BTMC ═══
    lines.append("━━━ 🇻🇳 <b>VÀNG BẢO TÍN MINH CHÂU</b> ━━━")
    btmc = prices.get("btmc")
    if btmc:
        if "9999" in btmc:
            g = btmc["9999"]
            buy_m = float(g['buy']) / 1_000_000 if g['buy'] != "N/A" else 0
            sell_m = float(g['sell']) / 1_000_000 if g['sell'] != "N/A" else 0
            lines.append(
                f"🔸 Vàng 9999: Mua <b>{format_number(buy_m, 1)}</b>"
                f" | Bán <b>{format_number(sell_m, 1)}</b>"
            )

        if "sjc" in btmc:
            g = btmc["sjc"]
            buy_m = float(g['buy']) / 1_000_000 if g['buy'] != "N/A" else 0
            sell_m = float(g['sell']) / 1_000_000 if g['sell'] != "N/A" else 0
            lines.append(
                f"🔸 Vàng SJC:  Mua <b>{format_number(buy_m, 1)}</b>"
                f" | Bán <b>{format_number(sell_m, 1)}</b>"
            )
        lines.append("<i>(đơn vị: triệu VNĐ/lượng)</i>")
    else:
        lines.append("⚠️ <i>Không lấy được giá vàng BTMC</i>")
    lines.append("")

    # ═══ Footer ═══
    lines.append("─────────────────────")
    lines.append("🤖 <i>MeGold Crypto Bot</i>")

    return "\n".join(lines)
