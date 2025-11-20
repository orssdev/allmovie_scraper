import pandas as pd
import os

data = pd.read_json('data.jsonl', lines=True).sort_values(by='id').reset_index(drop=True)
users = pd.read_json('users.jsonl', lines=True).sort_values(by='id').reset_index(drop=True)

combined = data.join(users.set_index('id'), on='id')
filtered = combined[combined['user_count'].notna()]
result = filtered.drop(columns=['url', 'poster_url', 'country', 'themes', 'subgenres']).reset_index(drop=True)
result['directors'] = result['directors'].apply(lambda x: [d['name'] for d in x] if isinstance(x, list) else [])

print(result)
result.to_csv('data.csv', index=False) 