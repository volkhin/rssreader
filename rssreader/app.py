#-*- coding: utf-8 -*-
from flask import Flask, render_template, Blueprint, request, flash, redirect, url_for
from flask.ext.login import login_required, current_user

from .config import DefaultConfig
from .extensions import db, login_manager
from user import user_blueprint, User
from feed import Feed, FeedEntry


ALL = ['create_app']
main_blueprint = Blueprint('main', __name__)
blueprints = (main_blueprint, user_blueprint)

@main_blueprint.route('/')
def index():
    if current_user.is_authenticated:
        entries = FeedEntry.query.join(Feed).filter_by(user_id=current_user.get_id()).all()
    else:
        entries = []
    return render_template('index.html', entries=entries)

def create_app(app_name=None):
    if app_name is None:
        app_name = DefaultConfig.PROJECT
    app = Flask(app_name)
    app.config.from_object(DefaultConfig)
    login_manager.login_view = 'user.login'
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    db.init_app(app)
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)
    login_manager.init_app(app)
    return app
