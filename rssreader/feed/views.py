#-*- coding: utf-8 -*-
from flask import Blueprint, render_template
from flask.ext.login import current_user

from .models import Feed, FeedEntry


feed_blueprint = Blueprint('feeds', __name__)

def get_global_data():
    d = dict()
    d['feeds'] = Feed.query.filter_by(user_id=current_user.get_id()).all()
    return d

@feed_blueprint.route('/feeds')
def index():
    if current_user.is_authenticated:
        entries = (FeedEntry.query.join(Feed).
                filter(FeedEntry.read==False, Feed.user_id==current_user.get_id()).
                order_by(FeedEntry.created_at.desc()).
                all())
    else:
        entries = []
    return render_template('index.html', entries=entries, **get_global_data())

@feed_blueprint.route('/feeds/<int:feed_id>')
def single_feed(feed_id):
    if current_user.is_authenticated:
        entries = (FeedEntry.query.join(Feed).
                filter(FeedEntry.read==False, Feed.id==feed_id, Feed.user_id==current_user.get_id()).
                order_by(FeedEntry.created_at.desc()).
                all())
    else:
        entries = []
    return render_template('index.html', entries=entries, **get_global_data())
