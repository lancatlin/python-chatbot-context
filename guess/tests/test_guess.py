from time import sleep
from unittest.mock import patch
from django.test import TestCase
from linebot.models.events import MessageEvent, TextMessage
from linebot.models.sources import SourceUser
from guess.views import route
from threading import Thread


def sample_msg(msg, user_id=1):
    return MessageEvent(message=TextMessage(text=msg), source=SourceUser(user_id=user_id))


def send(msg, user_id=1):
    thread = Thread(target=route, args=(sample_msg(msg, user_id), ))
    thread.start()
    sleep(0.1)


class Guess(TestCase):

    @patch('guess.guess.randint', return_value=63)
    @patch('guess.guess.Guess.reply')
    def test_guess(self, mock_reply, mock_random):
        send('guess')
        mock_reply.assert_called_with('From what number?')
        send('10')
        mock_reply.assert_called_with('To what number?')
        send('100')
        mock_reply.assert_called_with(f'Guess a number between 10 to 100')
        send('34')
        mock_reply.assert_called_with('too small')
        send('72')
        mock_reply.assert_called_with('too large')
        send('63')
        mock_reply.assert_called_with(
            f'You spent 3 times to guess the secret number.')
