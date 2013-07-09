#-*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, abort, jsonify, json
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
@feed_blueprint.route('/api/feeds', defaults={'api': True})
@login_required
def list_entries(**kws):
    data = CombinedMultiDict((request.values, kws))
    if current_user.is_authenticated:
        # TODO: query(Feed, FeedEntry).join('feed_id').filter_by(user_id) ?
        query = FeedEntry.query.join(Feed).filter(Feed.user_id==current_user.get_id())
        if 'feed_id' in data:
            query = query.filter(Feed.id==data['feed_id'])
        # if not current_user.show_read:
        show_read = json.loads(data.get('show_read', 'false'))
        if not show_read:
            query = query.filter(FeedEntry.read==False)
        if data.get('starred', False):
            query = query.filter(FeedEntry.starred==True)
        # query = query.order_by(FeedEntry.created_at.desc())
        entries = query.all()
    else:
        entries = []
    if 'api' in data:
        return json.dumps(entries)
    context = get_global_data()
    context['entries'] = entries
    return render_template('index.html', **context)

@feed_blueprint.route('/api/feeds/<int:entry_id>', methods=['GET', 'POST', 'PUT'])
@login_required
def single_entry(**kws):
    data = CombinedMultiDict((request.values, kws))
    entry = FeedEntry.query.get(data['entry_id'])
    if request.method == 'PUT':
        received_obj = json.loads(request.data)
        FeedEntry.query.filter_by(id=received_obj['id']).update(received_obj)
        db.session.commit()
        return json.dumps(entry)
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
