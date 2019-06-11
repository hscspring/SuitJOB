import json
import math
import os
from pnlp import piop, pmag

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(ROOT_PATH, "data", "model.txt")
IGNORE_PATH = os.path.join(ROOT_PATH, "data", "ignore.txt")

MODEL = piop.read_json(MODEL_PATH)
IGNORE = piop.read_lines(IGNORE_PATH)

def get_demand_normfactor():
    """
    Get demand normalization factor
    Parameters
    -----------
    
    Returns
    --------
        demand normalization factor, int type
    """
    csfs, ilfs, factors = [], [], []
    for cate, _others in MODEL.items():
        for post, others in _others['posts'].items():
            item = MODEL[cate]['posts'][post]['demand']
            csf = item.get('continuous_freq',0)
            ilf = item.get('interval_freq',0)
            phf = item.get('publish_freq', 0)
            # factor = (csf + ilf) / 2 * phf
            csfs.append(csf)
            ilfs.append(ilf)
            # factors.append(factor)
    assert len(csfs) == len(ilfs) == 39
    return math.ceil(sum(csfs)), math.ceil(sum(ilfs))

# def get_duty_normfactor():
#     """
#     Get duty normalization factor
#     Parameters
#     -----------
    
#     Returns
#     --------
#         duty normalization factor, dict type
#     """
#     factors = pmag.MagicDict()
#     for cate, _other in MODEL.items():
#         item_nfs = []
#         for w, _fp in _other["duty"].items():
#             freq = MODEL[cate]["duty"][w]["freq"]
#             # assert freq == _fp["freq"]
#             prob = _fp["prob"]
#             factor = freq * prob
#             item_nfs.append(factor)
#         factors[cate] = math.ceil(max(item_nfs))
#     assert len(factors) == 8
#     return factors

# def get_require_normfactor():
#     """
#     Get duty normalization factor
#     Parameters
#     -----------
    
#     Returns
#     --------
#         duty normalization factor, dict type
#     """
#     factors = pmag.MagicDict()
#     for cate, _other in MODEL.items():
#         cate_nfs = []
#         for post, others in _other["posts"].items():
#             item_nfs = []
#             for w, _fp in others["require"].items():
#                 item = MODEL[cate]["posts"][post]["require"][w]
#                 freq = item.get("freq", 0)
#                 prob = item.get("prob", 0)
#                 # assert freq == _fp["freq"]
#                 # assert prob == _fp["prob"]
#                 factor = freq * prob
#                 item_nfs.append(factor)
#             factors[cate][post] = math.ceil(max(item_nfs))
#         #     cate_nfs.append(item_nf)
#         # factors.append(cate_nfs)
#     assert len(factors) == 8
#     assert sum([len(pitem.values()) for c,pitem in factors.items()]) == 39
#     return factors

CFSUM, IFSUM = get_demand_normfactor() # 1814, 1947
DEMAND_NF = (CFSUM + IFSUM)/2


if __name__ == '__main__':
    print(ROOT_PATH)
    print(IGNORE)
    print(CFSUM, IFSUM, DEMAND_NF)


