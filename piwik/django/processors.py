# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site
from django.conf import settings

import xml.sax.saxutils as saxutils 

from piwik.django.models import PiwikSite
from piwik import PiwikAPI

PIWIK_CACHE = {}

def piwik_processor(request):
    current_site = Site.objects.get_current()
    piwik_site = PiwikSite.objects.filter(site=current_site.id)
    id_piwik = piwik_site[0].id_site
    try:
        javascript = PIWIK_CACHE[id_piwik]
    except KeyError:        
        piwik = PiwikAPI(settings.PIWIK_URL, settings.PIWIK_TOKEN)
        javascript = saxutils.unescape(piwik.getJavascriptTag(id_piwik))
        PIWIK_CACHE[id_piwik] = javascript
    return {'piwik_tag' : javascript}

