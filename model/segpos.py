import os
from pnlp import piop
from aip import AipNlp

from config import ID, AK, SK
from config import extract_path, segpos_path

client = AipNlp(ID, AK, SK)

def get_cate_res(cate_extract_file: str):
    cate_item = piop.read_json(cate_extract_file)
    dtimes, require, duty = [], [], []
    for item in cate_item:
        dtimes.append(item['dtime'])
        if len(item['require']) < 10:
            continue
        try:
            item_require = segpos(item['require'])
            require.extend(item_require)
        except Exception as e:
            print("GET ITEM ERROR.", e)
            continue
        try:
            item_duty = segpos(item['duty'])
            duty.extend(item_duty)
        except Exception as e:
            print("GET ITEM ERROR.", e)
            continue
    try:
        cate = item['category']
    except Exception as e:
        cate = ""
    return cate, duty, require, dtimes

def segpos(text: str) -> list:
    res = []
    try:
        bd_resp = client.lexer(text)
    except Exception as e:
        print("BaiDu Error:", e)
    for item in bd_resp['items']:
        pos = item['pos']
        w = item['item']
        res.append((w, pos))
    return res

if __name__ == '__main__':
    for file in os.listdir(extract_path):
        if file[0] == '.':
            continue
        fname = os.path.join(extract_path, file)
        outname = os.path.join(segpos_path, file)
        if os.path.exists(outname):
            continue
        data = dict()
        cate, fduty, frequire, fdtimes = get_cate_res(fname)
        data['cate'] = cate
        data['duty'] = fduty
        data['require'] = frequire
        data['dtimes'] = fdtimes
        piop.write_json(outname, data, indent=4, ensure_ascii=False)



