# -*- coding: utf-8 -*-
from .transport import THttpClient
from thrift.protocol import TCompactProtocol
from akad import AuthService, TalkService, ChannelService, CallService,  ShopService

class Session:

    def __init__(self, url, headers, path='', customThrift=True):
        self.host = url + path
        self.headers = headers
        self.customThrift = customThrift

    def Auth(self, isopen=True):
        transport = THttpClient(self.host, customThrift=self.customThrift)
        transport.setCustomHeaders(self.headers)
        protocol = TCompactProtocol.TCompactProtocol(transport)
        _auth  = AuthService.Client(protocol)

        if isopen:
            transport.open()

        return _auth

    def Talk(self, isopen=True):
        transport = THttpClient(self.host, customThrift=self.customThrift)
        transport.setCustomHeaders(self.headers)
        protocol = TCompactProtocol.TCompactProtocol(transport)
        _talk  = TalkService.Client(protocol)

        if isopen:
            transport.open()

        return _talk

    def Channel(self, isopen=True):
        transport = THttpClient(self.host, customThrift=self.customThrift)
        transport.setCustomHeaders(self.headers)
        protocol = TCompactProtocol.TCompactProtocol(transport)
        _channel  = ChannelService.Client(protocol)

        if isopen:
            self.transport.open()

        return self._channel

    def Call(self, isopen=True):
        transport = THttpClient(self.host, customThrift=self.customThrift)
        transport.setCustomHeaders(self.headers)
        protocol = TCompactProtocol.TCompactProtocol(transport)
        _call  = CallService.Client(protocol)

        if isopen:
            transport.open()

        return _call

    def Shop(self, isopen=True):
        transport = THttpClient(self.host, customThrift=self.customThrift)
        transport.setCustomHeaders(self.headers)
        protocol = TCompactProtocol.TCompactProtocol(transport)
        self_shop  = ShopService.Client(protocol)

        if isopen:
            transport.open()

        return _shop
