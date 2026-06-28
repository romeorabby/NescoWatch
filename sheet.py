import os
from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials

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


def get_consumers():

    ws = spreadsheet.worksheet("Consumers")

    rows = ws.get_all_records()

    consumers = []

    for row in rows:

        enabled = str(row.get("Enabled", "TRUE")).strip().upper()

        if enabled != "TRUE":
            continue

        consumers.append({
            "sheet": row["Sheet"],
            "name": row["Name"],
            "consumer": str(row["Consumer"])
        })

    return consumers


def get_sheet(sheet_name):

    return spreadsheet.worksheet(sheet_name)


def save_balance(sheet_name, balance):

    ws = get_sheet(sheet_name)

    now = datetime.now()

    ws.append_row([
        now.strftime("%Y-%m-%d"),
        now.strftime("%H:%M:%S"),
        balance,
        ""
    ])

    print(f"Saved -> {sheet_name}")
