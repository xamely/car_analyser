import requests
import re
import numpy as np
from bs4 import BeautifulSoup
from time import sleep
import csv
from random import uniform

def get_html(url):
    sleep(uniform(2, 5))
    r = requests.get(url)
    r.encoding = 'utf-8'
    return r.text

def write_csv(data):
    with open('cars.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow((data['Модель'],
                         data['Цена'],
                         data['Год выпуска'],
                         data['Пробег'],
                         data['Кузов'],
                         data['Объем'],
                         data['Мощность'],
                         data['Коробка'],
                         data['Тип двигателя'],
                         data['Топливо'],
                         data['Расход'],
                         data['Привод'],
                         data['Разгон'],
                         data['Максимальная скорость, км/ч'],
                         data['Страна марки'],
                         data['Класс'],
                         data['Цвет'],
                         data['Состояние'],
                         data['Владельцы'],
                         data['ПТС']))

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_ = 'ListingCars-module__container ListingCars-module__list').find_all('div', class_ = 'ListingItem-module__container')
    for ad in ads:
        link = ad.find('a', class_ = 'Link ListingItemTitle-module__link')['href']
        tmp_html = get_html(link)
        tmp_soup = BeautifulSoup(tmp_html, 'lxml')
        try:
            title = tmp_soup.find('div', class_ = 'CardHead-module__title').text
            price = tmp_soup.find('div', class_ = 'Price-module__caption CardHead-module__priceCaption').text
            price = float(re.sub('\xa0', '', re.sub('₽', '', price)))
            print('done title')
        except:
            print('error title')
            continue
    
        try:
            params = tmp_soup.find_all('div', class_ = 'CardInfo-module__CardInfo__row')
            print('done params')
        except:
            print('error params')
            continue

        year = np.nan # год выпуска
        mileage = np.nan # пробег
        bodytype = np.nan # тип кузова
        color = np.nan # цвет
        wheel = np.nan # руль
        condition = np.nan # состояние
        owners = np.nan # владельцы
        pts = np.nan # ПТС
        for par in params:
            try:
                info = par.find('div', class_ = 'CardInfo-module__CardInfo__cell').text.lower()
                data = par.find('div', class_ = 'CardInfo-module__CardInfo__cell CardInfo-module__CardInfo__cell_right').text.lower()
                print('done info')
            except:
                print('error info')
                continue

            if info == 'год выпуска': 
                year = float(data)
            elif info == 'пробег':
                mileage = float(re.sub('\xa0', '', re.sub('км', '', data)))
            elif info == 'кузов':
                bodytype = data
            elif info == 'цвет':
                color = data
            elif info == 'руль':
                wheel = data
            elif info == 'состояние':
                condition = data
            elif info == 'владельцы':
                owners = int(re.sub('[^0-9]', '', data))
            elif info == 'птс':
                pts = data

        link = tmp_soup.find('a', class_ = 'Link SpoilerLink CardCatalogLink-module__CardCatalogLink')['href']
        tmp_html = get_html(link)
        tmp_soup = BeautifulSoup(tmp_html, 'lxml')

        volume = np.nan # объем
        power = np.nan # мощность
        box = np.nan # коробка 
        engine_type = np.nan # тип двигателя
        fuel = np.nan # топливо
        rear_drive = np.nan # привод
        racing = np.nan # разгон
        consumption = np.nan # расход
        country = np.nan # страна марки
        car_class = np.nan # класс автомобиля
        max_speed = np.nan # максимальная скорость

        try:
            columns = tmp_soup.find_all('div', class_ = 'catalog__column catalog__column_half')
            print('done columns1')
        except:
            print('error columns1')
            continue
        
        lst = columns[2].find_all('dd', class_ = 'list-values__value')
        volume = float(re.sub('[^0-9\.]', '', lst[0].text))
        power = float(re.sub('[^0-9]', '', lst[1].text))
        box = lst[2].text
        engine_type = lst[3].text

        lst = columns[3].find_all('dd', class_ = 'list-values__value')
        names = columns[3].find_all('dt', class_ = 'list-values__label')
        for n in names:
            if n.text.lower() == 'топливо': 
                fuel = lst[0].text
            elif n.text.lower() == 'привод':
                rear_drive = lst[1].text
            elif n.text.lower() == 'разгон':
                racing = float(re.sub('[^0-9\.]', '', lst[2].text))
            elif n.text.lower() == 'расход':
                consumption = float(re.sub('[^0-9\.]', '', lst[3].text))
        
        try:
            columns = tmp_soup.find_all('div', class_ = 'catalog__details-group')
            print('done columns2')
        except:
            print('error columns2')
            continue

        for col in columns:
            name = col.find('div', class_ = 'catalog__h3').text.lower()
            if name == 'общая информация':
                lst = col.find_all('dd', class_ = 'list-values__value')
                country = lst[0].text
                car_class = lst[1].text 
            elif name == 'эксплуатационные показатели':
                lst = col.find_all('dd', class_ = 'list-values__value')
                max_speed = float(lst[0].text)

        data = {'Модель': title,
                'Цена': price,
                'Год выпуска': year,
                'Пробег': mileage,
                'Кузов': bodytype,
                'Объем': volume,
                'Мощность': power,
                'Коробка': box,
                'Тип двигателя': engine_type,
                'Топливо': fuel,
                'Расход': consumption,
                'Привод': rear_drive,
                'Разгон': racing,
                'Максимальная скорость, км/ч': max_speed,               
                'Страна марки': country,
                'Класс': car_class,
                'Цвет': color,
                'Состояние': condition,
                'Владельцы': owners,
                'ПТС': pts
        }

        write_csv(data)

def main():
    url = 'https://auto.ru/rostov-na-donu/cars/used/?sort=fresh_relevance_1-desc&page=1'
    base_url = 'https://auto.ru/rostov-na-donu/cars/used/?sort=fresh_relevance_1-desc&page='

    with open('cars.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(('Модель',
                         'Цена',
                         'Год выпуска',
                         'Пробег',
                         'Кузов',
                         'Объем',
                         'Мощность',
                         'Коробка',
                         'Тип двигателя',
                         'Топливо',
                         'Расход',
                         'Привод',
                         'Разгон',
                         'Максимальная скорость, км/ч',
                         'Страна марки',
                         'Класс',
                         'Цвет',
                         'Состояние',
                         'Владельцы',
                         'ПТС'))

    total_pages = 100
    #for i in range(1, total_pages):
    url_gen = base_url + str(1)
    html = get_html(url_gen)
    get_page_data(html)


if __name__ == "__main__":
    main()