#-*- coding: utf-8 -*-
from flask import Blueprint, request, render_template, flash, redirect, url_for, json
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.views import MethodView

from .forms import LoginForm
from .models import User
from ..database import db
from ..extensions import api_login_required


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


class SettingsView(MethodView):
    def get(self):
        return json.dumps(current_user)

    def put(self):
        received_obj = json.loads(request.data)
        User.query.filter_by(id=current_user.get_id()).update(received_obj)
        db.session.commit()
        return json.dumps(User.query.get(current_user.get_id()))


settings_view = api_login_required(SettingsView.as_view('settings_api1'))
user_blueprint.add_url_rule('/api/1/settings', view_func=settings_view,
        methods=['GET', 'PUT'])
