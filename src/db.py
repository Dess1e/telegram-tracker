from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.types import String, Integer, Date, Boolean
from sqlalchemy.schema import Column
from sqlalchemy.ext.declarative import declarative_base
from cfg import extract_db_cfg, get_cfg


db, user, passwd, port = extract_db_cfg(get_cfg())

engine = create_engine(
    f'postgresql://{user}:{passwd}@localhost:{port}/{db}'
)

session = sessionmaker(autocommit=True, autoflush=False, bind=engine)

tracker_session = scoped_session(session)

Base = declarative_base()


class OnlineHistory(Base):
    __tablename__ = 'online_history'

    user_id = Column(Integer(), primary_key=True)
    time = Column(Date(), primary_key=True)
    new_status = Column(String())


class LastOnline(Base):
    __tablename__ = 'last_online'

    user_id = Column(Integer(), primary_key=True)
    time = Column(Date(), primary_key=True)
    last_status = Column(String())


class UserInfo(Base):
    __tablename__ = 'user_info'

    user_id = Column(Integer(), primary_key=True)
    first_name = Column(String())
    last_name = Column(String())
    user_name = Column(String())
    bio = Column(String())
    trackable_online = Column(Boolean())
    last_modified = Column(Date())


class UserInfoHistory(Base):
    __tablename__ = 'user_info_history'

    user_id = Column(Integer(), primary_key=True)
    time = Column(Date())
    changed_field = Column(String())
    old_value = Column(String())
    new_value = Column(String())

