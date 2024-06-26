#!/usr/bin/env python3
""" Module for Session Database Authentication """
from datetime import datetime, timedelta
from models.user_session import UserSession
from api.v1.auth.session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class that stores session data in a file-based database"""

    def create_session(self, user_id=None):
        """ Create a session ID for a given user ID
        and store it in UserSession """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session = UserSession(user_id=user_id, session_id=session_id)
        session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Retrieve a user ID based on session ID """
        if session_id is None:
            return None

        # Ensure that UserSession data is loaded
        UserSession.load_from_file()

        # Search for the session ID in UserSession
        sessions = UserSession.search({'session_id': session_id})
        if not sessions:
            return None

        session = sessions[0]

        if self.session_duration <= 0:
            return session.user_id

        created_at = session.created_at
        if created_at is None:
            return None

        # Calculate expiration time
        if created_at + \
                timedelta(seconds=self.session_duration) < datetime.now():
            return None

        return session.user_id

    def destroy_session(self, request=None):
        """ Destroy a session by removing the UserSession entry """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        # Ensure that UserSession data is loaded
        UserSession.load_from_file()

        # Search for the session ID in UserSession
        sessions = UserSession.search({'session_id': session_id})
        if not sessions:
            return False

        session = sessions[0]
        session.remove()
        return True
