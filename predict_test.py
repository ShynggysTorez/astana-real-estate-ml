import pandas as pd
import joblib

# Загружаем модель
model = joblib.load("model_xgboost.pkl")

# Пример новых данных (в формате pandas DataFrame)
new_data = pd.DataFrame([{
    "total_area": 75,
    "room_count": 2,
    "floor_num": 5,
    "floor_total": 9,
    "year_built": 2021,
    "ceiling_height": 2.7,
    "region_clean": "Есильский р-н",
    "house_type": "монолитный",
    "condition": "свежий ремонт",
    "complex": "Arena Unity"
}])

# ⚙️ Убедись, что все препроцессоры совпадают с обучением
prediction = model.predict(new_data)
print(f"💰 Прогнозируемая цена: {prediction[0]:,.0f} ₸")
