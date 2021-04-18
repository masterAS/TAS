from sqlalchemy import Column, Integer, String, ForeignKey
from datetime import date
from sqlalchemy import create_engine
engine = create_engine('sqlite:///tas_db.db', echo = True)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
#class for user information 
class Users(Base):
   __tablename__ = 'users'
   username = Column(String, primary_key=True)
   first_name = Column(String)
   last_name = Column(String)
   email = Column(String)
   phone = Column(String)
   password = Column(String)
#class for accounting data 
class Account(Base):
    __tablename__ = 'account_data'
    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_number = Column(String)
    trip_no = Column(Integer)
    username = Column(String,ForeignKey('users.username'))
    transaction_type = Column(String)
    transaction_description = Column(String)
    amount_debit = Column(Integer)
    amount_credit = Column(Integer)
    balance = Column(Integer)
    transaction_date = Column(String)
    transaction_time = Column(String)
Base.metadata.create_all(engine)



