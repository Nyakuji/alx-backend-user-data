#!/usr/bin/env python3
""" Module for Session Authentication """
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """
    Represents a session-based authentication mechanism
    with session expiration.

    This class extends the base `SessionAuth` class and adds
    functionality to handle session expiration.
    It allows creating sessions with a specified duration and
    provides a method to retrieve the user ID
    associated with a session ID, taking into account the
    session expiration time.

    Attributes:
        session_duration (int): The duration of a session in seconds.

    Methods:
        create_session(user_id=None): Creates a new session for
        the specified user ID.
        user_id_for_session_id(session_id=None): Retrieves the user
        ID associated with the given session ID.

    """

    def __init__(self):
        super().__init__()
        self.session_duration = int(
            os.getenv("SESSION_DURATION")) if os.getenv("SESSION_DURATION") \
            else 0

    def create_session(self, user_id=None):
        """
        Creates a new session for the specified user ID.

        Args:
            user_id (str): The ID of the user for whom the session is
            being created.

        Returns:
            str: The ID of the created session, or None if the session
            creation failed.

        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dict = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves the user ID associated with the given session ID.

        Args:
            session_id (str): The ID of the session.

        Returns:
            str: The ID of the user associated with the session, or
            None if the session ID is invalid or expired.

        """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        session_dict = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dict.get("user_id")
        if "created_at" not in session_dict:
            return None
        expiration_time = session_dict["created_at"] + \
            timedelta(seconds=self.session_duration)
        if expiration_time < datetime.now():
            return None
        return session_dict.get("user_id")
