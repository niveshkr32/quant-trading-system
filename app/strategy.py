from indicators import rsi, ema

def generate_signal(df):
    df['RSI'] = rsi(df)
    df['EMA20'] = ema(df, 20)
    df['EMA50'] = ema(df, 50)

    latest = df.iloc[-1]

    if latest['RSI'] < 30 and latest['EMA20'] > latest['EMA50']:
        return "BUY", latest
    elif latest['RSI'] > 70 and latest['EMA20'] < latest['EMA50']:
        return "SELL", latest

    return "HOLD", latest
