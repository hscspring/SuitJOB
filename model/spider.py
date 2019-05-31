import os
import random
from selenium import webdriver
import time
from pnlp import piop

from config import urlist_path, html_path


def write_html(fpath, page_source):
    with open(fpath, 'w') as f:
        f.write(page_source)

def download():
    driver = webdriver.Chrome()
    filelist = os.listdir(urlist_path)
    for file in filelist:
        if file[0] == '.':
            continue
        data = piop.read_json(os.path.join(urlist_path, file))
        fpath = os.path.join(html_path, data['position'])
        piop.check_dir(fpath)
        urlist = data['urlist']
        for i, url in enumerate(urlist):
            fname = os.path.split(url)[-1]
            if os.path.exists(os.path.join(fpath, fname)):
                continue
            driver.get(url)
            ps = driver.page_source
            write_html(os.path.join(fpath, fname), ps)
            time.sleep(random.randint(1, 3))
            # 每 10 个重启一次
            if i % 10 == 0:
                driver.close()
                driver = webdriver.Chrome()

def check_repeat_url():
    # 重复 url 检验
    filelist = os.listdir(urlist_path)
    for file in filelist:
        if file[0] == '.':
            continue
        data = piop.read_json(os.path.join(urlist_path, file))
        fpath = os.path.join(html_path, data['position'])
        urlist = data['urlist']
        if len(urlist) != len(set(urlist)):
            print(file, len(set(urlist)), len(urlist))
        filenum = len([_ for _ in os.listdir(fpath) if _[0] != '.'])
        urlnum = len(urlist)
        if filenum != urlnum:
            print(file, filenum, urlnum)
        if filenum != len(set(urlist)):
            print("wrong")

if __name__ == '__main__':
    download()
    check_repeat_url()

