# -*- coding: utf-8 -*-
from .client import LINE
from threading import Thread
from types import *
from functools import wraps
import traceback
import logging

log = logging.getLogger(__name__)

class OEPoll(object):
	def __init__(self, client):
		if not isinstance(client, LINE):
			raise Exception('You need to set LINE instance to initialize OEPoll')
		
		self.client: LINE = client
		self.Opinterrupt: list = []
		self.add_command: list = []     
        
	def fetchOps(self, revision: int, count: int = 1):
	    return self.client.poll.fetchOperations(revision, count)
          
	def hooks(self,
	                types: int ,
	                func: LambdaType = None,
	                command: list or str = [],
	                prefix: list or str = ["."],
	                at: list = ["group"],
	                sensitive: bool = True,
	                **kwgs
	                ) -> callable:
		"""
		Use this method to wrap your function as decorator
		
		Attribute:
		types: <class int> value from OpType see akad.ttypes.OpType for detail
		func: <class lambda> include lambda method to register Anonymous function
		command: <class str or list> pass a list or string to command which will execute
		prefix: <class str or list> pass a list or string to set a prefix for command
		at: <class list> pass a one or two point for command will be execute 'any' for both
		sensitive: <class bool> pass True to conver to lower case 		
 		"""
		def decorator(function):
			@wraps(function)
			def _wrap(self, *args, **kwargs):
				func(*args, **kwargs)
				return True
			data = {
				function:{
					"func":func,
					"cmd":command,
					"prefix":prefix,
					"at":at,
					"sensitive":sensitive,
					**kwgs
				}	
			}
			self.add_command.append(data)
			return _wrap,self.Opinterrupt.append({types:function}),True
		return decorator
	
	def _exec(self, ops, func):
		gcheck = False
		pcheck = False
		try:
			msg = ops.message if ops.message else ops
			for i in range(len(self.add_command)):				
				if func in self.add_command[i] :
					if self.add_command[i][func]:
						self.do_job(op_type=ops.type, ops=ops,fuc=func,count=i)
					elif self.add_command[i][func]['func'] != None and self.add_command[i][func]['func'](msg):			
						self.do_job(op_type=ops.type, ops=ops,fuc=func,count=i)
					else:
						key = self.add_command[i][func]
						if key["at"][0] == "group" and msg.toType == 2:gcheck =True
						if key["at"][0] == "private" and msg.toType == 0:gcheck =True
						if key["at"][0] == "any" and (msg.toType == 0 or 2):gcheck = True
						text = msg.text if not key["sensitive"] else msg.text.lower() if msg.text != None else msg
						if key["prefix"]:
							for p in key["prefix"]:
								if text in [(p+x) for x in key["cmd"]]:
									pcheck = True
						else:
							if text in key["cmd"]:
								pcheck = True
					if gcheck and pcheck:
						self.do_job(op_type=ops.type, ops=ops,fuc=func,count=i)				
		except Exception:	
			log.warn(traceback.format_exc())
	
	def do_job(self,ops, op_type,fuc,count):
		try:
			th = Thread(target=self.Opinterrupt[count][op_type],args=(self.client,ops))
			th.start()
		except:
			log.error(traceback.format_exc())
			
	def setRevision(self, revision):
		self.client.revision = max(revision, self.client.revision)
	
	def trace(self):
		try:
			ops = self.fetchOps(self.client.revision)
			for op in ops:
				if self.add_command:
					for i in range(len(self.Opinterrupt)):
						if list(self.Opinterrupt[i].values())[0] in self.add_command[i]:
							if op.type in self.Opinterrupt[i].keys():
								self._exec(op, self.Opinterrupt[i][op.type])
							self.setRevision(op.revision)
		except EOFError:
			pass
		except UnboundLocalError:
			pass
		except Exception:
			log.error(traceback.format_exc())         