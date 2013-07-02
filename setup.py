# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

project = "rssreader"

with open('requirements.txt') as f:
    install_requires = [x.strip() for x in f.readlines() if x.strip()]

setup(
        name=project,
        version='0.1',
        description='rss reader',
        author='Artem Volkhin',
        author_email='artem@volkhin.com',
        packages=find_packages(),
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
