from datetime import datetime

from tracker import get_balance
from sheet import get_consumers, save_balance
from telegram import send_message


def main():

    print("=" * 50)
    print("Powered by Romeo")
    print("=" * 50)

    consumers = get_consumers()

    if len(consumers) == 0:
        print("No consumer found.")
        return

    report = []

    report.append("⚡ NescoWatch")
    report.append("Powered by Romeo")
    report.append("")

    success = 0
    failed = 0

    for item in consumers:

        print(f"Checking {item['name']} ({item['consumer']})")

        try:

            data = get_balance(item["consumer"])

            save_balance(
                item["sheet"],
                data["balance"]
            )

            report.append(
                f"✅ {item['name']}\n"
                f"🔢 {item['consumer']}\n"
                f"💰 {data['balance']} Tk\n"
            )

            success += 1

        except Exception as e:

            report.append(
                f"❌ {item['name']}\n"
                f"🔢 {item['consumer']}\n"
                f"⚠️ {str(e)}\n"
            )

            failed += 1

    report.append("")
    report.append("━━━━━━━━━━━━━━")
    report.append(f"✅ Success : {success}")
    report.append(f"❌ Failed : {failed}")
    report.append(
        datetime.now().strftime("🕒 %Y-%m-%d %H:%M:%S")
    )

    send_message("\n".join(report))

    print("Finished.")


if __name__ == "__main__":
    main()
