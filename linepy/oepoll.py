# -*- coding: utf-8 -*-
from akad.ttypes import TalkException, ShouldSyncException
from .client import LINE
from threading import Thread
from types import *

import os, sys, time, traceback

class OEPoll(object):
    OpInterrupt = {}
    client = None
    __squareSubId = {}
    __squareSyncToken = {}

    def __init__(self, client):
        if type(client) is not LINE:
            raise Exception('You need to set LINE instance to initialize OEPoll')
        self.client = client
        self.threads = []
    
    def __fetchOperation(self, revision, count=1):
        return self.client.poll.fetchOperations(revision, count)
        
    def __execute(self, op, threading):
        try:
            if threading:
                _td = Thread(target=self.OpInterrupt[op.type], args=(self.client,op))
                _td.start()
            else:
                self.OpInterrupt[op.type](op)
        except Exception as e:
            self.client.log(e)

    def addOpInterruptWithDict(self, OpInterruptDict):
        self.OpInterrupt.update(OpInterruptDict)

    def addOpInterrupt(self, OperationType, DisposeFunc):
        self.OpInterrupt[OperationType] = DisposeFunc
    
    def setRevision(self, revision):
        self.client.revision = max(revision, self.client.revision)

    def singleTrace(self, count=1, fetchOperations=None):
        if not fetchOperations:
            fetchOperations = self.client.fetchOperation
        try:
            operations = fetchOperations(self.client.revision, count=count)
        except KeyboardInterrupt:
            sys.exit()
        except ShouldSyncException:
            self.setRevision(self.client.poll.getLastOpRevision())
            return []
        except:
            return []

        if operations is None:
            return []
        else:
            return operations

    def message_handler(self, type):
    	def decorator(func):
    		def wraper(*arg, **kwg):
    			func(*arg, **kwg)
    		return wraper, self.addOpInterruptWithDict({type:func})
    	return decorator
    
    def untrace(self, threads=True): 	
    	try:    		    		
    		ops = self.__fetchOperation(self.client.revision)
    	except:
    		print(traceback.format_exc())
    	
    	for op in ops:
    		
    		if op.type in self.OpInterrupt.keys():
    			self.__execute(op, threads)
    		self.setRevision(op.revision)
	    
    def run(self):
    	while True:
    		self.untrace()

    def trace(self, threading=True, fetchOperations=None):
        if not fetchOperations:
            fetchOperations = self.client.fetchOperation
        try:
            operations = fetchOperations(self.client.revision)
        except KeyboardInterrupt:
            sys.exit()
        except ShouldSyncException:
            self.setRevision(self.client.poll.getLastOpRevision())
            return
        except:
            return
        
        for op in operations:
            if op.type in self.OpInterrupt.keys():
                self.__execute(op, threading)
            self.setRevision(op.revision)
        

    def singleFetchSquareChat(self, squareChatMid, limit=1):
        if squareChatMid not in self.__squareSubId:
            self.__squareSubId[squareChatMid] = 0
        if squareChatMid not in self.__squareSyncToken:
            self.__squareSyncToken[squareChatMid] = ''
        
        sqcEvents = self.client.fetchSquareChatEvents(squareChatMid, subscriptionId=self.__squareSubId[squareChatMid], syncToken=self.__squareSyncToken[squareChatMid], limit=limit, direction=1)
        self.__squareSubId[squareChatMid] = sqcEvents.subscription
        self.__squareSyncToken[squareChatMid] = sqcEvents.syncToken

        return sqcEvents.events
