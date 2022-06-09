from sqlalchemy import Column, Date, ForeignKey, Integer, String, Time
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employee'

    # autoincrement 
    eid = Column(Integer, primary_key=True)
    ename = Column(String(128), nullable=False)
    password = Column(String(128))
    role = Column(String(64), nullable=False)
    status = Column(String(32), nullable=False)
    dept = Column(String(64))


class ClockRecord(Base):
    __tablename__ = 'clock_records'

    rid = Column(Integer, primary_key=True)
    eid = Column(ForeignKey('employee.eid', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    check_point = Column(Time, nullable=False)
    rdate = Column(Date, nullable=False)
    status = Column(Integer, nullable=False)

    employee = relationship('Employee')

    def __init__(self, eid, checkpoint, rdate, status):
        # self.rid auto_increment
        self.eid = eid
        self.check_point = checkpoint
        self.rdate = rdate
        self.status = status


class Device(Base):
    __tablename__ = 'device'

    MAC = Column(String(32), primary_key=True, unique=True)
    dev_type = Column(String(32), nullable=False)
    dev_name = Column(String(128))
    eid = Column(ForeignKey('employee.eid', ondelete='CASCADE', onupdate='CASCADE'), index=True)

    employee = relationship('Employee')

    def __init__(self, mac, dev_type, dev_name, eid):
        self.MAC = mac
        self.dev_type = dev_type
        self.dev_name = dev_name
        self.eid = eid


