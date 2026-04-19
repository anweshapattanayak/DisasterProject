from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class User(Base):
    __tablename__ = "users"
<<<<<<< HEAD

    id = Column(Integer, primary_key=True, index=True)
=======
    id = Column(Integer, primary_key=True)
>>>>>>> auth-backend
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="user")


class Resource(Base):
    __tablename__ = "resources"
<<<<<<< HEAD

    id = Column(Integer, primary_key=True, index=True)
=======
    id = Column(Integer, primary_key=True)
>>>>>>> auth-backend
    name = Column(String)
    quantity = Column(Integer)


class Request(Base):
    __tablename__ = "requests"


    id = Column(Integer, primary_key=True, index=True)
=======
    id = Column(Integer, primary_key=True)
>>>>>>> auth-backend
    user_id = Column(Integer, ForeignKey("users.id"))
    resource_id = Column(Integer, ForeignKey("resources.id"))
    quantity = Column(Integer)
    priority = Column(String)
    status = Column(String, default="pending")