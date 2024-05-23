import os
from functools import wraps
from flask import session, abort
from google.oauth2 import id_token
import google.auth.transport.requests
from pymongo import MongoClient
from werkzeug.security import check_password_hash
from config import MONGODB_CLIENT, DB


def verify_user(username, password):
    user = DB.users.find_one({"username": username})
    if user and check_password_hash(user['password_hash'], password):
        return {"_id": user["id"], "username": username}, None
    else:
        return None, "Authentication failed"


def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        return function() if "email" in session else abort(401)

    return wrapper


def user_required(user_type):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "email" not in session:
                abort(401)
            if "user_type" not in session or user_type != session["user_type"]:
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator
