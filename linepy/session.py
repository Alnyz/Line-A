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
        auth_transport = THttpClient(self.host, customThrift=self.customThrift)
        auth_transport.setCustomHeaders(self.headers)
        auth_protocol = TCompactProtocol.TCompactProtocol(auth_transport)
        _auth  = AuthService.Client(auth_protocol)

        if isopen:
            auth_transport.open()

        return _auth

    def Talk(self, isopen=True):
        talk_transport = THttpClient(self.host, customThrift=self.customThrift)
        talk_transport.setCustomHeaders(self.headers)
        talk_protocol = TCompactProtocol.TCompactProtocol(talk_transport)
        _talk  = TalkService.Client(talk_protocol)

        if isopen:
            talk_transport.open()

        return _talk

    def Channel(self, isopen=True):
        ch_transport = THttpClient(self.host, customThrift=self.customThrift)
        ch_transport.setCustomHeaders(self.headers)
        ch_protocol = TCompactProtocol.TCompactProtocol(ch_transport)
        _channel  = ChannelService.Client(ch_protocol)

        if isopen:
            ch_transport.open()

        return _channel

    def Call(self, isopen=True):
        call_transport = THttpClient(self.host, customThrift=self.customThrift)
        call_transport.setCustomHeaders(self.headers)
        call_protocol = TCompactProtocol.TCompactProtocol(call_transport)
        _call  = CallService.Client(call_protocol)

        if isopen:
            call_transport.open()

        return _call

    def Shop(self, isopen=True):
        shop_transport = THttpClient(self.host, customThrift=self.customThrift)
        shop_transport.setCustomHeaders(self.headers)
        shop_protocol = TCompactProtocol.TCompactProtocol(shop_transport)
        _shop  = ShopService.Client(shop_protocol)

        if isopen:
            shop_transport.open()

        return _shop
