# -*- coding: utf-8 -*-
import unittest
from minimock import mock, restore, Mock
import httplib

from piwik import PiwikAPI

class testPiwikAPI(unittest.TestCase):
    def setUp(self):
        conn = Mock('httplib.HTTPConnection')
        mock('httplib.HTTPConnection', mock_obj=conn)
        conn.mock_returns = conn        
        self.conn = conn
        self.piwik = PiwikAPI('http://exemple.org/', '123')
        
    def setResponse(self, status, headers, body):
         mock_response = Mock('httplib.httpresponse')
         mock_response.status = int(status.split()[0])
         mock_response.reason = status.split(None, 1)[1]
         mock_response.read.mock_returns = body
         mock_response.getheader.mock_returns_func = headers.get
         mock_response.msg.headers = [
             '%s: %s' % (name, value) for name, value in headers.items()]
         self.conn.getresponse.mock_returns = mock_response

    def testGetAllSites(self):
        self.setResponse("200 OK", {}, "[[1]]")
        self.assertEquals([[1]], self.piwik.getSiteFromId(2))
