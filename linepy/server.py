# -*- coding: utf-8 -*-
from .config import Config
import json, requests, urllib
from hyper import HTTPConnection

class Server(Config):
	def __init__(self, host=None, appType=None):
		self.reqs = requests.Session()
		self._session = HTTPConnection(host.replace("https://",""))
		self.timelineHeaders = {}
		self.Headers = {}
		Config.__init__(self, appType)

	def parseUrl(self, path):
		return self.LINE_HOST_DOMAIN + path

	def urlEncode(self, url, path, params=[]):
		return url + path + '?' + urllib.parse.urlencode(params)

	def getJson(self, url, allowHeader=False):		
		if not allowHeader:
			res = self.reqs.get(url, timeout=None)
		else:
			res = self.reqs.get(url, headers=self.Headers, timeout=None)
		return json.loads(res.text)

	def setHeadersWithDict(self, headersDict):
		self.Headers.update(headersDict)

	def setHeaders(self, argument, value):
		self.Headers[argument] = value

	def setTimelineHeadersWithDict(self, headersDict):
		self.timelineHeaders.update(headersDict)

	def setTimelineHeaders(self, argument, value):
		self.timelineHeaders[argument] = value

	def additionalHeaders(self, source, newSource):
		headerList={}
		headerList.update(source)
		headerList.update(newSource)
		return headerList

	def optionsContent(self, url, data=None, headers=None):
		if headers is None:
			headers=self.Headers
		return self.request("OPTIONS", url, headers=headers, data=data)

	def postContent(self, url, data=None, files=None, headers=None):
		if headers is None:
			headers=self.Headers
		return self.request("POST", url, headers=headers, data=data, files=files)

	def getContent(self, url, headers=None):
		if headers is None:
			headers=self.Headers
		return self.request("GET", url, headers=headers)

	def deleteContent(self, url, data=None, headers=None):
		if headers is None:
			headers=self.Headers
		return self.request("DELETE", url, headers=headers, data=data)

	def putContent(self, url, data=None, headers=None):
		if headers is None:
			headers=self.Headers
		return self.request("PUT", url, headers=headers, data=data)

	def request(self,method, url, data=None, headers=None):
		self._session.request(method.upper(), url, body=data, headers=headers)
