# coding:utf-8


import os
import hug
import init, analysis

@hug.get('/')
def say_hi():
    return "Hi from SuitJOB API."

@hug.extend_api('/api')
def with_other_apis():
    return [init, analysis]

