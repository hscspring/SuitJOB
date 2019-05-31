import os
from bs4 import BeautifulSoup
import re
from pnlp import piop, ptxt

from config import DTIMEDICT
from config import html_path, extract_path

JOB_DESC_MARK_DICT = piop.read_lines("job_description_mark_sorted_dict.txt")

def split_duty_require(jobdetail: str) -> list:
    res = {}
    tmp = []
    for item in re.compile(r'\n+').split(jobdetail):
        item_chi = "".join(ptxt.Text(item, 'chi').extract.mats)
        if len(item_chi) == 0 or len(item_chi) > 8:
            continue
        for mark in JOB_DESC_MARK_DICT:
            if mark in item:
                tmp.append(mark)
    tmp = sorted(tmp, key=lambda x: len(x), reverse=True)[:2]
    rex  = "|".join(tmp)
    reg = re.compile(rf'{rex}')
    reslist = reg.split(jobdetail)
    reslist = [_ for _ in reslist if len(ptxt.Text(_, 'chi').extract.mats) > 1]
    return reslist

def get_item(html_file: str) -> dict:
    item = {}
    raw_html = piop.read_file(html_file)
    soup = BeautifulSoup(raw_html, features="lxml")
    content = soup.find("div", {"class": "position-content-l"})
    company = content.find("div", {"class": "company"}).get_text()
    jobname = content.find("span", {"class": "name"}).get_text()
    salary = content.find("span", {"class": "salary"}).get_text()
    labels = content.find("ul", {"class": "position-label clearfix"}
                         ).get_text().replace("\n", ",")[1:-1]
    request = content.find("p").get_text().split("\n/")[-1].replace(" /\n", ",")[:-1]
    dtime = content.find("p", {"class": "publish_time"}).get_text().split("\xa0")[0]
    if ":" in dtime:
        dtime = "2019-05-12"
    elif dtime in DTIMEDICT:
        dtime = DTIMEDICT[dtime]
    else:
        dtime = dtime

    jobadv = soup.find("dd", {"class": "job-advantage"}).get_text().replace("\n", "")
    jobdetail = soup.find("div", {"class": "job-detail"}).get_text()
    
    duty_require_list = split_duty_require(jobdetail)
    if len(duty_require_list) != 2:
        duty, require = "", ""
    else:
        duty, require = duty_require_list
        duty = ptxt.Text(duty, 'whi').clean
        require = ptxt.Text(require, 'whi').clean
    
    item['category'] = "_".join(html_file.split("/")[-2].split("_")[:-1])
    item['pname'] = html_file
    item['company'] = company
    item['jobname'] = jobname
    item['salary'] = salary
    item['labels'] = labels
    item['request'] = request
    item['jobadv'] = jobadv
    item['duty'] = "职位职责：" + duty
    item['require'] = "职位要求：" + require
    item['jobdetail'] = jobdetail
    item['dtime'] = dtime
    
    return item

if __name__ == '__main__':
    for pname in os.listdir(html_path):
        if pname[0] == '.':
            continue
        print("="*20, pname, "BEGIN", "="*20)
        out_file = os.path.join(extract_path, pname + ".txt")
        if os.path.exists(out_file):
            continue
        res = []
        for base_file in os.listdir(os.path.join(html_path, pname)):
            html_file = os.path.join(html_path, pname, base_file)
            try:
                item = get_item(html_file)
                res.append(item)
            except Exception as e:
                print(html_file, e)
                continue
        piop.write_json(out_file, res, indent=4, ensure_ascii=False)
        print("="*20, pname, "DONE", "="*20 + "\n\n")

