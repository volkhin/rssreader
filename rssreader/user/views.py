#-*- coding: utf-8 -*-
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask.ext.login import login_user, logout_user, current_user, login_required

from .forms import LoginForm
from .models import User
from ..database import db


user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(current_user=current_user)
    if form.validate_on_submit():
        user, authenticated = User.authenticate(form.login.data,
                form.password.data)
        if user and authenticated:
            flash('Authenticated as {}'.format(user.login))
            login_user(user)
            return redirect(request.args.get('next') or url_for('frontend.index'))
        else:
            flash('Invalid login', 'error')
    return render_template('login.html', form=form)

@user_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('frontend.index'))

@user_blueprint.route('/settings/show_read', endpoint='settings_show_read',
        methods=['POST'], defaults={'action': 'show_read'})
@user_blueprint.route('/settings/hide_read', endpoint='settings_hide_read',
        methods=['POST'], defaults={'action': 'hide_read'})
@login_required
def change_settings(**kws):
    if 'action' in kws:
        action = kws['action']
        if action == 'show_read':
            current_user.show_read = True
            db.session.commit()
        elif action == 'hide_read':
            current_user.show_read = False
            db.session.commit()
    return "OK"
