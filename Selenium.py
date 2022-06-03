import time
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import pandas as pd

path_drv = "C:\\Users\\smurov.anatoliy\\PycharmProjects\\Asinc_pars_energ\\geckodriver.exe"
url = "https://xn----7sb7akeedqd.xn--p1ai/platform/portal/tehprisEE_disconnection"



def get_data(url):
    options = webdriver.FirefoxOptions()
    options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.62 Safari/537.36")

    try:
        driver = webdriver.Firefox(executable_path=path_drv, options=options)
        driver.get(url=url)
        time.sleep(3)

        # Введение даты начала
        driver.find_element(By.ID, 'workplaceForm:disconnectionTabsView:DataOtklFilter_input').click()
        driver.find_element(By.ID, 'workplaceForm:disconnectionTabsView:DataOtklFilter_input').clear()
        driver.find_element(By.ID, 'workplaceForm:disconnectionTabsView:DataOtklFilter_input').send_keys('03062022')
        time.sleep(1)
        # Введение времени начала
        driver.find_element(By.ID, "workplaceForm:disconnectionTabsView:j_idt3994_input").click()
        driver.find_element(By.ID, "workplaceForm:disconnectionTabsView:j_idt3994_input").clear()
        driver.find_element(By.ID, "workplaceForm:disconnectionTabsView:j_idt3994_input").send_keys('0000')
        time.sleep(1)
        # Введение даты окончания
        driver.find_element(By.ID, "workplaceForm:disconnectionTabsView:DataRecoveryFilter_input").click()
        driver.find_element(By.ID, "workplaceForm:disconnectionTabsView:DataRecoveryFilter_input").clear()
        driver.find_element(By.ID, "workplaceForm:disconnectionTabsView:DataRecoveryFilter_input").send_keys('04062022')
        time.sleep(1)
        # Введение времени окончания
        driver.find_element(By.ID, "workplaceForm:disconnectionTabsView:j_idt4000_input").click()
        driver.find_element(By.ID, "workplaceForm:disconnectionTabsView:j_idt4000_input").clear()
        driver.find_element(By.ID, "workplaceForm:disconnectionTabsView:j_idt4000_input").send_keys('0000')
        time.sleep(1)

        # клик на фильтр субъекта
        driver.find_element(By.ID,"workplaceForm:disconnectionTabsView:j_idt3967").click()
        time.sleep(2)
        #Выбор субъекта из списка
        sel_subj = driver.find_element(By.ID,'workplaceForm:disconnectionTabsView:j_idt3967_items')
        sel_subj = driver.find_element(By.ID,"workplaceForm:disconnectionTabsView:j_idt3967_4").click()
        time.sleep(2)
        # Клик на показать
        driver.find_element(By.ID,"workplaceForm:disconnectionTabsView:j_idt4002").click()
        time.sleep(3)

        next = driver.find_element(By.XPATH,"//*[@id='workplaceForm:disconnectionTabsView:disconnectionReests_paginator_bottom']/a[3]")#.click()
        while next:
            next.click()
            time.sleep(2)
            page = driver.find_element(By.XPATH, '//*[@id="workplaceForm:disconnectionTabsView:disconnectionReests_paginator_bottom"]/span')
            page = page.find_elements(By.CSS_SELECTOR, '#workplaceForm\:disconnectionTabsView\:disconnectionReests_paginator_bottom > span > a.ui-paginator-page.ui-state-default.ui-corner-all.ui-state-active')
            # page = page.find_element('aria-label')
            print(page)
        pprint(next)

        time.sleep(5)
        # pprint(next)
        # if
        #     driver.find_element(By.CLASS_NAME, 'ui-paginator-next ui-state-default ui-corner-all').click()



        with open("index.html", "w", encoding='utf-8') as file:
            file.write(driver.page_source)
        time.sleep(5)


    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

def main():
    get_data(url)


if __name__=="__main__":
    main()


