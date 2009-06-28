# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site
from django.conf import settings

import xml.sax.saxutils as saxutils 

from piwik.django.models import PiwikSite
from piwik import PiwikAPI

def piwik_processor(request):
    current_site = Site.objects.get_current()
    id_piwik = PiwikSite.objects.filter(site=current_site.id)
    piwik = PiwikAPI(settings.PIWIK_URL, settings.PIWIK_TOKEN)
    return {'piwik_tag' : saxutils.unescape(piwik.getJavascriptTag(id_piwik[0].id_site))}
