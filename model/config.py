import os
from pnlp import piop

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_URL = "https://www.lagou.com/zhaopin/"

ID = "16302011"
AK = "jDOKyp4qpzeXFHSq91h7K0AG"
SK = "70l8NbS35BG8NuiKhbzEQDBVWdX0HysS"



IGNORE = piop.read_lines('stop_words.txt')
NEEDPOS = ['n', 'nz', 'vn', 'a', 'an']
DTIMEDICT = {
    '1天前': "2019-05-11",
    "2天前": "2019-05-10", 
    "3天前": "2019-05-09"
}


model_path = os.path.join(BASE_DIR, 'model')
urlist_path = os.path.join(BASE_DIR, 'data', 'position_urlist')
html_path = os.path.join(BASE_DIR, 'data', 'html')
category_path = os.path.join(BASE_DIR, 'data', 'category')
extract_path = os.path.join(BASE_DIR, 'data', 'extract')
segpos_path = os.path.join(BASE_DIR, 'data', 'segpos')


cate_gw = piop.read_yml(os.path.join(category_path, 'category.yml'))
cate_url = piop.read_yml(os.path.join(category_path, 'category_url_jointag.yml'))

if __name__ == '__main__':
    print(BASE_DIR)
    print(extract_path)
    print(segpos_path)