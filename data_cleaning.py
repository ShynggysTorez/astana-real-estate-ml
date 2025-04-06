import pandas as pd
import re

# Загрузка исходного файла
df = pd.read_csv("krisha_astana_detailed.csv")

# Очистка цены
df['price'] = df['price'].astype(str).str.replace(r'[^\d]', '', regex=True).astype(float)

# Очистка этажности
df['floor'] = df['floor'].astype(str)
df[['floor_num', 'floor_total']] = df['floor'].str.extract(r'(\d+)\s*из\s*(\d+)')
df['floor_num'] = pd.to_numeric(df['floor_num'], errors='coerce')
df['floor_total'] = pd.to_numeric(df['floor_total'], errors='coerce')

# Год постройки
df['year_built'] = pd.to_numeric(df['year_built'], errors='coerce')

# Высота потолков
df['ceiling_height'] = df['ceiling_height'].astype(str)
df['ceiling_height'] = df['ceiling_height'].str.replace(',', '.').str.extract(r'([\d.]+)').astype(float)

# Площадь
df['area'] = df['area'].astype(str)
df['total_area'] = df['area'].str.extract(r'(\d+[.,]?\d*)')[0].str.replace(',', '.').astype(float)

# Количество комнат
df['room_count'] = df['title'].str.extract(r'(\d+)-комнат').astype(float)

# Цена за м²
df['price_per_m2'] = df['price'] / df['total_area']

# Разделение района и улицы
split_location = df['location'].astype(str).str.split(',', n=1, expand=True)
df['region_name'] = split_location[0].str.strip()
df['street'] = split_location[1].str.strip() if split_location.shape[1] > 1 else None

# Стандартизация районов
known_regions = ['Есильский р-н', 'Алматы р-н', 'Нура р-н', 'Сарыарка р-н', 'р-н Байконур', 'Сарайшык р-н']
df['region_clean'] = df['region_name'].where(df['region_name'].isin(known_regions), None)

# Обработка нестандартных улиц (как делали в Colab)
df.loc[df['street'].str.contains('Мангилик Ел 61', na=False), 'region_clean'] = 'Есильский р-н'
df.loc[df['street'].str.contains('Тураг 7|Туран 57г|Кайым Мухамедханова|Айтматова 40|Сыганак 52|Е 18 1', na=False), 'region_clean'] = 'Нура р-н'
df.loc[df['street'].str.contains('Бектурова 17|Нажмеденова 29/2|Ракымжан Кошкарбаев 36|Байтурсынова 47/1', na=False), 'region_clean'] = 'Сарайшык р-н'
df.loc[df['street'].str.contains('Ташенова 4', na=False), 'region_clean'] = 'р-н Байконур'
df.loc[df['street'].str.contains('Кажымукан 6/1|Тауелсиздик 25', na=False), 'region_clean'] = 'Алматы р-н'

# Сохраняем очищенный файл
df.to_csv("krisha_cleaned.csv", index=False, encoding='utf-8-sig')
print("✅ Чистка завершена. Файл сохранён как krisha_cleaned.csv")
