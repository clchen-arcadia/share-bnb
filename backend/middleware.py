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
        if g.user is not None:
            return func(*args, **kwargs)
        else:
            return jsonify({"error": "User must be logged in."}), 401
    return wrapped

def ensure_admin(func):
    def wrapped2(*args, **kwargs):
        if(g.user is None):
            return jsonify({"error": "User not authorized."}), 401
        if (g.user.get('is_admin') is True):
            return func(*args, **kwargs)
        else:
            return jsonify({"error": "User not authorized."}), 401
    return wrapped2

def ensure_admin_or_correct_user(func):
    def wrapped3(*args, **kwargs):
        if(g.user is None):
            return jsonify({"error": "User not authorized."}), 401
        if (g.user.get('is_admin') is True
                or g.user.get('username') == kwargs['username']):
            return func(*args, **kwargs)
        else:
            return jsonify({"error": "User not authorized."}), 401
    return wrapped3

def ensure_admin_or_correct_host(func)
