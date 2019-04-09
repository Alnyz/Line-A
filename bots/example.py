import sys
sys.path.append("../")

from mains import  MainBots
from linepy import Filters

init = MainBots(token="<YOUR TOKEN>")
line = init.line

@init.poll.is_message(13)
def NOTIF_INVITE(ops):
	print(ops)

@init.poll.is_message(11, Filters.update_name | Filters.update_qr)
def NOTIF_UPDATE_GROUP(ops):
	"""
	This method meant, get all notifed update group contain name or qr
	you can use Filters.update_all for get all update name,qr,image of group
	"""
	print(ops)
	
@init.poll.is_message(26, Filters.user("your mid") & Filters.sticker)
def Receive_sticker(ops):
	print(ops)
	
@init.poll.is_message(26, Filters.command("hello", prefix="."))
def receive_command(ops):	
	line.sendMessage(ops.message.to, "hello to")

init.run()
