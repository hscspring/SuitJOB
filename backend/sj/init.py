import random
import hug

from utils import random_pick
from config import MODEL, IGNORE


def pick_words(cate: str, lst: list, num: int) -> list:
    """
    Add category to random picked words.

    Parameters
    ----------
    cate: str
        category
    lst, num: 
        See `random_pick`.
    
    Returns
    -------
    List with category.
    
    Notes
    -----
    
    """
    wlist = random_pick(lst, num)
    res = [(w, cate) for w in wlist if w not in IGNORE]
    return res

def remove_repeat(item_list: list) -> list:
    """
    Remove repeated items from a given list.

    Parameters
    ----------
    item_list: list
        The given list.
    
    Returns
    -------
    Non-repeating list.
    
    Notes
    -----
    
    """
    dct = dict(item_list)
    res = []
    for key,value in dct.items():
        res.append((key, value))
    return res

@hug.cli()
@hug.get('/init', output=hug.output_format.json)
def generate():
    """
    Generate (random pick) duty and require list.
    Each item of those lists contains word and their category.

    Parameters
    ----------

    Returns
    -------
    Duty list and Require list with non-repeated items.
    
    Notes
    -----
    
    """
    duty_list, require_list = [], []
    for key, value in MODEL.items():
        duty_wdict = value['duty']
        require_wdict = value['require']
        duty_wclist = pick_words(key, [*duty_wdict], 7)
        require_wclist = pick_words(key, [*require_wdict], 7)
        duty_list.extend(duty_wclist)
        require_list.extend(require_wclist)
    duty_list = remove_repeat(duty_list)
    require_list = remove_repeat(require_list)
    random.shuffle(duty_list)
    random.shuffle(require_list)
    return {"like": duty_list, "cando": require_list}


if __name__ == '__main__':
    res = generate()
    print(res)
