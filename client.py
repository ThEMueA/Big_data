import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv("order_details.csv")


print("Общи приходи:", df["Amount"].sum().round(2))
print("Обща себестойност:", df["Price"].sum().round(2))
print("Обща печалба:", df["Profit"].sum().round(2))

stats = df.groupby("Product")[["Amount", "Price", "Profit"]].sum().round(2)
print(stats)


stats.plot(kind="bar", title="Приходи и печалба по продукт")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

