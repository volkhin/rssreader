# -*- coding: utf-8 -*-

from setuptools import setup

project = "rssreader"

setup(
        name=project,
        version='0.1',
        description='rss reader',
        author='Artem Volkhin',
        author_email='artem@volkhin.com',
        packages=["rssreader"],
        include_package_data=True,
        zip_safe=False,
        install_requires=[
            'Flask',
            'Flask-SQLAlchemy',
            'Flask-Login',
            'Flask-WTF',
            'Flask-Script',
            'nose',
            'opml',
            'feedparser',
            ],
        classifiers=[
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
            'Topic :: Software Development :: Libraries'
            ]
        )
