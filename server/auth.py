import os
from functools import wraps
from flask import session, abort
from google.oauth2 import id_token
import google.auth.transport.requests


def verify_token(token):
    try:
        info = id_token.verify_oauth2_token(token, google.auth.transport.requests.Request(),
                                            "298770111102-pjqiii259fb57ue60428vfdbo0s2i0ko.apps.googleusercontent.com")
        return {"id": info["sub"], "email": info["email"]}, None
    except Exception as e:
        return None, e


def login_required(function):
    def wrapper(*args, **kwargs):
        return function() if "google_id" in session else abort(401)

    return wrapper


def user_required(user_type):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "google_id" not in session:
                abort(401)
            if "user_type" not in session or user_type != session["user_type"]:
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator
