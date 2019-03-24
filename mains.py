from linepy import OpType, OEPoll, LINE
from linepy.talk import Talk
from akad.ttypes import Message
from bots.plugins.database import DataBase
from bots.plugins.configs import Filters
import traceback, random

class MainBots(object):
	def __init__(self,
					token: str = None,
					email: str = None,
					passwd: str = None,
					):
		self.list_bots: list = []
		if token and not passwd:
			self.line = LINE(token)
		if email and passwd:
			self.line = LINE(email, passwd)
		if not (token or email and passwd):
			self.line = LINE()
		
		self.prefix = [".","/",">",""]
		self.img_url = "http://dl.profile.line-cdn.net/"
		self.poll = OEPoll(self.line)
		self.db = DataBase()
		self.db.add_bot(
				self.line.getProfile().mid,
				instance=str(self.line))
					
	def run(self, handler: dict or set = {}) -> dict:
		self.poll.addOpInterruptWithDict(handler)
		while True:
			self.poll.trace()
		
	def log(self, logger):
		def decorator(func):
			def wraper(*arg, **kwg):
				try:
					func(*arg, **kwg)
				except Exception as e:
					print(logger.format_exc())
			return wraper
		return decorator
	
	def reply(self,client, message, text):
		"""
		Use this method to Reply message to user
		@client: class<linepy.LINE.client>
		@message: class <akad.ttypes.Message>
		@text: pass a string of text you want to send
		exampe:
		client.reply(client=client, message=message, text='hallo')
		"""
		g = message.id
		return client.sendReplyMessage(g, message.to, text)
	 
	def at_getMid(self, message):
		key = eval(message.contentMetadata["MENTION"])
		key["MENTIONEES"][0]["M"]
		if len(key["MENTIONEES"]) <= 1:
			return key["MENTIONEES"][0]["M"]
		else:
			lists = []
			for i in key["MENTIONEES"]:
				lists.append(i["M"])
			return lists
	
	def add_users(self,
							client: LINE,
							group_id: str,
							mid: str or list,
							into: str,
							**kwg) -> bool:
		"""
		use this method to insert some user to DataBase
		@client: class<linepy.LINE.client>
		@group_id: undefined mid of group as string
		@mid: undefined mid of user pass string or list
		@into: pass a specified role for user e.g: blacklist,whitelist whatever you want
		@kwg: pass another argument as dict
		
		:Return: True if success false otherwise
		"""
		data = self.db
		if isinstance(mid, list):
			u = client.getContacts(mid)
			for i in u:
				data.add_users(mid=i.mid,
										into=into,
										name=i.displayName,
										at_group=group_id,
										globals=True)
		else:
			p = client.getContact(mid)
			data.add_users(mid=p.mid,
									into=into,
									name=p.displayName,
									at_group=group_id,
									globals=True)
		return True
			
	@Filters.is_admin()
	def add_group(self,
							client: LINE,
							mid: str or list,
							**kwg) -> bool:
		"""
		Use this method to add Group to database
		@client: class<linepy.LINE.Client>
		@mid: undefined string of Group mid, pass a string or list
		@kwg: other argument for include to your db e.g: grop.name pass a dict
		
		:Return: True if success false otherwise
		"""
		data = self.db
		if isinstance(mid, list):
			g = client.getGroups(mid)
			for i in g:
				data.add_group(
					i.mid,
					name=i.name,
					picture=self.img_url+i.pictureStatus,
					create=g.createdTime,
					creator=dict(
						id=i.creator.id,
						name=i.creator.displayName
					)
				)
		else:
			g = client.getGroup(mid)
			data.add_group(
				mid,
				name=g.name,
				picture=self.img_url+g.pictureStatus,
				create=g.createdTime,
				creator=dict(
					id=g.creator.mid,
					name=g.creator.displayName))
		return True
	
	@Filters.is_admin()
	def add_admin(self,
							client: LINE,
							mid: str or list,
							**kwg) -> bool:	
		"""
		Use this method to add Admin to database
		@client: class<linepy.LINE.Client>
		@mid: unidefined string of user mid, pass a string or list
		@kwg: other argument for include to your db e.g: user.displayName pass a dict
		
		:Return: True if success false otherwise
		"""
		data = self.db
		if isinstance(mid, list):
			c = client.getContacts(mid)
			for i in c:
				id = i.mid
				name = i.displayName
				data.add_admin(id, name=name)
		else:
			c = client.getContact(mid)			
			data.add_admin(mid, name=c.displayName)		
		return True