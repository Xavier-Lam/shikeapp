# -*- coding: utf-8 -*-

import datetime

from sqlalchemy import Boolean, Column, create_engine, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import config

engine = create_engine(config.database_str)
Session = sessionmaker(bind=engine)
Model = declarative_base()

class User(Model):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    uid = Column(String(10), nullable=False)
    openid = Column(String(32), nullable=False)
    idfa = Column(String(36), nullable=False)
    key = Column(String(36), nullable=False)
    is_delete = Column(Boolean, default=False)
    createdate = Column(DateTime, default=datetime.datetime.now)
    sort = Column(String, default="")
    
    def __repr__(self):
        return '<User (uid="%s", name="%s", id="%s")>'%(self.uid, self.name, self.id)
        
# Base.metadata.create_all(engine)