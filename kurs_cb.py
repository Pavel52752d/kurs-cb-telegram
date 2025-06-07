import requests
from datetime import datetime
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# === Получаем курсы ЦБ РФ ===
cb_url = "https://www.cbr-xml-daily.ru/daily_json.js"
cb_response = requests.get(cb_url)
cb_data = cb_response.json()

usd = cb_data['Valute']['USD']['Value']
eur = cb_data['Valute']['EUR']['Value']
cny = cb_data['Valute']['CNY']['Value']

cb_date = datetime.strptime(cb_data['Date'], "%Y-%m-%dT%H:%M:%S%z").strftime("%d.%m.%Y")

# === Получаем курс биткоина к доллару через CoinGecko ===
btc_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
btc_response = requests.get(btc_url)
btc_data = btc_response.json()

btc_usd = btc_data.get("bitcoin", {}).get("usd")
if btc_usd is None:
    btc_line = "⚠️ ₿ BTC: не удалось получить курс"
else:
    btc_line = f"🟠 ₿ Bitcoin: {btc_usd:,.0f} $"

# === Формируем сообщение с отступами ===
message = (
    f"📅 Курс ЦБ РФ на {cb_date}\n\n"
    f"💵 USD: {usd:.2f} ₽\n\n"
    f"💶 EUR: {eur:.2f} ₽\n\n"
    f"🇨🇳 CNY: {cny:.2f} ₽\n\n"
    f"{btc_line}"
)

# === Отправка в Telegram ===
requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
)

print("✅ Курс отправлен в Telegram.")
