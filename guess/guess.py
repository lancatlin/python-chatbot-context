from .message_queue import MessageQueue, RequestTimout
from .line import reply_text, get_room, get_msg
from random import randint


class Guess:
    '''Guess handle a guess number game'''

    def __init__(self, event):
        self.event = event
        try:
            self.guess()
        except RequestTimout:
            self.reply('Timeout')

    def guess(self):
        '''Game function'''
        min_value = self.ask_number('From what number?')
        max_value = self.ask_number('To what number?')
        secret = randint(min_value, max_value)
        msg = f'Guess a number between {min_value} to {max_value}'
        counter = 0
        while True:
            counter += 1
            answer = self.ask_number(msg)
            if answer > secret:
                msg = 'Too large'
            elif answer < secret:
                msg = 'Too small'
            else:
                break
        self.reply(f'You spent {counter} times to guess the secret number.')

    def ask(self, *msg):
        '''Ask a question to current user'''
        self.reply(*msg)
        self.event = MessageQueue.request(get_room(self.event))
        return get_msg(self.event)

    def ask_number(self, *msg):
        '''Ask a number, if not number, ask again'''
        try:
            content = self.ask(*msg)
            return int(content)
        except ValueError:
            return self.ask_number('Please input an integer.', *msg)

    def reply(self, *msg):
        '''Reply words to user'''
        reply_text(self.event, *msg)
