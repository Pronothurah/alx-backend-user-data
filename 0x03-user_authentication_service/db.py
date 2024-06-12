#!/usr/bin/env python3
"""DB Model"""
from typing import Any
from sqlalchemy import create_engine, tuple_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """saves user to DB"""
        new_user = User(email=email, hashed_password=hashed_password)
        try:
            self._session.add(new_user)
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            new_user = None
            raise e
        return new_user

    def find_user_by(self, **kwargs: Any) -> User:
        """Finds a user based on a set of filters.
        """
        query = self._session.query(User)
        for key, value in kwargs.items():
            if hasattr(User, key):
                query = query.filter(getattr(User, key) == value)
            else:
                raise InvalidRequestError(f"Invalid attribute: {key}")
        user = query.first()
        if user is None:
            raise NoResultFound(f"No user found with attributes {kwargs}")
        return user

    def update_user(self, user_id: int, **kwargs: Any) -> None:
        """Updates user attributes and commit to database"""
        user = self.find_user_by(id=user_id)
        if user is None:
            raise ValueError(f"User with id {user_id} not found")
        update_source = {}
        for key, value in kwargs.items():
            if hasattr(User, key):
                update_source[getattr(User, key)] = value
            else:
                raise ValueError()
            setattr(user, key, value)
        self._session.query(User).filter(User.id == user.id).update(
            update_source,
            synchronize_session=False
        )
        self._session.commit()
