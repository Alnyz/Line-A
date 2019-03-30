import sys
sys.path.append("../")

from mains import  MainBots

init = MainBots(token="ua2ac7e460623054aa4dc49af04c608b2:aWF0OiAxNTUxNjI0Njc2MDg4Cg==..RGgUJk5zmIZtsDZsjKy77MKxPt4=")

@init.poll.hooks(26, at=["private"], command=["hi","halo"], prefix=[".","/"])
def message(client, message):
	msg = message.message
	client.sendMessage(msg._from, "Hallo on Private")

@init.poll.hooks(13, func=lambda m: m)
def notif_invite(client, message):
	print("NOTIFIED INVITE")	
	
init.runs()