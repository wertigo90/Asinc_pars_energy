import os
import time
import sqlite3
from datetime import datetime, timedelta
from pprint import pprint

# import selenium
from bs4 import BeautifulSoup as bs

from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as ww
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import pandas as pd

#################################################
################  Создание БД  ##################
#################################################
conn = sqlite3.connect('discon.db')
cur = conn.cursor()
########## Наполнение базы таблицей
cur.execute('''CREATE TABLE IF NOT EXISTS disconections(            
            subject TEXT,
            organisation TEXT,
            filial TEXT,
            res TEXT,
            munic TEXT,
            naspunkt TEXT,
            street TEXT,
            numofstr TEXT,
            startdate timestamp,
            starttime timestamp,
            finishdate timestamp,
            finishtime timestamp);
            ''')
            # supply TEXT,
            # namework TEXT,
            # numpeop INT);
            # ''')
cur.execute('DELETE FROM disconections;',);
conn.commit()
conn.close()

############ Выбор пути драйвера и сайта
# path_drv = 'C:\\Users\\smurov.anatoliy\\PycharmProjects\\Asinc_pars_energ\\geckodriver.exe'# для Linux скачать соответствующий драйвер и указать путь.
path_drv = 'D:\\Documents\\Programming\\pars_energ\\chromedriver.exe'
url = 'https://xn----7sb7akeedqd.xn--p1ai/platform/portal/tehprisEE_disconnection'

############ Количество страниц регионов и настройка дат и времени
ids = list(range(85))
date_start = datetime.now()
date_start = date_start.strftime("%d.%m.%Y")
date_end = datetime.now() + timedelta(days=1)
date_end = date_end.strftime("%d.%m.%Y")

############ Вебдрайвер и настройки для Chrome
options = webdriver.ChromeOptions()
# options.add_argument("start-maximized")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.62 Safari/537.36")
options.add_argument("--headless")
driver = webdriver.Chrome(executable_path= path_drv, options= options)
driver.implicitly_wait(1)
driver.set_page_load_timeout(25)

########## Вебдрайвер и настройки для Firefox
# options = webdriver.FirefoxOptions()
# options.headless = False  #True - работа в фоне False - открытие браузера
# options.set_preference(
#     'general.useragent.override',
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.62 Safari/537.36',
# )
# profile = webdriver.FirefoxProfile()
# profile.set_preference("network.proxy.type", 0) # Direct = 0 - без прокси
# driver = webdriver.Firefox(executable_path=path_drv, options=options, firefox_profile=profile)
# driver.maximize_window()

wait = ww(driver, 10)



