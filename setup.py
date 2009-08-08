# -*- coding: utf-8 -*-
try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='piwik',
    version='0.2',
    
    description='Access Piwik in python',
    
    author='François de Metz',
    author_email='francois@2metz.fr',
    url='http://forge.2metz.fr/p/python-piwik/',
    
    packages = find_packages(),

    require = {
        'simplejson'
    },
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
