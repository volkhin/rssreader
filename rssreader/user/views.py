#-*- coding: utf-8 -*-
from flask import Blueprint, request, render_template, flash, redirect, url_for, json
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.views import MethodView

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


class SettingsView(MethodView):
    def get(self):
        return json.dumps(current_user)

    def put(self):
        received_obj = json.loads(request.data)
        User.query.filter_by(id=current_user.id).update(received_obj)
        db.session.commit()
        return json.dumps(received_obj)


settings_view = login_required(SettingsView.as_view('settings_api1'))
user_blueprint.add_url_rule('/api/1/settings', view_func=settings_view,
        methods=['GET', 'PUT'])


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
