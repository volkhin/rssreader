#-*- coding: utf-8 -*-
from flask.ext.login import LoginManager, current_user
login_manager = LoginManager()
from functools import wraps
from flask import jsonify

def api_login_required(func):
    @wraps(func)
    def decorated_view(*args, **kws):
        if not current_user.is_authenticated():
            return jsonify(error='login required')
        return func(*args, **kws)
    return decorated_view
