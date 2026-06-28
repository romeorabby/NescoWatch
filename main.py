from datetime import datetime

from tracker import get_balance
from sheet import get_consumers, save_balance
from telegram import send_message


def main():

    print("Powered by Romeo")
    print("---------------------------")

    consumers = get_consumers()

    summary = []

    summary.append("⚡ NescoWatch")
    summary.append("Powered by Romeo")
    summary.append("")

    for item in consumers:

        try:

            print(f"Checking {item['consumer']}")

            data = get_balance(item["consumer"])

            save_balance(
                item["sheet"],
                data["balance"]
            )

            summary.append(
                f"✅ {item['name']}\n"
                f"🔢 {item['consumer']}\n"
                f"💰 {data['balance']} Tk\n"
            )

        except Exception as e:

            print(e)

            summary.append(
                f"❌ {item['name']}\n"
                f"🔢 {item['consumer']}\n"
                f"{e}\n"
            )

    summary.append("")
    summary.append(
        "🕒 " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    send_message("\n".join(summary))

    print("Finished.")


if __name__ == "__main__":
    main()
