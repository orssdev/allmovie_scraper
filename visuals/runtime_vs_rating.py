import os
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(os.path.join('..', 'data', 'data.csv'))

plt.figure()
plt.scatter(df['runtime'], df['user_rating'])
plt.xlabel("Runtime (minutes)")
plt.ylabel("User Rating")
plt.title("Duration vs. Rating")
plt.show()