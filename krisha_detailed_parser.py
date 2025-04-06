import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Загружаем существующий CSV с объявлениями
df = pd.read_csv('krisha_astana_full.csv')

# Создадим список для обогащённых данных
detailed_data = []

headers = {"User-Agent": "Mozilla/5.0"}

# 🔧 Вставим новую функцию извлечения данных
def parse_extended(soup):
    characteristics = {}

    # 1. Основной блок offer__info-item
    for item in soup.find_all('div', class_='offer__info-item'):
        key = item.get('data-name')
        val_tag = item.find('div', class_='offer__advert-short-info')
        if key and val_tag:
            characteristics[key] = val_tag.get_text(strip=True)

    # 2. Параметры в dt/dd блоках
    for item in soup.select('.offer__parameters dl'):
        key_tag = item.find('dt')
        val_tag = item.find('dd')
        if key_tag and val_tag:
            key = key_tag.get('data-name')
            val = val_tag.get_text(strip=True)
            if key:
                characteristics[key] = val

    # 3. Описание объявления
    desc_block = soup.find('div', class_='js-description')
    if desc_block:
        characteristics['description'] = desc_block.get_text(strip=True)

    return characteristics

# 🚀 Проходим по каждой ссылке
for i, row in df.iterrows():
    url = row['link']
    print(f'🔎 Обработка {i + 1}/{len(df)}: {url}')

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        characteristics = parse_extended(soup)

        # Добавим нужные параметры
        detailed_data.append({
            'title': row['title'],
            'price': row['price'],
            'district': row['district'],
            'location': row['location'],
            'link': row['link'],
            'region_clean': row.get('region_clean'),
            'house_type': characteristics.get('flat.building'),
            'year_built': characteristics.get('house.year'),
            'floor': characteristics.get('flat.floor'),
            'ceiling_height': characteristics.get('ceiling'),
            'complex': characteristics.get('map.complex'),
            'condition': characteristics.get('flat.renovation'),
            'area': characteristics.get('live.square'),
            'description': characteristics.get('description'),
        })

        time.sleep(1.2)

    except Exception as e:
        print(f'🚨 Ошибка на {url}: {e}')
        continue

# 💾 Сохраняем результат
detailed_df = pd.DataFrame(detailed_data)
detailed_df.to_csv('krisha_astana_detailed.csv', index=False, encoding='utf-8-sig')
print(f'✅ Сохранено {len(detailed_df)} объявлений с расширенными параметрами.')
