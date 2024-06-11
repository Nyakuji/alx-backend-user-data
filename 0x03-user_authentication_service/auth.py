#!/usr/bin/env python3
"""Auth module
"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hashes the input password using bcrypt.

    Args:
        password: The password to be hashed.

    Returns:
        The hashed password as bytes.

    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user.

        Args:
            email: The email of the user.
            password: The password of the user.

        Returns:
            The User object representing the registered user.

        Raises:
            ValueError: If a user already exists with the passed email.

        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists.")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(
                email=email, hashed_password=hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates if a login is valid.

        Args:
            email: The email of the user.
            password: The password of the user.

        Returns:
            True if the login is valid, False otherwise.

        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode(), user.hashed_password):
                return True
            else:
                return False
        except NoResultFound:
            return False

    def _generate_uuid() -> str:
        """Generates a new UUID.

        Returns:
            A string representation of the new UUID.

        """
        return str(uuid.uuid4())
