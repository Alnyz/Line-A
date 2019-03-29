import sys
sys.path.append("../")

from mains import  MainBots

init = MainBots(token="YOUR TOKEN")

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
	
<<<<<<< HEAD
@init.poll.hooks(13, func=lambda m: m)
def notif(client, message):
	print("NOTIFIED INVITE")	
init.runs()
=======
while True:
	init.poll.trace()
>>>>>>> 7a16f380f75f58bdd496ab2098f177a7a070e27d
