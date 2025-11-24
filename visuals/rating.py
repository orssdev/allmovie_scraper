import os
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(os.path.join('..', 'data', 'data.csv'))

plt.figure()
plt.hist(df['user_rating'].dropna(), bins=20)
plt.xlabel("User Rating")
plt.ylabel("Number of Movies")
plt.title("Rating Distribution")
plt.show()