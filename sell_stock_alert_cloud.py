import csv
import yfinance as yf
import smtplib
from email.message import EmailMessage
import os


# ==========================================
# FILES
# ==========================================

STOCKS_FILE = "stockstosell.csv"
RECEIVERS_FILE = "receiversemail.csv"


# ==========================================
# EMAIL SETTINGS
# ==========================================

# GitHub Secrets
EMAIL_SENDER = os.environ.get("MY_EMAIL")
EMAIL_PASSWORD = os.environ.get("MY_PASSWORD")


# ==========================================
# LOAD STOCKS TO SELL
# ==========================================

def load_stocks(filename):
    stocks = []

    with open(filename, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            symbol = row["symbol"].strip().upper()
            company = row["company"].strip()
            buyingprice = float(row["buyingprice"])
            targetsellingpercentage = float(
                row["targetsellingpercentage"]
            )

            stocks.append({
                "symbol": symbol,
                "company": company,
                "buyingprice": buyingprice,
                "targetsellingpercentage": targetsellingpercentage
            })

    return stocks


# ==========================================
# LOAD EMAIL RECEIVERS
# ==========================================

def load_receivers(filename):
    receivers = []

    with open(filename, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            email = row["email"].strip()

            if email:
                receivers.append(email)

    return receivers


# ==========================================
# GET CURRENT STOCK PRICE
# ==========================================

def get_stock_price(symbol):
    ticker = yf.Ticker(symbol)

    return ticker.info.get("currentPrice")


# ==========================================
# SEND EMAIL
# ==========================================

def send_email(alerts, receivers):

    msg = EmailMessage()

    msg["Subject"] = "SELL Stock Alert"
    msg["From"] = EMAIL_SENDER
    msg["To"] = ", ".join(receivers)

    body = (
        "The following stocks have reached "
        "their target selling price:\n\n"
    )

    for alert in alerts:
        body += f"{alert}\n"

    body += "This is an automated selling stocks alert."

    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    # --------------------------------------
    # Load CSV files
    # --------------------------------------

    try:
        stocks = load_stocks(STOCKS_FILE)
        receivers = load_receivers(RECEIVERS_FILE)

    except FileNotFoundError as e:
        print(f"File not found: {e}")
        exit(1)

    # --------------------------------------
    # Check email configuration
    # --------------------------------------

    if not EMAIL_SENDER:
        print("ERROR: MY_EMAIL is not set.")
        exit(1)

    if not EMAIL_PASSWORD:
        print("ERROR: MY_PASSWORD is not set.")
        exit(1)

    if not receivers:
        print("ERROR: No email receivers found.")
        exit(1)

    # --------------------------------------
    # Check stocks
    # --------------------------------------

    alerts = []

    print("Checking stocks for SELL alerts...\n")

    for stock in stocks:

        symbol = stock["symbol"]
        company = stock["company"]
        buyingprice = stock["buyingprice"]
        targetsellingpercentage = stock["targetsellingpercentage"]

        # ----------------------------------
        # Calculate target selling price
        # ----------------------------------

        sell_price = buyingprice * (
            1 + targetsellingpercentage / 100
        )

        try:

            price = get_stock_price(symbol)

            if price is None:
                print(f"{symbol}: Price unavailable")
                continue

            # ----------------------------------
            # Calculate current profit
            # ----------------------------------

            gain_percent = (
                (price - buyingprice) / buyingprice
            ) * 100

            print(
                f"{symbol} ({company}): "
                f"${price:.2f} | "
                f"Buy: ${buyingprice:.2f} | "
                f"Target: ${sell_price:.2f} "
                f"({targetsellingpercentage:.2f}%) | "
                f"Gain: {gain_percent:.2f}%"
            )

            # ----------------------------------
            # SELL ALERT
            # ----------------------------------

            if price >= sell_price:

                alerts.append(
                    f"{symbol} ({company})\n"
                    f"Current price: ${price:.2f}\n"
                    f"Buying price: ${buyingprice:.2f}\n"
                    f"Target selling price: ${sell_price:.2f}\n"
                    f"Target gain: "
                    f"{targetsellingpercentage:.2f}%\n"
                    f"Current gain: {gain_percent:.2f}%\n"
                )

        except Exception as e:

            print(
                f"Error checking {symbol}: {e}"
            )

    # --------------------------------------
    # Send email if alerts exist
    # --------------------------------------

    if alerts:

        send_email(alerts, receivers)

        print("\nSELL alert email sent!")
        print(f"Recipients: {len(receivers)}")
        print(f"Sell stocks triggering alert: {len(alerts)}")

    else:

        print("\nNo SELL alerts triggered.")