# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models
from django.forms.fields import Select
from django import forms
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.functional import update_wrapper

from piwik import PiwikAPI
from piwik.django.models import PiwikSite

from django.conf import settings

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
        link = reverse('admin:admin_piwik_stats', kwargs={'id_site_piwik':site.id_site})
        return '<a href="%s">Stats</a>' % link;

    view_stats.allow_tags = True

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        urls = patterns('',
            url(r'^(?P<id_site_piwik>[\d]+)/stats/$', wrap(self.stats), name='admin_piwik_stats'),
        )
        return urls + super(PiwikSitesAdmin, self).get_urls()

    def call_method_with_metadata(self, piwik, id_site_piwik, period, api_module, api_action):
        data = piwik.call('%s.%s' % (api_module, api_action), params={'idSite': id_site_piwik,
                                                                      'period': period,
                                                                      'date': 'yesterday'}, format='json')
        metadata = piwik.call('API.getMetadata', params={'idSite': id_site_piwik,
                                                         'apiModule': api_module,
                                                         'apiAction': api_action}, format='json')
        return [data, metadata]

    def stats(self, request, id_site_piwik=None):
        [url, token] = get_piwik_settings()
        piwik = PiwikAPI(url, token)
        period = request.GET.get('period', 'day')
        site = PiwikSite.objects.get(id_site=id_site_piwik)
        title = 'Stats: %s' % site.site.name
        [visits, visits_metadata]           = self.call_method_with_metadata(piwik, id_site_piwik, period, 'VisitsSummary', 'get')
        [usercountry, usercountry_metadata] = self.call_method_with_metadata(piwik, id_site_piwik, period, 'UserCountry', 'getCountry')
        [referer, referer_metadata]         = self.call_method_with_metadata(piwik, id_site_piwik, period, 'Referers', 'getRefererType')
        return render_to_response('admin/piwik/stats.html', {'visitssummary': visits,
                                                             'visitssummary_metadata': visits_metadata,
                                                             'usercountry': usercountry,
                                                             'usercountry_metadata': usercountry_metadata,
                                                             'referer' : referer,
                                                             'referer_metadata' : referer_metadata,
                                                             'period': period,
                                                             'title': title,
                                                             'piwik_url': url},
                                  RequestContext(request))

admin.site.register(PiwikSite, PiwikSitesAdmin)
