import sys
sys.path.append("../")

from mains import  MainBots
import traceback

init = MainBots(token="YOUR TOKEN")

@init.poll.hooks(types=26)
@init.log(traceback)
def receive_msg(client, m):
	msg = m.message
	from_ = msg._from		
	if (msg.contentType == 0 and msg.text != None):
		#GET ALL CONTENT TYPE TEXT
		text = msg.text.lower()
		
		if text.startswith("hai"):
			# #this will reply to specified chat from user
			init.reply(client=client, message=msg, text="hai to")
		if text.startswith("addadmin"):
			# #this will add someuser with tag or not to database
			init.add_admin(client=client,mid=msg)
			
@init.poll.hooks(types=13)
@init.log(traceback)
def invited(client, m):
	print("NOTIF INVITE")
	group = m.param1
	who = m.param2
	target = m.param3.split()
	if init.db.listed(bots=True)["_id"] in target:
		if who == init.db.listed(admin=True)["_id"]:	
			client.acceptGroupInvitation(group)
			init.add_group(client, group)
		else:
			client.acceptGroupInvitation(group)
			client.sendMessage(group, "Only admin")
			client.leaveGroup(group)

@init.poll.hooks(types=19)
@init.log(traceback)
def kicked(client, m):
	print("NOTIF KICK")
	groups = m.param1
	who = m.param2
	target = m.param3.split()
	if groups in init.db.listed(groups=True)["_id"]:
		if who in init.db.listed(admin=True)["_id"]:
			pass
		else:
			init.add_users(client=client, group_id=groups, mid=who, into="blacklist")		
	
init.runs()
