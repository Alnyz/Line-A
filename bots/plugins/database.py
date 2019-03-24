from pymongo import MongoClient
import pymongo

import traceback

URI ="YOUR MONGO DB URI,no have? see www.mongodb.com"
myclient = MongoClient(URI, ssl=True, retryWrites=True)

class DataBase(object):
	def __init__(self):
		self.db = myclient.base_line
		self.col = self.db
		
	def add_bot(self, mid, **kwg):
		try:
			data = {
				"_id":mid,
				"other":kwg
			}
			if mid in self.listed(bots=True)["_id"]:
				pass
			else:
				self.col.bot_db.insert_one(data)
				return True
		except pymongo.errors.DuplicateKeyError:
			return False
	
	def add_group(self, mid: str, **kwg):
		try:
			data = {
				"_id":mid,
				"other":kwg
			}
			if mid in self.listed(groups=True)["_id"]:
				pass
			else:
				self.col.group_db.insert_one(data)
				return True
		except pymongo.errors.DuplicateKeyError:
			return False
			
	def add_admin(self, mid: str, **kwg):
		try:
			data = {
				"_id":mid,
				"other":kwg
			}
			if mid in self.listed(admin=True)["_id"]:
				pass
			else:
				self.col.admin_db.insert_one(data)
				return True			
		except pymongo.errors.DuplicateKeyError:
			return False
	
	def add_users(self, mid: str, into:str, **kwg):
		try:
			data = {
				"_id":mid,
				"is":into,
				"other":kwg
			}
			if mid in self.listed(users=True)["_id"]:
				pass
			else:
				self.col.users_db.insert_one(data)
				return True			
		except pymongo.errors.DuplicateKeyError:
			return False
	
	def listed(self,
					admin: bool = False,
					bots: bool = False,
					groups: bool = True,
					users: bool = False):
		if admin:
			for i in self.col.admin_db.find():
				return i
		if bots:
			for i in self.col.bot_db.find():
				return i	
		if groups:
			for i in self.col.group_db.find():
				return i
		if users:
			for i in self.col.users_db.find():
				return i
				