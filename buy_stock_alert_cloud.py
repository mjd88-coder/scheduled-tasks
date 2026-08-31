import csv
import yfinance as yf
import smtplib
from email.message import EmailMessage
import os


# ==========================================
# FILES
# ==========================================

STOCKS_FILE = "stockstobuy.csv"
RECEIVERS_FILE = "receiversemail.csv"


# ==========================================
# EMAIL SETTINGS
# ==========================================

# These should remain in GitHub Secrets
EMAIL_SENDER = os.environ.get("MY_EMAIL")
EMAIL_PASSWORD = os.environ.get("MY_PASSWORD")


# ==========================================
# LOAD STOCKS
# ==========================================

def load_stocks(filename):
    stocks = []

    with open(filename, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            symbol = row["symbol"].strip().upper()
            company = row["company"].strip()
            buyingprice = float(row["buyingprice"])

            stocks.append({
                "symbol": symbol,
                "company": company,
                "buyingprice": buyingprice
            })

    return stocks


# ==========================================
# LOAD EMAIL RECIPIENTS
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
# GET STOCK PRICE
# ==========================================

def get_stock_price(symbol):
    ticker = yf.Ticker(symbol)

    return ticker.info.get("currentPrice")


# ==========================================
# SEND EMAIL
# ==========================================

def send_email(alerts, receivers):

    msg = EmailMessage()

    msg["Subject"] = "BUY Stock Alert"
    msg["From"] = EMAIL_SENDER
    msg["To"] = ", ".join(receivers)

    body = (
        "The following stocks are below "
        "their target buy prices:\n\n"
    )

    for alert in alerts:
        body += f"{alert}\n"

    body += "\n"
    body += "This is an automated stock price alert."

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

    print("Checking stocks...\n")

    for stock in stocks:

        symbol = stock["symbol"]
        company = stock["company"]
        buyingprice = stock["buyingprice"]

        try:

            price = get_stock_price(symbol)

            if price is None:
                print(f"{symbol}: Price unavailable")
                continue

            print(
                f"{symbol} ({company}): "
                f"${price:.2f} "
                f"| Target: ${buyingprice:.2f}"
            )

            # --------------------------------
            # BUY ALERT
            # --------------------------------

            if price < buyingprice:

                alerts.append(
                    f"{symbol} ({company})\n"
                    f"Current price: ${price:.2f}\n"
                    f"Buying price: ${buyingprice:.2f}\n"
                    f"Price difference: "
                    f"${buyingprice - price:.2f} below buying price\n"
                    f"Potential discount: "
                    f"{((buyingprice - price) / buyingprice) * 100:.2f}%\n"
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

        print("\nBUY alert email sent!")
        print(f"Recipients: {len(receivers)}")
        print(f"Stocks triggering alert: {len(alerts)}")

    else:

        print("\nNo alerts triggered.")