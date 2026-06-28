from sheet import (
    get_consumers,
    save_balance,
    get_alert,
    now_bd
)

from tracker import get_balance
from telegram import send_message


def main():

    print("=" * 50)
    print("Powered by Romeo")
    print("=" * 50)

    consumers = get_consumers()

    summary = []

    summary.append("⚡ NescoWatch")
    summary.append("Powered by Romeo")
    summary.append("")

    success = 0
    failed = 0

    for item in consumers:

        try:

            data = get_balance(item["consumer"])

            balance = float(data["balance"])

            info = save_balance(
                item["sheet"],
                balance
            )

            yesterday = info["yesterday"]

            if yesterday is None:
                yesterday_text = "N/A"
            else:
                yesterday_text = f"{yesterday:.3f}"

            summary.append("━━━━━━━━━━━━━━━━━━")
            summary.append(f"👤 {item['name']}")
            summary.append(f"🔢 {item['consumer']}")
            summary.append("")
            summary.append(f"📅 Yesterday : {yesterday_text} Tk")
            summary.append(f"💰 Balance   : {balance:.3f} Tk")
            summary.append(f"📉 Daily Uses: {info['daily_uses']:.3f} Tk")
            summary.append("")

            alert = get_alert(
                balance,
                item["name"],
                item["consumer"]
            )

            if alert:
                send_message(alert)

            success += 1

        except Exception as e:

            failed += 1

            summary.append("━━━━━━━━━━━━━━━━━━")
            summary.append(f"👤 {item['name']}")
            summary.append(f"❌ {e}")
            summary.append("")

    summary.append("━━━━━━━━━━━━━━━━━━")
    summary.append(f"✅ Updated : {success}")
    summary.append(f"❌ Failed  : {failed}")
    summary.append("")
    summary.append(
        f"🕒 {now_bd()['date']} {now_bd()['time']}"
    )

    send_message("\n".join(summary))

    print("Finished")


if __name__ == "__main__":
    main()
