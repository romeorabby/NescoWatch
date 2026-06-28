from tracker import get_balance
from sheet import save_balance
from telegram import send_message

print("Fetching balance...")

data = get_balance()

print(f"Consumer : {data['customer']}")
print(f"Balance  : {data['balance']} Tk")

# Save to Google Sheet
save_balance(
    data["customer"],
    data["balance"]
)

# Send Telegram Message
message = f"""⚡ NescoWatch
Powered by Romeo

👤 Consumer : {data['customer']}
💰 Balance  : {data['balance']} Tk
"""

send_message(message)

print("Done.")