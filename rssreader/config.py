#-*- coding: utf-8 -*-
import os


class BaseConfig(object):
    PROJECT = 'rssreader'
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    DEBUG = False
    TESTING = False
    # SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = 'sdfs3qere75tgubhhj'

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///production.db'

class TestingConfig(BaseConfig):
    # SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TESTING = True
    CSRF_ENABLED = False

