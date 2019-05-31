import json
import math
import os
from pnlp import piop

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(ROOT_PATH, "model", "model.txt")
IGNORE_PATH = os.path.join(ROOT_PATH, "backend", "ignore.txt")

MODEL = piop.read_json(MODEL_PATH)
IGNORE = piop.read_lines(IGNORE_PATH)

def get_demand_sum():
    csfs = []
    ilfs = []
    for cate, _others in MODEL.items():
        for post, others in _others['posts'].items():
            item = MODEL[cate]['posts'][post]['demand']
            csf = item.get('continuous_freq',0)
            ilf = item.get('interval_freq',0)
            csfs.append(csf)
            ilfs.append(ilf)
    print(len(csfs), len(ilfs))
    assert len(csfs) == len(ilfs)
    return math.ceil(sum(csfs)), math.ceil(sum(ilfs))

CFSUM, IFSUM = get_demand_sum() # 1814, 1947
DEMAND_F = (CFSUM + IFSUM)/2


if __name__ == '__main__':
    print(ROOT_PATH)
    print(IGNORE)
    print(CFSUM, IFSUM)