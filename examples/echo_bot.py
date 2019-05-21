from linepy import LINE, OEPoll, Filters
import time

line = LINE("YOUR TOKEN")
#pass without any argument for login use QrCode -> LINE()
route = OEPoll(line)

@route.handler(26, Filters.command("speed", prefix="."))
def speed(ops):
	#Fetch speed
	rs = time.time()
	line.sendMessage(ops.message._from, "...")
	line.sendMessage(ops.message._from, f"Fetch; {time.time()-rs}")

@route.handler(26, Filters.command("hai", prefix=[".","/"]))
def say_hai(ops):
	msg = ops.message
	to = msg.to if msg.toType == 2 else msg._from
	user = line.getContact(msg._from).displayName
	line.sendMessage(to, "Hai, {} from echo bot!".format(user))

route.start()