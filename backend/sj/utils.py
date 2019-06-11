import numpy as np


def random_pick(pick_list: list, num: int) -> list:
    """
    Random (a uniform distribution) pick up n items from a given list.

    Parameters
    ----------
    pick_list: list
        The given list.
    num: int
        How many to pick up.
    
    Returns
    -------
    Picked items.
    
    Notes
    -----
    
    """
    res = []
    index = np.random.choice(len(pick_list), num, replace=False)
    for i in list(index):
        res.append(pick_list[i])
    return res

def safe_divide(a, b):
    """Prevent ZeroDivisionError"""
    return a/(1e-5+b)