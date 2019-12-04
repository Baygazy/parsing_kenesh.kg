import requests
from bs4 import BeautifulSoup
import csv
import datetime
from multiprocessing import Pool

# План:
# 1) Мы создадим однопоточный парсер
# 2) Замерим время
# 3) После мы создадим многопоточный парсер в котором
# будем использовать библиотеку multiproccesing и будем
# работать с классом Pool
# 4) Дальше замерим время
# 5) И экспортируем полученный данные в формат csv .

def get_html(url):
    r = requests.get(url)
    return r.text

def get_all_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    tds = soup.find('table', class_='table').find_all('td')
    links = []
    for td in tds:
        a = td.find('a').get('href')
        link = 'http://www.kenesh.kg' + a
        if link not in links and 'fraction' not in link:
            links.append(link)
    return links

def get_page_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        name = soup.find('h3', class_='deputy-name').text.strip()
    except:
        name = "neto"
    try:
        number = soup.find("p", class_='mb-10').text.strip()
    except:
        number = "neto"
    try:
        bio = soup.find('div', id='biography').text.strip()
    except:
        bio = 'neto'
    data = {"name": name, "number": number, "bio": bio}
    return data

def write_csv(data):
    with open('deputy.csv','a') as file:
        writer = csv.writer(file)
        writer.writerow((data['name'], data['number'], data['bio']))            # Здесь записывает в файл csv
        print(data['name'], '\n', data['number'], '\n', data['bio'],'parsed')   # Здесь просто принтит в терминал

def make_all(url):
    html = get_html(url)
    data = get_page_data(html)
    write_csv(data)

def main():
    start = datetime.datetime.now()
    url = 'http://kenesh.kg/ky/deputy/list/35'
    all_links = get_all_links(get_html(url))
    with Pool(40)as p:
        p.map(make_all, all_links)
    end = datetime.datetime.now()
    result = end - start
    print(str(result))

if __name__ == "__main__":   # точка входа
    main()
