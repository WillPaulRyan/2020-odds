from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class NewLog(Base):
    __tablename__ = 'election'
    timestamp = Column(DateTime, primary_key=True)
    trump = Column(Integer)
    warren = Column(Integer)
    booker = Column(Integer)
    biden = Column(Integer)
    sanders = Column(Integer)
    klobuchar = Column(Integer)
    harris = Column(Integer)
    gillibrand = Column(Integer)
    gabbard = Column(Integer)
    orourke = Column(Integer)
    yang = Column(Integer)
    buttigieg = Column(Integer)
    castro = Column(Integer)

    def __init__(self, timestamp, trump, warren, booker, biden, sanders, klobuchar, harris, gillibrand, gabbard, orourke, yang, buttigieg, castro):
        self.timestamp = timestamp
        self.trump = trump
        self.warren = warren
        self.booker = booker
        self.biden = biden
        self.sanders = sanders
        self.klobuchar = klobuchar
        self.harris = harris
        self.gillibrand = gillibrand
        self.gabbard = gabbard
        self.orourke = orourke
        self.yang = yang
        self.buttigieg = buttigieg
        self.castro = castro
        