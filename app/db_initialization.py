from sqlalchemy import Column, Integer, String, ForeignKey
from datetime import date
from sqlalchemy import create_engine
engine = create_engine('sqlite:///DB/tas_db.db', echo = True)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
#class for user information 
class Users(Base):
   __tablename__ = 'users'
   userid = Column(String, primary_key=True)
   first_name = Column(String)
   last_address = Column(String)
   email = Column(String)
   phone = Column(String)
   password = Column(String)
#class for accounting data 

class Account(Base):
    __tablename__ = 'account_data'
    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_number = Column(String)
    userid = Column(String,ForeignKey('users.userid'))
    amount_debit = Column(Integer)
    amount_credit = Column(Integer)
    balancer = Column(Integer)
    transaction_date = Column(String)

Base.metadata.create_all(engine)



