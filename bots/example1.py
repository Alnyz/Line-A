import sys
sys.path.append("../")

from mains import  MainBots

init = MainBots(token="YOUR TOKEB")

@init.poll.hooks(26, at=["private"], command=["hi","halo"], prefix=[".","/"])
def message(client, message):
	msg = message.message
	client.sendMessage(msg._from, "Hallo on Private")

@init.poll.hooks(13, func=lambda m: m)
def notif_invite(client, message):
	print("NOTIFIED INVITE")	
	
init.runs()
