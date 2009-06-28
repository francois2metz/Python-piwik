# -*- coding: utf-8 -*-
from django.conf import settings

class PiwikMiddleware:
    def process_request(self, request):
        settings.TEMPLATE_CONTEXT_PROCESSORS = settings.TEMPLATE_CONTEXT_PROCESSORS + ('piwik.django.processors.piwik_processor',)
