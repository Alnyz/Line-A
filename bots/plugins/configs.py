from .database import DataBase

def is_mid_admin():
	db = DataBase()
	return db.listed(admin=True)
	
class Filters:	
	def is_admin():
		def decorator(func):
			def wraper(*arg, **kwg):
				if kwg:
					msg = kwg["message"]
					client = kwg["client"]
					if msg._from == is_mid_admin()["_id"]:
						return func(*arg,**kwg)
					else:
						client.sendMessage(msg.to,"Value Error: make sure you have Permissions")
			return wraper
		return decorator