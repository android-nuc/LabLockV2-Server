import serial
import threading
import queue
import config
from enum import Enum
import logging
import db
import time

logging.basicConfig(level='INFO')
exit_status = 0


class SendItem:
    def __init__(self, value):
        self.value = value


class EventType(Enum):
    receive = 1
    send = 2


try:
    ser = serial.Serial(config.PORT, config.BPS, timeout=config.TIMEOUT)
except Exception as e:
    logging.error('[{}] {}'.format(db.get_time(), e))
    exit(0)

que = queue.Queue()


def receive_thread():
    global exit_status
    while not exit_status:  # 如果未请求退出则继续运行
        try:
            data = ser.read(1)
            if data == b'':  # 超时时重新读取
                continue
            if data == b'\xf2':  # 心跳检测
                heart()
                logging.debug('ping')
                continue
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
            exit_status = 1
            exit(0)


def send_thread():
    global exit_status
    while not exit_status:
        try:
            data = que.get(True, config.TIMEOUT)
            ser.write(data.value)
        except queue.Empty:  # 读取超时时继续等待
            pass
        except Exception as e:
            logging.error('[{}] ERROR!! {}'.format(db.get_time(), e))
            exit_status = 1
            exit(0)


def unlock():
    que.put(SendItem(b'\x01'))


def di():
    que.put(SendItem(b'\x02'))


def heart():
    que.put(SendItem(b'\xf2'))


if __name__ == "__main__":
    receive = threading.Thread(target=receive_thread)
    send = threading.Thread(target=send_thread)
    receive.start()
    send.start()
    logging.info('[{}] Android Smart Lock start'.format(db.get_time()))
    try:
        while not exit_status:
            time.sleep(10)  # 使主线程等待
    except KeyboardInterrupt:  # 收到ctrl+c时进入退出步骤
        logging.info('[{}] exit'.format(db.get_time()))
        exit_status = 1
