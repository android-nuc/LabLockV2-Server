import config
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import model
import datetime
import logging

data_db = sqlalchemy.create_engine(config.DB)
base = declarative_base(data_db)
cursor = sessionmaker(bind=data_db)


def verify(id: list) -> bool:
    session = cursor()
    user = session.query(model.User).filter(
        model.User.card_1 == id[0] and model.User.card_2 == id[1] and model.User.card_3 == id[
            2] and model.User.card_4 == id[3]).first()
    if user is None:
        log_deny(id)
        logging.warning('[{}] log deny card:{}'.format(get_time(),id))
        return False
    if user.enabled:
        log_success(user.uid)
        logging.info('[{}] log success card:{}'.format(get_time(),id))
        return True
    else:
        log_deny(id)
        logging.warning('[{}] log not enabled card:{}'.format(get_time(),id))
        return False


def log_success(uid):
    session = cursor()
    log = model.UnlockLog(uid=uid, time=get_time())
    session.add(log)
    session.commit()
    pass


def log_deny(id: list):
    session = cursor()
    log = model.DenyLog(card_1=id[0], card_2=id[1], card_3=id[2], card_4=id[3], time=get_time())
    session.add(log)
    session.commit()
    pass


def get_time():
    now = datetime.datetime.now()
    return now


if __name__ == "__main__":
    base.metadata.create_all(data_db)
