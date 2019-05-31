import hug
import numpy as np
from pnlp import pmag

from utils import safe_divide
from config import MODEL, DEMAND_F


@hug.cli()
@hug.post(output=hug.output_format.json)
def choose(user_chosen_dict: dict, topk: int = 5):
    score = calc_score(user_chosen_dict)
    res = [(w,f) for (w,f) in score][: topk]
    res = [(w,int(f*100/res[0][1])) for (w,f) in res]
    return res


def calc_score(user_chosen_dict: dict):
    res = pmag.MagicDict()

    duty_list = user_chosen_dict['like']
    require_list = user_chosen_dict['cando']

    duty_cate_score = get_duty_cate_score(duty_list)
    require_post_score = get_require_post_score(require_list)
    demand_post_score = get_demand_post_score(require_list)

    for cate, _posts in require_post_score.items():
        cate_s = duty_cate_score.get(cate, 0)
        for post, post_s in _posts.items():
            demand_s = demand_post_score[cate][post]
            score = cate_s * 0.5 + post_s * 0.3 + demand_s * 0.2
            res[cate+"-"+post] = score
    sorted_res = sorted(res.items(), key=lambda x: x[1], reverse=True)
    return sorted_res


def get_duty_cate_score(chosen_duty_list: list) -> dict:
    res = pmag.MagicDict()
    for w, cate in chosen_duty_list:
        freq = MODEL[cate]['duty'][w]['freq']
        prob = MODEL[cate]['duty'][w]['prob']
        score = prob # freq * prob
        if cate in res:
            res[cate] += score
        else:
            res[cate] = score
    return res


def get_require_post_score(chosen_require_list: list):
    res = pmag.MagicDict()
    for w, cate in chosen_require_list:
        posts = MODEL[cate]['posts']
        for post in [*posts]:
            if w in posts[post]['require']:
                freq = posts[post]['require'][w]['freq']
                prob = posts[post]['require'][w]['prob']
                score = prob # freq * prob
            else:
                continue
            if post in res[cate]:
                res[cate][post] += score
            else:
                res[cate][post] = score
    return res


def get_demand_post_score(chosen_require_list: list):
    res = pmag.MagicDict()
    for w, cate in chosen_require_list:
        posts = MODEL[cate]['posts']
        for post in [*posts]:
            if w in posts[post]['require']:
                demand = posts[post]['demand']
                score = ((demand['continuous_freq'] + demand['interval_freq']
                          )*demand['publish_freq']/(2*DEMAND_F))
            else:
                continue
            if post in res[cate]:
                continue
            else:
                res[cate][post] = score
    return res

def get_demand_post_score_from_require_res(require_post_score: dict):
    res = pmag.MagicDict()
    for cate, posts in require_post_score.items():
        for post, _ in posts.items():
            demand = MODEL[cate]['posts'][post]['demand']
            score = ((demand['continuous_freq'] + demand['interval_freq']
                          )*demand['publish_freq']/(2*DEMAND_F))
            res[cate][post] = score
    return res


if __name__ == '__main__':
    import pprint
    from init import generate
    from utils import random_pick

    user_chosen_dict = generate()

    like = user_chosen_dict['like']
    cando = user_chosen_dict['cando']
    choose_like = random_pick(like, 7)
    choose_cando = random_pick(cando, 7)
  
    print("Choose Like: ", choose_like)
    print("Choose Cando: ", choose_cando)

    res1 = get_duty_cate_score(choose_like)
    res2 = get_require_post_score(choose_cando)
    res3 = get_demand_post_score(choose_cando)
    res = choose(user_chosen_dict)
    pprint.pprint(("duty:", res1))
    pprint.pprint(("requre:", res2))
    pprint.pprint(("demand:", res3))
    pprint.pprint((get_demand_post_score_from_require_res(res2)))
    pprint.pprint(res)





