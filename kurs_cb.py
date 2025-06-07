import requests
from datetime import datetime
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

url = "https://www.cbr-xml-daily.ru/daily_json.js"
response = requests.get(url)
data = response.json()

usd = data['Valute']['USD']['Value']
eur = data['Valute']['EUR']['Value']
cny = data['Valute']['CNY']['Value']

date = datetime.strptime(
    data['Date'], "%Y-%m-%dT%H:%M:%S%z"
).strftime("%d.%m.%Y")

message = f"📅 Курс ЦБ РФ на {date}\n\n"
message += f"💵 USD: {usd:.2f} ₽\n\n"
message += f"💶 EUR: {eur:.2f} ₽\n\n"
message += f"🇨🇳 CNY: {cny:.2f} ₽"

requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
)

print("✅ Курс отправлен в Telegram.")
