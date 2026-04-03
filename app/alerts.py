import requests

BOT_TOKEN = "8652752416:AAHRHdMM5FCaSfKXKtFCnmmcIwLzYwpalpc"
CHAT_ID = "1517706156"

def send_alert(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
