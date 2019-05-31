import random
import hug

from utils import random_pick
from config import MODEL, IGNORE


def pick_words(cate: str, lst: list, num: int) -> list:
    wlist = random_pick(lst, num)
    res = [(w, cate) for w in wlist if w not in IGNORE]
    return res


@hug.cli()
@hug.post(output=hug.output_format.json)
def generate():
    duty_list, require_list = [], []
    for key, value in MODEL.items():
        duty_wdict = value['duty']
        require_wdict = value['require']
        duty_wclist = pick_words(key, [*duty_wdict], 7)
        require_wclist = pick_words(key, [*require_wdict], 7)
        duty_list.extend(duty_wclist)
        require_list.extend(require_wclist)
    random.shuffle(duty_list)
    random.shuffle(require_list)
    return {"like": duty_list, "cando": require_list}


if __name__ == '__main__':
    res = generate()
    print(res)
