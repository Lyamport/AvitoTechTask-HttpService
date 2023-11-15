from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta


Base = declarative_base()


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    first_octets = Column(String(15))
    last_octet = Column(String(4))
    time = Column(DateTime, default=datetime.now)


class BlackList(Base):
    __tablename__= 'blacklist'
    id = Column(Integer, primary_key=True)
    first_octets = Column(String(15))
    time = Column(DateTime, default=datetime.now)


engine = create_engine('sqlite:///addresses.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

database_is_locked = False
lock_period = 120


def get_first_and_last_octets(ip):
    first_three_octets = "".join(str(ip).split(".")[0:3])
    last_octet = str(ip).split(".")[3]
    return first_three_octets, last_octet


def add_address(ip):
    one_minute_ago = datetime.now() - timedelta(minutes=1)
    two_minutes_ago = datetime.now() - timedelta(minutes=2)

    count = session.query(Address).filter(Address.first_octets == get_first_and_last_octets(ip)[0], Address.time >= one_minute_ago).count()
    if count > 100:
        if session.query(BlackList).filter(BlackList.first_octets == get_first_and_last_octets(ip)[0], BlackList.time > two_minutes_ago).count() == 0:
            new_blacklist = BlackList(first_octets=get_first_and_last_octets(ip)[0])
            session.add(new_blacklist)
            session.commit()
    check = session.query(BlackList).filter(BlackList.first_octets == get_first_and_last_octets(ip)[0], BlackList.time > two_minutes_ago).count()
    if check > 0:
        return False

    new_address = Address(first_octets=get_first_and_last_octets(ip)[0], last_octet=get_first_and_last_octets(ip)[1])
    session.add(new_address)
    session.commit()
    return True
