from flask import session
from flask import redirect
from flask import abort

from functools import wraps

from cidc_portal.main.services.utils import url_for_with_prefix


def requires_login():
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if (
                "jwt_token" not in session
                or session["jwt_token"] is None
                or "cidc_user_info" not in session
                or session["cidc_user_info"]["role"] is None
            ):
                return redirect(url_for_with_prefix("/login"))
            return f(*args, **kwargs)

        return wrapped

    return wrapper


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if session["cidc_user_info"]["role"] not in roles[0]:
                abort(403)
            return f(*args, **kwargs)

        return wrapped

    return wrapper
