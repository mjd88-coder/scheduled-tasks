import csv
import yfinance as yf
import smtplib
from email.message import EmailMessage
import os


# ==========================================
# FILES
# ==========================================

STOCKS_FILE = "stocksbuyselldata.csv"
RECEIVERS_FILE = "receiversemail.csv"


# ==========================================
# EMAIL SETTINGS
# ==========================================

# GitHub Secrets
EMAIL_SENDER = os.environ.get("MY_EMAIL")
EMAIL_PASSWORD = os.environ.get("MY_PASSWORD")


# ==========================================
# LOAD STOCKS
# ==========================================

# ==========================================
# LOAD STOCKS
# ==========================================

def load_stocks(filename):
    stocks = []

    with open(
        filename,
        mode="r",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        reader = csv.DictReader(file)

        # --------------------------------------
        # Clean column names
        # --------------------------------------

        if reader.fieldnames is None:
            raise ValueError("CSV file has no header row.")

        reader.fieldnames = [
            field.strip().lower() if field else None
            for field in reader.fieldnames
        ]

        print("CSV columns found:", reader.fieldnames)

        # --------------------------------------
        # Required columns
        # --------------------------------------

        required_columns = {
            "symbol",
            "company",
            "buyingprice",
            "targetsellingpercentage"
        }

        actual_columns = {
            field for field in reader.fieldnames
            if field
        }

        missing_columns = required_columns - actual_columns

        if missing_columns:
            raise ValueError(
                "Missing required CSV columns: "
                + ", ".join(sorted(missing_columns))
            )

        # --------------------------------------
        # Read rows
        # --------------------------------------

        for row_number, row in enumerate(reader, start=2):

            # Skip completely empty rows
            if not row or all(
                value is None or not str(value).strip()
                for value in row.values()
            ):
                continue

            # ----------------------------------
            # Clean row values
            # ----------------------------------

            cleaned_row = {}

            for key, value in row.items():

                # Ignore columns without a name
                if key is None:
                    continue

                # Ignore empty values safely
                if value is None:
                    value = ""

                cleaned_row[key.strip().lower()] = value.strip()

            # ----------------------------------
            # Check required values
            # ----------------------------------

            try:

                symbol = cleaned_row["symbol"].upper()
                company = cleaned_row["company"]

                buyingprice = float(
                    cleaned_row["buyingprice"]
                )

                targetsellingpercentage = float(
                    cleaned_row["targetsellingpercentage"]
                )

            except KeyError as e:

                print(
                    f"ERROR in CSV row {row_number}: "
                    f"Missing column {e}"
                )
                continue

            except ValueError as e:

                print(
                    f"ERROR in CSV row {row_number}: "
                    f"Invalid number: {e}"
                )
                continue

            # ----------------------------------
            # Validate values
            # ----------------------------------

            if not symbol:
                print(
                    f"WARNING: Empty symbol in row "
                    f"{row_number}. Skipping."
                )
                continue

            if not company:
                print(
                    f"WARNING: Empty company in row "
                    f"{row_number}. Skipping."
                )
                continue

            if buyingprice <= 0:
                print(
                    f"WARNING: Invalid buying price for "
                    f"{symbol} in row {row_number}. Skipping."
                )
                continue

            # ----------------------------------
            # Add stock
            # ----------------------------------

            stocks.append({
                "symbol": symbol,
                "company": company,
                "buyingprice": buyingprice,
                "targetsellingpercentage":
                    targetsellingpercentage
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

def send_email(buy_alerts, sell_alerts, receivers):

    msg = EmailMessage()

    # --------------------------------------
    # Email subject
    # --------------------------------------

    if buy_alerts and sell_alerts:
        msg["Subject"] = "BUY & SELL Stock Alerts"

    elif buy_alerts:
        msg["Subject"] = "BUY Stock Alert"

    elif sell_alerts:
        msg["Subject"] = "SELL Stock Alert"

    msg["From"] = EMAIL_SENDER
    msg["To"] = ", ".join(receivers)

    # --------------------------------------
    # Build email body
    # --------------------------------------

    body = "Automated Stock Monitoring Alert\n"
    body += "================================\n\n"

    # --------------------------------------
    # BUY ALERTS
    # --------------------------------------

    if buy_alerts:

        body += "BUY ALERTS\n"
        body += "----------\n\n"

        body += (
            "The current price is below the specified "
            "buying price.\n\n"
        )

        for alert in buy_alerts:
            body += alert
            body += "\n"

    # --------------------------------------
    # SELL ALERTS
    # --------------------------------------

    if sell_alerts:

        body += "SELL ALERTS\n"
        body += "-----------\n\n"

        body += (
            "The current price has reached or exceeded "
            "the target selling price.\n\n"
        )

        for alert in sell_alerts:
            body += alert
            body += "\n"

    body += "This is an automated stock monitoring alert."

    msg.set_content(body)

    # --------------------------------------
    # Send email
    # --------------------------------------

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
    # Alert lists
    # --------------------------------------

    buy_alerts = []
    sell_alerts = []

    # --------------------------------------
    # Check stocks
    # --------------------------------------

    print("Checking stocks for BUY and SELL alerts...\n")

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
            # Calculate current gain/loss
            # ----------------------------------

            gain_percent = (
                (price - buyingprice) / buyingprice
            ) * 100

            print(
                f"{symbol} ({company}): "
                f"${price:.2f} | "
                f"Buy: ${buyingprice:.2f} | "
                f"Target Sell: ${sell_price:.2f} "
                f"({targetsellingpercentage:.2f}%) | "
                f"Gain: {gain_percent:.2f}%"
            )

            # ==================================
            # BUY ALERT
            # ==================================

            if price < buyingprice:

                buy_alerts.append(
                    f"{symbol} ({company})\n"
                    f"Current price: ${price:.2f}\n"
                    f"Buying price: ${buyingprice:.2f}\n"
                    f"Price difference: "
                    f"${buyingprice - price:.2f} below buying price\n"
                    f"Potential discount: "
                    f"{((buyingprice - price) / buyingprice) * 100:.2f}%\n"
                )

            # ==================================
            # SELL ALERT
            # ==================================

            if price >= sell_price:

                sell_alerts.append(
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

    # ==========================================
    # SEND EMAIL IF ALERTS EXIST
    # ==========================================

    if buy_alerts or sell_alerts:

        send_email(
            buy_alerts,
            sell_alerts,
            receivers
        )

        print("\nAlert email sent!")
        print(f"Recipients: {len(receivers)}")
        print(f"BUY stocks triggering alert: {len(buy_alerts)}")
        print(f"SELL stocks triggering alert: {len(sell_alerts)}")

    else:

        print("\nNo BUY or SELL alerts triggered.")