#################################################
###############  Перебор сайта  #################
#################################################
def get_data(url):
    driver.set_page_load_timeout(10)
    driver.implicitly_wait(5)
    driver.get(url=url)
    name_subj = ''
    data_ids = driver.page_source

    # поиск актуальных ids
    soup = bs(data_ids, 'lxml')
    idt = soup.find('span', text='Дата начала отключения').findNext('span', class_='ui-calendar hours-filter')
    idt_st_tm = idt.attrs['id']
    idt = soup.find('span', text='Дата окончания отключения').findNext('span', class_='ui-calendar hours-filter')
    idt_fn_tm = idt.attrs['id']
    idt = soup.find('div', class_="ui-g-12 ui-md-6 ui-lg-3").findNext('div')
    id_sel = idt.attrs['id']
    idt = soup.find('div', class_='ui-g-12').findNext('button', class_="ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only main-button butNormalWeight")
    id_show = idt.attrs['id']
    print('show = '+id_show)
    print('select = '+id_sel)
    print('time start = ' + idt_st_tm)
    print('time end = ' + idt_fn_tm)

    # вводим в фильтр начало и окончание работ
    try:
        time.sleep(5)
        wait.until(
            lambda d: d.find_element(By.ID, 'workplaceForm:disconnectionTabsView:DataOtklFilter_input')).send_keys(
            date_start)
        pprint('ввод даты начало')
        time.sleep(0.3)
        wait.until(lambda d: d.find_element(By.ID, f"{idt_st_tm}_input")).send_keys(
            '00:00')
        pprint('ввод время начало')
        time.sleep(0.3)
        wait.until(
            lambda d: d.find_element(By.ID, "workplaceForm:disconnectionTabsView:DataRecoveryFilter_input")).send_keys(
            date_end)
        pprint('ввод дата окончания')
        time.sleep(0.3)
        wait.until(lambda d: d.find_element(By.ID, f"{idt_fn_tm}_input")).send_keys(
            '00:00')
        pprint('ввод время окончания')
        time.sleep(1)

        ####### Выбор субьекта РФ
        for i in range(85):
            try:
                wait.until(lambda d: d.find_element(By.ID, f"{id_sel}_label")).click()
                sel_subj = wait.until(lambda d: d.find_element(By.ID, f"{id_sel}_{i}"))
                pprint('выбор субъекта')
                name_subj = sel_subj.get_attribute('data-label')
                sel_subj.click()
                pprint('клик субъект')
                time.sleep(1)
            except ElementNotInteractableException:
                print("_______________ERR________________")
                print("click subj")
                time.sleep(1)
                continue

            cccc = 0
            while True:
                try:
                    click = wait.until(lambda d:d.find_element(By.ID, f'{id_show}'))
                    click.click()
                    time.sleep(1)

                except ElementClickInterceptedException:
                    print("_______________ERR________________")
                    print('click show')

                except StaleElementReferenceException:
                    print('_________________INFO________________')
                    print('пробуюу нажать кнопку показать')
                    continue

                # except Exception as ex:
                #     print("_______________ERR________________")
                #     print("_______________________________________________________________________________")
                #     print(ex)

                else:
                    print('ошибка показать')
                    break

            pprint('клик показать')
            time.sleep(1)

            cccc = 0
            # показывать по 15
            while cccc < 5:
                try:
                    driver.find_element(By.XPATH,
                                        '//*[@id="workplaceForm:disconnectionTabsView:disconnectionReests_paginator_bottom"]/div/ul/li[3]').click()
                    time.sleep(0.5)

                except Exception as ex:
                    print("_______________ERR________________")
                    print('raws err = ')
                    # print(ex)
                    cccc += 1
                    time.sleep(0.5)
                    # continue
                else:
                    break

            #проверка индекса страницы
            cccc = 0
            while cccc<5:
                try:
                    pagenator = driver.find_element(By.XPATH, '//*[@id="workplaceForm:disconnectionTabsView:disconnectionReests_paginator_bottom"]/a[1]')
                    # time.sleep(1)
                    label = pagenator.get_attribute('aria-label')
                    if label != 1:
                        try:
                            pagenator.click()
                            time.sleep(0.3)
                        except ElementNotInteractableException:
                            print("_______________ERRR______________")
                            print("НЕТ ПАГИНАТОРА, пробуюу еще")
                            cccc+=1
                            continue
                        else:
                            break
                            print("Продолжаю")
                except Exception as ex:
                    print('__________________ERRRROOOOORRRRRR________________________')
                    print(ex)

            try:
                page_ind = wait.until(lambda d: d.find_element(
                                        By.XPATH,
                                        '//*[@id="workplaceForm:disconnectionTabsView:disconnectionReests_paginator_bottom"]/span',
                                    ))
                page = page_ind.find_element(
                    By.CSS_SELECTOR,
                    '#workplaceForm\:disconnectionTabsView\:disconnectionReests_paginator_bottom > span > a.ui-paginator-page.ui-state-default.ui-state-active.ui-corner-all',
                    )
                num = page.get_attribute('aria-label')
                ind_str = int(num)
                print(ind_str)
                if ind_str > 0:
                    parse_data(data=driver.page_source, name_subj=name_subj)

            except Exception as ex:
                print("_______________INFO________________")
                print("Отсутствует элемент")
                # print(ex)
                continue

            while True:
                try:
                    while True:
                        try:
                            nexts = wait.until(lambda d: d.find_element(By.XPATH, '//*[@id="workplaceForm:disconnectionTabsView:disconnectionReests_paginator_bottom"]/a[3]'))
                            pprint('next')
                            # pprint(nexts)
                            if nexts:
                                try:
                                    nexts.click()
                                    pprint('клик след страница')
                                    time.sleep(1.5)
                                    parse_data(data= driver.page_source, name_subj=name_subj)
                                    time.sleep(1)

                                except ElementClickInterceptedException:
                                    print("___________________ERR_______________")
                                    print("Ошибка Клик перехвачен")
                                    continue

                                except ElementNotInteractableException:
                                    print("_______________ERR________________")
                                    print("Элемент не интерактивен!")
                                    break

                                except Exception as ex:
                                    print("___________________ERR_______________")
                                    print(ex)
                                    # print(ex)
                                    break
                                else:
                                    break
                            else:
                                print("yce")
                                break

                        except ElementNotInteractableException:
                            print("_______________ERR________________")
                            print('Нет страниц далее')
                            # print(ex)
                            # cccc += 1
                            # continue
                            break

                except ElementNotInteractableException:
                    print("_______________ERR________________")
                    print("not pages")
                    cccc += 1
                    time.sleep(1)
                    continue
                else:
                    print("Следующий субьект")
                    break

    # except TimeoutException:
    #     print("timeout")
    #     get_data(url)
    #
    # except StaleElementReferenceException:
    #     print('1111111111111111111111')
    #     get_data(url)




    except ElementNotInteractableException:
        print("_______________ERR________________")
        print("errr errr errr errr ХЗ ХЗ ХЗ err err err")

    finally:
        print("all done may be")
        driver.close()
        driver.quit()


