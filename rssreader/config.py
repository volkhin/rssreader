#-*- coding: utf-8 -*-
import os


class DefaultConfig(object):
    PROJECT = 'rssreader'
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    DEBUG=True
    # SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SECRET_KEY = 'sdfs3qere75tgubhhj'
