from functools import wraps

from flask import session, url_for, redirect, request


def requires_login(func):
    @wraps(func)
    def decorator_function(*arg, **kwargs):
        if "email" not in session.keys() or session["email"] is None:
            return redirect(url_for('user.login_user', next=request.path))
        return func(*arg, **kwargs)
    return decorator_function