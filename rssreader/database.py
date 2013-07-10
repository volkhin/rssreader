#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from .config import config


class DatabaseAbstraction(object):
    def __init__(self):
        self.Model = declarative_base() 
        self.Model.is_db_model = True
        for module in sqlalchemy, sqlalchemy.orm:
            for key in module.__all__:
                if not hasattr(self, key):
                    setattr(self, key, getattr(module, key))

    @property
    def metadata(self):
        return self.Model.metadata

    def init(self):
        engine_options = {'convert_unicode': True, 'echo': False}
        self.engine = create_engine(config.SQLALCHEMY_DATABASE_URI, **engine_options)
        session_options = {
                'autocommit': False,
                'autoflush': True,
                'bind': self.engine
                }
        self.session = scoped_session(sessionmaker(**session_options))
        self.Model.query = self.session.query_property()

    def create_all(self):
        self.metadata.create_all(bind=self.engine)

    def drop_all(self):
        self.metadata.drop_all(bind=self.engine)

    def teardown(self):
        self.session.remove()


db = DatabaseAbstraction()
