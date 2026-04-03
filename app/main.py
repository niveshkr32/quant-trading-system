import yfinance as yf
import time

from prometheus_client import start_http_server, Gauge
from strategy import generate_signal
from ai_model import train_model, predict
from alerts import send_alert

stocks = ["RELIANCE.NS", "TCS.NS"]

price_g = Gauge('price', 'Stock Price', ['stock'])
ai_pred_g = Gauge('ai_price', 'AI Prediction', ['stock'])
signal_g = Gauge('signal', 'Signal', ['stock'])

models = {}

print("Training models...")
for stock in stocks:
    df = yf.download(stock, period="60d", interval="5m")
    models[stock] = train_model(df)

start_http_server(8000)

last_signal = {}

while True:
    for stock in stocks:
        df = yf.download(stock, period="5d", interval="5m")

        signal, latest = generate_signal(df)
        model, scaler = models[stock]

        pred = predict(model, scaler, df)

        price = latest['Close']
        confidence = (pred - price) / price * 100

        final = "HOLD"

        if signal == "BUY" and confidence > 1:
            final = "BUY"
        elif signal == "SELL" and confidence < -1:
            final = "SELL"

        price_g.labels(stock=stock).set(price)
        ai_pred_g.labels(stock=stock).set(pred)
        signal_g.labels(stock=stock).set(
            1 if final == "BUY" else -1 if final == "SELL" else 0
        )

        if final != "HOLD" and last_signal.get(stock) != final:
            msg = f"{final} {stock} @ {price} | AI: {pred}"
            print(msg)
            send_alert(msg)
            last_signal[stock] = final

    time.sleep(60)
