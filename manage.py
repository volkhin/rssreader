#!/usr/bin/env python
#-*- coding: utf-8 -*-
import rssreader.tools
from flask.ext.script import Manager
from rssreader import create_app
from rssreader.config import config
from rssreader import db
from rssreader.user.models import User


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

@manager.command
def fetch_feeds():
    rssreader.tools.fetch_feeds()


if __name__ == "__main__":
    manager.run()
