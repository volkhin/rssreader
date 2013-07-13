#-*- coding: utf-8 -*-
from flask import Blueprint, render_template, request
from flask.ext.login import current_user, login_required

from ..tools import fetch_feeds, import_opml


frontend_blueprint = Blueprint('frontend', __name__)

@frontend_blueprint.route('/')
def index():
    if current_user.is_authenticated():
        return render_template('index.html')
    return "Landing page"

@frontend_blueprint.route('/update_feeds')
@login_required
def update_feeds():
    fetch_feeds(current_user.get_id())
    return "OK"

@frontend_blueprint.route('/upload_opml', methods=['POST'])
@login_required
def upload_opml():
    opml_file = request.files['opml']
    content = opml_file.read()
    import_opml(current_user.get_id(), data=content)
    return "{}"
