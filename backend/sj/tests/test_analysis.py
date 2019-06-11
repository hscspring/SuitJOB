# coding:utf8

import os
import sys
import pytest
from pnlp import pmag


ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_PATH)

from analysis import calc_score
from analysis import (get_duty_cate_score, 
    get_require_post_score, 
    get_demand_post_score)


duty = [('日常管理', '职能'), ('团队成员', '销售'), ('业务流程', '产品')]
require = [('开发流程', '技术'), ('设计工作经验', '设计'), ('合作能力', '技术')]


def test_duty():
    duty_s = get_duty_cate_score(duty)
    assert type(duty_s) == pmag.MagicDict
    assert len([*duty_s]) == 3

def test_require():
    require_s = get_require_post_score(require)
    assert type(require_s) == pmag.MagicDict
    assert len([*require_s]) == 2

def test_demand():
    demand_s = get_demand_post_score(require)
    assert type(demand_s) == pmag.MagicDict
    assert len([*demand_s]) == 2

def test_calc():
    user_chosen = {"like": duty, "cando": require}
    res = calc_score(user_chosen)
    assert type(res) == list

if __name__ == '__main__':
    pass