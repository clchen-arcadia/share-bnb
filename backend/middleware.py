from flask import g, jsonify
from functools import wraps
import os
from dotenv import load_dotenv

load_dotenv()

from models import Listing

my_secret_key = os.getenv('SECRET_KEY')


def ensure_logged_in(func):
    @wraps(func)
    def validate_login(*args, **kwargs):
        if g.user is not None:
            return func(*args, **kwargs)
        else:
            return jsonify({"error": "User must be logged in."}), 401
    return validate_login


def ensure_admin(func):
    @wraps(func)
    def validate_admin(*args, **kwargs):
        if (g.user is None):
            return jsonify({"error": "User not authorized."}), 401
        if (g.user.get('is_admin') is True):
            return func(*args, **kwargs)
        else:
            return jsonify({"error": "User not authorized."}), 401
    return validate_admin


def ensure_admin_or_correct_user(func):
    @wraps(func)
    def validate_admin_user(*args, **kwargs):
        if (g.user is None):
            return jsonify({"error": "User not authorized."}), 401
        if (g.user.get('is_admin') is True
                or g.user.get('username') == kwargs['username']):
            return func(*args, **kwargs)
        else:
            return jsonify({"error": "User not authorized."}), 401
    return validate_admin_user


def ensure_admin_or_correct_host(func):
    @wraps(func)
    def validate_admin_host(*args, **kwargs):
        if (g.user is None):
            return jsonify({"error": "User not authorized."}), 401
        listing = Listing.query.get_or_404(kwargs['listing_id'])
        if (g.user.get('is_admin') is True
                or g.user.get('username') == listing.host_username):
            return func(*args, **kwargs)
        else:
            return jsonify({"error": "User not authorized."}), 401
    return validate_admin_host


def ensure_correct_user(func):
    @wraps(func)
    def validate_user(*args, **kwargs):
        if (g.user is None):
            return jsonify({"error": "User not authorized."}), 401
        if g.user.get('username') == kwargs['username']:
            return func(*args, **kwargs)
        else:
            return jsonify({"error": "User not authorized."}), 401
    return validate_user
