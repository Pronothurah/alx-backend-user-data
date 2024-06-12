#!/usr/bin/env python3
"""Module SQLAlchemy model named User"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """Represents a record from the `user` table.
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(256), nullable=False, unique=True)
    hashed_password = Column(String(256), nullable=False)
    session_id = Column(String(256), nullable=True)
    reset_token = Column(String(256), nullable=True)
