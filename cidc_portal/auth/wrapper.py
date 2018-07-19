from flask import session
from flask import redirect

from functools import wraps

from cidc_portal.main.views import url_for_with_prefix


def requires_login():
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if session["jwt_token"] is None:
                return redirect(url_for_with_prefix("/login"))
            return f(*args, **kwargs)
        return wrapped
    return wrapper


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if session["user_role"] not in roles:
                return error_response()
            return f(*args, **kwargs)
        return wrapped
    return wrapper


def error_response():
    return "You've got no permission to access this page.", 403