from time import time
import requests
import threading
from flask import Flask, jsonify, request
from threading import Timer

import random
import timeit

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def requestNOW():
    node = '127.0.0.1:5000'
    response = requests.get(f'http://{node}/validate')
    print(response)
    
set_interval(requestNOW,6)