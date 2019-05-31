import os
from bs4 import BeautifulSoup
from selenium import webdriver
import random
import time
from pnlp import piop

from config import cate_gw, cate_url
from config import urlist_path
from config import BASE_URL


def get_urlist(title):
    res, position_links = [], []
    gangwei_base_url = BASE_URL + title + "/"
    driver = webdriver.Chrome()
    for i in range(1, 31):
        url = gangwei_base_url + str(i) + "/?filterOption=2"
        driver.get(url)
        driver.execute_script("window.scrollBy(0,100)")
        ps = driver.page_source
        soup = BeautifulSoup(ps, features="lxml")
        is404 = soup.find("p", {"class": "tip"})
        if is404:
            print(url, is404.get_text())
        else:
            position_links = soup.find_all("a", {"class": "position_link"})
            position_links = [pl.get("href") for pl in position_links]
        if len(position_links) > 0:
            res.extend(position_links)
        else:
            break
        sec = random.randint(1, 3)
        time.sleep(sec)
        # 每 10 个重启一次
        if i % 10 == 0:
            driver.close()
            driver = webdriver.Chrome()
    return res


def flat_all_cates():
    all_items = []
    for cate, sub_cate in cate_gw.items():
        for scate, gangwei in sub_cate.items():
            gangwei_list = gangwei.split(";")
            gangwei_title_list = cate_url[cate][scate].split(";")
            for i, gw in enumerate(gangwei_list):
                all_items.append((cate, scate, gw, gangwei_title_list[i]))
    return all_items

if __name__ == '__main__':
    all_items = flat_all_cates()
    for item in all_items:
        url_dict = {}
        cate = item[0]
        gangwei = item[1]
        zw = item[2]
        title = item[3]
        urlist = get_urlist(title)
        # 不满 30 页的
        if len(urlist) < 15*30:
            print(cate, "\t", gangwei, "\t", zw, "\t", len(urlist))
        url_dict['position'] = cate + "_" + gangwei + "_" + zw + "_" + title
        url_dict['urlist'] = urlist
        out_fpath = os.path.join(urlist_path, url_dict['position'] + ".txt")
        piop.write_json(out_fpath, url_dict, indent=4, ensure_ascii=False)
    
