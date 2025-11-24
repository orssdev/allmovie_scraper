import ast
import os
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(os.path.join('..', 'data', 'data.csv'))

df['genres'] = df['genres'].apply(ast.literal_eval)
df_genre = df.explode('genres')

genres = sorted(df_genre['genres'].unique())
data = [df_genre[df_genre['genres'] == g]['user_rating'].dropna() for g in genres]

plt.figure()
plt.boxplot(data, labels=genres)
plt.xticks(rotation=90)
plt.title("Genre vs. Rating")
plt.xlabel("Genre")
plt.ylabel("User Rating")
plt.show()