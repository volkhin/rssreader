#!/usr/bin/env python
#-*- coding: utf-8 -*-

from fabric.api import local
project = 'rssreader'

def reset():
    '''
    Reset local env.
    '''
    local('rm -rf *.pyc')
    local('python manage.py initdb')

def setup():
    '''
    Setup virtual env.
    '''
    local('virtualenv env')
    activate_this = 'env/bin/activate_this.py'
    execfile(activate_this, dict(__file__=activate_this))
    local('python setup.py install')
    reset()

def run():
    '''
    Run local debug server.
    '''
    reset()
    local('python manage.py run')
