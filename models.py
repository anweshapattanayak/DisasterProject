from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(String)

class Resource(Base):
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    quantity = Column(Integer)

class Request(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    resource_id = Column(Integer, ForeignKey("resources.id"))
    quantity = Column(Integer)
    priority = Column(String)
    status = Column(String, default="pending")
    verified = Column(Boolean, default=False)

class Disaster(Base):
    __tablename__ = "disasters"
    id = Column(Integer, primary_key=True)
    location = Column(String)
    type = Column(String)
    severity = Column(String)

class Volunteer(Base):
    __tablename__ = "volunteers"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    skill = Column(String)
    status = Column(String, default="available")