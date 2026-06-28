import re
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://customer.nesco.gov.bd/pre/panel"


def get_balance(consumer_number):

    session = requests.Session()

    response = session.get(BASE_URL)

    if response.status_code != 200:
        raise Exception("Cannot open NESCO website")

    soup = BeautifulSoup(response.text, "lxml")

    token = soup.find("input", {"name": "_token"})["value"]

    payload = {
        "_token": token,
        "cust_no": consumer_number,
        "submit": "রিচার্জ হিস্ট্রি"
    }

    headers = {
        "Referer": BASE_URL,
        "User-Agent": "Mozilla/5.0"
    }

    response = session.post(
        BASE_URL,
        data=payload,
        headers=headers,
        timeout=30
    )

    match = re.search(
        r'অবশিষ্ট ব্যালেন্স.*?value="([^"]+)"',
        response.text,
        re.S
    )

    if not match:
        raise Exception(f"Balance not found for {consumer_number}")

    return {
        "consumer": consumer_number,
        "balance": match.group(1).strip()
    }
