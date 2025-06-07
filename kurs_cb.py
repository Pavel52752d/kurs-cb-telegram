import requests
from datetime import datetime
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# === Получаем курс валют с ЦБ РФ ===
cb_url = "https://www.cbr-xml-daily.ru/daily_json.js"
cb_response = requests.get(cb_url)
cb_data = cb_response.json()

usd = cb_data['Valute']['USD']['Value']
eur = cb_data['Valute']['EUR']['Value']
cny = cb_data['Valute']['CNY']['Value']

cb_date = datetime.strptime(
    cb_data['Date'], "%Y-%m-%dT%H:%M:%S%z"
).strftime("%d.%m.%Y")

# === Получаем курс биткоина в рублях (через CoinGecko) ===
btc_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=rub"
btc_response = requests.get(btc_url)
btc_data = btc_response.json()
btc_rub = btc_data['bitcoin']['rub']

# === Формируем сообщение ===
message = f"📅 Курс ЦБ РФ на {cb_date}\n\n"
message += f"💵 USD: {usd:.2f} ₽\n"
message += f"💶 EUR: {eur:.2f} ₽\n"
message += f"🇨🇳 CNY: {cny:.2f} ₽\n\n"
message += f"₿ BTC: {btc_rub:,.0f} ₽"  # Без копеек, с разделением разрядов

# === Отправляем в Telegram ===
requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
)

print("✅ Курс отправлен в Telegram.")
