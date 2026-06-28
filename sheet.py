import os
from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials
from zoneinfo import ZoneInfo

# -----------------------------
# Google Connection
# -----------------------------

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "service-account.json",
    scopes=SCOPES
)

client = gspread.authorize(creds)

spreadsheet = client.open_by_key(
    os.getenv("SHEET_ID")
)

# Bangladesh Time
BD_TIME = ZoneInfo("Asia/Dhaka")


# -----------------------------
# Current Date & Time
# -----------------------------

def now_bd():

    now = datetime.now(BD_TIME)

    return {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%I:%M:%S %p"),
        "datetime": now
    }


# -----------------------------
# Read Consumers Sheet
# -----------------------------

def get_consumers():

    ws = spreadsheet.worksheet("Consumers")

    rows = ws.get_all_values()

    consumers = []

    # Row 1 = Title
    # Row 2 = Header
    # Data starts from Row 3

    for row in rows[2:]:

        if len(row) < 4:
            continue

        sheet_name = row[0].strip()
        name = row[1].strip()
        consumer = row[2].strip()
        enabled = row[3].strip().upper()

        if enabled != "TRUE":
            continue

        consumers.append({
            "sheet": sheet_name,
            "name": name,
            "consumer": consumer
        })

    return consumers


# -----------------------------
# Get User Sheet
# -----------------------------

def get_user_sheet(sheet_name):

    return spreadsheet.worksheet(sheet_name)
    # -----------------------------
# Last Balance
# -----------------------------

def get_last_balance(sheet_name):

    ws = get_user_sheet(sheet_name)

    rows = ws.get_all_values()

    if len(rows) <= 2:
        return None

    last = rows[-1]

    try:
        return float(last[2])
    except:
        return None


# -----------------------------
# Today's First Balance
# -----------------------------

def get_today_first_balance(sheet_name):

    ws = get_user_sheet(sheet_name)

    rows = ws.get_all_values()

    if len(rows) <= 2:
        return None

    today = now_bd()["date"]

    for row in rows[2:]:

        if len(row) < 3:
            continue

        if row[0].strip() == today:

            try:
                return float(row[2])
            except:
                return None

    return None


# -----------------------------
# Yesterday Last Balance
# -----------------------------

def get_yesterday_balance(sheet_name):

    ws = get_user_sheet(sheet_name)

    rows = ws.get_all_values()

    if len(rows) <= 2:
        return None

    today = now_bd()["date"]

    yesterday_balance = None

    for row in rows[2:]:

        if len(row) < 3:
            continue

        date = row[0].strip()

        if date != today:

            try:
                yesterday_balance = float(row[2])
            except:
                pass

    return yesterday_balance


# -----------------------------
# Daily Uses
# -----------------------------

def calculate_daily_uses(sheet_name, current_balance):

    first_balance = get_today_first_balance(sheet_name)

    if first_balance is None:
        return 0.0

    return round(first_balance - current_balance, 3)
    # -----------------------------
# Save Balance
# -----------------------------

def save_balance(sheet_name, current_balance):

    ws = get_user_sheet(sheet_name)

    current_balance = float(current_balance)

    yesterday_balance = get_yesterday_balance(sheet_name)

    if yesterday_balance is None:
        daily_uses = 0.000
    else:
        daily_uses = round(
            yesterday_balance - current_balance,
            3
        )

    now = now_bd()

    ws.append_row([
        now["date"],
        now["time"],
        current_balance,
        daily_uses
    ])

    return {
        "yesterday": yesterday_balance,
        "daily_uses": daily_uses
    }


# -----------------------------
# Balance Status
# -----------------------------

def get_balance_status(balance):

    balance = float(balance)

    if balance > 50:
        return "NORMAL"

    if balance >= -20:
        return "LOW"

    if balance > -450:
        return "NEGATIVE"

    return "CRITICAL"


# -----------------------------
# Alert Message
# -----------------------------

def get_alert(balance, name, consumer):

    status = get_balance_status(balance)

    if status == "LOW":

        return f"""⚠️ LOW BALANCE ALERT

👤 {name}
🔢 {consumer}

💰 Balance : {balance:.3f} Tk

⚡ Please recharge soon.
"""

    if status == "CRITICAL":

        return f"""🚨 CRITICAL BALANCE ALERT

👤 {name}
🔢 {consumer}

💰 Balance : {balance:.3f} Tk

⚡ Immediate recharge required.
"""

    return None
