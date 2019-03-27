import sys
sys.path.append("../")

from mains import  MainBots

init = MainBots(token="u7bbe611b259e30f6ec652f40fce4e7bf:aWF0OiAxNTUxNjUyMzc5NDI2Cg==..KocjqFv1Q7noudJUSi/5KzTn2lA=")

@init.poll.hooks(types=26, commands=["haq","hii"], at=["private"], prefix=[".","/"])
def messages(client, message):
	msg = message.message
	client.sendMessage(msg._from, f"Nice to meet you {msg._from}")
	
while True:
	init.poll.trace()