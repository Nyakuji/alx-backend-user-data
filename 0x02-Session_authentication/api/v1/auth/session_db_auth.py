#!/usr/bin/env python3
""" Module for Session Database Authentication """
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class to manage session ID with file-based storage """

    def create_session(self, user_id=None):
        """ Create a session ID for the user and store it in UserSession """
        if user_id is None:
            return None

        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        # Create and store new instance of UserSession
        session = UserSession(user_id=user_id, session_id=session_id)
        session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Retrieve a user ID based on session ID """
        if session_id is None:
            return None

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

        if created_at + \
                timedelta(seconds=self.session_duration) < datetime.now():
            return None

        return session.user_id

    def destroy_session(self, request=None):
        """ Destroy a UserSession based on the session
        ID from the request cookie """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        # Search for the session ID in UserSession
        sessions = UserSession.search({'session_id': session_id})
        if not sessions:
            return False

        session = sessions[0]
        session.remove()
        return True
