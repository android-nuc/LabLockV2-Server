# coding: utf-8
from sqlalchemy import Column, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class DenyLog(Base):
    __tablename__ = 'deny_log'

    id = Column(INTEGER(10), primary_key=True)
    time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    card_1 = Column(TINYINT(3), nullable=False, server_default=text("'0'"))
    card_2 = Column(TINYINT(3), nullable=False, server_default=text("'0'"))
    card_3 = Column(TINYINT(3), nullable=False)
    card_4 = Column(TINYINT(3), nullable=False)


class UnlockLog(Base):
    __tablename__ = 'unlock_log'

    id = Column(INTEGER(10), primary_key=True)
    uid = Column(INTEGER(10), nullable=False)
    time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class User(Base):
    __tablename__ = 'users'

    uid = Column(INTEGER(10), primary_key=True)
    name = Column(String(14), nullable=False)
    student_id = Column(String(14), nullable=False)
    card_1 = Column(TINYINT(3), nullable=False, server_default=text("'0'"))
    card_2 = Column(TINYINT(3), nullable=False, server_default=text("'0'"))
    card_3 = Column(TINYINT(3), nullable=False)
    card_4 = Column(TINYINT(3), nullable=False)
    enabled = Column(TINYINT(1), nullable=False, server_default=text("'1'"))
