import ast
import os
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(os.path.join('..', 'data', 'data.csv'))

df['genres'] = df['genres'].apply(ast.literal_eval)
df_genre = df.explode('genres')

genres = sorted(df_genre['genres'].unique())
data = [df_genre[df_genre['genres'] == g]['user_rating'].dropna() for g in genres]

plt.style.use('dark_background')
plt.figure()

plt.violinplot(data, showmeans=True, widths=0.9)
plt.xticks(ticks=range(1, len(genres)+1), labels=genres, rotation=90, fontsize=5)
plt.title("Genre vs. Rating (Violin Plot)")
plt.xlabel("Genre")
plt.ylabel("User Rating")
plt.show()