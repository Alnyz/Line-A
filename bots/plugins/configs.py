import sys
sys.path.append("../")
from .database import DataBase
import mains
from linepy import LINE
from akad.ttypes import Message

def is_mid_admin():
	db = DataBase()
	return db.listed(admin=True)
	
class Filters:	
	def is_admin():
		def decorator(func):
			def wraper(*arg, **kwg):
				if kwg is not {}:
					for c in kwg.values():
						if isinstance(c, LINE):
							pass
						elif isinstance(c, Message):
							if c._from in is_mid_admin()["_id"]:
								func(*arg, **kwg)
								return True
							else:
								if isinstance(arg[0], mains.MainBots):
									arg[0].line.sendMessage(c.to, "ValueError: make sure you've permissions")
			return wraper
		return decorator
