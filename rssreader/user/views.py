#-*- coding: utf-8 -*-
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask.ext.login import login_user, logout_user, current_user

from .forms import LoginForm
from .models import User


user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(current_user=current_user)
    if request.method == 'POST' and form.validate_on_submit():
        user, authenticated = User.authenticate(form.login.data,
                form.password.data)
        if user and authenticated:
            flash('Authenticated as {}'.format(user.login))
            login_user(user)
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('Invalid login', 'error')
    return render_template('login.html', form=form)

@user_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
