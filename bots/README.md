## New style of Handler

*now you only pass a decorator for hook any functions which you want*

# Example1
```python
from mains import MainBots

init = MainBots(token="YOUR BOT TOKEN")

@init.poll.hooks(type=25, command=["halo"], at=["group"], prefix=[".", "/"])
def send_message(client, messages):
    """
    Attribute:
    
    """
    msg = messages.message
    client.sendMessage(msg.to, "Hayy... ")
    
init.runs()
```

# Example2
```python

from mains import MainBots

init = MainBots(token="YOUR TOKEN")

@init.poll.hooks(type=26)
def receive_message(client, message):
    """
    type: class <int>
    client: class <linepy.client.LINE>
    message: class <akad.ttypes.Message>
    
    what's meant?
    type of type must classes from int
    type 26 that's meant OpType.RECEIVE_MESSAGE
    
    :Return: client object and Message objects
    """
    pass
    
#Run bot
init.runs()
```

## Any example for any Notified

```python

@init.poll.hooks(type=19)
def notif_kicked(client, message):
    pass

@init.poll.hooks(type=13)
def notif_joined(client, message):
    pass
    
@init.poll.hookz(type=32)
def notif_cancled(client, message):
    pass
```
## NOTE: if your have headache of decorator please contact me

> TODO: i'll update features as soon as possible, if you and any idea or found some bug free for report
