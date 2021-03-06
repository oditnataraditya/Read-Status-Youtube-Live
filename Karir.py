from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.ie.options import ElementScrollBehavior
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from re import search
import re
import time
import pandas as pd
import gspread
from random import randint

gc = gspread.oauth()
data = gc.open_by_url("https://docs.google.com/spreadsheets/d/1dUQxJn1fOIw9dx1weECAuw7fGzlrTA8cbZcq3dTBhPk/edit#gid=1458472153") #Link checkpoint yang ingin diubah
ws_stream = data.worksheet("Streamyard") # disesuaikan dengan checkpoint terakhir
vform = ws_stream.get_all_values()
data = pd.DataFrame.from_records(vform, columns=vform[1])
data= data[["Link YT - AKEM\n(Youtube)"]]

data = data[324:363]
# .drop(index=data.index[:2,], 
#         axis=0, 
#         inplace=True)
# data.drop(index=data.index[5:], 
#         axis=0, 
#         inplace=True)

profile_path = r'C:\Users\Acer\AppData\Roaming\Mozilla\Firefox\Profiles\51rk56w7.default'
options=Options()
options.set_preference = ('profile', profile_path)
options.headless = False
service = Service(r'D:\Python YGB\Scraper\geckodriver.exe')

data_link = data.values.tolist()
link_youtube= []
for x in data_link:
    for link in x:
        link_youtube.append(link)
status = []
deskripsi = []
thumbnail = []
judul = []
driver = webdriver.Firefox(options=options, service=service)
for link in link_youtube:
    try:
        driver.get(link)
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="info-strings"]/yt-formatted-string'))
            ) #|(By.XPATH, '//*[@id="count"]/ytd-video-view-count-renderer/span[1]')
            live_stat = driver.find_element(By.XPATH,'//*[@id="info-strings"]/yt-formatted-string').text
            if search("Scheduled", str(live_stat)):
                stat = "Belum memulai livestream"
            elif search("Started", str(live_stat)):
                stat = "Sedang livestream"
            else:
                stat = "Sudah menjadi video"
            status.append(stat)
            desk = driver.find_element(By.XPATH, '//*[@id="description"]/yt-formatted-string').text
            title = driver.find_element(By.XPATH, '//*[@id="container"]/h1/yt-formatted-string').text
            exp = "^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*"
            s = re.findall(exp,link)[0][-1]
            thumb = f"https://i.ytimg.com/vi/{s}/maxresdefault.jpg"
            deskripsi.append(desk)
            thumbnail.append(thumb)
            judul.append(title)
        except:
            stat = 'Livestream youtube tidak ada'
            status.append(stat)
            desk = "Tidak ada deskripsi"
            title = "Tidak ada judul"
            thumb = "Tidak ada thumbnail"
            deskripsi.append(desk)
            thumbnail.append(thumb)
            judul.append(title)
    except:
        stat = 'Tidak ada link youtube'
        status.append(stat)
        desk = "Tidak ada deskripsi"
        title = "Tidak ada judul"
        thumb = "Tidak ada thumbnail"
        deskripsi.append(desk)
        thumbnail.append(thumb)
        judul.append(title)
driver.quit()
status_pd = {
    "Status Youtube" : status,
    "Deskripsi" : deskripsi,
    "Judul" : judul,
    "Gambar video" : thumbnail
}
data_rapi = pd.DataFrame(status_pd)
list_rapi = data_rapi.to_numpy().tolist()
headers_rapi = data_rapi.columns.tolist()
dataupdate = [headers_rapi] + list_rapi

ws_stream.update("F325", dataupdate)
print("Selesai")