# coding:utf8

import os
import sys
import pytest

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_PATH)

from init import pick_words, remove_repeat


def test_pick_words():
    cate = "cate1"
    lst = "a b c d a".split()
    num = 3
    res = pick_words(cate, lst, num)
    assert len(res) == 3
    assert res[0][1] == cate
    assert type(res) == list

def test_remove_repeat():
    item_list = [('a', 'cate1'), ('a', 'cate2'), ('b', 'cate2')]
    res = remove_repeat(item_list)
    assert len(res) == 2
    assert type(res) == list


if __name__ == '__main__':
    pass