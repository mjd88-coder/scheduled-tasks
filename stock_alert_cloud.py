import time
import yfinance as yf
import smtplib
from email.message import EmailMessage
import os
# ==========================================
# SETTINGS
# ==========================================

# Your Gmail address
#EMAIL_SENDER = "dmjdstockinfo@gmail.com"

# Where you want to receive the alert
#EMAIL_RECEIVER = "dmjdstockinfo@gmail.com"

# Gmail App Password
#EMAIL_PASSWORD = "agsd ruxv iaou zrfr"

# import os and use it to get the Github repository secrets
EMAIL_SENDER = os.environ.get("MY_EMAIL")
EMAIL_PASSWORD = os.environ.get("MY_PASSWORD")

# ---------- CONFIG ----------
STOCKS = {
    "AMZN": 265.0,   # Disney
    "AAPL": 170.0,  # Apple
    "GOOG": 200.0,  # GOOGLE
    "META": 300.0,  # Product that connect people , FB
    "MSFT": 350.0,  # Microsoft
    "NVDA": 175.0,  # NVDIA
    "TSM": 240.0,   # Taiwan Semiconductor Manufacturing Company Limited
    "TSLA": 345.0,  # Testla
}

def get_stock_price(symbol):
    ticker = yf.Ticker(symbol)
    return ticker.info.get("currentPrice")


def send_email(alerts):
    msg = EmailMessage()
    msg["Subject"] = "Stock Price Alert"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_SENDER

    body = "The following stocks are below their alert prices:\n\n"
    for alert in alerts:
        body += f"{alert}\n"

    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)


if __name__ == "__main__":
    alerts = []

    for symbol, threshold in STOCKS.items():
        try:
            price = get_stock_price(symbol)
            print(f"{symbol}: {price}")

            if price is not None and price < threshold:
                alerts.append(
                    f"{symbol} is ${price} (below ${threshold})"
                )

        except Exception as e:
            print(f"Error checking {symbol}: {e}")

    if alerts:
        send_email(alerts)
        print("Email alert sent!")
    else:
        print("No alerts triggered.")

