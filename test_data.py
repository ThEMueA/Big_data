
from faker import Faker
import pandas as pd
import random
import numpy as np

#100 klienta

Faker.seed(42)
fake = Faker()

data = []
for x in range(100):
    if(x==2): age =222222

    else: age =  fake.random_int(min=18,max=80)

    data.append({
        "Id": "u" + str( fake.unique.random_int(min=1, max=111)),
        "Name": fake.unique.name(),
        "Age":  age,
        "City":fake.random_element(elements=("Sofia","Plovdiv","Varna","Burgas","Cherganovo","Veliko Turnovo","","Trqvna","Bqla","Petrich","Tulbuhin","Kazanluk","Qmbol","plovdiv","bqla","varna")),
        "Registration_date":fake.date_between(start_date="-1y", end_date="today"),
        "Category":fake.random_element(elements=("End-users","Distributors","Retailers","Dropshippers","Tradespeople"))
        })

    #Клиенти: уникален идентификатор, име, възраст, населено място, дата на регистрация и клиентска категория.


dfc = pd.DataFrame(data)

print(dfc.head)
print(dfc["Age"])
print(dfc["City"])
data.clear()

pnames=("boom box",
"thermostat",
"paper",
"stockings",
"glow stick",
"buckle",
"outlet",
"lip gloss",
"canvas",
"couch",
"bookmark",
"mirror",
"purse",
"candy wrapper",
"cell phone",
"chocolate",
"bed",
"knife",
"wagon",
"cat","dog","","dog","dog", "dog")

pcat=("Automotive",
"Baby",
"Beauty",
"Books",
"",
"Clothing",
"Computers",
"Electronics",
"Games",
"Garden",
"Grocery")



for x in range(40):
    
    if(x==12): act_price = 222222

    else: act_price = round( random.uniform(8,122), 4)

    sel_price_ps = fake.random_int(min=114,max=133)
    data.append({
        "Id":"p" + str( fake.unique.random_int(min=101, max=141)),
        "Name": fake.random_element(pnames),
        "Selling_price":round( act_price*sel_price_ps/100,4),
        "Actual_price": act_price,
        "Category":fake.random_element(pcat)
        })


dfp = pd.DataFrame(data)

print(dfp.head)

data.clear()


cnames = tuple(dfc["Name"])


for x in range(1000):
    
    sel_price_ps = fake.random_int(min=114,max=133)
    data.append({
        "Id":"o"+str(fake.unique.random_int(min=301, max=1500)),
        "Client": fake.random_element(cnames),
        "Date": fake.date_between(start_date="-1y", end_date="today"),
        "Status": fake.random_element(elements= ("Pending", "Processing"," Shipped", "Delivered", "Completed", "Canceled", "Refunded","On hold",""  )),
        "Payment_method": fake.random_element(elements=("Credit card","Debit card","Bank transfer","On delivery",""))
        })


    


dfo = pd.DataFrame(data)


print(dfo.head)

data.clear()



ids = tuple(dfc["Id"])


product_comments = (
    "Great quality",
    "Fast shipping",
    "Works as expected",
    "Highly recommend",
    "Very durable",
    "Worth the price",
    "Not bad",
    "Poor build quality",
    "Stopped working quickly",
    "Love this product",
    "Exceeded my expectations",
    "Decent for price",
    "Arrived damaged",
    "Easy to use",
    "Terrible customer service",
    "Exactly as described",
    "Very disappointed",
    "Super fast delivery",
    "Great value",
    "Would buy again",
    ""
)




for x in range(300):
    sel_price_ps = fake.random_int(min=114,max=133)
    data.append({
        "Id": fake.random_element(ids),  
        "Date": fake.date_between(start_date="-1y", end_date="today"),
        "Description": fake.random_element(product_comments),
        "Grade": fake.random_int(min=1,max=10)
        })


dfcp = pd.DataFrame(data)

print(dfcp.head)

data.clear()




print(dfp.head)

pnames = tuple(dfp['Name'])

dfp = dfp.set_index('Name')

dates = tuple(dfo["Date"])

for x in range(992):
    
    quantity = fake.random_int(min=1,max=3)
    name = fake.random_element(pnames)
    date = fake.random_element(dates)
    print(name)
    price, aprice = dfp.loc[[name], ['Selling_price', 'Actual_price']].iloc[0].astype(float)
    
    data.append({
        "Product": name,
        "Quantity": quantity,
        "Price": price,
        "Date": date,
        "Amount": quantity*price,
        "Profit" :quantity*price - quantity*aprice 
        })


dfpd = pd.DataFrame(data)

print(dfpd.head)

data.clear()

print(dfp)



ndfc = pd.DataFrame(np.repeat(dfc.values, 6, axis=0), columns=dfc.columns)
ndfp = pd.DataFrame(np.repeat(dfp.values, 9, axis=0), columns=dfp.columns)
ndfo = pd.DataFrame(np.repeat(dfo.values, 22, axis=0), columns=dfo.columns)


ndfc.to_csv("clients.csv", encoding='utf-8', index=False)
ndfp.to_csv("products.csv", encoding='utf-8', index=False)
ndfo.to_csv("orders.csv", encoding='utf-8', index=False)
dfcp.to_csv("client_opinion.csv", encoding='utf-8', index=False)
dfpd.to_csv("order_details.csv", encoding='utf-8', index=False)