def parse_data(data, name_subj):
    data = data
    name_subj = name_subj
    subjects = []
    organisations = []
    filials = []
    ress = []
    munics = []
    naspunkts = []
    streets = []
    numofstrs = []
    startdates = []
    starttimes = []
    finishdates = []
    finishtimes = []
    # supplys = []
    # nameworks = []
    # numpeops = []
    # data_base = (subjects, organisations, filials, ress, munics, naspunkt, street, numofstr, startdatetime, finishdatetime, supply, namework, numpeop)
    data_base = {"col_subj":subjects,
                 "col_org": organisations,
                 "col_fil": filials,
                 "col_res": ress,
                 "col_mun": munics,
                 "col_nasp": naspunkts,
                 "col_street": streets,
                 "col_numst": numofstrs,
                 "col_start_date": startdates,
                 "col_start_time": starttimes,
                 "col_fin_date": finishdates,
                 "col_fin_time": finishtimes}
                 #"col_sup": supplys,
                 #"col_name": nameworks,
                 #"col_nump": numpeops}

    # for files in os.listdir('./datas'):
    #     file_name = os.path.basename(files)
    #     file_name = os.path.splitext(file_name)[0]
    #     file_name = file_name.split('.')
    #     file_name = file_name[0]
    # print(file_name)
    #     with open(os.path.join("./datas", files), 'r', encoding="utf-8") as f:
        #         text = f.read()
        #         soup = bs(text, "html")
        # with open('./datas/Белгородская область.index1.html', 'r', encoding='utf-8') as f:
            # print(f.name)
            # file_name = os.path.basename(f.name)
            # file_name = os.path.splitext(file_name)[0]
            # file_name = file_name.split('.')
            # file_name = file_name[0]
            # print(file_name)

    text_of = data
    soup = bs(text_of, 'lxml')
    # text = soup.find('tbody', class_='ui-datatable-data ui-widget-content')#.find('tr',class_='ui-widget-content ui-datatable-even').find_all('td')
    # table = soup.find_all('table')
    # all_cols = []
    # for row in table:
    #     table_cols = row.find_all('td')
    #     all_cols.extend(table_cols)
    #
    # for row in all_cols[4:-65]:
    #     row = row.text.strip()
    #     # print(row)

    text = soup.find('div', class_='ui-datatable-scrollable-body').find_all('tr')

    all_cols = []
    for row in text:
        cccc = row.find_all('td')
        all_cols.extend(cccc)
        # cccc = cccc.text.strip()
        # print(cccc)

    for some in all_cols[::12]:
        organiz = some.text.strip().replace('\n', '')
        organiz = organiz.replace('"','')
        # print(f'Субьект РФ= {file_name}\nkey table = subject')
        # print(f'Сетевая организация= {organiz}\nkey table = organisation')
        # data_base["col_subj"] = file_name
        # data_base["col_org"] = organiz
        # data_base[0].append(file_name)
        # data_base[1].append(organiz)
        subjects.append(name_subj)
        organisations.append(organiz)
        # pprint(data_base)
        # conn = sqlite3.connect('discon.db')
        # cur = conn.cursor()
        # cur.execute(f'''INSERT INTO disconections(subject, organisation)
        #                 VALUES("{file_name}", "{organiz}");
        #                 ''')
        # conn.commit()
        # conn.close()

    for some in all_cols[1::12]:
        filial = some.text.strip().replace('\n', '')
        filial = filial.replace('"','')
        # print(f'Филиал = {filial}\nkey table = filial')
        # data_base[2].append(filial)
        # data_base["col_fil"] = filial
        filials.append(filial)

    for some in all_cols[2::12]:
        res = some.text.strip().replace('\n', '')
        # print(f'РЭС = {res}\nkey table = res')
        # data_base["col_res"] = res
        # data_base[3].append(res)
        ress.append(res)

    for some in all_cols[3::12]:
        munic = some.text.strip().replace('\n', '')
        # print(f'Муниципальное образование = {munic}\nkey table = munic')
        # data_base["col_mun"] = munic
        # data_base[4].append(munic)
        munics.append(munic)

    for some in all_cols[4::12]:
        naspunkt = some.text.strip().replace('\n', '')
        # print(f'Населенный пункт = {naspunkt}\nkey table = naspunkt')
        # data_base["col_nasp"] = naspunkt
        # data_base[5].append(naspunkt)
        naspunkts.append(naspunkt)

    for some in all_cols[5::12]:
        street = some.text.strip().replace('\n', '')
        # print(f'Улица = {street}\nkey table = street')
        # data_base["col_street"] = street
        # data_base[6].append(street)
        streets.append(street)

    for some in all_cols[6::12]:
        numofstr = some.text.strip().replace('\n', '')
        # print(f'№№ домов, объекты = {numofstr}\nkey table = numofstr')
        # data_base["col_numst"] = numofstr
        # data_base[7].append(numofstr)
        numofstrs.append(numofstr)

    for some in all_cols[7::12]:
        startdatetime = some.text.strip().replace('\n', '')
        start_date_time = startdatetime.replace(" ",'')
        start_date = start_date_time[:10]
        start_time = start_date_time[10:]
        print(start_date)
        print(start_time)
        # print(f'Начало отключения Дата и Время = {startdatetime}\nkey table = startdatetime')
        # data_base["col_start"] = startdatetime
        # data_base[8].append(startdatetime)
        # startdatetimes.append(startdatetime)
        startdates.append(start_date)
        starttimes.append(start_time)

    for some in all_cols[8::12]:
        finishdatetime = some.text.strip().replace('\n', '')
        finish_date_time = finishdatetime.replace(' ', '')
        finish_date = finish_date_time[:10]
        finish_time = finish_date_time[10:]
        # print(f'Окончание отключения = {finishdatetime}\nkey table = finishdatetime')
        # data_base["col_fin"] = finishdatetime
        # data_base[9].append(finishdatetime)
        # finishdatetimes.append(finishdatetime)
        finishdates.append(finish_date)
        finishtimes.append(finish_time)

    # for some in all_cols[9::12]:
    #     supply = some.text.strip().replace('\n', '')
    #     # print(f'Оборудования = {supply}\nkey table = supply')
    #     # data_base["col_sup"] = supply
    #     # data_base[10].append(supply)
    #     supplys.append(supply)
    #
    # for some in all_cols[10::12]:
    #     namework = some.text.strip().replace('\n', '')
    #     # print(f'Наименование работ = {namework}\nkey table = namework')
    #     # data_base["col_name"] = namework
    #     # data_base[11].append(namework)
    #     nameworks.append(namework)
    #
    # for some in all_cols[11::12]:
    #     numpeop = some.text.strip().replace('\n', '')
    #     # print(f'Количество обесточенного населения = {numpeop}\nkey table = numpeop')
    #     # data_base["col_nump"] = numpeop
    #     # data_base[12].append(numpeop)
    #     numpeops.append(numpeop)

    # print(len(data_base["col_subj"]))
    for i in range(len(data_base["col_subj"])):
        # print (data_base["col_subj"][i])
    #     for j in data_base:
    #         print(j[i])
    #
    #     print('----------------------')

        conn = sqlite3.connect('discon.db')
        cur = conn.cursor()
        cur.execute(f'''INSERT INTO disconections(subject,
                        organisation,
                        filial,
                        res,
                        munic,
                        naspunkt,
                        street, 
                        numofstr, 
                        startdate, 
                        starttime, 
                        finishdate, 
                        finishtime
                        )
                        VALUES('{data_base['col_subj'][i]}', 
                        '{data_base['col_org'][i]}', 
                        '{data_base['col_fil'][i]}', 
                        '{data_base['col_res'][i]}', 
                        '{data_base['col_mun'][i]}', 
                        '{data_base['col_nasp'][i]}', 
                        '{data_base['col_street'][i]}', 
                        '{data_base['col_numst'][i]}', 
                        '{data_base['col_start_date'][i]}', 
                        '{data_base['col_start_time'][i]}', 
                        '{data_base['col_fin_date'][i]}',
                        '{data_base['col_fin_time'][i]}');
                        ''')
                        # '{data_base['col_sup'][i]}',
                        # '{data_base['col_name'][i]}',
                        # '{data_base['col_nump'][i]}');
                        # ''')
        conn.commit()
        conn.close()

def prnt_db():
    conn = sqlite3.connect('discon.db')
    cur = conn.cursor()
    for row in cur.execute('SELECT * FROM disconections'):
        print(row)

    conn.close()


def main():
    get_data(url)
    prnt_db()

if __name__ == "__main__":
    main()
