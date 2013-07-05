#-*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, abort
from flask.ext.login import current_user, login_required
from werkzeug.datastructures import CombinedMultiDict

from .models import Feed, FeedEntry
from .forms import SubscribeForm
from ..database import db


feed_blueprint = Blueprint('feeds', __name__)

def get_global_data():
    d = dict()
    d['feeds'] = Feed.query.filter_by(user_id=current_user.get_id()).all()
    d['subscribe_form'] = SubscribeForm()
    return d

@feed_blueprint.route('/feeds')
@feed_blueprint.route('/feeds/<int:feed_id>', endpoint='single_feed')
@login_required
def list_entries(**kws):
    data = CombinedMultiDict((request.values, kws))
    if current_user.is_authenticated:
        # TODO: query(Feed, FeedEntry).join('feed_id').filter_by(user_id) ?
        query = FeedEntry.query.join(Feed).filter(Feed.user_id==current_user.get_id())
        if 'feed_id' in data:
            query = query.filter(Feed.id==data['feed_id'])
        if not current_user.show_read:
            query = query.filter(FeedEntry.read==False)
        if data.get('starred', False):
            query = query.filter(FeedEntry.starred==True)
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
@feed_blueprint.route('/mark_entry_starred', endpoint='mark_entry_starred',
        methods=['POST'], defaults={'action': 'star'})
@feed_blueprint.route('/mark_entry_unstarred', endpoint='mark_entry_unstarred',
        methods=['POST'], defaults={'action': 'unstar'})
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
        elif action == 'star':
            entry.mark_star()
        elif action == 'unstar':
            entry.mark_unstar()
    return render_template('index.html', entries=[entry], **get_global_data())

@feed_blueprint.route('/subscribe', methods=['POST'])
@login_required
def subscribe():
    form = SubscribeForm()
    if form.validate_on_submit():
        rss_url = request.form['url']
        feed = Feed.query.filter_by(url=rss_url, user_id=current_user.id).first()
        if feed is None:
            feed = Feed(rss_url, current_user.id)
            db.session.add(feed)
            db.session.commit()
            feed.update()
            return "OK"
        else:
            return "Feed already exists"
    abort(400)
