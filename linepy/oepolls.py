# -*- coding: utf-8 -*-
from akad.ttypes import TalkException, ShouldSyncException
from .client import LINE
from threading import Thread
from types import *
from functools import wraps
from itertools import zip_longest
import os, sys, time, traceback

import logging

log = logging.getLogger(__name__)

class OEPolls(object):
	def __init__(self, client):
		if not isinstance(client, LINE):
			raise Exception('You need to set LINE instance to initialize OEPoll')
		
		self.client: LINE = client
		self.Opinterrupt: dict = {}
		self.add_command: dict = {}		
		
	def fetchOps(self, revision: int, count: int = 1):
		return self.client.poll.fetchOperations(revision, count)
			
	def hooks(self,
					types: int,
					commands: str or list = [],
					prefix: list or str = [],
					at: list or str = ["group"],
					sensitive: bool = True
					) -> callable:
		"""
		Crazy thinks! Use this decorator for wrap your functions
		
		Attribute:
		types: type from OpType value see <akad.ttypes.OpType> for detail
		command: list of your command, or pass a string for this one
		prefix: set a list for your prefix command e.g prefix=['.','/'] default []
		at: return True if this command at Group,Private or both set a list of this arg
		sensitive: case sensitive, make your command execute as lower case
		
		:Return: True -> callable
		"""
		def decorator(func):
			@wraps(func)
			def _wrap(self, *arg, **kwg):
				func(*arg, **kwg)
				return True
			data = {				
				func:{
					"cmd":commands,
					"prefix":prefix,
					"sensitive":sensitive,
					"at":at,
				}	
			}
			self.add_command.update(data)
			return _wrap, self.Opinterrupt.update({types:func}),True
		return decorator
	
	def _exec(self, ops, func):
		if ops.type not in [26, 25]:
			self.do_job(op_type=ops.type, ops=ops)
		else:
			try:
				cs = False
				execs = False
				msg = ops.message
				key = self.add_command[func]
				
				if key["prefix"] != []:
					pref = key["prefix"]
				else:
					pref = ""
					
				if key["at"][0].lower() == "group":
					if msg.toType == 2:
						cs = True
				elif key["at"][0].lower() == "private":
					if msg.toType == 0:
						cs = True	
				if key["sensitive"]:
					msg.text = msg.text.lower()
				
				try:
					if any([msg.text.startswith(x) for x in pref]):
						execs = True
					elif msg.text in [(x+k) for x,k in zip_longest(pref, key["cmd"], fill_value="")]:
						execs = True
				except TypeError:
					pass
				except Exception:
					print(log.warn(traceback.format_exc()))
					
				if execs and cs:		
					self.do_job(op_type=ops.type, ops=ops)
			except Exception:
				print(log.warn(traceback.format_exc()))
	
	def do_job(self,ops, op_type):
		try:
			th = Thread(target=self.Opinterrupt[op_type], args=(self.client, ops))
			th.start()
		except:
			print(traceback.format_exc())
			
	def setRevision(self, revision):
		self.client.revision = max(revision, self.client.revision)
        	
	def trace(self):
		try:
			ops = self.fetchOps(self.client.revision)
		except EOFError:
			pass
		except UnboundLocalError:
			pass
		except Exception:
			print(traceback.format_exc())
		
		for op in ops:
			if op.type in self.Opinterrupt.keys():
				self._exec(op, self.Opinterrupt[op.type])			
			self.setRevision(op.revision)
			
			