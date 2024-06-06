#!/usr/bin/env python3
""" Module for Session Database Authentication """
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from uuid import uuid4


class SessionDBAuth(SessionExpAuth):
    """ Session Database Authentication Class """

    def create_session(self, user_id=None):
        """ Creates a Session ID for a user_id """

        if not user_id:
            return None
        session_id = str(uuid4())
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Returns a User ID based on a Session ID"""
        if not session_id:
            return None
        user_session = UserSession.search({"session_id": session_id})
        if not user_session:
            return None
        return user_session[0].user_id

    def destroy_session(self, request=None):
        """ Deletes the user session / logout """
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_session = UserSession.search({"session_id": session_id})
        if user_session:
            user_session[0].remove()
            return True
        return False
