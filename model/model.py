import os
from collections import Counter
import datetime
from pnlp import pmag, piop

from config import segpos_path, model_path, category_path
from config import cate_gw
from config import IGNORE, NEEDPOS



def list2ngrams(lst: list, n: int, exact=True) -> list:
    """ Convert list into character ngrams. """
    return ["||".join(lst[i:i+n]) for i in range(len(lst)-(n-1))]


def every_in_list(lst1: list, lst2: list) -> bool:
    res = []
    for item in lst1:
        if item in lst2:
            continue
        else:
            res.append(item)
    if len(res) == 0:
        return True
    else:
        return False


def atleast_one_in_list(lst1: list, lst2: list) -> bool:
    res = []
    for item in lst1:
        if item in lst2:
            res.append(item)
    if len(res) == 0:
        return False
    else:
        return True


def get_common(wp_list: list, ignore: list, need: list, n=100) -> list:
    res = []
    for item in list2ngrams([w+"||"+p for (w, p) in wp_list], 2):
        tmp = item.split("||")
        ww = [tmp[0], tmp[2]]
        if atleast_one_in_list(ww, ignore):
            continue
        pp = [tmp[1], tmp[3]]
        if every_in_list(pp, need):
            res.append(("".join(ww)))  # + " " + " ".join(pp)
#     return [(wp, f) for (wp, f) in Counter(res).most_common() if f >= 5]
    return Counter(res).most_common(n)


def filter_require(duty: list, require: list) -> list:
    res = []
    duty_wlist = [w for w, f in duty]
    for item in require:
        if item[0] in duty_wlist:
            continue
        else:
            res.append(item)
    return res


def get_need_item(wf_list: list) -> list:
    res = pmag.MagicDict()
    n = sum([f for (w, f) in wf_list])
    for w, f in wf_list:
        res[w]['freq'] = f
        res[w]['prob'] = f/n
    return res


def get_dtime_item(dtime_list: list):
    res = {}
    count = len(dtime_list)
    if count == 0:
        res['count'] = 0
        res['continuous_freq'] = 0
        res['interval_freq'] = 0
        res['publish_freq'] = 0
    else:
        sorted_dt = sorted(dtime_list)
        begin = datetime.datetime.strptime(sorted_dt[0], "%Y-%m-%d")
        end = datetime.datetime.strptime(sorted_dt[-1], "%Y-%m-%d")
        res['count'] = count
        res['continuous_freq'] = count/((end-begin).days+1)
        res['interval_freq'] = count/len(set(dtime_list))
        res['publish_freq'] = len(set(dtime_list))/((end-begin).days+1)
    return res


if __name__ == '__main__':
    segpos_files = sorted(os.listdir(segpos_path))
    res = pmag.MagicDict()
    for cate, _post in cate_gw.items():
        duty_list, require_list, dtimes_list = [], [], []
        tmp = pmag.MagicDict()
        for post, job in _post.items():
            tmp_duty_list, tmp_require_list, tmp_dtimes_list = [], [], []
            tag = cate+"_"+post
            for file in segpos_files:
                if tag in file:
                    fname = os.path.join(segpos_path, file)
                    cate_data = piop.read_json(fname)
                    tmp_duty_list.extend(cate_data['duty'])
                    tmp_require_list.extend(cate_data['require'])
                    tmp_dtimes_list.extend(cate_data['dtimes'])

            tmp_duty = get_common(tmp_duty_list, IGNORE, NEEDPOS)
            tmp_require = filter_require(tmp_duty,
                                         get_common(
                                             tmp_require_list,
                                             IGNORE,
                                             NEEDPOS))

            tmp[post]['duty'] = get_need_item(tmp_duty)
            tmp[post]['require'] = get_need_item(tmp_require)
            tmp[post]['demand'] = get_dtime_item(tmp_dtimes_list)

            duty_list.extend(tmp_duty_list)
            require_list.extend(tmp_require_list)
            dtimes_list.extend(tmp_dtimes_list)

        duty = get_common(duty_list, IGNORE, NEEDPOS)
        require = filter_require(
            duty, get_common(require_list, IGNORE, NEEDPOS))

        res[cate]['duty'] = get_need_item(duty)
        res[cate]['require'] = get_need_item(require)
        res[cate]['demand'] = get_dtime_item(dtimes_list)
        res[cate]['posts'] = tmp
    piop.write_json(os.path.join(model_path, "model.txt"),
                    res, indent=4, ensure_ascii=False)
