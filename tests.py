from selenium import webdriver

path_drv = "C:\\Users\\smurov.anatoliy\\PycharmProjects\\Asinc_pars_energ\\geckodriver.exe"
url = "https://xn----7sb7akeedqd.xn--p1ai/platform/portal/tehprisEE_disconnection"

options = webdriver.FirefoxOptions()
options.headless = True
options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.62 Safari/537.36")

driver = webdriver.Firefox(executable_path=path_drv, options=options)
driver.get(url=url)

