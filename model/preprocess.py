import os
from bs4 import BeautifulSoup
import re
from pnlp import piop, ptxt

from config import urlist_path, html_path


def check():
    # 页面检查
    allist = []
    filelist = os.listdir(urlist_path)
    for file in filelist:
        if file[0] == '.':
            continue
        data = piop.read_json(os.path.join(urlist_path, file))
        fpath = html_path + data['position']
        urlist = list(set(data['urlist']))
        allist.extend(urlist)
    print(len(allist), len(set(allist)))

    allfiles = []
    for pname in os.listdir(html_path):
        if pname[0] == '.':
            continue
        for base_file in os.listdir(os.path.join(html_path, pname)):
            allfiles.append(base_file)
    print(len(allfiles), len(set(allfiles)))

    assert len(allfiles) == len(allist)
    assert len(set(allfiles)) == len(set(allist))

def get_jobdiscrib_mark():
    # 输出职位职责和职位要求的说明
    # 对结果剔除 freq 小于 5 的，然后人工筛选一下
    res = dict()
    tmp = dict()
    for pname in os.listdir(html_path):
        if pname[0] == '.':
            continue
        for base_file in os.listdir(os.path.join(html_path, pname)):
            if base_file in tmp:
                continue
            tmp[base_file] = ""
            html_file = os.path.join(html_path, pname, base_file)
            raw_html = piop.read_file(html_file)
            soup = BeautifulSoup(raw_html, features="lxml")
            try:
                jobdetail = soup.find("div", {"class": "job-detail"}).get_text()
            except Exception as e:
                continue
            for item in re.compile(r"\n+").split(jobdetail):
                if re.compile(r'[\da-zA-Z]+').search(item) or len(item) == 0 or len(item) > 8:
                    continue
                item = "||".join(ptxt.Text(item, 'chi').extract.mats)
                if item not in res:
                    res[item] = 1
                else:
                    res[item] += 1
    sorted_res = sorted(res.items(), key=lambda x:x[1], reverse=True)
    print(len(sorted_res))
    with open("job_description_mark_sorted_dict.txt", 'w') as f:
        for item in sorted_res:
            item = item[0] + "||" + str(item[1])
            f.write(item+"\n")

if __name__ == '__main__':
    check()
    get_jobdiscrib_mark()



