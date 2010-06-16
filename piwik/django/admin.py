# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models
from django.forms.fields import Select
from django import forms

from piwik import PiwikAPI
from piwik.django.models import PiwikSite

from django.conf import settings

from django.http import HttpResponse

from django.utils.functional import update_wrapper

def get_piwik_settings():
    try:
        url = settings.PIWIK_URL
    except AttributeError:
        from django.core.exceptions import ImproperlyConfigured
        raise ImproperlyConfigured("please set PIWIK_URL in your settings.")

    try:
        token = settings.PIWIK_TOKEN
    except AttributeError:
        from django.core.exceptions import ImproperlyConfigured
        raise ImproperlyConfigured("please set PIWIK_TOKEN in your settings.")
    return [url, token]

class PiwikWidget(Select):
    def getPiwikSites(self):
        [url, token] = get_piwik_settings()
        piwik = PiwikAPI(url, token)
        sites = piwik.getAllSites()
        choices = []
        for site in sites:
            site_id = int(site["idsite"])
            choices.append((site_id, '%d - %s' % (site_id, site["name"])))
        return tuple(choices)
    def render(self, name, value, attrs=None, choices=()):
        return super(PiwikWidget, self).render(name, value, attrs=attrs, choices=self.getPiwikSites())

class PiwikSiteForm(forms.ModelForm):
    id_site = forms.IntegerField(widget=PiwikWidget())
    class Meta:
        model = PiwikSite

class PiwikSitesAdmin(admin.ModelAdmin):
    form = PiwikSiteForm
    list_display = ('id_site', 'site', 'view_stats')
    
    def view_stats(self, site):
        from django.core.urlresolvers import reverse
        link = reverse('admin:admin_piwik_stats', kwargs={'id_site':site.id_site})
        return '<a href="%s">Stats</a>' % link;

    view_stats.allow_tags = True

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url
        
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)
        
        urls = patterns('',
            url(r'^(?P<id_site>[\d]+)/stats/$', wrap(self.stats), name='admin_piwik_stats'),
        )
        return urls + super(PiwikSitesAdmin, self).get_urls()

    def stats(self, request, id_site=None):
        [url, token] = get_piwik_settings()
        piwik = PiwikAPI(url, token)
        visits = piwik.call('VisitsSummary.get', params={'idSite': id_site,
                                                         'period': 'day',
                                                         'date': 'yesterday'}, format='Html')
        return HttpResponse(visits)
        
admin.site.register(PiwikSite, PiwikSitesAdmin)
