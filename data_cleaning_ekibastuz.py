import pandas as pd
import numpy as np

# 📥 Загрузка данных
df = pd.read_csv(r"C:\Users\cheen\PycharmProjects\krisha_parser_project\krisha_ekibastuz_detailed.csv")

# 💰 Очистка цены
df['price'] = df['price'].astype(str).str.replace(r'[^\d]', '', regex=True).astype(float)

# ❌ Удаление ценовых выбросов
df = df[(df['price'] >= 5_000_000) & (df['price'] <= 100_000_000)]

# 📐 Площадь (из area)
df['area'] = df['area'].astype(str)
df['total_area'] = df['area'].str.extract(r'(\d+[.,]?\d*)')[0].str.replace(',', '.').astype(float)

# 🛏️ Комнаты (из title)
df['room_count'] = df['title'].str.extract(r'(\d+)-комнат').astype(float)

# 🏢 Этажность (пример "4 из 9")
df['floor'] = df['floor'].astype(str)
df[['floor_num', 'floor_total']] = df['floor'].str.extract(r'(\d+)\s*из\s*(\d+)')
df['floor_num'] = pd.to_numeric(df['floor_num'], errors='coerce')
df['floor_total'] = pd.to_numeric(df['floor_total'], errors='coerce')

# 🏗️ Год постройки
df['year_built'] = pd.to_numeric(df['year_built'], errors='coerce')

# 🧱 Высота потолков (например, "2.7 м")
df['ceiling_height'] = df['ceiling_height'].astype(str)
df['ceiling_height'] = df['ceiling_height'].str.replace(',', '.').str.extract(r'([\d.]+)').astype(float)

# 📊 Цена за квадратный метр
df['price_per_m2'] = df['price'] / df['total_area']

# 🧾 Быстрая сводка по числовым полям
print("\n📈 Статистика по очищенным данным:\n")
print(df[['price', 'total_area', 'room_count', 'floor_num', 'floor_total', 'year_built', 'ceiling_height', 'price_per_m2']].describe())

# 💾 Сохраняем результат
df.to_csv("ekibastuz_cleaned.csv", index=False, encoding='utf-8-sig')
print(f"\n✅ Данные успешно сохранены: ekibastuz_cleaned.csv ({len(df)} строк)")
