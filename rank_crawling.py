from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time

from def1 import merge_list


def ranking(*args):
    img_datas = []
    text_datas = []

    path = 'C:\WebDriver/chromedriver.exe'
    driver = webdriver.Chrome(path)

    # 통합 랭킹 받아오기
    driver.get("https://m.kinolights.com/ranking/kino")
    time.sleep(0.1)
    req = driver.page_source

    soup = BeautifulSoup(req, 'html.parser')
    src_datas = soup.find_all('span', class_ = "poster-img")
    for data in src_datas:
        img_datas.append(data.img['src'])
        
    datas = soup.find_all('span', class_ = "title-text")
    for i, data in enumerate(datas):
        if(i == 0):
            pass
        else :
            text_datas.append(data.get_text())
            
    kino_list = merge_list(img_datas, text_datas)

    img_datas.clear()
    text_datas.clear()

    #넷플릭스 랭킹 받아오기

    driver.get("https://m.kinolights.com/ranking/netflix")
    time.sleep(0.1)
    req = driver.page_source

    soup = BeautifulSoup(req, 'html.parser')
    src_datas = soup.find_all('span', class_ = "poster-img")
    for data in src_datas:
        img_datas.append(data.img['src'])
        
    datas = soup.find_all('span', class_ = "title-text")
    for i, data in enumerate(datas):
        if(i == 0):
            pass
        else :
            text_datas.append(data.get_text())
            
    netflix_list = merge_list(img_datas, text_datas)

    img_datas.clear()
    text_datas.clear()

    # 웨이브 랭킹 받아오기

    driver.get("https://m.kinolights.com/ranking/wavve")
    time.sleep(0.1)
    req = driver.page_source

    soup = BeautifulSoup(req, 'html.parser')
    src_datas = soup.find_all('span', class_ = "poster-img")
    for data in src_datas:
        img_datas.append(data.img['src'])
        
    datas = soup.find_all('span', class_ = "title-text")
    for i, data in enumerate(datas):
        if(i == 0):
            pass
        else :
            text_datas.append(data.get_text())
            
    wave_list = merge_list(img_datas, text_datas)

    img_datas.clear()
    text_datas.clear()

    # 티빙 랭킹 받아오기

    driver.get("https://m.kinolights.com/ranking/tving")
    time.sleep(0.1)
    req = driver.page_source

    soup = BeautifulSoup(req, 'html.parser')
    src_datas = soup.find_all('span', class_ = "poster-img")
    for data in src_datas:
        img_datas.append(data.img['src'])
        
    datas = soup.find_all('span', class_ = "title-text")
    for i, data in enumerate(datas):
        if(i == 0):
            pass
        else :
            text_datas.append(data.get_text())
            
    tving_list = merge_list(img_datas, text_datas)

    img_datas.clear()
    text_datas.clear()

    # 디즈니 플러스 받아오기

    driver.get("https://m.kinolights.com/ranking/disney")
    time.sleep(0.1)
    req = driver.page_source

    soup = BeautifulSoup(req, 'html.parser')
    src_datas = soup.find_all('span', class_ = "poster-img")
    for data in src_datas:
        img_datas.append(data.img['src'])
        
    datas = soup.find_all('span', class_ = "title-text")
    for i, data in enumerate(datas):
        if(i == 0):
            pass
        else :
            text_datas.append(data.get_text())
            
    disney_list = merge_list(img_datas, text_datas)

    img_datas.clear()
    text_datas.clear()

    # 왓챠 받아오기

    driver.get("https://m.kinolights.com/ranking/watcha")
    time.sleep(0.1)
    req = driver.page_source

    soup = BeautifulSoup(req, 'html.parser')
    src_datas = soup.find_all('span', class_ = "poster-img")
    for data in src_datas:
        img_datas.append(data.img['src'])
        
    datas = soup.find_all('span', class_ = "title-text")
    for i, data in enumerate(datas):
        if(i == 0):
            pass
        else :
            text_datas.append(data.get_text())
            
    watcha_list = merge_list(img_datas, text_datas)

    img_datas.clear()
    text_datas.clear()

    # 영화 받아오기


    driver.get("https://m.kinolights.com/ranking/boxoffice")
    time.sleep(0.1)
    req = driver.page_source

    soup = BeautifulSoup(req, 'html.parser')
    src_datas = soup.find_all('span', class_ = "poster-img")
    for data in src_datas:
        img_datas.append(data.img['src'])
        
    datas = soup.find_all('span', class_ = "title-text")
    for i, data in enumerate(datas):
        if(i == 0):
            pass
        else :
            text_datas.append(data.get_text())
            
    movie_list = merge_list(img_datas, text_datas)

    img_datas.clear()
    text_datas.clear()

    driver.close()
    return kino_list, netflix_list, wave_list, tving_list, disney_list, watcha_list, movie_list
