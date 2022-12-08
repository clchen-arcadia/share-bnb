import jwt
import os


my_secret_key = os.getenv('SECRET_KEY')


def create_token(user):
    username = user.username
    isAdmin = user.isAdmin
    isHost = user.isHost

    try:

        payload = {
            'username': username,
            'isAdmin': isAdmin,
            'isHost': isHost
        }
        token = jwt.encode(payload,
                           my_secret_key, algorithm='HS256')
        return token

    except Exception as e:
        return e
