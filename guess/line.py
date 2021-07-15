from dotenv import load_dotenv
import os

from linebot import LineBotApi, WebhookHandler
from linebot.models.send_messages import TextSendMessage

load_dotenv()

handler = WebhookHandler(os.getenv('LINE_SECRET'))
line_bot_api = LineBotApi(os.getenv('LINE_TOKEN'))


def get_room(event):
    return event.source.user_id


def get_msg(event):
    return event.message.text.strip()


def reply_text(event, *messages, **kwargs):
    line_bot_api.reply_message(
        event.reply_token,
        messages=[TextSendMessage(text=message, **kwargs)
                  for message in messages],
    )
