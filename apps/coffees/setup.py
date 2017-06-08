# coding: utf-8
from __future__ import unicode_literals

import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='laboite.apps.coffees',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    license='AGPL v3',
    description='Displays the number of coffees you take today',
    long_description=README,
    url='laboite.cc',
    author='Baptiste Gaultier',
    author_email='baptiste@laboite.cc',
    namespace_packages=('laboite', 'laboite.apps',),
    classifiers=(
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ),
    zip_safe=False
)
