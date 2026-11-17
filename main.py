import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom
import seaborn as sns



dfc = pd.read_csv("clients.csv")
dfp = pd.read_csv("products.csv")
dfo = pd.read_csv("orders.csv")
dfco = pd.read_csv("client_opinion.csv")
dfod = pd.read_csv("order_details.csv")

print("Клиенти")
print("Размер", dfc.shape)
print("\n Типове")
print(dfc.dtypes)
print("\n Липсващи стойности")
print(dfc.isna().sum())
print("\n Процент")
print(dfc.isna().mean()*100)
print("\n Дубликати")
print(dfc.duplicated().sum())
print("\n Градове")
print(dfc["City"].unique())
print("\n")
print(dfc["City"].value_counts())
print("\n")

print("Продукти")
print("Размер", dfp.shape)
print("\n Типове")
print(dfp.dtypes)
print("\n Липсващи стойности")
print(dfp.isna().sum())
print("\n Процент")
print(dfp.isna().mean()*100)
print("\n Дубликати")
print(dfp.duplicated().sum())
print("\n")

print("Поръчки")
print("Размер", dfo.shape)
print("\n Типове")
print(dfo.dtypes)
print("\n Липсващи стойности")
print(dfo.isna().sum())
print("\n Процент")
print(dfo.isna().mean()*100)
print("\n Дубликати")
print(dfo.duplicated().sum())
print("\n")

print("Мнения на клиенти")
print("Размер", dfco.shape)
print("\n Типове")
print(dfco.dtypes)
print("\n Липсващи стойности")
print(dfco.isna().sum())
print("\n Процент")
print(dfco.isna().mean()*100)
print("\n Дубликати")
print(dfco.duplicated().sum())
print("\n")

print("Детайли за поръчка")
print("Размер", dfod.shape)
print("\n Типове")
print(dfod.dtypes)
print("\n Липсващи стойности")
print(dfod.isna().sum())
print("\n Процент")
print(dfod.isna().mean()*100)
print("\n Дубликати")
print(dfod.duplicated().sum())
print("\n")




dfc["City"]= dfc["City"].str.strip().str.lower()
dfc["Registration_date"] = pd.to_datetime(dfc["Registration_date"])
dfc["City"] = dfc["City"].fillna(dfc["City"].mode()[0])
dfc = dfc.drop_duplicates()

dfp["Category"] = dfp["Category"].fillna(dfp["Category"].mode()[0])
dfp = dfp.drop_duplicates()


dfo["Date"] = pd.to_datetime(dfo["Date"])
dfo["Status"] = dfo["Status"].fillna(dfo["Status"].mode()[0])
dfo["Payment_method"] = dfo["Payment_method"].fillna(dfo["Payment_method"].mode()[0])

dfo = dfo.drop_duplicates()



dfco["Date"] = pd.to_datetime(dfco["Date"])

dfco["Description"] = dfco["Description"].fillna(dfco["Description"].mode()[0])



dfod["Product"] = dfod["Product"].fillna(dfod["Product"].mode()[0])
dfod["Date"] = pd.to_datetime(dfod["Date"])
dfod = dfod.drop_duplicates()



print("/////////////") 
print("/////////////")
print("/////////////")
print("/////////////")


print("Клиенти")
print("Размер", dfc.shape)
print("\n Типове")
print(dfc.dtypes)
print("\n Липсващи стойности")
print(dfc.isna().sum())
print("\n Процент")
print(dfc.isna().mean()*100)
print("\n Дубликати")
print(dfc.duplicated().sum())
print("\n Градове")
print(dfc["City"].unique())
print("\n")
print(dfc["City"].value_counts())
print("\n")

print("Продукти")
print("Размер", dfp.shape)
print("\n Типове")
print(dfp.dtypes)
print("\n Липсващи стойности")
print(dfp.isna().sum())
print("\n Процент")
print(dfp.isna().mean()*100)
print("\n Дубликати")
print(dfp.duplicated().sum())
print("\n")

print("Поръчки")
print("Размер", dfo.shape)
print("\n Типове")
print(dfo.dtypes)
print("\n Липсващи стойности")
print(dfo.isna().sum())
print("\n Процент")
print(dfo.isna().mean()*100)
print("\n Дубликати")
print(dfo.duplicated().sum())
print("\n")

print("Мнения на клиенти")
print("Размер", dfco.shape)
print("\n Типове")
print(dfco.dtypes)
print("\n Липсващи стойности")
print(dfco.isna().sum())
print("\n Процент")
print(dfco.isna().mean()*100)
print("\n Дубликати")
print(dfco.duplicated().sum())
print("\n")

