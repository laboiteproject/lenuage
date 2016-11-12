# coding: utf-8

import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='laboite.apps.bikes',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='AGPL v3',
    description='Bikes availability in your nearest stations in Rennes and Paris',
    long_description=README,
    url='https://www.laboite.cc/',
    author='LaBoîteProject team',
    author_email='support@laboite.cc',
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
)
