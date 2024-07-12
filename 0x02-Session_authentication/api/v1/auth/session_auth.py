#!/usr/bin/env python3

"""Module for session authentication"""
import uuid
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """Session authentication class."""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a Session ID for a user_id."""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a User ID based on a Session ID."""
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Returns a User instance based on a cookie value."""
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if user_id:
            return User.get(user_id)
        return None

    def destroy_session(self, request=None):
        """
        Destroys an authenticated session.

        Parameters:
        - request: The Flask request object that contains the session cookie.

        Returns:
        - True if the session was successfully destroyed.
        - False if the session could not be destroyed.
        """
        # Retrieve the session ID from the request cookie
        session_id = self.session_cookie(request)

        # Retrieve the user ID associated with the session ID
        user_id = self.user_id_for_session_id(session_id)

        # If the request, session ID, or user ID is None, return False
        if (request is None or session_id is None) or user_id is None:
            return False

        # If the session ID exists in the session store, delete it
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]

        return True