print("Детайли за поръчка")
print("Размер", dfod.shape)
print("\n Типове")
print(dfod.dtypes)
print("\n Липсващи стойности")
print(dfod.isna().sum())
print("\n Процент")
print(dfod.isna().mean()*100)
print("\n Дубликати")
print(dfod.duplicated().sum())
print("\n")


#Първоначална обработка

#outliners

print("/////////////") 
print("/////////////")
print("/////////////")
print("/////////////")
print("/////////////") 



print(dfc["Age"].describe())
print(dfp["Selling_price"].describe())
print(dfp["Actual_price"].describe())


plt.boxplot(dfc["Age"])
plt.title("Възраст")
plt.ylabel("години")
plt.show()



plt.boxplot(dfp["Selling_price"])
plt.title("Продажна цена")
plt.ylabel("евро")
plt.show()


plt.boxplot(dfp["Actual_price"])
plt.title("Цена")
plt.ylabel("евро")
plt.show()


plt.boxplot(dfod["Profit"])
plt.title("Печалба")
plt.ylabel("евро")
plt.show()




#///// poneje razpredelenieto e daleche ot normalno,
#shte polzvam iqr vmesto z-score

Q1 = dfc["Age"].quantile(0.25)
Q3 = dfc["Age"].quantile(0.75)
IQR = Q3-Q1

lower = Q1-1.5*IQR
upper = Q3+1.5*IQR

dfc = dfc[
      (dfc["Age"] >= lower) &
      (dfc["Age"] <= upper)
        ]




Q1 = dfp["Selling_price"].quantile(0.25)
Q3 = dfp["Selling_price"].quantile(0.75)
IQR = Q3-Q1

lower = Q1-1.5*IQR
upper = Q3+1.5*IQR

dfp = dfp[
      (dfp["Selling_price"] >= lower) &
      (dfp["Selling_price"] <= upper)
        ]






Q1 = dfp["Actual_price"].quantile(0.25)
Q3 = dfp["Actual_price"].quantile(0.75)
IQR = Q3-Q1

lower = Q1-1.5*IQR
upper = Q3+1.5*IQR

dfp = dfp[
      (dfp["Actual_price"] >= lower) &
      (dfp["Actual_price"] <= upper)
        ]
      




Q1 = dfod["Profit"].quantile(0.25)
Q3 = dfod["Profit"].quantile(0.75)
IQR = Q3-Q1

lower = Q1-1.5*IQR
upper = Q3+1.5*IQR

dfod = dfod[
      (dfod["Profit"] >= lower) &
      (dfod["Profit"] <= upper)
        ]






print(dfc["Age"].describe())
print(dfp["Selling_price"].describe())
print(dfp["Actual_price"].describe())


plt.boxplot(dfc["Age"])
plt.title("Възраст")
plt.ylabel("години")
plt.show()



plt.boxplot(dfp["Selling_price"])
plt.title("Продажна цена")
plt.ylabel("евро")
plt.show()


plt.boxplot(dfp["Actual_price"])
plt.title("Цена")
plt.ylabel("евро")
plt.show()

plt.boxplot(dfod["Profit"])
plt.title("Печалба")
plt.ylabel("евро")
plt.show()


#no purvo drugoto



print("\n")
print("\n")
print("\n")


print("Средна стойност")
print("Години ", dfc["Age"].mean())
print("Продажна цена ", dfp["Selling_price"].mean())
print("Цена ", dfp["Actual_price"].mean())
print("Оценка ", dfco["Grade"].mean())
print("Количество ", dfod["Quantity"].mean())
print("Обща стойност ", dfod["Amount"].mean())


print("\n")


print("Медиана")
print("Години ", dfc["Age"].median())
print("Продажна цена ", dfp["Selling_price"].median())
print("Цена ", dfp["Actual_price"].median())
print("Оценка ", dfco["Grade"].median())
print("Количество ", dfod["Quantity"].median())
print("Обща стойност ", dfod["Amount"].median())



print("\n")


print("Минимум")
print("Години ", dfc["Age"].min())
print("Продажна цена ", dfp["Selling_price"].min())
print("Цена ", dfp["Actual_price"].min())
print("Оценка ", dfco["Grade"].min())
print("Количество ", dfod["Quantity"].min())
print("Обща стойност ", dfod["Amount"].min())



print("\n")


