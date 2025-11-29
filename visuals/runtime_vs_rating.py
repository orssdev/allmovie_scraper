import os
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('dark_background')
df = pd.read_csv(os.path.join('..', 'data', 'data.csv'))
plt.hexbin(df['runtime'], df['user_rating'], gridsize=30, cmap='Reds')
plt.xlabel("Runtime (minutes)")
plt.ylabel("User Rating")
plt.title("Duration vs. Rating (Hexbin)")
plt.colorbar(label='Count')
plt.show()