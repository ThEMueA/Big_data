import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.metrics import mean_absolute_error, mean_squared_error


dfc = pd.read_csv("clients.csv")
dfp = pd.read_csv("products.csv")

dfco = pd.read_csv("client_opinion.csv")
dfod = pd.read_csv("order_details.csv")
dfo = pd.read_csv("orders.csv")

print(dfc.columns)
print(dfp.columns)
print(dfo.columns)
print(dfco.columns)
print(dfod.columns)





#dfod["Date"] = dfod.to_datetime(df["Date"])
dfod = dfod.set_index("Date")
dfod = dfod.sort_index()

dfod["Profit"] = dfod["Profit"].interpolate()

split_date = "2026-09-01"

train = dfod.loc[dfod.index < split_date]
test = dfod.loc[dfod.index >= split_date]


last_value = train["Profit"].iloc[-1]
nativef = np.repeat(last_value,len(test))
print(nativef)




train_values = train[["Profit"]].values
test_values = test[["Profit"]].values

scaler = MinMaxScaler()
train_scaled = scaler.fit_transform(train_values)
test_scaled = scaler.transform(test_values)


def create_sq(data, window_size):
    X=[]
    Y=[]
    for i in range(len(data) - window_size):
        X.append(data[i:i + window_size])
        Y.append(data[i + window_size])
    return np.array(X), np.array(Y)

wind = 14
x_train, y_train = create_sq(train_scaled, wind)
print("форма на X train", x_train.shape)



comb = np.concatenate([
    train_scaled[-wind:],
    test_scaled
    ])
x_test,y_test = create_sq(comb, wind)


model = Sequential([
    LSTM(51, input_shape=(wind, 1)),
    Dense(1)
    ])

model.compile(optimizer="adam", loss="mse")

history = model.fit(
        x_train, y_train,
        epochs=32,
        batch_size=16,
        validation_split=0.1,
        verbose=1)


plt.plot(history.history["loss"], label="Train")
plt.plot(history.history["val_loss"], label="Validation")
plt.title("ltsm обучение")
plt.xlabel("epoch")
plt.ylabel("loss")
plt.legend()
plt.show()


pred_scaled = model.predict(x_test)

predictions = scaler.inverse_transform(pred_scaled)
actual = scaler.inverse_transform(y_test)


mae = mean_absolute_error(actual, predictions)
mse = mean_squared_error(actual, predictions)
rmse = np.sqrt(mse)

print( f"   MAE = {mae}  MSE = {mse}   RMSE = {rmse}")

plt.figure(figsize=(12,5))
plt.plot(test.index[:len(actual)], actual,
         label="Actual", linewidth=2)
plt.plot(test.index[:len(predictions)], 
         predictions, label="LTSM", linestyle="--")
plt.title("LTSM")
plt.xlabel("Date")
plt.ylabel("Profit")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


plt.figure(figsize=(12,5))
plt.plot(test.index[:len(actual)], actual,label="Actual", linewidth=2)
plt.plot(test.index[:len(predictions)],predictions, label="LTSM", linestyle="--")
plt.plot(test.index, nativef, label="native")
plt.title("LTSM")
plt.xlabel("Date")
plt.ylabel("Profit")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()






