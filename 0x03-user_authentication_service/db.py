#!/usr/bin/env python3
"""DB module.
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class.
    """

    def __init__(self) -> None:
        """Initialize a new DB instance.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user to the database.
        """
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **kwargs):
        """Finds a specific user given set 
        of filters"""
        for key, value in kwargs.items():
            if hasattr(User, key):
                conditions = []
                conditions.append(getattr(User, key) == value)
            else:
                raise InvalidRequestError()
        result = self._session.query(User).filter(*conditions).first()

        if result is None:
            raise NoResultFound()

        return result

    def update_user(user_id: int, *kwargs) -> None:
        """Updates a specific user's attributes
        """
        user = self._session.query(find_user_by(user_id))
        for key, value in kwargs.items():
            setattr(user, key) == value
            self._session.add()
            self._session.commit()
        raise ValueError
















