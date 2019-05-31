# coding:utf-8


import os
import hug
import init, analysis

@hug.get('/')
def say_hi():
    return "Hi from Auto Comment API."

@hug.extend_api('/api')
def with_other_apis():
    return [init, analysis]

