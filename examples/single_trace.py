from linepy import LINE, OEPoll, Filters

line = LINE("YOUR TOKEN")
#pass withput any argument for login use QrCode -> LINE()
route = OEPoll(line)

@route.handler(26, Filters.text & Filters.group)
def receive_command(ops):
	msg = op.message
	to = msg.to if msg.toType == 2 else msg._from
	text = msg.text.lower()
	if text == "hai":
		user = line.getContact(msg._from).displayName
		line.sendMessage(to, "Hai, {} nice to meet you!".format(user))
		
	#pass some command to trigger bot
	
route.start()	