# -*- coding: utf-8 -*-
import urllib
import httplib
import urlparse
import simplejson

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
        if data is not None and format == 'json':
            return simplejson.loads(data)
        return data

    def getAllSites(self):
        return self.call('SitesManager.getSitesWithAtLeastViewAccess')

    def getSiteFromId(self, id):
        return self.call('SitesManager.getSiteFromId', params = {'idSite' : id})

    def getJavascriptTag(self, id, piwikUrl = '', actionName = ''):
        result = self.call('SitesManager.getJavascriptTag', params = {'idSite' : id})
        if result:
            return result['value']
        return None
