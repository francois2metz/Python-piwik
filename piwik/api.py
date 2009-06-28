# -*- coding: utf-8 -*-
import urllib
import httplib
import urlparse
try:
    import simplejson
except ImportError:
    from django.utils import simplejson

class PiwikAPI:
    def __init__(self, url, token_auth):
        self.url = url
        self.token_auth = token_auth

        (scheme, netloc, path, query, fragment) = urlparse.urlsplit(self.url)
        self.host = netloc
    def call(self, method, params = {}, format = 'json'):
        args = {'module' : 'API',
                'method' : method,
                'format' : format,
                'token_auth' : self.token_auth}
        args.update(params)
        conn = httplib.HTTPConnection(self.host)
        conn.request('GET', u"%s?%s" % (self.url, urllib.urlencode(args)), headers={'User-Agent' : 'Django Piwik'})
        result = conn.getresponse()
        data = None
        if result.status == 200:
            data = result.read()
        conn.close()
        return data
    def getAllSites(self):
        result = self.call('SitesManager.getAllSitesId')
        if result:
            return simplejson.loads(result)
        return None
    def getSiteFromId(self, id):
        result = self.call('SitesManager.getSiteFromId', params = {'idSite' : id})
        if result:
            json = simplejson.loads(result)
            if hasattr(json, 'result'):
                raise json['message']
            return json
        return None
    def getJavascriptTag(self, id, piwikUrl = '', actionName = ''):
        result = self.call('SitesManager.getJavascriptTag', params = {'idSite' : id})
        if result:
            return simplejson.loads(result)['value']
        return None
