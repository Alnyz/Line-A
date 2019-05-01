from linepy import LINE, OEPoll, Filters
import time

line = LINE("YOUR TOKEN")
#pass withput any argument for login use QrCode -> LINE()
route = OEPoll(line)

@route.is_message(26, Filters.command("stest", prefix="."))
def receive_command(ops):
	#Fetch speed
	rs = time.time()
	line.sendMessage(ops.message._from, "...")
	line.sendMessage(ops.message._from, f"Fetch; {time.time()-rs}")
	
route.start()