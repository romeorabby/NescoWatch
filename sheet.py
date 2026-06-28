import os
import gspread

from datetime import datetime
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

spreadsheet = client.open_by_key(os.getenv("SHEET_ID"))


def get_consumers():

    sheet = spreadsheet.worksheet("Consumers")

    rows = sheet.get_all_values()

    consumers = []

    for row in rows[1:]:

        if len(row) < 3:
            continue

        sheet_name = row[0].strip()
        display_name = row[1].strip()
        consumer_number = row[2].strip()

        if consumer_number == "":
            continue

        consumers.append({
            "sheet": sheet_name,
            "name": display_name,
            "consumer": consumer_number
        })

    return consumers


def save_balance(sheet_name, balance):

    ws = spreadsheet.worksheet(sheet_name)

    now = datetime.now()

    ws.append_row([
        now.strftime("%Y-%m-%d"),
        now.strftime("%H:%M:%S"),
        balance
    ])

    print(f"Saved -> {sheet_name}")

def save_balance(sheet_name, balance):

    ws = spreadsheet.worksheet(sheet_name)

    now = datetime.now()

    ws.append_row([
        now.strftime("%Y-%m-%d"),
        now.strftime("%H:%M:%S"),
        balance,
        ""
    ])

    print(f"Saved -> {sheet_name}")


def get_consumers():

    ws = spreadsheet.worksheet("Consumers")

    rows = ws.get_all_values()

    consumers = []

    for row in rows[1:]:

        if len(row) < 4:
            continue

        enabled = row[3].strip().upper()

        if enabled != "TRUE":
            continue

        consumers.append({
            "sheet": row[0].strip(),
            "name": row[1].strip(),
            "consumer": row[2].strip()
        })

    return consumers
