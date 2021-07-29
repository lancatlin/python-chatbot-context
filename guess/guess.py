from .message_queue import MessageQueue, RequestTimout
from .line import reply_text, get_room, get_msg
from random import randint


class Guess:
    def __init__(self, event):
        self.event = event
        try:
            self.guess()
        except RequestTimout:
            self.reply('Timeout')

    def guess(self):
        min_value = self.ask_number('From what number?')
        max_value = self.ask_number('To what number?')
        secret = randint(min_value, max_value)
        msg = f'Guess a number between {min_value} to {max_value}'
        counter = 0
        while True:
            counter += 1
            answer = self.ask_number(msg)
            if answer > secret:
                msg = 'too large'
            elif answer < secret:
                msg = 'too small'
            else:
                break
        self.reply(f'You spent {counter} times to guess the secret number.')

    def ask(self, *msg):
        self.reply(*msg)
        self.event = MessageQueue.request(get_room(self.event))
        return get_msg(self.event)

    def ask_number(self, *msg):
        try:
            content = self.ask(*msg)
            return int(content)
        except ValueError:
            return self.ask_number('Please input an integer.', *msg)

    def reply(self, *msg):
        reply_text(self.event, *msg)
