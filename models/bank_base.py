from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('sqlite:///bankmanager.db')
Base = declarative_base()

class Client(Base):
    __tablename__ = 'T_CLIENT'
    id = Column(Integer, primary_key=True)
    c_name = Column("Name", String)
    c_surname = Column("Surname", String)
    c_security_number = Column("Social security No", Integer)
    c_phone = Column("Phone No", Integer)
    c_accounts = relationship("Account") 

class Bank(Base):
    __tablename__ = 'T_BANK'
    id = Column(Integer, primary_key=True)
    b_name = Column("Name", String)
    b_address = Column("Address", String)
    b_code = Column("Bank Code", Integer)
    swift = Column("SWIFT", String)
    b_accounts = relationship("Account")

class Account(Base):
    __tablename__ = 'T_ACCOUNT'
    id = Column(Integer, primary_key=True)
    a_number = Column("Number", String)
    a_ballance = Column("Ballance", Float)
    client = Column(Integer, ForeignKey("T_CLIENT.id"))
    bank = Column(Integer, ForeignKey("T_BANK.id"))
       

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()