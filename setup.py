# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='piwik',
    version='0.3',
    
    description='Access Piwik in python',
    long_description=open('README.rst').read(),

    author='François de Metz',
    author_email='francois@2metz.fr',
    url='http://forge.2metz.fr/p/python-piwik/',
    
    packages = find_packages(),

    
    install_requires = [
        'simplejson'
    ],
    extras_require = {
        'django':  ["Django>=1.0"],
    },

    classifiers = [
        'Framework :: Django',
        'Operating System :: OS Independent',
        'Topic :: Internet :: Log Analysis',
        'License :: OSI Approved :: BSD License',
    ],
)
