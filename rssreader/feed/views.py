#-*- coding: utf-8 -*-
from .forms import SubscribeForm
from flask import Blueprint, request, abort, json
from flask.ext.login import current_user, login_required
from flask.views import MethodView

from ..database import db
from .models import Feed, FeedEntry


feed_blueprint = Blueprint('feeds', __name__)

class EntriesView(MethodView):
    def get(self, entry_id):
        query = FeedEntry.query.join(Feed).filter(Feed.user_id==current_user.get_id())
        # if 'feed_id' in data:
            # query = query.filter(Feed.id==data['feed_id'])
        if entry_id is not None:
            query.filter(FeedEntry.id==entry_id)
        # if not current_user.show_read:
        show_read = json.loads(request.args.get('show_read', 'false'))
        if not show_read:
            query = query.filter(FeedEntry.read==False)
        starred_only = json.loads(request.args.get('starred_only', 'false'))
        if starred_only:
            query = query.filter(FeedEntry.starred==True)
        # query = query.order_by(FeedEntry.created_at.desc())
        entries = query.all()
        return json.dumps(entries)

    def post(self):
        pass

    def put(self, entry_id):
        # entry = FeedEntry.query.get(request.values['entry_id'])
        received_obj = json.loads(request.data)
        FeedEntry.query.filter_by(id=entry_id).update(received_obj)
        db.session.commit()
        return json.dumps(received_obj)

    def delete(self, entry_id):
        pass

entries_view = login_required(EntriesView.as_view('entries_api1'))
feed_blueprint.add_url_rule('/api/1/entries', view_func=entries_view,
        defaults={'entry_id': None}, methods=['GET',])
feed_blueprint.add_url_rule('/api/1/entries', view_func=entries_view,
        methods=['POST',])
feed_blueprint.add_url_rule('/api/1/entries/<int:entry_id>', view_func=entries_view,
        methods=['GET', 'PUT', 'DELETE',])


class FeedsView(MethodView):
    def get(self, feed_id):
        query = Feed.query
        if feed_id is not None:
            query = query.filter_by(id=feed_id)
        feeds = query.all()
        return json.dumps(feeds)

    def post(self):
        pass

    def put(self, feed_id):
        pass

    def delete(self, feed_id):
        pass

feeds_view = login_required(FeedsView.as_view('feeds_api1'))
feed_blueprint.add_url_rule('/api/1/feeds', view_func=feeds_view,
        defaults={'feed_id': None}, methods=['GET',])
feed_blueprint.add_url_rule('/api/1/feeds', view_func=feeds_view,
        methods=['POST',])
feed_blueprint.add_url_rule('/api/1/feeds/<int:feed_id>', view_func=feeds_view,
        methods=['GET', 'PUT', 'DELETE',])


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
