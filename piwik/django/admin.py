# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models
from django.forms.fields import Select
from django import forms

from piwik import PiwikAPI
from piwik.django.models import PiwikSite

from django.conf import settings

class PiwikWidget(Select):
    def getPiwikSites(self):
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
        piwik = PiwikAPI(url, token)
        sites = piwik.getAllSites()
        choices = []
        for index in sites:
            id = int(index[0])
            site = piwik.getSiteFromId(id)
            choices.append((id, '%d - %s' % (id, site[0]["name"])))
        return tuple(choices)
    def render(self, name, value, attrs=None, choices=()):
        return super(PiwikWidget, self).render(name, value, attrs=attrs, choices=self.getPiwikSites())

class PiwikSiteForm(forms.ModelForm):
    id_site = forms.IntegerField(widget=PiwikWidget())
    class Meta:
        model = PiwikSite

class PiwikSitesAdmin(admin.ModelAdmin):
    form = PiwikSiteForm
    list_display = ('id_site', 'site')
    
admin.site.register(PiwikSite, PiwikSitesAdmin)
