# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'We-Jinyao'
__mtime__ = '2023/4/8'
"""
from selenium import webdriver
import time, requests, os, random,multiprocessing


def download_pdf(url, folder, filename):
    response = requests.get(url)
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(f'{folder}/{filename}.pdf', 'wb') as f:
        f.write(response.content)
    print(f"{filename} is done")
    time.sleep(random.randint(500, 3000) / 1000)

def get_ipo_pdf(element):
    lis = element.find_elements_by_tag_name("li")
    href_lis, folder_lis, filename_lis = [], [], []
    for li in lis:
        span = li.find_element_by_xpath(".//span[1]")
        div = li.find_element_by_xpath(".//div")
        if div.text.startswith("标题"):
            continue
        a = div.find_element_by_xpath(".//span[1]/a")
        if a.text.endswith("上市公告书") or a.text.endswith("上市发行公告") or a.text.endswith("科创板上市招股说明书") or a.text.endswith("科创板上市招股意向书"):
            href_lis.append(a.get_attribute("href"))
            folder = span.text
            folder_lis.append(f'{download_folder}/{folder}')
            filename_lis.append(a.text)
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    pool.starmap(download_pdf, zip(href_lis, folder_lis, filename_lis))
    pool.close()

sleep_time = 3
start_page = 2 # 从第几页开始
data_value = 2 # 0:全部 1:主板 2:科创板
download_folder = "pdf2"
if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get("http://www.sse.com.cn/ipo/disclosure/")
    time.sleep(sleep_time)
    board = ["#selectCate-xxpl > span:nth-child(1)", "#selectCate-xxpl > span:nth-child(2)", "#selectCate-xxpl > span:nth-child(3)"]
    driver.find_element_by_css_selector(board[data_value]).click()
    time.sleep(sleep_time)
    if start_page > 1:
        driver.execute_script(f"xxplList({start_page});")
    time.sleep(sleep_time)
    next_page = driver.find_element_by_css_selector(
        "body > div.container.ipo-content > div:nth-child(2) > div > div > ul > li.next > a")
    while (1):
        element = driver.find_element_by_css_selector("body > div.container.ipo-content > div:nth-child(2) > div > ul")
        get_ipo_pdf(element)
        if next_page.get_attribute("href") == 'javascript:void(0);': # 判断是否到最后一页
            break
        next_page.click()
        time.sleep(sleep_time)
        next_page = driver.find_element_by_css_selector(
            "body > div.container.ipo-content > div:nth-child(2) > div > div > ul > li.next > a")
        time.sleep(random.randint(0, sleep_time))
    driver.close()
    print("done")
