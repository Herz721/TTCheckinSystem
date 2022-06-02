from sqlalchemy import Column, Date, ForeignKey, Integer, String, Time
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class EMPLOYEE(Base):
    __tablename__ = 'EMPLOYEE'

    EID = Column(Integer, autoincrement=True, primary_key=True)
    ENAME = Column(String(64), nullable=False)
    MAC = Column(String(32), nullable=False, unique=True)
    DEVICE = Column(String(32), nullable=False)

    def __init__(self, name, mac, device):
        # self.EID = id
        self.ENAME = name
        self.MAC = mac
        self.DEVICE = device


class CLOCKRECORD(Base):
    __tablename__ = 'CLOCKRECORDS'

    RID = Column(Integer, autoincrement=True, primary_key=True)
    EID = Column(ForeignKey('EMPLOYEE.EID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    CHECKPOINT = Column(Time, nullable=False)
    RDATE = Column(Date, nullable=False)
    STATUS = Column(Integer, nullable=False)

    EMPLOYEE = relationship('EMPLOYEE')

    def __init__(self, eid, checkpoint, rdate, status):
        # self.RID = rid
        self.EID = eid
        self.CHECKPOINT = checkpoint
        self.RDATE = rdate
        self.STATUS = status

