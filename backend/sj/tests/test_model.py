# coding:utf8

import os
import sys
import pytest

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_PATH)


from config import MODEL, IGNORE

def test_model_format():
    assert type(MODEL) == dict

def test_model_category_num():
    assert len(*[MODEL]) == 8

def test_model_sub_category_num():
    num = 0
    for cate in [*MODEL]:
        posts = MODEL[cate]['posts']
        num += len([*posts])
    assert num == 39

def test_ignore_format():
    assert type(IGNORE) == list


if __name__ == '__main__':
    print(ROOT_PATH)
    print(IGNORE)