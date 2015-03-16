#! /usr/bin/python
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

from datetime import datetime, timedelta

engine = create_engine('mysql://username:password@mysqldatabase:3306/rbd',echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Tabsiteerror(Base):
    __tablename__ = "tabSiteErrorLog"

    errorId = Column(Integer, primary_key=True)
    exceptionData = Column(String)
    sessionData = Column(String)
    requestData = Column(String)
    formData = Column(String)
    cgiData = Column(String)
    errordatetime = Column(DateTime)

#testquery = session.query(Tabsiteerror).first()
today = datetime.today()
thirtydaysago = datetime.now() - timedelta(days = 30)
thirtysevendaysago = datetime.now() - timedelta(days = 37)
testquery = session.query(Tabsiteerror).filter(Tabsiteerror.exceptionData != 'Deleted').filter(Tabsiteerror.errordatetime < thirtydaysago).filter(Tabsiteerror.errordatetime > thirtysevendaysago).all()

#errorID = [testquery.errorId, testquery.errordatetime]

testquery.exceptionData = "Deleted"
testquery.sessionData = "Deleted"
testquery.requestData = "Deleted"
testquery.formData = "Deleted"
testquery.cgiData = "Deleted"
session.commit()
             
#print testquery.errordatetime
#print testquery.exceptionData
#print errorID
print  today
print  thirtydaysago
print  thirtysevendaysago
