from sqlalchemy.orm import backref
from flask import request, jsonify, make_response
from functools import wraps
import time


def test_decorator(f):  # f is equal to the joel function itself
    def wrapped():
        print("before")
        _start = time.time()
        result = f()
        _end = time.time()
        print("after")
        print(_end - _start)
        return result
    return wrapped

    # test_decorator is returning the function "wrapped"
