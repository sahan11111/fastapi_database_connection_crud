from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "users" # Name of the database table

    id = Column(Integer, primary_key=True, index=True) # Primary key, auto-incrementing
    name = Column(String, index=True) # User name
    phone_number = Column(String, unique=True, index=True) # Unique phone number
    email = Column(String, unique=True, index=True) # Unique email