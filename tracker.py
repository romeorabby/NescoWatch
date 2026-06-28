import re
import requests
from bs4 import BeautifulSoup

from config import CUSTOMER_NUMBER, BASE_URL


def get_balance():

    session = requests.Session()

    response = session.get(BASE_URL)

    if response.status_code != 200:
        raise Exception("Cannot open NESCO website")

    soup = BeautifulSoup(response.text, "lxml")

    token = soup.find("input", {"name": "_token"})["value"]

    payload = {
        "_token": token,
        "cust_no": CUSTOMER_NUMBER,
        "submit": "রিচার্জ হিস্ট্রি"
    }

    headers = {
        "Referer": BASE_URL,
        "User-Agent": "Mozilla/5.0"
    }

    response = session.post(
        BASE_URL,
        data=payload,
        headers=headers
    )

    html = response.text

    match = re.search(
        r'অবশিষ্ট ব্যালেন্স.*?value="([^"]+)"',
        html,
        re.S
    )

    if not match:
        raise Exception("Balance not found")

    balance = match.group(1).strip()

    return {
        "customer": CUSTOMER_NUMBER,
        "balance": balance
    }