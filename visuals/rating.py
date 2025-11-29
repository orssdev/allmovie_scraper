import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(os.path.join('..', 'data', 'data.csv'))
plt.style.use('dark_background')
plt.figure()
plt.hist(df['user_rating'].dropna(), bins=np.arange(0.5, 11.5, 1), color='red', edgecolor='darkred', linewidth=1.2 )
plt.xlabel("User Rating")
plt.ylabel("Number of Movies")
plt.title("Rating Distribution")
plt.show()