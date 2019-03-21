import sys
sys.path.append("../")

from linepy import OpType
from mains import  MainBots
import time



init = MainBots(
	token="YOUR TOKEN"
	)


def msg(c, op):
	msg = op.message
	
	
handler = {
	OpType.RECEIVE_MESSAGE: msg
}

init.run(handler=handler)
