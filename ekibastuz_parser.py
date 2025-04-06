import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

ads_data = []
headers = {"User-Agent": "Mozilla/5.0"}

# ✅ Соберём 149 страниц по Экибастузу
for page in range(1, 150):
    print(f'🔄 Страница {page} из 149')
    url = f'https://krisha.kz/prodazha/kvartiry/ekibastuz/?page={page}'

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f'⚠️ Пропущена {page} (код {response.status_code})')
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        ads = soup.find_all('div', class_='a-card__inc')

        for ad in ads:
            try:
                title = ad.find('a', class_='a-card__title').text.strip()
                price = ad.find('div', class_='a-card__price').text.strip()
                location = ad.find('div', class_='a-card__subtitle').text.strip()
                link = "https://krisha.kz" + ad.find('a', class_='a-card__title')['href']

                # Район, если указан
                district = location.split(',')[-1].strip() if ',' in location else None

                ads_data.append({
                    'title': title,
                    'price': price,
                    'location': location,
                    'district': district,
                    'link': link
                })

            except Exception:
                continue

        time.sleep(1.2)

    except Exception as e:
        print(f'🚨 Ошибка на {url}: {e}')
        continue

# Сохраняем базу ссылок
df = pd.DataFrame(ads_data)
df.to_csv('krisha_ekibastuz_full.csv', index=False, encoding='utf-8-sig')
print(f'✅ Сохранено объявлений: {len(df)}')
