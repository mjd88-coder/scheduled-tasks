import csv
import os
import smtplib
import tkinter as tk
from tkinter import ttk, messagebox
from email.message import EmailMessage

import yfinance as yf


# ============================================================
# FILES
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STOCKS_FILE = os.path.join(BASE_DIR, "stockstobuy.csv")
RECEIVERS_FILE = os.path.join(BASE_DIR, "receiversemail.csv")


# ============================================================
# EMAIL SETTINGS
# ============================================================

EMAIL_SENDER = os.environ.get("MY_EMAIL")
EMAIL_PASSWORD = os.environ.get("MY_PASSWORD")


# ============================================================
# LOAD STOCKS FROM CSV
# ============================================================

def load_stocks(filename):

    stocks = []

    with open(
        filename,
        mode="r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            symbol = row["symbol"].strip().upper()
            company = row["company"].strip()
            buying_price = float(row["buyingprice"])

            stocks.append({
                "symbol": symbol,
                "company": company,
                "buyingprice": buying_price
            })

    return stocks


# ============================================================
# SAVE STOCKS TO CSV
# ============================================================

def save_stocks(filename, stocks):

    fieldnames = [
        "symbol",
        "company",
        "buyingprice"
    ]

    with open(
        filename,
        mode="w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for stock in stocks:

            writer.writerow({
                "symbol": stock["symbol"],
                "company": stock["company"],
                "buyingprice": stock["buyingprice"]
            })


# ============================================================
# REMOVE DUPLICATES
# ============================================================

def remove_duplicate_symbols(stocks):

    unique_stocks = []
    seen_symbols = set()
    duplicates = []

    for stock in stocks:

        symbol = stock["symbol"].strip().upper()

        if symbol in seen_symbols:

            duplicates.append(symbol)

        else:

            seen_symbols.add(symbol)
            unique_stocks.append(stock)

    return unique_stocks, duplicates


# ============================================================
# LOAD EMAIL RECIPIENTS
# ============================================================

def load_receivers(filename):

    receivers = []

    with open(
        filename,
        mode="r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            email = row["email"].strip()

            if email:
                receivers.append(email)

    return receivers


# ============================================================
# GET CURRENT STOCK PRICE
# ============================================================

def get_stock_price(symbol):

    ticker = yf.Ticker(symbol)

    # --------------------------------------------------------
    # First attempt: fast_info
    # --------------------------------------------------------

    try:

        price = ticker.fast_info.get("lastPrice")

        if price is not None:
            return float(price)

    except Exception:
        pass

    # --------------------------------------------------------
    # Second attempt: ticker.info
    # --------------------------------------------------------

    try:

        price = ticker.info.get("currentPrice")

        if price is not None:
            return float(price)

    except Exception:
        pass

    return None


# ============================================================
# SEND EMAIL
# ============================================================

def send_email(alerts, receivers):

    if not EMAIL_SENDER:

        raise Exception(
            "MY_EMAIL environment variable is not configured."
        )

    if not EMAIL_PASSWORD:

        raise Exception(
            "MY_PASSWORD environment variable is not configured."
        )

    if not receivers:

        raise Exception(
            "No email recipients found."
        )

    msg = EmailMessage()

    msg["Subject"] = "BUY Stock Alert"
    msg["From"] = EMAIL_SENDER
    msg["To"] = ", ".join(receivers)

    body = (
        "The following stocks are below "
        "their target buy prices:\n\n"
    )

    for alert in alerts:

        body += alert
        body += "\n"

    body += (
        "\nThis is an automated stock price alert."
    )

    msg.set_content(body)

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as server:

        server.login(
            EMAIL_SENDER,
            EMAIL_PASSWORD
        )

        server.send_message(msg)


# ============================================================
# MAIN APPLICATION
# ============================================================

class StockMonitorApp:

    def __init__(self, root):

        self.root = root

        # ====================================================
        # WINDOW
        # ====================================================

        self.root.title("Stock Buy Monitor")

        try:

            self.root.state("zoomed")

        except tk.TclError:

            try:
                self.root.attributes("-zoomed", True)

            except tk.TclError:
                pass

        # ====================================================
        # DATA
        # ====================================================

        self.stocks = []
        self.processed_stocks = []
        self.last_alerts = []

        self.selected_symbol = None
        self.add_mode = False

        # ====================================================
        # VARIABLES
        # ====================================================

        self.symbol_var = tk.StringVar()
        self.company_var = tk.StringVar()
        self.buying_price_var = tk.StringVar()
        self.search_var = tk.StringVar()

        self.status_var = tk.StringVar(
            value="Ready"
        )

        # ====================================================
        # CREATE GUI
        # ====================================================

        self.create_gui()

        # ====================================================
        # LOAD CSV
        # ====================================================

        self.load_csv_data()


    # ========================================================
    # CREATE GUI
    # ========================================================

    def create_gui(self):

        # ====================================================
        # STYLES
        # ====================================================

        style = ttk.Style()

        style.configure(
            "Bold.TLabel",
            font=("Arial", 10, "bold")
        )

        style.configure(
            "Bold.TLabelframe",
            font=("Arial", 11, "bold")
        )

        style.configure(
            "Bold.TLabelframe.Label",
            font=("Arial", 11, "bold")
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )

        style.configure(
            "Treeview",
            font=("Arial", 10)
        )

        # ====================================================
        # MAIN TITLE
        # ====================================================

        title_frame = ttk.Frame(
            self.root,
            padding=15
        )

        title_frame.pack(fill="x")

        ttk.Label(
            title_frame,
            text="Stock Monitoring and BUY Price Management",
            font=("Arial", 24, "bold")
        ).pack(side="left")

        # ====================================================
        # STOCK EDITOR
        # ====================================================

        editor_frame = ttk.LabelFrame(
            self.root,
            text="Stock Editor",
            style="Bold.TLabelframe",
            padding=15
        )

        editor_frame.pack(
            fill="x",
            padx=15,
            pady=5
        )

        # ====================================================
        # SYMBOL
        # ====================================================

        ttk.Label(
            editor_frame,
            text="Symbol:",
            style="Bold.TLabel"
        ).grid(
            row=0,
            column=0,
            padx=8,
            pady=8,
            sticky="w"
        )

        self.symbol_entry = ttk.Entry(
            editor_frame,
            textvariable=self.symbol_var,
            width=20,
            font=("Arial", 11)
        )

        self.symbol_entry.grid(
            row=0,
            column=1,
            padx=8,
            pady=8,
            sticky="ew"
        )

        # ====================================================
        # COMPANY
        # ====================================================

        ttk.Label(
            editor_frame,
            text="Company:",
            style="Bold.TLabel"
        ).grid(
            row=0,
            column=2,
            padx=8,
            pady=8,
            sticky="w"
        )

        self.company_entry = ttk.Entry(
            editor_frame,
            textvariable=self.company_var,
            width=40,
            font=("Arial", 11)
        )

        self.company_entry.grid(
            row=0,
            column=3,
            padx=8,
            pady=8,
            sticky="ew"
        )

        # ====================================================
        # TARGET BUY PRICE
        # ====================================================

        ttk.Label(
            editor_frame,
            text="Target Buy Price:",
            style="Bold.TLabel"
        ).grid(
            row=0,
            column=4,
            padx=8,
            pady=8,
            sticky="w"
        )

        self.buying_price_entry = ttk.Entry(
            editor_frame,
            textvariable=self.buying_price_var,
            width=18,
            font=("Arial", 11)
        )

        self.buying_price_entry.grid(
            row=0,
            column=5,
            padx=8,
            pady=8,
            sticky="ew"
        )

        # ====================================================
        # EDITOR BUTTONS
        # ====================================================

        button_frame = ttk.Frame(editor_frame)

        button_frame.grid(
            row=1,
            column=0,
            columnspan=6,
            pady=(12, 2)
        )

        ttk.Button(
            button_frame,
            text="Add New Stock",
            command=self.add_new_stock_mode
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            button_frame,
            text="Save Changes / CSV",
            command=self.save_button_clicked
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            button_frame,
            text="Delete Selected",
            command=self.delete_stock
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            button_frame,
            text="Cancel",
            command=self.cancel_edit
        ).pack(
            side="left",
            padx=5
        )

        # ====================================================
        # STOCKS TO BUY TABLE
        # ====================================================

        table_frame = ttk.LabelFrame(
            self.root,
            text="Stocks to Buy",
            style="Bold.TLabelframe",
            padding=10
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=5
        )

        # ====================================================
        # SEARCH BAR
        # ====================================================

        search_frame = ttk.Frame(table_frame)

        search_frame.pack(
            fill="x",
            pady=(0, 10)
        )

        ttk.Label(
            search_frame,
            text="Search Symbol / Company:",
            style="Bold.TLabel"
        ).pack(
            side="left",
            padx=(5, 8)
        )

        self.search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=40,
            font=("Arial", 11)
        )

        self.search_entry.pack(
            side="left",
            padx=5
        )

        ttk.Button(
            search_frame,
            text="Search",
            command=self.search_stocks
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            search_frame,
            text="Refresh",
            command=self.refresh_csv_table
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            search_frame,
            text="Clear Search",
            command=self.clear_search
        ).pack(
            side="left",
            padx=5
        )

        self.search_entry.bind(
            "<Return>",
            self.search_stocks
        )

        # ====================================================
        # STOCK TREEVIEW
        # ====================================================

        columns = (
            "symbol",
            "company",
            "buyingprice"
        )

        self.stock_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        self.stock_tree.heading(
            "symbol",
            text="Symbol",
            anchor="w"
        )

        self.stock_tree.heading(
            "company",
            text="Company",
            anchor="w"
        )

        self.stock_tree.heading(
            "buyingprice",
            text="Target Buy Price",
            anchor="e"
        )

        self.stock_tree.column(
            "symbol",
            width=150,
            anchor="w",
            stretch=False
        )

        self.stock_tree.column(
            "company",
            width=500,
            anchor="w",
            stretch=True
        )

        self.stock_tree.column(
            "buyingprice",
            width=180,
            anchor="e",
            stretch=False
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.stock_tree.yview
        )

        self.stock_tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.stock_tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.stock_tree.bind(
            "<<TreeviewSelect>>",
            self.on_stock_selected
        )

        self.stock_tree.bind(
            "<Double-1>",
            self.on_stock_double_click
        )

        # ====================================================
        # COMMAND BUTTON PANEL
        #
        # MOVED HERE:
        # BETWEEN STOCKS TO BUY AND CURRENT STOCK INFORMATION
        # ====================================================

        command_frame = ttk.LabelFrame(
            self.root,
            text="Commands",
            style="Bold.TLabelframe",
            padding=10
        )

        command_frame.pack(
            fill="x",
            padx=15,
            pady=5
        )

        command_button_frame = ttk.Frame(
            command_frame
        )

        command_button_frame.pack(
            anchor="center"
        )

        ttk.Button(
            command_button_frame,
            text="Refresh Stock Prices",
            command=self.process_stocks
        ).pack(
            side="left",
            padx=8
        )

        ttk.Button(
            command_button_frame,
            text="Send BUY Alerts by Email",
            command=self.email_alerts
        ).pack(
            side="left",
            padx=8
        )

        # ====================================================
        # CURRENT STOCK INFORMATION
        # ====================================================

        processed_frame = ttk.LabelFrame(
            self.root,
            text="Current Stock Information",
            style="Bold.TLabelframe",
            padding=10
        )

        processed_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=5
        )

        processed_columns = (
            "symbol",
            "company",
            "current",
            "target",
            "difference",
            "discount",
            "status"
        )

        headings = {
            "symbol": "Symbol",
            "company": "Company",
            "current": "Current Price",
            "target": "Target Price",
            "difference": "Difference",
            "discount": "Discount %",
            "status": "Status"
        }

        widths = {
            "symbol": 100,
            "company": 300,
            "current": 130,
            "target": 130,
            "difference": 130,
            "discount": 120,
            "status": 180
        }

        self.processed_tree = ttk.Treeview(
            processed_frame,
            columns=processed_columns,
            show="headings"
        )

        for column in processed_columns:

            if column in (
                "symbol",
                "company"
            ):

                self.processed_tree.heading(
                    column,
                    text=headings[column],
                    anchor="w"
                )

                self.processed_tree.column(
                    column,
                    width=widths[column],
                    anchor="w"
                )

            else:

                self.processed_tree.heading(
                    column,
                    text=headings[column],
                    anchor="center"
                )

                self.processed_tree.column(
                    column,
                    width=widths[column],
                    anchor="center"
                )

        processed_scrollbar = ttk.Scrollbar(
            processed_frame,
            orient="vertical",
            command=self.processed_tree.yview
        )

        self.processed_tree.configure(
            yscrollcommand=processed_scrollbar.set
        )

        self.processed_tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        processed_scrollbar.pack(
            side="right",
            fill="y"
        )

        # ====================================================
        # STATUS BAR
        # ====================================================

        ttk.Label(
            self.root,
            textvariable=self.status_var,
            style="Bold.TLabel",
            relief="sunken",
            anchor="w",
            padding=5
        ).pack(
            fill="x",
            side="bottom"
        )

        # ====================================================
        # GRID CONFIGURATION
        # ====================================================

        editor_frame.columnconfigure(
            1,
            weight=1
        )

        editor_frame.columnconfigure(
            3,
            weight=2
        )

        editor_frame.columnconfigure(
            5,
            weight=1
        )


    # ========================================================
    # SORT STOCKS ALPHABETICALLY
    # ========================================================

    def sort_stocks_by_symbol(self):

        self.stocks.sort(
            key=lambda stock:
                stock["symbol"].strip().upper()
        )


    # ========================================================
    # LOAD CSV DATA
    # ========================================================

    def load_csv_data(self):

        try:

            loaded_stocks = load_stocks(
                STOCKS_FILE
            )

            cleaned_stocks, duplicates = (
                remove_duplicate_symbols(
                    loaded_stocks
                )
            )

            self.stocks = cleaned_stocks

            if duplicates:

                save_stocks(
                    STOCKS_FILE,
                    self.stocks
                )

            self.sort_stocks_by_symbol()

            self.refresh_stock_table(
                select_first=True
            )

            if duplicates:

                duplicate_text = ", ".join(
                    sorted(set(duplicates))
                )

                messagebox.showwarning(
                    "Duplicate Symbols Removed",
                    "Duplicate symbols were found.\n\n"
                    f"{duplicate_text}\n\n"
                    "Only the first occurrence "
                    "of each symbol was kept."
                )

            self.status_var.set(
                f"{len(self.stocks)} stocks loaded "
                "alphabetically."
            )

        except FileNotFoundError:

            messagebox.showerror(
                "CSV File Error",
                "Could not find:\n\n"
                f"{STOCKS_FILE}"
            )

        except Exception as e:

            messagebox.showerror(
                "CSV Error",
                str(e)
            )


    # ========================================================
    # REFRESH CSV TABLE
    # ========================================================

    def refresh_csv_table(self):

        try:

            loaded_stocks = load_stocks(
                STOCKS_FILE
            )

            cleaned_stocks, duplicates = (
                remove_duplicate_symbols(
                    loaded_stocks
                )
            )

            self.stocks = cleaned_stocks

            if duplicates:

                save_stocks(
                    STOCKS_FILE,
                    self.stocks
                )

            self.sort_stocks_by_symbol()

            self.selected_symbol = None
            self.add_mode = False

            self.clear_editor()

            self.search_var.set("")

            self.refresh_stock_table(
                select_first=True
            )

            self.processed_stocks = []
            self.last_alerts = []

            for item in self.processed_tree.get_children():

                self.processed_tree.delete(item)

            self.status_var.set(
                f"CSV refreshed: "
                f"{len(self.stocks)} stocks loaded "
                "alphabetically."
            )

            if duplicates:

                duplicate_text = ", ".join(
                    sorted(set(duplicates))
                )

                messagebox.showwarning(
                    "Duplicate Symbols Removed",
                    "Duplicate symbols were found "
                    "in the CSV.\n\n"
                    f"{duplicate_text}\n\n"
                    "Only the first occurrence "
                    "of each symbol was kept."
                )

            else:

                messagebox.showinfo(
                    "CSV Refreshed",
                    "The Stocks to Buy table was "
                    "refreshed from the CSV file.\n\n"
                    f"Stocks loaded: {len(self.stocks)}"
                )

        except FileNotFoundError:

            messagebox.showerror(
                "CSV Refresh Error",
                "Could not find:\n\n"
                f"{STOCKS_FILE}"
            )

        except Exception as e:

            messagebox.showerror(
                "CSV Refresh Error",
                "Could not refresh the Stocks to Buy table.\n\n"
                f"{e}"
            )


    # ========================================================
    # SEARCH STOCKS
    # ========================================================

    def search_stocks(self, event=None):

        search_text = (
            self.search_var
            .get()
            .strip()
            .lower()
        )

        if not search_text:

            self.refresh_stock_table(
                select_first=True
            )

            self.status_var.set(
                f"Showing all {len(self.stocks)} stocks."
            )

            return

        matching_stocks = []

        for stock in self.stocks:

            symbol = stock["symbol"].strip().lower()
            company = stock["company"].strip().lower()

            if (
                search_text in symbol
                or
                search_text in company
            ):

                matching_stocks.append(stock)

        matching_stocks.sort(
            key=lambda stock:
                stock["symbol"].strip().upper()
        )

        self.display_stock_table(
            matching_stocks,
            select_first=bool(matching_stocks)
        )

        self.selected_symbol = None
        self.add_mode = False

        self.symbol_var.set("")
        self.company_var.set("")
        self.buying_price_var.set("")

        self.symbol_entry.config(
            state="normal"
        )

        self.company_entry.config(
            state="normal"
        )

        self.status_var.set(
            f"Search '{self.search_var.get()}': "
            f"{len(matching_stocks)} match(es) found."
        )

        if not matching_stocks:

            messagebox.showinfo(
                "Search",
                "No stocks matched your search.\n\n"
                f"Search: {self.search_var.get()}"
            )


    # ========================================================
    # CLEAR SEARCH
    # ========================================================

    def clear_search(self):

        self.search_var.set("")

        self.selected_symbol = None
        self.add_mode = False

        self.symbol_var.set("")
        self.company_var.set("")
        self.buying_price_var.set("")

        self.symbol_entry.config(
            state="normal"
        )

        self.company_entry.config(
            state="normal"
        )

        self.sort_stocks_by_symbol()

        self.refresh_stock_table(
            select_first=True
        )

        self.status_var.set(
            f"Search cleared: "
            f"{len(self.stocks)} stocks shown."
        )


    # ========================================================
    # DISPLAY STOCK TABLE
    # ========================================================

    def display_stock_table(
        self,
        stocks,
        select_first=False
    ):

        for item in self.stock_tree.get_children():

            self.stock_tree.delete(item)

        sorted_stocks = sorted(
            stocks,
            key=lambda stock:
                stock["symbol"].strip().upper()
        )

        for stock in sorted_stocks:

            symbol = stock["symbol"].strip().upper()
            company = stock["company"].strip()

            self.stock_tree.insert(
                "",
                "end",
                iid=symbol,
                values=(
                    f"  {symbol}",
                    f"  {company}",
                    f'{stock["buyingprice"]:.2f}'
                )
            )

        if select_first:

            children = self.stock_tree.get_children()

            if children:

                first_item = children[0]

                self.stock_tree.selection_set(
                    first_item
                )

                self.stock_tree.focus(
                    first_item
                )

                self.stock_tree.see(
                    first_item
                )

                self.root.after(
                    50,
                    lambda:
                        self.select_first_stock(first_item)
                )


    # ========================================================
    # SELECT FIRST STOCK
    # ========================================================

    def select_first_stock(self, item_id):

        if self.add_mode:
            return

        if not self.stock_tree.exists(item_id):
            return

        self.stock_tree.selection_set(item_id)
        self.stock_tree.focus(item_id)
        self.stock_tree.see(item_id)

        self.on_stock_selected()


    # ========================================================
    # REFRESH STOCK TABLE
    # ========================================================

    def refresh_stock_table(
        self,
        select_first=False
    ):

        self.sort_stocks_by_symbol()

        self.display_stock_table(
            self.stocks,
            select_first=select_first
        )


    # ========================================================
    # FIND STOCK BY SYMBOL
    # ========================================================

    def find_stock_by_symbol(self, symbol):

        symbol = symbol.strip().upper()

        for stock in self.stocks:

            if (
                stock["symbol"].strip().upper()
                ==
                symbol
            ):

                return stock

        return None


    # ========================================================
    # SELECT STOCK
    # ========================================================

    def on_stock_selected(self, event=None):

        if self.add_mode:
            return

        selection = self.stock_tree.selection()

        if not selection:
            return

        selected_symbol = (
            selection[0].strip().upper()
        )

        stock = self.find_stock_by_symbol(
            selected_symbol
        )

        if stock is None:
            return

        self.selected_symbol = (
            stock["symbol"].strip().upper()
        )

        self.add_mode = False

        self.symbol_var.set(
            stock["symbol"]
        )

        self.company_var.set(
            stock["company"]
        )

        self.buying_price_var.set(
            f'{stock["buyingprice"]:.2f}'
        )

        self.symbol_entry.config(
            state="readonly"
        )

        self.company_entry.config(
            state="readonly"
        )

        self.buying_price_entry.config(
            state="normal"
        )

        self.status_var.set(
            f"Selected: {stock['symbol']} - "
            f"{stock['company']}. "
            "Change the target price and click "
            "'Save Changes / CSV'."
        )


    # ========================================================
    # DOUBLE CLICK
    # ========================================================

    def on_stock_double_click(self, event=None):

        self.on_stock_selected(event)


    # ========================================================
    # ADD NEW STOCK MODE
    # ========================================================

    def add_new_stock_mode(self):

        self.add_mode = True
        self.selected_symbol = None

        self.symbol_var.set("")
        self.company_var.set("")
        self.buying_price_var.set("")

        self.symbol_entry.config(
            state="normal"
        )

        self.company_entry.config(
            state="normal"
        )

        self.buying_price_entry.config(
            state="normal"
        )

        selection = self.stock_tree.selection()

        if selection:

            self.stock_tree.selection_remove(
                selection
            )

        self.symbol_entry.focus_set()

        self.status_var.set(
            "Add New Stock mode: "
            "enter Symbol, Company and Target Buy Price, "
            "then click 'Save Changes / CSV'."
        )


    # ========================================================
    # GET BUYING PRICE
    # ========================================================

    def get_buying_price(self):

        price_text = (
            self.buying_price_var
            .get()
            .strip()
        )

        if not price_text:

            raise ValueError(
                "Please enter a target buying price."
            )

        price_text = price_text.replace(",", ".")

        try:

            price = float(price_text)

        except ValueError:

            raise ValueError(
                "The buying price must be a number."
            )

        if price <= 0:

            raise ValueError(
                "The buying price must be greater than zero."
            )

        return price


    # ========================================================
    # GET NEW STOCK DATA
    # ========================================================

    def get_new_stock_data(self):

        symbol = (
            self.symbol_var
            .get()
            .strip()
            .upper()
        )

        company = (
            self.company_var
            .get()
            .strip()
        )

        if not symbol:

            raise ValueError(
                "Please enter a stock symbol."
            )

        if not company:

            raise ValueError(
                "Please enter the company name."
            )

        price = self.get_buying_price()

        return {
            "symbol": symbol,
            "company": company,
            "buyingprice": price
        }


    # ========================================================
    # CHECK SYMBOL EXISTS
    # ========================================================

    def symbol_exists(self, symbol):

        symbol = symbol.strip().upper()

        for stock in self.stocks:

            if (
                stock["symbol"].strip().upper()
                ==
                symbol
            ):

                return True

        return False


    # ========================================================
    # SAVE BUTTON
    # ========================================================

    def save_button_clicked(self):

        if self.add_mode:

            self.save_new_stock()
            return

        if self.selected_symbol:

            self.update_selected_stock()
            return

        messagebox.showwarning(
            "Save Stock",
            "Please either:\n\n"
            "1. Click 'Add New Stock' to add a new stock, or\n\n"
            "2. Select a stock from the table to edit it."
        )


    # ========================================================
    # SAVE NEW STOCK
    # ========================================================

    def save_new_stock(self):

        if not self.add_mode:

            messagebox.showwarning(
                "Add Stock",
                "Please click 'Add New Stock' first."
            )

            return

        try:

            new_stock = self.get_new_stock_data()

        except ValueError as e:

            messagebox.showwarning(
                "Invalid Stock Data",
                str(e)
            )

            return

        new_symbol = new_stock["symbol"]

        if self.symbol_exists(new_symbol):

            messagebox.showwarning(
                "Duplicate Symbol",
                f"The symbol '{new_symbol}' already exists.\n\n"
                "A stock symbol can only exist once."
            )

            self.symbol_entry.focus_set()

            return

        old_stocks = [
            stock.copy()
            for stock in self.stocks
        ]

        self.stocks.append(new_stock)

        if not self.save_current_stocks(
            show_message=False
        ):

            self.stocks = old_stocks
            self.refresh_stock_table()
            return

        try:

            self.stocks = load_stocks(
                STOCKS_FILE
            )

        except Exception as e:

            self.stocks = old_stocks
            self.refresh_stock_table()

            messagebox.showerror(
                "CSV Reload Error",
                "The stock was saved, but the CSV "
                "could not be reloaded.\n\n"
                f"{e}"
            )

            return

        self.sort_stocks_by_symbol()

        self.add_mode = False
        self.selected_symbol = None

        self.refresh_stock_table(
            select_first=True
        )

        self.clear_editor()

        self.processed_stocks = []
        self.last_alerts = []

        for item in self.processed_tree.get_children():

            self.processed_tree.delete(item)

        self.status_var.set(
            f"{new_symbol} successfully added. "
            f"{len(self.stocks)} stocks loaded."
        )

        messagebox.showinfo(
            "Stock Added",
            "New stock successfully added.\n\n"
            f"Symbol: {new_stock['symbol']}\n"
            f"Company: {new_stock['company']}\n"
            f"Target price: {new_stock['buyingprice']:.2f}\n\n"
            "The CSV file has been updated.\n"
            "The Stocks to Buy table has been repopulated "
            "alphabetically."
        )


    # ========================================================
    # UPDATE SELECTED STOCK
    # ========================================================

    def update_selected_stock(self):

        if not self.selected_symbol:

            messagebox.showwarning(
                "Update Stock",
                "Please select a stock first."
            )

            return

        original_symbol = (
            self.selected_symbol
            .strip()
            .upper()
        )

        selected_stock = self.find_stock_by_symbol(
            original_symbol
        )

        if selected_stock is None:

            messagebox.showerror(
                "Update Error",
                f"Stock '{original_symbol}' could not be found."
            )

            return

        editor_symbol = (
            self.symbol_var
            .get()
            .strip()
            .upper()
        )

        if editor_symbol != original_symbol:

            messagebox.showerror(
                "Symbol Verification Failed",
                "The symbol in the editor does not match "
                "the selected stock.\n\n"
                f"Selected: {original_symbol}\n"
                f"Editor:   {editor_symbol}\n\n"
                "The update was cancelled."
            )

            return

        editor_company = (
            self.company_var
            .get()
            .strip()
        )

        original_company = (
            selected_stock["company"].strip()
        )

        if editor_company != original_company:

            messagebox.showerror(
                "Company Verification Failed",
                "The company in the editor does not "
                "match the selected stock.\n\n"
                f"Selected: {original_company}\n"
                f"Editor:   {editor_company}\n\n"
                "The update was cancelled."
            )

            return

        try:

            new_price = self.get_buying_price()

        except ValueError as e:

            messagebox.showwarning(
                "Invalid Buying Price",
                str(e)
            )

            return

        old_price = selected_stock["buyingprice"]

        if abs(old_price - new_price) < 0.000001:

            messagebox.showinfo(
                "No Change",
                f"The buying price for "
                f"{original_symbol} is already "
                f"{old_price:.2f}."
            )

            return

        old_stocks = [
            stock.copy()
            for stock in self.stocks
        ]

        updated = False

        for stock in self.stocks:

            stock_symbol = (
                stock["symbol"].strip().upper()
            )

            stock_company = (
                stock["company"].strip()
            )

            if (
                stock_symbol == original_symbol
                and
                stock_company == original_company
            ):

                stock["buyingprice"] = new_price
                updated = True
                break

        if not updated:

            messagebox.showerror(
                "Update Error",
                "The selected stock could not be updated.\n\n"
                "Symbol and company verification failed."
            )

            return

        if not self.save_current_stocks(
            show_message=False
        ):

            self.stocks = old_stocks
            self.refresh_stock_table()
            return

        try:

            self.stocks = load_stocks(
                STOCKS_FILE
            )

        except Exception as e:

            self.stocks = old_stocks
            self.refresh_stock_table()

            messagebox.showerror(
                "CSV Reload Error",
                "The CSV was saved, but it could "
                "not be reloaded.\n\n"
                f"{e}"
            )

            return

        self.sort_stocks_by_symbol()

        self.selected_symbol = None
        self.add_mode = False

        self.refresh_stock_table(
            select_first=True
        )

        self.clear_editor()

        self.processed_stocks = []
        self.last_alerts = []

        for item in self.processed_tree.get_children():

            self.processed_tree.delete(item)

        self.status_var.set(
            f"{original_symbol} updated successfully. "
            f"New target price: {new_price:.2f}"
        )

        messagebox.showinfo(
            "Stock Updated",
            "The stock was successfully updated.\n\n"
            f"Symbol: {original_symbol}\n"
            f"Company: {original_company}\n"
            f"Old target price: {old_price:.2f}\n"
            f"New target price: {new_price:.2f}\n\n"
            "The Stocks to Buy table has been refreshed.\n"
            "The CSV file has been updated."
        )


    # ========================================================
    # DELETE STOCK
    # ========================================================

    def delete_stock(self):

        if not self.selected_symbol:

            messagebox.showwarning(
                "Delete Stock",
                "Please select a stock first."
            )

            return

        selected_symbol = (
            self.selected_symbol
            .strip()
            .upper()
        )

        selected_stock = self.find_stock_by_symbol(
            selected_symbol
        )

        if selected_stock is None:

            messagebox.showerror(
                "Delete Error",
                f"Stock '{selected_symbol}' was not found."
            )

            return

        answer = messagebox.askyesno(
            "Confirm Delete",
            "Do you really want to delete this stock?\n\n"
            f"Symbol: {selected_stock['symbol']}\n"
            f"Company: {selected_stock['company']}\n"
            f"Target price: "
            f"{selected_stock['buyingprice']:.2f}"
        )

        if not answer:
            return

        old_stocks = [
            stock.copy()
            for stock in self.stocks
        ]

        self.stocks = [
            stock
            for stock in self.stocks
            if (
                stock["symbol"].strip().upper()
                != selected_symbol
            )
        ]

        if not self.save_current_stocks(
            show_message=False
        ):

            self.stocks = old_stocks
            self.refresh_stock_table()
            return

        self.selected_symbol = None
        self.add_mode = False

        self.sort_stocks_by_symbol()

        self.refresh_stock_table(
            select_first=True
        )

        self.clear_editor()

        self.processed_stocks = []
        self.last_alerts = []

        for item in self.processed_tree.get_children():

            self.processed_tree.delete(item)

        self.status_var.set(
            f"{selected_symbol} deleted and CSV updated."
        )

        messagebox.showinfo(
            "Stock Deleted",
            f"Stock '{selected_symbol}' "
            "was successfully deleted.\n\n"
            "The CSV file has been updated."
        )


    # ========================================================
    # CANCEL
    # ========================================================

    def cancel_edit(self):

        self.clear_editor()

        selection = self.stock_tree.selection()

        if selection:

            self.stock_tree.selection_remove(
                selection
            )

        self.status_var.set(
            "Editor cleared."
        )


    # ========================================================
    # CLEAR EDITOR
    # ========================================================

    def clear_editor(self):

        self.symbol_var.set("")
        self.company_var.set("")
        self.buying_price_var.set("")

        self.selected_symbol = None
        self.add_mode = False

        self.symbol_entry.config(
            state="normal"
        )

        self.company_entry.config(
            state="normal"
        )

        self.buying_price_entry.config(
            state="normal"
        )


    # ========================================================
    # SAVE CURRENT STOCKS
    # ========================================================

    def save_current_stocks(
        self,
        show_message=True
    ):

        try:

            symbols = [
                stock["symbol"].strip().upper()
                for stock in self.stocks
            ]

            if len(symbols) != len(set(symbols)):

                duplicate_symbols = []

                seen = set()

                for symbol in symbols:

                    if (
                        symbol in seen
                        and
                        symbol not in duplicate_symbols
                    ):

                        duplicate_symbols.append(symbol)

                    else:

                        seen.add(symbol)

                messagebox.showerror(
                    "Duplicate Symbol",
                    "The CSV was NOT saved.\n\n"
                    "Duplicate symbols detected:\n\n"
                    + "\n".join(duplicate_symbols)
                )

                return False

            save_stocks(
                STOCKS_FILE,
                self.stocks
            )

            if not os.path.isfile(STOCKS_FILE):

                raise Exception(
                    "CSV file was not created."
                )

            verified_stocks = load_stocks(
                STOCKS_FILE
            )

            if len(verified_stocks) != len(self.stocks):

                raise Exception(
                    "CSV verification failed: "
                    "record count does not match."
                )

            for saved_stock, current_stock in zip(
                verified_stocks,
                self.stocks
            ):

                if (
                    saved_stock["symbol"].strip().upper()
                    !=
                    current_stock["symbol"].strip().upper()
                ):

                    raise Exception(
                        "CSV verification failed: "
                        "symbol does not match."
                    )

                if (
                    saved_stock["company"].strip()
                    !=
                    current_stock["company"].strip()
                ):

                    raise Exception(
                        "CSV verification failed: "
                        "company does not match."
                    )

                if abs(
                    saved_stock["buyingprice"]
                    -
                    current_stock["buyingprice"]
                ) > 0.000001:

                    raise Exception(
                        "CSV verification failed: "
                        "buying price does not match."
                    )

            self.status_var.set(
                "CSV saved and verified successfully."
            )

            if show_message:

                messagebox.showinfo(
                    "CSV Saved",
                    "CSV successfully saved and verified.\n\n"
                    f"{STOCKS_FILE}"
                )

            return True

        except Exception as e:

            messagebox.showerror(
                "CSV Save Error",
                "Could not save the CSV file.\n\n"
                f"{e}"
            )

            return False


    # ========================================================
    # PROCESS STOCKS
    # ========================================================

    def process_stocks(self):

        if not self.stocks:

            messagebox.showinfo(
                "Stock Check",
                "There are no stocks to process."
            )

            return

        self.status_var.set(
            "Checking current stock prices..."
        )

        self.root.update_idletasks()

        for item in self.processed_tree.get_children():

            self.processed_tree.delete(item)

        self.processed_stocks = []
        alerts = []

        for stock in self.stocks:

            symbol = stock["symbol"]
            company = stock["company"]
            target = stock["buyingprice"]

            try:

                current = get_stock_price(symbol)

                if current is None:

                    self.processed_tree.insert(
                        "",
                        "end",
                        values=(
                            f"  {symbol}",
                            f"  {company}",
                            "N/A",
                            f"{target:.2f}",
                            "N/A",
                            "N/A",
                            "Price unavailable"
                        )
                    )

                    continue

                difference = target - current

                discount = (
                    difference / target
                ) * 100

                if current < target:

                    status = "BUY ALERT"

                    alerts.append(
                        f"{symbol} ({company})\n"
                        f"Current price: {current:.2f}\n"
                        f"Buying price: {target:.2f}\n"
                        f"Difference: {difference:.2f} below target\n"
                        f"Potential discount: {discount:.2f}%\n"
                    )

                elif current == target:

                    status = "AT TARGET"

                else:

                    status = "ABOVE TARGET"

                self.processed_tree.insert(
                    "",
                    "end",
                    values=(
                        f"  {symbol}",
                        f"  {company}",
                        f"{current:.2f}",
                        f"{target:.2f}",
                        f"{difference:.2f}",
                        f"{discount:.2f}%",
                        status
                    )
                )

                self.processed_stocks.append({

                    "symbol": symbol,
                    "company": company,
                    "current": current,
                    "target": target,
                    "difference": difference,
                    "discount": discount,
                    "status": status
                })

            except Exception as e:

                self.processed_tree.insert(
                    "",
                    "end",
                    values=(
                        f"  {symbol}",
                        f"  {company}",
                        "ERROR",
                        f"{target:.2f}",
                        "-",
                        "-",
                        str(e)
                    )
                )

        self.last_alerts = alerts

        alert_count = len(alerts)

        self.status_var.set(
            f"Processing completed: "
            f"{len(self.stocks)} stocks checked, "
            f"{alert_count} BUY alerts."
        )

        if alert_count > 0:

            messagebox.showinfo(
                "Stock Check Completed",
                "Processing completed.\n\n"
                f"Stocks checked: {len(self.stocks)}\n"
                f"BUY alerts: {alert_count}"
            )

        else:

            messagebox.showinfo(
                "Stock Check Completed",
                "Processing completed.\n\n"
                "No BUY alerts triggered."
            )


    # ========================================================
    # EMAIL ALERTS
    # ========================================================

    def email_alerts(self):

        if not self.processed_stocks:

            self.process_stocks()

        alerts = self.last_alerts

        if not alerts:

            messagebox.showinfo(
                "Email",
                "There are no BUY alerts to send."
            )

            return

        try:

            receivers = load_receivers(
                RECEIVERS_FILE
            )

            if not receivers:

                messagebox.showerror(
                    "Email Error",
                    "No email recipients found."
                )

                return

            answer = messagebox.askyesno(
                "Send BUY Alerts",
                f"Send BUY alerts to "
                f"{len(receivers)} recipient(s)?"
            )

            if not answer:
                return

            send_email(
                alerts,
                receivers
            )

            self.status_var.set(
                "BUY alert email sent successfully."
            )

            messagebox.showinfo(
                "Email Sent",
                "BUY alert email sent successfully.\n\n"
                f"Recipients: {len(receivers)}\n"
                f"BUY alerts: {len(alerts)}"
            )

        except FileNotFoundError:

            messagebox.showerror(
                "Email Error",
                "Could not find:\n\n"
                f"{RECEIVERS_FILE}"
            )

        except Exception as e:

            messagebox.showerror(
                "Email Error",
                str(e)
            )


    # ========================================================
    # CLOSE APPLICATION
    # ========================================================

    def close_application(self):

        answer = messagebox.askyesno(
            "Exit Stock Monitor",
            "Do you really want to exit?"
        )

        if answer:
            self.root.destroy()


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = StockMonitorApp(root)

    root.mainloop()