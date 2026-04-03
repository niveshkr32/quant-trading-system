import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

def train_model(df):
    data = df['Close'].values.reshape(-1,1)

    scaler = MinMaxScaler()
    data = scaler.fit_transform(data)

    X, y = [], []
    for i in range(60, len(data)):
        X.append(data[i-60:i])
        y.append(data[i])

    X, y = np.array(X), np.array(y)

    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(60,1)))
    model.add(LSTM(50))
    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=3, batch_size=32, verbose=0)

    return model, scaler

def predict(model, scaler, df):
    last_60 = df['Close'].values[-60:].reshape(-1,1)
    last_60 = scaler.transform(last_60)

    pred = model.predict(np.array([last_60]), verbose=0)
    return scaler.inverse_transform(pred)[0][0]
