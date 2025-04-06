import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Загрузка модели
model = joblib.load("model_ekibastuz_xgboost.pkl")

st.title("🏠 Ekibastuz Apartment Price Predictor")

st.markdown("Enter the details of an apartment in Ekibastuz to get a predicted price.")

# Ввод параметров
total_area = st.slider("Total area (m²)", 20, 200, 60)
room_count = st.slider("Number of rooms", 1, 6, 2)
floor_num = st.slider("Floor number", 1, 20, 5)
floor_total = st.slider("Total number of floors", 1, 30, 9)
year_built = st.slider("Year built", 1960, 2025, 2015)
ceiling_height = st.slider("Ceiling height (m)", 2.0, 4.0, 2.7)

# Категориальные параметры
house_type = st.selectbox("Building type", ["кирпичный", "панельный", "монолитный", "иной"])
condition = st.selectbox("Condition", ["свежий ремонт", "не новый, но аккуратный ремонт", "черновая отделка", "требует ремонта", "свободная планировка", "NaN"])
complex_name = st.text_input("Residential complex name (optional)", "")

# Подготовка данных
input_data = pd.DataFrame([{
    "total_area": total_area,
    "room_count": room_count,
    "floor_num": floor_num,
    "floor_total": floor_total,
    "year_built": year_built,
    "ceiling_height": ceiling_height,
    "house_type": house_type,
    "condition": condition,
    "complex": complex_name if complex_name else "NaN"
}])

# Предсказание
if st.button("Predict"):
    prediction = model.predict(input_data)[0]
    st.subheader(f"💰 Predicted Price: {prediction:,.0f} ₸")
