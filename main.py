import serial
import threading
import queue
import config
from enum import Enum
import os
import logging

logging.basicConfig(level='INFO')
exit_status = 0


class SendItem:
    def __init__(self, value):
        self.value = value


class EventType(Enum):
    receive = 1
    send = 2


try:
    import db

    ser = serial.Serial(config.PORT, config.BPS)
except Exception as e:
    logging.error('[{}] {}'.format(db.get_time(), e))
    os._exit(0)

que = queue.Queue()


def receive_thread():
    while not exit_status:
        try:
            data = ser.read(1)
            if data == b'\x00':
                continue
            if data == b'\xfd':
                card_id = []
                for i in range(0, 4):
                    card_id.append(int.from_bytes(ser.read(1), 'little'))
                if db.verify(card_id):
                    unlock()
                else:
                    di()
        except Exception as e:
            logging.error('[{}] ERROR!! {}'.format(db.get_time(), e))


def send_thread():
    while not exit_status:
        try:
            data = que.get()
            ser.write(data.value)
        except Exception as e:
            logging.error('[{}] ERROR!! {}'.format(db.get_time(), e))


def unlock():
    que.put(SendItem(b'\x01'))


def di():
    que.put(SendItem(b'\x02'))


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
