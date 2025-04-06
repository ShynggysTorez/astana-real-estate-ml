# 📄 Расширенный парсинг по каждой ссылке
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

df = pd.read_csv("C:/Users/cheen/PycharmProjects/krisha_parser_project/krisha_ekibastuz_full.csv")

detailed_data = []
headers = {"User-Agent": "Mozilla/5.0"}

def parse_extended(soup):
    data = {}

    # 1. Основной блок
    for item in soup.find_all('div', class_='offer__info-item'):
        key = item.get('data-name')
        val = item.find('div', class_='offer__advert-short-info')
        if key and val:
            data[key] = val.get_text(strip=True)

    # 2. dt/dd параметры
    for item in soup.select('.offer__parameters dl'):
        dt = item.find('dt')
        dd = item.find('dd')
        if dt and dd:
            key = dt.get('data-name')
            if key:
                data[key] = dd.get_text(strip=True)

    # 3. Описание
    desc = soup.find('div', class_='js-description')
    if desc:
        data['description'] = desc.get_text(strip=True)

    return data

# 🌀 Основной цикл
for i, row in df.iterrows():
    url = row['link']
    print(f"🔎 {i + 1}/{len(df)}: {url}")
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        details = parse_extended(soup)

        detailed_data.append({
            'title': row['title'],
            'price': row['price'],
            'district': row['district'],
            'location': row['location'],
            'link': row['link'],
            'region_clean': row.get('region_clean'),
            'house_type': details.get('flat.building'),
            'year_built': details.get('house.year'),
            'floor': details.get('flat.floor'),
            'ceiling_height': details.get('ceiling'),
            'complex': details.get('map.complex'),
            'condition': details.get('flat.renovation'),
            'area': details.get('live.square'),
            'description': details.get('description'),
        })

        time.sleep(1.2)

    except Exception as e:
        print(f'❌ Ошибка на {url}: {e}')
        continue

# 💾 Сохраняем расширенные данные
df_detailed = pd.DataFrame(detailed_data)
df_detailed.to_csv('krisha_ekibastuz_detailed.csv', index=False, encoding='utf-8-sig')
print(f"✅ Расширенных объявлений сохранено: {len(df_detailed)}")
