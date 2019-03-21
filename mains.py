from linepy import OpType, OEPoll, LINE
from linepy.talk import Talk
from typing import Union
import threading

class MainBots(object):
	def __init__(self,
					token: str = None,
					email: str = None,
					passwd: str = None,
					):
		self.message_handlers: Union[list] = []
		self.list_bots: Union[list] = []
		
		if token and not passwd:
			self.line = LINE(token)
		if email and passwd:
			self.line = LINE(email, passwd)
		if not (token or email and passwd):
			self.line = LINE()
		
		self.poll = OEPoll(self.line)
		
		
	def run(self, handler: Union[dict, set]) -> dict:
		self.poll.addOpInterruptWithDict(handler)
		while True:
			self.poll.trace()
