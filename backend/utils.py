import numpy as np


def random_pick(pick_list: list, num: int) -> list:
    res = []
    index = np.random.choice(len(pick_list), num, replace=False)
    for i in list(index):
        res.append(pick_list[i])
    return res

def safe_divide(a, b):

    return a/(1e-5+b)