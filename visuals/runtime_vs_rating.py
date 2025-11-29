import os
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('dark_background')
df = pd.read_csv(os.path.join('..', 'data', 'data.csv'))
min_runtime = 60
max_runtime = 150
filtered_df = df[(df['runtime'] <= max_runtime) & (df['runtime'] >= min_runtime)]
plt.hexbin(filtered_df['runtime'], filtered_df['user_rating'], gridsize=30, cmap='Reds')
plt.xlabel("Runtime (minutes)")
plt.ylabel("User Rating")
plt.title("Duration vs. Rating (Hexbin, Outliers Removed)")
plt.colorbar(label='Count')
plt.show()