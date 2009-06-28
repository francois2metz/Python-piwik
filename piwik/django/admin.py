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
        piwik = PiwikAPI(settings.PIWIK_URL, settings.PIWIK_TOKEN)
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
    
admin.site.register(PiwikSite, PiwikSitesAdmin)
