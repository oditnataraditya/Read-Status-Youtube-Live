from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.ie.options import ElementScrollBehavior
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from re import search
import time
import pandas as pd
import gspread
from random import randint

gc = gspread.oauth()

options=Options()
options.profile = r'C:\Users\Acer\AppData\Roaming\Mozilla\Firefox\Profiles\51rk56w7.default'
options.headless = False
service = Service(r'D:\Python YGB\Scraper\geckodriver.exe')

link_youtube = []
status = []
for link in link_youtube:
    driver = webdriver.Firefox(options=options, service=service)
    driver.implicitly_wait(10)
    driver.get(link)

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="count"]/ytd-video-view-count-renderer/span[1]'))
        )
        live_stat = driver.find_element(By.XPATH, '//*[@id="count"]/ytd-video-view-count-renderer/span[1]').text
        if search("waiting", str(live_stat)):
            stat = "Belum tayang livestream"
        elif search("views", str(live_stat)):
            stat = "Sedang tayang"
        elif search("watching", str(live_stat)):
            stat = "Sedang livestream"
        status.append(stat)
    finally:
        driver.close()
        time.sleep(randint(0,2))
        # print(status)
status_pd = {
    "Status Youtube" : status
}
status_pd = pd.DataFrame(status_pd)


print("Selesai")