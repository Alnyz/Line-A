from linepy import LINE, OEPoll, Filters
import time

line = LINE("YOUR TOKEN")
#now you can disable notice after login
#pass Flase for display_notice inside LINE e.g LINE(display_notice=False)
#pass without any argument for login use QrCode -> LINE()

route = OEPoll(line)
"""
args route:
	wrokers: <int> some workers for do action if threaded is True
	threaded: <bool> pass True if you want this Threaded, False otherwise
"""
@route.handler(25, Filters.command("speed", prefix="."))
def speed(ops):
	#Fetch speed
	rs = time.time()
	line.sendMessage(ops.message.to, "...")
	line.sendMessage(ops.message.to, f"Fetch; {time.time()-rs}")

route.start()