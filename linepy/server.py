# -*- coding: utf-8 -*-
from .config import Config
import json, requests, urllib
from hyper.contrib import HTTPAdapter

class Server(Config):
	def __init__(self, host=None, appType=None):
		self._session = requests.Session()
		self._session.mount("https://", HTTPAdapter())
		self._session.mount("http://", HTTPAdapter())
		self.timelineHeaders = {}
		self.Headers = {}
		Config.__init__(self, appType)

	def parseUrl(self, path):
		return self.LINE_HOST_DOMAIN + path

	def urlEncode(self, url, path, params=[]):
		return url + path + '?' + urllib.parse.urlencode(params)

	def getJson(self, url, allowHeader=False):		
		if not allowHeader:
			res = self._session.get(url=url, timeout=None)
		else:
			res = self._session.get(url=url, headers=self.Headers, timeout=None)
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
		return self._session.options(url, headers=headers, data=data)

	def postContent(self, url, data=None, headers=None, files=None):
		if headers is None:
			headers=self.Headers	
		return self._session.post(url, headers=headers, data=data, files=files)
		
	def getContent(self, url, headers=None):	
		if headers is None:
			headers=self.Headers
		return self._session.get(url=url, headers=headers, stream=True)
		
	def deleteContent(self, url, data=None, headers=None):
		if headers is None:
			headers=self.Headers
		return self._session.delete(url=url, headers=headers, data=data)

	def putContent(self, url, data=None, headers=None):
		if headers is None:
			headers=self.Headers
		return self._session.put(url=url, headers=headers, data=data)
