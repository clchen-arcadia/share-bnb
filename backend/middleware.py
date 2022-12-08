from sqlalchemy.orm import backref
from flask import request, g, jsonify
from functools import wraps
import time
import jwt
import os

from models import Listing

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
    def validate_login(*args, **kwargs):
        if g.user is not None:
            return func(*args, **kwargs)
        else:
            return jsonify({"error": "User must be logged in."}), 401
    return validate_login

def ensure_admin(func):
    def validate_admin(*args, **kwargs):
        if(g.user is None):
            return jsonify({"error": "User not authorized."}), 401
        if (g.user.get('is_admin') is True):
            return func(*args, **kwargs)
        else:
            return jsonify({"error": "User not authorized."}), 401
    return validate_admin

def ensure_admin_or_correct_user(func):
    def validate_admin_user(*args, **kwargs):
        if(g.user is None):
            return jsonify({"error": "User not authorized."}), 401
        if (g.user.get('is_admin') is True
                or g.user.get('username') == kwargs['username']):
            return func(*args, **kwargs)
        else:
            return jsonify({"error": "User not authorized."}), 401
    return validate_admin_user

def ensure_admin_or_correct_host(func):
    def validate_admin_host(*args, **kwargs):
        if(g.user is None):
            return jsonify({"error": "User not authorized."}), 401
        listing = Listing.query.get_or_404(kwargs['listing_id'])
        if (g.user.get('is_admin') is True
                or g.user.get('username') == listing.host_username):
            return func(*args, **kwargs)
        else:
            return jsonify({"error": "User not authorized."}), 401
    return validate_admin_host
