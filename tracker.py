import re
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://customer.nesco.gov.bd/pre/panel"


def get_balance(consumer_number):

    session = requests.Session()

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/137.0 Safari/537.36"
        )
    }

    try:

        response = session.get(
            BASE_URL,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

    except requests.RequestException as e:
        raise Exception(f"NESCO Website Error: {e}")

    soup = BeautifulSoup(response.text, "lxml")

    token = soup.find("input", {"name": "_token"})

    if token is None:
        raise Exception("Security token not found")

    payload = {
        "_token": token["value"],
        "cust_no": consumer_number,
        "submit": "রিচার্জ হিস্ট্রি"
    }

    try:

        response = session.post(
            BASE_URL,
            headers=headers,
            data=payload,
            timeout=30
        )

        response.raise_for_status()

    except requests.RequestException as e:
        raise Exception(f"NESCO Server Error: {e}")

    match = re.search(
        r'অবশিষ্ট ব্যালেন্স.*?value="([^"]+)"',
        response.text,
        re.S
    )

    if not match:
        raise Exception("Balance not found")

    try:
        balance = float(match.group(1).strip())
    except ValueError:
        raise Exception("Invalid balance format")

    return {
        "consumer": consumer_number,
        "balance": balance
    }
