# -*- coding: utf-8 -*-

from setuptools import setup

project = "rssreader"

with open('requirements.txt') as f:
    install_requires = [x.strip() for x in f.readlines()]
    install_requires = [x for x in install_requires if x]

setup(
        name=project,
        version='0.1',
        description='rss reader',
        author='Artem Volkhin',
        author_email='artem@volkhin.com',
        packages=["rssreader"],
        include_package_data=True,
        zip_safe=False,
        install_requires=install_requires,
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
