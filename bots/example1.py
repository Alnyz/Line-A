import sys
sys.path.append("../")

from mains import  MainBots

init = MainBots(token="u7bbe611b259e30f6ec652f40fce4e7bf:aWF0OiAxNTUxNjUyMzc5NDI2Cg==..KocjqFv1Q7noudJUSi/5KzTn2lA=")

@init.poll.hooks(26, at=["private"], command=["hi","halo"], prefix=[".","/"])
def message(client, message):
	msg = message.message
	client.sendMessage(msg._from, "Hallo on Private")

@init.poll.hooks(26, at=["group"], command=["ha","hey"], prefix=["+",">"])
def more(client, message):
	msg = message.message
	client.sendMessage(msg.to, "Hallo on Group")


@init.poll.hooks(26, at=["any"], command=["hy","oi"], prefix=["=","!"])
def again(client, message):
	msg = message.message
	client.sendMessage(msg.to if msg.toType == 2 else msg._from, "Hy im on Both")
	
@init.poll.hooks(13, func=lambda m: m)
def notif(client, message):
	print("NOTIFIED INVITE")	
init.runs()