from .message_queue import MessageQueue
from .line import reply_text, get_room, get_msg


class Guess:
    def __init__(self, event):
        self.event = event
        self.guess()

    def guess(self):
        msg = self.ask('Please input something')
        self.reply(f'you input {msg}')

    def ask(self, *msg):
        self.reply(*msg)
        self.event = MessageQueue.request(get_room(self.event))
        return get_msg(self.event)

    def reply(self, *msg):
        reply_text(self.event, *msg)
