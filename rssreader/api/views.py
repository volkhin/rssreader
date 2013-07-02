#-*- coding: utf-8 -*-
from flask import Blueprint, request

from ..extensions import db
from ..feed import FeedEntry


api_blueprint = Blueprint('api', __name__, url_prefix='/api')

@api_blueprint.route('/mark_read', methods=['POST'])
def mark_read():
    entry_id = request.values['entry_id']
    FeedEntry.query.get(entry_id).mark_read()
    db.session.commit() #TODO: do we need it here?
    return "OK"
