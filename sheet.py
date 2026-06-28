import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

from config import SHEET_ID

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "service-account.json",
    scopes=SCOPES
)

client = gspread.authorize(creds)

sheet = client.open_by_key(SHEET_ID).sheet1


def save_balance(consumer, balance):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sheet.append_row([
        now,
        consumer,
        balance
    ])

    print("✅ Saved to Google Sheet")