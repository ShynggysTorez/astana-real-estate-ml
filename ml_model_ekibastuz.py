import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor
import joblib

# 📥 Загружаем очищенные данные
df = pd.read_csv("ekibastuz_cleaned.csv")

# 🎯 Целевая переменная
y = df['price']

# 🧠 Признаки
X = df.drop(columns=['price', 'price_per_m2', 'title', 'location', 'link',
                     'district', 'region_clean', 'region_name', 'street', 'description'], errors='ignore')

# 📌 Категориальные и числовые признаки
numeric_features = ['total_area', 'room_count', 'floor_num', 'floor_total', 'year_built', 'ceiling_height']
categorical_features = ['house_type', 'condition', 'complex']

# ⚙️ Предобработка
preprocessor = ColumnTransformer(transformers=[
    ('num', StandardScaler(), numeric_features),
    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
])

# 🚀 Модель
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', XGBRegressor(n_estimators=200, learning_rate=0.1, max_depth=6, random_state=42))
])

# ✂️ Разделим на обучающую и тестовую выборку
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 🧠 Обучение
model.fit(X_train, y_train)

# 🔍 Предсказание
y_pred = model.predict(X_test)

# 📊 Метрики
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"📊 MAE: {mae:,.0f} ₸")
print(f"📉 RMSE: {rmse:,.0f} ₸")
print(f"🎯 R² Score: {r2:.2f}")

# 💾 Сохраняем модель
joblib.dump(model, "model_ekibastuz_xgboost.pkl")
print("✅ Модель Ekibastuz сохранена как model_ekibastuz_xgboost.pkl")
