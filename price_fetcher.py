"""
Module lấy giá từ các nguồn API.
- XAUUSD: Swissquote Forex Data Feed
- BTC, ETH: CoinGecko Public API
- Vàng BTMC: Vang.Today API
"""

import requests
import logging
from config import (
    XAUUSD_API, CRYPTO_API,
    BTMC_9999_API, BTMC_SJC_API,
    REQUEST_TIMEOUT
)

logger = logging.getLogger(__name__)


def fetch_xauusd():
    """
    Lấy giá vàng thế giới XAUUSD từ Swissquote.
    Returns: dict {"bid": float, "ask": float, "spread": float} hoặc None nếu lỗi.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(XAUUSD_API, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()

        # Swissquote trả về mảng, lấy phần tử đầu tiên
        if data and len(data) > 0:
            spreads = data[0].get("spreadProfilePrices", [])
            if spreads:
                bid = spreads[0].get("bid", 0)
                ask = spreads[0].get("ask", 0)
                return {
                    "bid": float(bid),
                    "ask": float(ask),
                    "spread": round(float(ask) - float(bid), 2)
                }

        logger.warning("XAUUSD: Dữ liệu trả về không đúng format")
        return None

    except requests.RequestException as e:
        logger.error(f"Lỗi khi lấy giá XAUUSD: {e}")
        return None
    except (KeyError, IndexError, ValueError) as e:
        logger.error(f"Lỗi parse dữ liệu XAUUSD: {e}")
        return None


def fetch_crypto():
    """
    Lấy giá BTC và ETH từ CoinGecko.
    Returns: dict {"btc": {"usd": float, "change_24h": float},
                    "eth": {"usd": float, "change_24h": float}} hoặc None nếu lỗi.
    """
    try:
        response = requests.get(CRYPTO_API, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()

        result = {}
        if "bitcoin" in data:
            result["btc"] = {
                "usd": data["bitcoin"].get("usd", 0),
                "change_24h": data["bitcoin"].get("usd_24h_change", 0)
            }
        if "ethereum" in data:
            result["eth"] = {
                "usd": data["ethereum"].get("usd", 0),
                "change_24h": data["ethereum"].get("usd_24h_change", 0)
            }

        return result if result else None

    except requests.RequestException as e:
        logger.error(f"Lỗi khi lấy giá Crypto: {e}")
        return None
    except (KeyError, ValueError) as e:
        logger.error(f"Lỗi parse dữ liệu Crypto: {e}")
        return None


def fetch_btmc_gold():
    """
    Lấy giá vàng Bảo Tín Minh Châu từ Vang.Today API.
    Returns: dict {"9999": {"buy": str, "sell": str},
                    "sjc": {"buy": str, "sell": str}} hoặc None nếu lỗi.
    """
    result = {}

    # Lấy giá vàng 9999
    try:
        response = requests.get(BTMC_9999_API, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()

        if data and isinstance(data, list) and len(data) > 0:
            item = data[0]
            result["9999"] = {
                "buy": item.get("buy", "N/A"),
                "sell": item.get("sell", "N/A"),
                "name": item.get("name", "Vàng 9999")
            }
        elif data and isinstance(data, dict):
            result["9999"] = {
                "buy": data.get("buy", "N/A"),
                "sell": data.get("sell", "N/A"),
                "name": data.get("name", "Vàng 9999")
            }
    except requests.RequestException as e:
        logger.error(f"Lỗi khi lấy giá vàng BTMC 9999: {e}")
    except (KeyError, ValueError) as e:
        logger.error(f"Lỗi parse dữ liệu BTMC 9999: {e}")

    # Lấy giá vàng SJC
    try:
        response = requests.get(BTMC_SJC_API, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()

        if data and isinstance(data, list) and len(data) > 0:
            item = data[0]
            result["sjc"] = {
                "buy": item.get("buy", "N/A"),
                "sell": item.get("sell", "N/A"),
                "name": item.get("name", "Vàng SJC")
            }
        elif data and isinstance(data, dict):
            result["sjc"] = {
                "buy": data.get("buy", "N/A"),
                "sell": data.get("sell", "N/A"),
                "name": data.get("name", "Vàng SJC")
            }
    except requests.RequestException as e:
        logger.error(f"Lỗi khi lấy giá vàng BTMC SJC: {e}")
    except (KeyError, ValueError) as e:
        logger.error(f"Lỗi parse dữ liệu BTMC SJC: {e}")

    return result if result else None


def fetch_all_prices():
    """
    Tổng hợp tất cả giá từ các nguồn.
    Returns: dict với keys: "xauusd", "crypto", "btmc"
    Nếu 1 nguồn fail, các nguồn khác vẫn được trả về.
    """
    prices = {
        "xauusd": fetch_xauusd(),
        "crypto": fetch_crypto(),
        "btmc": fetch_btmc_gold()
    }

    # Kiểm tra có ít nhất 1 nguồn thành công
    has_data = any(v is not None for v in prices.values())
    if not has_data:
        logger.error("Không thể lấy dữ liệu từ bất kỳ nguồn nào!")

    return prices
