from sqlalchemy.orm import backref
from flask import request, g, jsonify
from functools import wraps
import time
import jwt
import os

my_secret_key = os.getenv('SECRET_KEY')


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


def ensure_logged_in(func):
    def wrapped(*args, **kwargs):
        if g.user != None:
            return func(*args, **kwargs)
        else:
            return jsonify({"error": "User must be logged in."}), 401
    return wrapped

# TODO: isAdmin check
# TODO: is correct Host check
# TODO: isAdmin or current user
