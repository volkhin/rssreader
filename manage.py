#!/usr/bin/env python
#-*- coding: utf-8 -*-
from flask.ext.script import Manager

import rssreader.tools
from rssreader.user.models import User
from rssreader import create_app
from rssreader.extensions import db


app = create_app()
manager = Manager(app)

@manager.command
def initdb():
    db.drop_all()
    db.create_all()
    admin = User('admin', 'admin')
    user2 = User('user2', 'pass')
    db.session.add(admin)
    db.session.add(user2)
    db.session.commit()
    rssreader.tools.import_ompl()
    rssreader.tools.fetch_feeds()

@manager.command
def fetch_feeds():
    rssreader.tools.fetch_feeds()


if __name__ == "__main__":
    manager.run()
