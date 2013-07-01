#!/usr/bin/env python
#-*- coding: utf-8 -*-
from flask import Flask, render_template, Blueprint, request, flash, redirect, url_for
from flask.ext.login import login_required, login_user, logout_user

from .config import DefaultConfig
from .extensions import db, login_manager
from .models import FeedEntry, User
from .forms import LoginForm


# ALL = ['create_app']
main_blueprint = Blueprint('main', __name__)
blueprints = (main_blueprint,)

@main_blueprint.route('/')
@login_required
def index():
    entries = FeedEntry.query.all()
    return render_template('index.html', entries=entries)
    output = '<br/>'.join(entry.title for entry in entries)
    return output

@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user, authenticated = User.authenticate(form.login.data,
                form.password.data)
        if user and authenticated:
            flash('Authenticated as {}'.format(user.login))
            login_user(user)
        else:
            flash('Invalid login', 'error')
        return redirect(url_for('.index'))
    return render_template('login.html', form=form)

@main_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('.login'))

def create_app(app_name=None):
    if app_name is None:
        app_name = DefaultConfig.PROJECT
    app = Flask(app_name)
    app.config.from_object(DefaultConfig)
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    db.init_app(app)
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)
    login_manager.init_app(app)
    return app
