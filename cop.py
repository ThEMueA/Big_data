import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import nltk
nltk.download("vader_lexicon")
from nltk.sentiment import SentimentIntensityAnalyzer



df = pd.read_csv("client_opinion.csv")



df["Clean"] = df["Description"].copy()

print(df["Clean"].head())
 
df["Date"] = pd.to_datetime(df["Date"], format="mixed", errors="coerce")

df["Day"] = df["Date"].dt.day_name()
df["Week"] = df["Date"].dt.to_period("W")
df["Month"] = df["Date"].dt.month


def clean_text(text):
  text = text.lower()
  text = re.sub(r"http\S+|www\.\S+", "", text)  
  text = re.sub( r"@\w+", "", text )
  text = re.sub( r"#", "" , text )
  text = re.sub( r" [a^-zA-Z0-9\s]" , " ", text)
  text = re.sub(r"\s+" ,"" ,text).strip()
  return text



df["Clean"] = df["Clean"].apply(clean_text)


print(df["Clean"].head())

print("here")



stop_words = set(ENGLISH_STOP_WORDS)
print(list(stop_words)[:20])


for text in df["Clean"].head(10):
    tokens = text.split()
    filtered = [w for w in tokens if w not in stop_words]
    print("Org ", tokens)
    print("No stop ", filtered)
    print()






vectorizer = CountVectorizer()

x = vectorizer.fit_transform(df["Clean"])

print(vectorizer.get_feature_names_out())

print(x)

x_dense = x.toarray()
print(x_dense)



word_counts = x.sum(axis=0).A1

word_freq = pd.DataFrame({
    "word":  vectorizer.get_feature_names_out(),

   "frequency": word_counts
    })


word_freq = word_freq.sort_values("frequency", ascending = False)

print(word_freq.head(n=20).to_string(index = False))




top_words=word_freq.head(15)



plt.figure(figsize=(10,6))
plt.barh(top_words["word"], top_words["frequency"])
plt.xlabel("Freq")
plt.ylabel("Word")
plt.gca().invert_yaxis()
plt.show()






vectorizer = CountVectorizer(ngram_range =(1, 2))

x_rams = vectorizer.fit_transform(df["Clean"])

counts = x_rams.sum(axis=0).A1

ngrams =  pd.DataFrame({
    "word": vectorizer.get_feature_names_out()
   ,

   "frequency": counts
    })


ngrams = ngrams.sort_values("frequency", ascending = False)
print(ngrams)



plt.figure(figsize=(10,6))
plt.barh(ngrams["word"], ngrams["frequency"])
plt.xlabel("Frequency")
plt.ylabel("Word")
plt.gca().invert_yaxis()
plt.show()





tfidf = TfidfVectorizer(stop_words="english")

X_tfidr = tfidf.fit_transform(df["Clean"])

feturenames = tfidf.get_feature_names_out()

scores = X_tfidr.sum(axis=0).A1

tfidf_word = pd.DataFrame({
    "word": feturenames
    ,
   "frequency": scores
    })



tfidf_word = tfidf_word.sort_values("frequency", ascending = False)

print(tfidf_word.head(20))


plt.figure(figsize=(10,6))
plt.barh(tfidf_word["word"], tfidf_word["frequency"])
plt.xlabel("Score")
plt.ylabel("Word")
plt.gca().invert_yaxis()
plt.show()








sia = SentimentIntensityAnalyzer()

def get_sent(text):
    score = sia.polarity_scores(text)
    compound = score["compound"]
    if compound >= 0.05:
        return "Positive"
    elif compound <= -0.5:
        return "Negative"
    else:
        return "Netrual"



df["Sentiment"] = df["Clean"].apply(get_sent)

print(df[["Description", "Sentiment"]].head(10))



sentiment_counts = df["Sentiment"].value_counts()
print(sentiment_counts)



plt.bar(sentiment_counts.index, sentiment_counts.values)
plt.title("Sentiment for describtion")
plt.xlabel("Sentiment")
plt.ylabel("Count of comments")
plt.show()

 

sentiment_share = (
        df["Sentiment"].value_counts(normalize=True)*100
        )

print(sentiment_share)


daily_sentiment = pd.crosstab(df["Week"], df["Sentiment"])
print(daily_sentiment)



daily_sentiment.plot(figsize=(12,5))
plt.title("Sentiment по дни")
plt.xlabel("Дата")
plt.ylabel("Брой пъбликации")
plt.show()








