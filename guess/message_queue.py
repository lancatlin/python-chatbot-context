import queue
from threading import RLock
from .line import get_room


class RequestTimout(Exception):
    pass


class MessageQueue:
    _lock = RLock()
    _requests = {}
    _responses = {}

    @classmethod
    def create_if_not_exists(cls, room):
        with cls._lock:
            if room not in cls._requests:
                cls._requests[room] = queue.Queue(maxsize=1)

            if room not in cls._responses:
                cls._responses[room] = queue.Queue(maxsize=1)

    @classmethod
    def handle(cls, event):
        room = get_room(event)
        cls.create_if_not_exists(room)

        try:
            if not cls._requests[room].empty():
                cls._responses[room].put(event, timeout=1)
                cls._requests[room].get()
                return True
            return False
        except queue.Empty:
            '''No request, ignore the message'''
            return False

    @classmethod
    def request(cls, room, timeout=30):
        try:
            cls.create_if_not_exists(room)

            cls._requests[room].put_nowait(True)
            return cls._responses[room].get(timeout=timeout)

        except queue.Empty:
            MessageQueue.clear(room)
            raise RequestTimout

    @classmethod
    def available(cls, room):
        cls.create_if_not_exists(room)
        return cls._requests[room].empty()

    @classmethod
    def clear(cls, room):
        cls.create_if_not_exists(room)
        try:
            cls._requests[room].get_nowait()
        except queue.Empty:
            pass
