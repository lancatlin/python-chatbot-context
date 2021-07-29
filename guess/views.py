from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from linebot.models.events import MessageEvent
from linebot.models.messages import TextMessage

from .line import handler, reply_text, get_msg
from .message_queue import MessageQueue
from .guess import Guess


@csrf_exempt
def endpoint(request):
    if request.method == 'POST':
        signatrue = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        handler.handle(body, signatrue)

    return HttpResponse()


@handler.add(MessageEvent, message=TextMessage)
def route(event):
    if MessageQueue.handle(event):
        return

    msg = get_msg(event)
    if msg == 'guess':
        Guess(event)
    else:
        reply_text(event, 'command not defined')
