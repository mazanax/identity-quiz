from datetime import datetime
from functools import wraps

from flask import request

from models import AccessToken


def protected(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        token = access_token()
        return fn(*args, **kwargs) if token is not None and user() is not None else ({}, 401)
    return wrapped


def access_token():
    if 'AUTHORIZATION' not in request.headers:
        return None

    now = datetime.utcnow()
    token = AccessToken.select().where(AccessToken.token == request.headers.get('AUTHORIZATION'),
                                       AccessToken.created_at <= now,
                                       AccessToken.expire_at > now)

    if not token.exists():
        return None

    return token.get()


def user():
    token = access_token()
    return token.user if token is not None and token.user.deleted_at is None else None
