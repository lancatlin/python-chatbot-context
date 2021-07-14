from dotenv import load_dotenv
import os

from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookHandler
from linebot.models.events import MessageEvent
from linebot.models.messages import TextMessage
from linebot.models.send_messages import TextSendMessage

load_dotenv()

line_bot_api = LineBotApi(os.getenv('LINE_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_SECRET'))

@csrf_exempt
def endpoint(request):
    if request.method == 'POST':
        signatrue = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        handler.handle(body, signatrue)

    return HttpResponse()

def reply_text(event, *messages, **kwargs):
    line_bot_api.reply_message(
        event.reply_token,
        messages=[TextSendMessage(text=message, **kwargs)
                  for message in messages],
    )

@handler.add(MessageEvent, message=TextMessage)
def route(event):
    reply_text(event, 'hello') 
