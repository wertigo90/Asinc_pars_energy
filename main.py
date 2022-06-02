from datetime import time
from pprint import pprint
from bs4 import BeautifulSoup
from selenium import webdriver

from requests import get
import requests
import os

headers = ({'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.62 Safari/537.36',
            "Accept": "application/xml, text/xml, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Content-Length": "3408",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "Path=/platform; JSESSIONID=Pa3hv4kmiSZubJLzi0Oc5utPHYbVwJqmVaIsn7gW.prod-app4; _ym_uid=1653635797688283398; _ym_d=1653635797; _ym_isad=2",
            "Faces-Request": "partial/ajax",
            "Host": "xn----7sb7akeedqd.xn--p1ai",
            "Origin": "https://xn----7sb7akeedqd.xn--p1ai",
            "Referer": "https://xn----7sb7akeedqd.xn--p1ai/platform/portal/tehprisEE_disconnection",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "X-Requested-With": "XMLHttpRequest",
            })

portal = "https://xn----7sb7akeedqd.xn--p1ai/platform/portal/tehprisEE_disconnection"

post_data = ({"javax.faces.partial.ajax": "true",
              "javax.faces.source": "workplaceForm%3AdisconnectionTabsView%3Aj_idt4002",
              "javax.faces.partial.execute": "workplaceForm%3AdisconnectionTabsView%3Aj_idt4001",
              "javax.faces.partial.render": "workplaceForm%3AdisconnectionTabsView%3AdisconnectionReests+workplaceForm%3AdisconnectionDocument",
              "workplaceForm%3AdisconnectionTabsView%3Aj_idt4002": "workplaceForm%3AdisconnectionTabsView%3Aj_idt4002",
              "workplaceForm": "workplaceForm",
              "workplaceForm%3Afirst": "",
              "workplaceForm%3Asecond": "",
              "workplaceForm%3Athird": "",
              "workplaceForm%3Afourth": "",
              "workplaceForm%3Aconsole_focus": "",
              "workplaceForm%3Aconsole_input": "plan",
              "workplaceForm%3AdisconnectionTabsView%3Aj_idt3967_focus": "",
              "workplaceForm%3AdisconnectionTabsView%3Aj_idt3967_input": "Adygeya",
              "workplaceForm%3AdisconnectionTabsView%3Aj_idt3971_focus": "",
              "workplaceForm%3AdisconnectionTabsView%3Aj_idt3971_input": "",
              "workplaceForm%3AdisconnectionTabsView%3Aj_idt3976": "",
              "workplaceForm%3AdisconnectionTabsView%3Aj_idt3979": "",
              "workplaceForm%3AdisconnectionTabsView%3Aj_idt3982_focus": "",
              "workplaceForm%3AdisconnectionTabsView%3Aj_idt3982_input": "51171",
              "workplaceForm%3AdisconnectionTabsView%3Aj_idt3986_focus": "",
              "workplaceForm%3AdisconnectionTabsView%3Aj_idt3986_input": "",
              "workplaceForm%3AdisconnectionTabsView%3ADataOtklFilter_input": "",
              "workplaceForm%3AdisconnectionTabsView%3Aj_idt3994_input": "",
              "workplaceForm%3AdisconnectionTabsView%3ADataRecoveryFilter_input": "",
              "workplaceForm%3AdisconnectionTabsView%3Aj_idt4000_input": "",
              "workplaceForm%3AdisconnectionTabsView%3AdisconnectionReests_rppDD": ["10", "10"],
              # "workplaceForm%3AdisconnectionTabsView%3AdisconnectionReests_rppDD": "10",
              "workplaceForm%3AdisconnectionTabsView%3AdisconnectionReests_scrollState": "0%2C0",
              "workplaceForm%3AdisconnectionTabsView%3Aj_idt4064_focus": "",
              "workplaceForm%3AdisconnectionTabsView%3Aj_idt4064_input": "Moscow",
              "workplaceForm%3AdisconnectionTabsView%3Aj_idt4068": "",
              "workplaceForm%3AdisconnectionTabsView%3Aj_idt4071": "",
              "workplaceForm%3AdisconnectionTabsView%3Aj_idt4075_focus": "",
              "workplaceForm%3AdisconnectionTabsView%3Aj_idt4075_input": "51159",
              "workplaceForm%3AdisconnectionTabsView%3Aj_idt4079_focus": "",
              "workplaceForm%3AdisconnectionTabsView%3Aj_idt4079_input": "",
              "workplaceForm%3AdisconnectionTabsView%3ADataOtklFilterAvar_input": "31.05.2022",
              "workplaceForm%3AdisconnectionTabsView%3Aj_idt4087_input": "",
              "workplaceForm%3AdisconnectionTabsView%3ADataRecoveryFilterAvar_input": "",
              "workplaceForm%3AdisconnectionTabsView%3Aj_idt4093_input": "",
              # "workplaceForm%3AdisconnectionTabsView%3AdisconnectionReestsAvar_rppDD": "10",
              "workplaceForm%3AdisconnectionTabsView%3AdisconnectionReestsAvar_rppDD": ["10", "10"],
              "workplaceForm%3AdisconnectionTabsView%3AdisconnectionReestsAvar_scrollState": "0%2C0",
              "workplaceForm%3AdisconnectionTabsView%3Aj_idt4155_focus": "",
              "workplaceForm%3AdisconnectionTabsView%3Aj_idt4155_input": "Moscow",
              "workplaceForm%3AdisconnectionTabsView%3Aj_idt4159_focus": "",
              "workplaceForm%3AdisconnectionTabsView%3Aj_idt4159_input": "51159",
              "workplaceForm%3AdisconnectionTabsView%3Aj_idt4163_focus": "",
              "workplaceForm%3AdisconnectionTabsView%3Aj_idt4163_input": "2020",
              # "workplaceForm%3AdisconnectionTabsView%3AReliabilityIndexReestr_rppDD": "10",
              "workplaceForm%3AdisconnectionTabsView%3AReliabilityIndexReestr_rppDD": ["10", "10"],
              "workplaceForm%3AdisconnectionTabsView%3AReliabilityIndexReestr_scrollState": "0%2C0",
              "workplaceForm%3AdisconnectionTabsView_activeIndex": "0",
              "workplaceForm%3Abranch": "",
              "workplaceForm%3Aregion": "",
              "workplaceForm%3Aorg": "",
              "mapRadio": "1",
              "javax.faces.ViewState": "-8158830143025040315%3A-5751097430482873884",
              "javax.faces.ClientWindow": "bNsiQOGd0_6ixNgvpU7FR8CYboOj_PLtWqDZZMH9%3A2"})

params = ({"dashBoard": "tehprisEE_disconnection"})

# responce = get(portal, headers=headers)

r = requests.post(portal, headers=headers, data=post_data, params=params)
r = requests.get(portal, headers={
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                    'Cache-Control': 'max-age=0',
                    'Connection': 'keep-alive',
                    'Cookie': 'Path=/platform; JSESSIONID=dxASg3t41cCCLc9FRlPmY651wN4XSFsAxywsaX3g.prod-app4; _ym_uid=1653635797688283398; _ym_d=1653635797; _ym_isad=2',
                    'Host': 'xn----7sb7akeedqd.xn--p1ai',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Sec-Fetch-User': '?1',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.62 Safari/537.36',
                    'sec-ch-ua': '"Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
})

site=f'https://xn----7sb7akeedqd.xn--p1ai/platform/portal/{r}'

req = requests.post(site, headers=headers, data=post_data, params=params)

# soup = BeautifulSoup(r.text, 'html.parser') #возможно responce.text?
# finds = soup.find('div', class_='ui-datatable-scrollable-body')
with open('123.txt', 'w', encoding='utf-8') as file:
    file.write(r.text)
    file.close()


pprint(req)
pprint(req.text)

