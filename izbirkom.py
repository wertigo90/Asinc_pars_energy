from pprint import pprint
import requests
from bs4 import BeautifulSoup as bs
import asyncio
import aiohttp
import json


headers = ({'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cookie': 'BCSI-CS-a43c75adfdd7b6cc=2; izbFP=44d03f4353c728671bf5370a14f013a3; BCSI-CS-34ea573993872bca=2; session-cookie=16fa3e8a1cfa4f4916a722b2beb261f5cca658f38c151ce7f93c9bf06991a08633d1eaebad37f70201d5a924c6208ab7; sputnik_session=1655704691135|2; JSESSIONID=fafb851d3099cd6c9764353ca44f',
            'Host': 'www.adygei.vybory.izbirkom.ru',
            'Proxy-Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest'
            })
start_url = "http://www.adygei.vybory.izbirkom.ru/region/adygei?action=ik"
start_vrn = '2012000350926'
start_id = '#'
start_part_url = f"Tree&region=01&vrn={start_vrn}"

list_ids = []

data = []


def list_urls():
    global data
    url = start_url+start_part_url
    payload = {'action': 'ikTree', 'region': '01', 'vrn': start_vrn, 'id': start_id}
    list_ids.append(start_vrn)
    data.append({'id': start_vrn})
    req = requests.get(url=url, headers=headers, params=payload)
    src = req.json()
    # print(src)
    for i in src[0]['children']:
        list_ids.append(i['id'])
        # print(i['id'])
        payload = {'action': 'ikTree', 'region': '01', 'vrn': i['id'], 'onlyChildren': 'true', 'id': i['id']}
        part_url = f"Tree&region=01&vrn={i['id']}"
        url = start_url+part_url
        req = requests.get(url=url, headers=headers, params=payload)
        src = req.json()
        # pprint(src)
        for i in src:
            # print(i['id'])
            list_ids.append(i['id'])
            data.append({'id': i['id']})

        # print(i['id'])
    # pprint(list_ids)
    # with open('data.json', 'w') as outfile:
    #     json.dump(data, outfile)
    #
    # with open('data.json', 'r') as readfile:
    #     data = json.load(readfile)
    #     print(data)



def get_data():
    for id in list_ids:
        id_id = id
        part_url = f"&vrn={id}"
        url = start_url+part_url
        payload = {'action': 'ik', 'vrn': f'{id}'}
        req = requests.get(url=url, headers=headers, params=payload)
        # print(req.status_code)
        src = req.text
        parse(src=src, id= id_id)
        # soup = bs(src, 'lxml')
        # with open('./datas/index.html', 'w', encoding='utf-8') as file:
        #     file.write(src)
        #     file.close()


def parse(src, id):
    global data
    soup = bs(src, 'lxml')
    # print(soup)
    name_kom = soup.find('div', class_='center-colm').find('h2')
    addr = soup.find('span', id = 'address_ik')
    tel = soup.find('strong', text='Телефон: ').find_parent()
    fax = soup.find('strong', text='Факс: ').find_parent()
    email_adr = soup.find('strong', text='Адрес электронной почты: ').find_parent()
    end_powers = soup.find('strong', text='Срок окончания полномочий: ').find_parent()
    name = str(name_kom.text)
    # id = id
    # print(id + " id")
    print(name + " name")
    print(addr.text + " address")
    print(tel.text + " phone")
    print(fax.text + " none")
    print(email_adr.text + "None")
    print(end_powers.text + "None")

    data.append({
        'reg': name
    })





def main():
    global data
    # with open('index.html', 'r', encoding='utf-8') as src:
    #     src = src.read()
    #     # print(src.read())
    #     parse(src=src)
    # get_data()
    list_urls()
    get_data()
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

    with open('data.json', 'r') as readfile:
        data = json.load(readfile)
        print(data)


if __name__=="__main__":
    main()