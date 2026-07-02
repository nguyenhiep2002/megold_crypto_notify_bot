# 🤖 MeGold Crypto Notify Bot

Bot Telegram tự động thông báo giá vàng thế giới (XAUUSD), BTC, ETH, và giá vàng Bảo Tín Minh Châu vào 4 khung giờ mỗi ngày.

## 📊 Thông tin cập nhật

| Dữ liệu | Nguồn |
|----------|-------|
| XAUUSD (Vàng thế giới) | Swissquote |
| BTC, ETH | CoinGecko |
| Vàng BTMC (9999 & SJC) | Vang.Today |

## 🕐 Lịch gửi thông báo

- 09:00 sáng
- 13:00 chiều
- 19:00 tối
- 23:00 đêm

*(Múi giờ Việt Nam - UTC+7)*

## ⚙️ Cài đặt

### 1. Cài dependencies

```bash
pip install -r requirements.txt
```

### 2. Cấu hình Bot Token

**Cách 1 (Khuyến khích):** Set biến môi trường

```bash
# Windows CMD
set TELEGRAM_BOT_TOKEN=your_token_here

# Windows PowerShell
$env:TELEGRAM_BOT_TOKEN="your_token_here"

# Linux/Mac
export TELEGRAM_BOT_TOKEN=your_token_here
```

**Cách 2:** Sửa trực tiếp trong `config.py`:

```python
BOT_TOKEN = "your_token_here"
```

### 3. Lấy Bot Token

1. Mở Telegram, tìm [@BotFather](https://t.me/BotFather)
2. Gửi `/newbot` và làm theo hướng dẫn
3. Copy token được cung cấp

## 🚀 Sử dụng

### Test gửi ngay

```bash
python main.py --now
```

### Chạy bot với lịch tự động

```bash
python main.py
```

### Chạy nền trên Windows (PowerShell)

```powershell
Start-Process -NoNewWindow python -ArgumentList "main.py"
```

## 📁 Cấu trúc dự án

```
megold_crypto_notify_bot/
├── config.py          # Cấu hình (token, schedule, API endpoints)
├── main.py            # Entry point + scheduler
├── price_fetcher.py   # Module lấy giá từ các API
├── message_builder.py # Module format tin nhắn
├── telegram_sender.py # Module gửi Telegram
├── requirements.txt   # Dependencies
└── README.md          # File này
```
