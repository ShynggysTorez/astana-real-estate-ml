import streamlit as st
import pandas as pd
import joblib
import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# === ЗАГРУЗКА МОДЕЛИ ===
model = joblib.load("model_xgboost.pkl")

st.set_page_config(page_title="🧠 Прогноз цен на квартиры в Астане", layout="centered")

st.title("🏙️ Прогноз стоимости квартиры (Астана)")
st.markdown("Введите параметры квартиры, чтобы получить прогнозируемую стоимость.")

# === Ввод параметров пользователем ===
region = st.selectbox("Район", ['Есильский р-н', 'Алматы р-н', 'Нура р-н', 'Сарыарка р-н', 'р-н Байконур', 'Сарайшык р-н'])
house_type = st.selectbox("Тип дома", ['монолитный', 'кирпичный', 'панельный', 'иной'])
condition = st.selectbox("Состояние", ['свежий ремонт', 'не новый, но аккуратный ремонт', 'черновая отделка', 'требует ремонта', 'свободная планировка'])
complex_name = st.text_input("Название ЖК (если нет — оставьте пустым)", value="")

total_area = st.slider("Общая площадь (м²)", 20, 300, 70)
room_count = st.slider("Количество комнат", 1, 6, 2)
floor_num = st.slider("Этаж", 1, 30, 3)
floor_total = st.slider("Этажей в доме", floor_num, 40, 9)
year_built = st.slider("Год постройки", 1960, 2026, 2021)
ceiling_height = st.slider("Высота потолков (м)", 2.2, 4.0, 2.8, step=0.05)

# === Подготовка входа ===
input_dict = {
    'region_clean': [region],
    'house_type': [house_type],
    'condition': [condition],
    'complex': [complex_name],
    'total_area': [total_area],
    'room_count': [room_count],
    'floor_num': [floor_num],
    'floor_total': [floor_total],
    'year_built': [year_built],
    'ceiling_height': [ceiling_height]
}
input_df = pd.DataFrame(input_dict)

# === Предсказание ===
if st.button("🔮 Прогнозировать цену"):
    prediction = model.predict(input_df)[0]
    prediction_rounded = round(prediction, -4)

    st.success(f"💰 Прогнозируемая стоимость: **{prediction_rounded:,.0f} ₸**")
    st.caption("Это предварительная оценка на основе данных, обученных на квартирах в Астане.")
