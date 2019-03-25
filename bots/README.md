## New style of Handler

*now you only pass a decorator for hook any functions which you want*


# Example
```python

from mains import MainBots

init = MainBots(token="YOUR TOKEN")

@init.poll.message_handler(type=26)
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
    
#Run bot
init.runs()
```

> TODO: i'll update features as soon as possible, if you and any idea or found some bug free for report
