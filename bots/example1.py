import sys
sys.path.append("../")

from mains import  MainBots

init = MainBots(token="YOUR TOKEN")

@init.poll.hooks(types=26, commands=["haq","hii"], at=["private"], prefix=[".","/"])
def messages(client, message):
	msg = message.message
	client.sendMessage(msg._from, f"Nice to meet you {msg._from}")
	
while True:
	init.poll.trace()
