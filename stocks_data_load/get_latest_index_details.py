import time

from selenium import webdriver
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
nse_link = 'https://www.nseindia.com/market-data/live-equity-market'

# browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
browser = webdriver.Chrome(ChromeDriverManager().install())
browser.maximize_window()
browser.get(nse_link)

time.sleep(5)
dwnload = browser.find_element_by_xpath("//a[@onclick='dnldEquityStock()']").click()

browser.quit()