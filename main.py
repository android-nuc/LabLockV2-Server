import serial
import threading
import queue
import config
from enum import Enum
import os
import logging

logging.basicConfig(level='INFO')
exit_status = 0

class Event:
    def __init__(self, type, value):
        self.type = type
        self.value = value


class EventType(Enum):
    receive = 1
    send = 2


try:
    import db
    ser = serial.Serial(config.PORT, config.BPS)
except Exception as e:
    logging.error('[{}] {}'.format(db.get_time(),e))
    os._exit(0)

que = queue.Queue()


def receive_thread():
    while not exit_status:
        data = ser.read(1)
        if data == b'\x00':
            continue
        if data == b'\xfd':
            card_id = []
            for i in range(0, 4):
                card_id.append(int.from_bytes(ser.read(1),'little'))
            if db.verify(card_id):
                unlock()
            else:
                di()


def send_thread():
    while not exit_status:
        data = que.get()
        if data.type == EventType.send:
            ser.write(data.value)


def unlock():
    que.put(Event(EventType.send, b'\x01'))


def di():
    que.put(Event(EventType.send, b'\x02'))


if __name__ == "__main__":
    threading.Thread(target=receive_thread).start()
    threading.Thread(target=send_thread).start()

    print('Android Smart Lock start')
    try:
        input()
        exit_status = 1
    except Exception:
        os._exit(0)
    os._exit(0)
