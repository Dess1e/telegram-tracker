
import configparser
import logging as log
from sqlalchemy import create_engine
from sqlalchemy.types import String, Integer, Date
from sqlalchemy.schema import Column
from sqlalchemy.ext.declarative import declarative_base
from main import CFG, CONFIG_NAME


def extract_db_cfg(cfg):
    try:
        db = cfg['postgres']['db_name']
        user = cfg['postgres']['db_user']
        passwd = cfg['postgres']['db_pass']
        return db, user, passwd
    except KeyError:
        log.error(f'Could not parse postgres section in {CONFIG_NAME}')
        quit(1)


db, user, passwd = extract_db_cfg(CFG)

engine = create_engine(
    f'postgresql://{user}:{passwd}@localhost/{db}'
)

Base = declarative_base()


class OnlineHistory(Base):
    __tablename__ = 'online_history'

    user_id = Column(Integer())
    time = Column(Date())
    new_status = Column(String())


class LastOnline(Base):
    __tablename__ = 'last_online'

    user_id = Column(Integer())
    time = Column(Date())
    last_status = Column(String())


