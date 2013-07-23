#-*- coding: utf-8 -*-
from flask import Blueprint, request, abort, json
from flask.ext.login import current_user
from flask.views import MethodView

from ..tools import add_feed_to_update_queue, subscribe_to_url, import_opml, fetch_feeds
from ..extensions import api_login_required
from ..database import db
from .models import Feed, FeedEntry


feed_blueprint = Blueprint('feeds', __name__)

class EntriesView(MethodView):
    def get(self, entry_id):
        query = FeedEntry.query.join(Feed).filter(Feed.user_id==current_user.get_id())
        if entry_id is not None:
            query = query.filter(FeedEntry.id==entry_id)
        feed_id = request.args.get('feed_id', None)
        if feed_id:
            query = query.filter(Feed.id==feed_id)
        show_read = current_user.show_read
        # show_read = json.loads(request.args.get('show_read', 'false'))
        if not show_read:
            query = query.filter(FeedEntry.read==False)
        starred_only = json.loads(request.args.get('starred_only', 'false'))
        if starred_only:
            query = query.filter(FeedEntry.starred==True)
        query = query.order_by(FeedEntry.created_at.desc())
        entries = query.all()
        return json.dumps(entries)

    def post(self):
        pass

    def put(self, entry_id):
        received_obj = json.loads(request.data)
        FeedEntry.query.filter_by(id=entry_id).update(received_obj)
        db.session.commit()
        return json.dumps(FeedEntry.query.get(entry_id))

    def delete(self, entry_id):
        FeedEntry.query.filter_by(id=entry_id).delete()
        db.session.commit()
        return '{}'

entries_view = api_login_required(EntriesView.as_view('entries_api1'))
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
        data = json.loads(request.data)
        url = data['url']
        feed = subscribe_to_url(url, current_user.get_id())
        if feed:
            add_feed_to_update_queue(feed)
        return json.dumps(feed)

    def put(self, feed_id):
        pass

    def delete(self, feed_id):
        Feed.query.filter_by(id=feed_id).delete()
        db.session.commit()
        return '{}'

feeds_view = api_login_required(FeedsView.as_view('feeds_api1'))
feed_blueprint.add_url_rule('/api/1/feeds', view_func=feeds_view,
        defaults={'feed_id': None}, methods=['GET',])
feed_blueprint.add_url_rule('/api/1/feeds', view_func=feeds_view,
        methods=['POST',])
feed_blueprint.add_url_rule('/api/1/feeds/<int:feed_id>', view_func=feeds_view,
        methods=['GET', 'PUT', 'DELETE',])

@feed_blueprint.route('/update_feeds')
@api_login_required
def update_feeds():
    fetch_feeds(current_user.get_id())
    return '{}'

@feed_blueprint.route('/upload_opml', methods=['POST'])
@api_login_required
def upload_opml():
    opml_file = request.files['opml']
    content = opml_file.read()
    import_opml(current_user.get_id(), data=content)
    return '{}'
