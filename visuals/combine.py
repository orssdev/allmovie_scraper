import pandas as pd
import os

data = pd.read_json(os.path.join('..', 'data.jsonl'), lines=True)
users = pd.read_json(os.path.join('..', 'users.jsonl'), lines=True)

print(data)
print(users)