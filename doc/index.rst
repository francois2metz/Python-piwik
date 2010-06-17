.. Python Piwik documentation master file, created by
   sphinx-quickstart on Thu Jun 17 03:02:40 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

========================================
Python Piwik documentation!
========================================

Install
=======

Source
------

Source available on GitHub.

.. code-block:: bash

   $> git clone git://github.com/francois2metz/Python-piwik.git


Via pip
-------

.. code-block:: bash

   $> pip install piwik


Django app
==========

Python piwik also contain an django application that can be easily integrated on your Django project.

Add piwik.django to your installed apps settings, add middleware piwik.django.middleware.PiwikMiddleware, and add PIWIK_URL and PIWIK_TOKEN.

* PIWIK_URL is Url of you Piwik installation with / at end
* PIWIK_TOKEN found token on your piwik installation -> API -> token_auth also available Settings -> Users 

settings.py:

.. code-block:: python

   INSTALLED_APPS = (
       ...,
       'django.contrib.sites', # piwik django dependency
       'piwik.django',
       ...,
   )
   MIDDLEWARE_CLASSES = (
       ...,
       'piwik.django.middleware.PiwikMiddleware',
        ...,
   )
   PIWIK_TOKEN = 'your token'
   PIWIK_URL = 'http://piwik.example.org/'

.. code-block:: bash
   
   $> ./manage.py syncdb

Go to your admin site and rely piwik sites with django site.

For add piwik tag on you website, simply use RequestContext.

.. code-block:: python

   from django.template import RequestContext
   def index(request):
       return render_to_response("index.html", RequestContext(request, {}))

Add this in your template::

   {% autoescape off %}
   {{ piwik_tag }}
   {% endautoescape %} 



Indices and tables
==================

* :ref:`search`

