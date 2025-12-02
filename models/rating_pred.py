import os
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv(os.path.join('..', 'data', 'data.csv'))

df['genres'] = df['genres'].apply(lambda x: eval(x) if pd.notna(x) else [])
df['release_year'] = pd.to_datetime(df['release'], errors='coerce').dt.year

mlb = MultiLabelBinarizer()
genres_encoded = mlb.fit_transform(df['genres'])
genres_df = pd.DataFrame(genres_encoded, columns=mlb.classes_)
df = pd.concat([df, genres_df], axis=1)

df['director_name'] = df['directors'].apply(lambda x: eval(x)[0] if pd.notna(x) and len(eval(x)) > 0 else 'Unknown')
le = LabelEncoder()
df['director_encoded'] = le.fit_transform(df['director_name'])

df = pd.get_dummies(df, columns=['mpaa_rating'], dummy_na=True)
df['budget'] = df['budget'].fillna(df['budget'].median())
df['box_office'] = df['box_office'].fillna(df['box_office'].median())

df = df[df['user_rating'].notna()]

features = (
    ['runtime', 'director_encoded', 'budget', 'box_office', 'release_year'] +
    list(mlb.classes_) +
    [col for col in df.columns if col.startswith('mpaa_rating_')]
)

X = df[features]
y = df['user_rating']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print("RMSE:", rmse)
print("R2:", r2_score(y_test, y_pred))

importances = model.feature_importances_
feat_names = X.columns
plt.figure(figsize=(12, 8))
plt.barh(feat_names, importances)
plt.xlabel("Feature Importance")
plt.ylabel("Features")
plt.title("Feature Importance for Movie Rating Prediction")
plt.show()