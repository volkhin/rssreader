#-*- coding: utf-8 -*-
from flask import Blueprint, render_template
from flask.ext.login import current_user


frontend_blueprint = Blueprint('frontend', __name__)
@frontend_blueprint.route('/')
def index():
    if current_user.is_authenticated():
        return render_template('index.html')
    return "Landing page"
