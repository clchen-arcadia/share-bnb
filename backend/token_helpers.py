import jwt
import os


my_secret_key = os.getenv('SECRET_KEY')


def create_token(user):

    username = user.username
    is_admin = user.is_admin
    is_host = user.is_host

    payload = {
        'username': username,
        'is_admin': is_admin,
        'is_host': is_host
    }

    if isinstance(my_secret_key, str) is not True:
        raise TypeError('Secret Key in env file not a string Code: C06')

    token = jwt.encode(
        payload,
        my_secret_key,
        algorithm='HS256'
    )

    return token
