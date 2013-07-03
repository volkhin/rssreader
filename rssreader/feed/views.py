#-*- coding: utf-8 -*-
from flask import Blueprint, render_template, request
from flask.ext.login import current_user, login_required
from werkzeug.datastructures import CombinedMultiDict

from .models import Feed, FeedEntry


feed_blueprint = Blueprint('feeds', __name__)

def get_global_data():
    d = dict()
    d['feeds'] = Feed.query.filter_by(user_id=current_user.get_id()).all()
    return d

@feed_blueprint.route('/feeds')
@feed_blueprint.route('/feeds/<int:feed_id>', endpoint='single_feed')
@login_required
def list_entries(**kws):
    if current_user.is_authenticated:
        query = FeedEntry.query.join(Feed).filter(Feed.user_id==current_user.get_id())
        query = query.filter(FeedEntry.read==False)
        if 'feed_id' in kws:
            query = query.filter(Feed.id==kws['feed_id'])
        query = query.order_by(FeedEntry.created_at.desc())
        entries = query.all()
    else:
        entries = []
    return render_template('index.html', entries=entries, **get_global_data())

@feed_blueprint.route('/entry/<int:entry_id>', endpoint='entry')
@feed_blueprint.route('/mark_entry_read', endpoint='mark_entry_read',
        methods=['POST'], defaults={'action': 'read'})
@feed_blueprint.route('/mark_entry_unread', endpoint='mark_entry_unread',
        methods=['POST'], defaults={'action': 'unread'})
@login_required
def single_entry(**kws):
    data = CombinedMultiDict((request.values, kws))
    entry = FeedEntry.query.get(data['entry_id'])
    if 'action' in data:
        action = data['action']
        if action == 'read':
            entry.mark_read()
        elif action == 'unread':
            entry.mark_unread()
    return render_template('index.html', entries=[entry], **get_global_data())
