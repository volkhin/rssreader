#-*- coding: utf-8 -*-
import os

__all__ = ['config']

class BaseConfig(object):
    PROJECT = 'rssreader'
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    DEBUG = False
    TESTING = False
    # SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = 'sdfs3qere75tgubhhj'
    REDIS_CONNECTION_OPTIONS = {}

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost:5432/rssreader'

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///production.db'

class TestingConfig(BaseConfig):
    # SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TESTING = True
    CSRF_ENABLED = False

class Config(object):
    def __init__(self):
        self.config = None
        self.all_configs = {
                'development': DevelopmentConfig,
                'production': ProductionConfig,
                'testing': TestingConfig
                }

    def set(self, config):
        if config not in self.all_configs.keys():
            raise AttributeError('Unknown config: {}'.format(config))
        self.config = self.all_configs[config]
        
    def __dir__(self):
        if self.config is None:
            raise RuntimeError('Config is not set')
        return dir(self.config)

    def __getattr__(self, name):
        if self.config is None:
            raise RuntimeError('Config is not set')
        return getattr(self.config, name)

config = Config()
config.set('development')
