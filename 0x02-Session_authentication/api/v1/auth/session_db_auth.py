#!/usr/bin/env python3
"""Session authentication with expiration
and storage support module for the API.
"""
from flask import request
from datetime import datetime, timedelta

from models.user_session import UserSession
from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """Session authentication class with expiration and storage support.
    """

    def create_session(self, user_id=None) -> str:
        """Creates and stores a session id for the user.
        """
        # Create a session ID using the parent method
        session_id = super().create_session(user_id)
        if type(session_id) == str:
            # Prepare data for storing session in the database
            kwargs = {
                'user_id': user_id,
                'session_id': session_id,
            }
            # Create and save a new UserSession instance
            user_session = UserSession(**kwargs)
            user_session.save()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieves the user id of the user associated with
        a given session id.
        """
        try:
            # Search for sessions in the database with the given session ID
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None
        cur_time = datetime.now()
        # Calculate expiration time based on session duration
        time_span = timedelta(seconds=self.session_duration)
        exp_time = sessions[0].created_at + time_span
        if exp_time < cur_time:
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None) -> bool:
        """Destroys an authenticated session.
        """
        session_id = self.session_cookie(request)
        try:
            # Search for sessions in the database with the given session ID
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(sessions) <= 0:
            return False
        # Remove the session from the database
        sessions[0].remove()
        return True