print("Максимум")
print("Години ", dfc["Age"].max())
print("Продажна цена ", dfp["Selling_price"].max())
print("Цена ", dfp["Actual_price"].max())
print("Оценка ", dfco["Grade"].max())
print("Количество ", dfod["Quantity"].max())
print("Обща стойност ", dfod["Amount"].max())


print("\n")


print("Мода")
print("Град ", dfc["City"].mode())
print("Категория ", dfp["Category"].mode())
print("Метод на плащане ", dfo["Payment_method"].mode())
print("Статус ", dfo["Status"].mode())



print("\n")


print("Дисперсия")
print("Години ", dfc["Age"].var())
print("Продажна цена ", dfp["Selling_price"].var())
print("Цена ", dfp["Actual_price"].var())
print("Оценка ", dfco["Grade"].var())
print("Количество ", dfod["Quantity"].var())
print("Обща стойност ", dfod["Amount"].var())



print("\n")


print("Стандартно отклонение")
print("Години ", dfc["Age"].std())
print("Продажна цена ", dfp["Selling_price"].std())
print("Цена ", dfp["Actual_price"].std())
print("Оценка ", dfco["Grade"].std())
print("Количество ", dfod["Quantity"].std())
print("Обща стойност ", dfod["Amount"].std())





print("\n")


print("Обобщено")
print("Години ", dfc["Age"].describe())
print("Продажна цена ", dfp["Selling_price"].describe())
print("Цена ", dfp["Actual_price"].describe())
print("Оценка ", dfco["Grade"].describe())
print("Количество ", dfod["Quantity"].describe())



#диаграми











plt.hist(dfod["Quantity"], bins=4)
plt.title("Разделение на количествата")
plt.xlabel("Количество")
plt.ylabel("Честота")
plt.show()


plt.hist(dfp["Actual_price"], bins=8)
plt.title("Разделение на цените")
plt.xlabel("Цена")
plt.ylabel("Честота")
plt.show()


plt.hist(dfod["Amount"], bins=6)
plt.title("Разделение на общи цени")
plt.xlabel("цена")
plt.ylabel("Честота")
plt.show()



##Разпределения

data = np.random.normal(170,10,1000)
plt.hist(data, bins=30)
plt.title("Нормално разпределение")
plt.xlabel("стойност")
plt.ylabel("честота")
plt.show()



data = np.random.uniform(low=0,high=10,size=1000)
plt.hist(data, bins=20)
plt.title("Равномерно разпределение")
plt.xlabel("стойност")
plt.ylabel("честота")
plt.show()

n = 10
p = 0.4

x = np.arange(0,n+1)
prb = binom.pmf(x, n, p)

plt.bar(x, prb)
plt.title("Биномно")
plt.xlabel("Брой успехи")
plt.ylabel("Вероятност")
plt.show()

#зависимост



plt.hist(dfod["Quantity"], bins=4)
plt.title("Разделение на количествата")
plt.xlabel("Количество")
plt.ylabel("Честота")
plt.show()


plt.hist(dfod["Amount"], bins=6)
plt.title("Разделение на общи цени")
plt.xlabel("цена")
plt.ylabel("Честота")
plt.show()

dfod["Quantity"]
dfod["Amount"]

plt.scatter(dfod["Quantity"], dfod["Amount"])
plt.xlabel("Количество")
plt.ylabel("Продажби")
plt.title("Количество и сума продажби")
plt.show()



spearman_matrix = dfod[["Quantity","Amount","Price"]].corr(method="spearman")
pearson_metrix = dfod[["Quantity","Amount","Price"]].corr(method="pearson")




sns.heatmap(spearman_matrix, annot = True, fmt =".2f")
plt.title("Spearman heat map amount")
plt.show()



sns.heatmap(pearson_metrix, annot = True, fmt =".2f")
plt.title("Pearson heat map amount")
plt.show()





spearman_matrix = dfod[["Quantity","Profit","Price"]].corr(method="spearman")
pearson_metrix = dfod[["Quantity","Profit","Price"]].corr(method="pearson")




sns.heatmap(spearman_matrix, annot = True, fmt =".2f")
plt.title("Spearman heat map profit")
plt.show()



sns.heatmap(pearson_metrix, annot = True, fmt =".2f")
plt.title("Pearson heat map profit")
plt.show()






#onehot

#orders and od


#export

dfc.to_csv("clients.csv", encoding='utf-8', index=False)
dfp.to_csv("products.csv", encoding='utf-8', index=False)
dfo.to_csv("orders.csv", encoding='utf-8', index=False)
dfco.to_csv("client_opinion.csv", encoding='utf-8', index=False)
dfod.to_csv("order_details.csv", encoding='utf-8', index=False)



