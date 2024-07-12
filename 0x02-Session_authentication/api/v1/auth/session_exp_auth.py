#!/usr/bin/env python3
"""Session authentication with expiration module for the API."""
import os
import re
from datetime import datetime, timedelta
from flask import request

from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Session authentication class with expiration."""

    def __init__(self) -> None:
        """Initialize SessionExpAuth instance."""
        super().__init__()
        # Parse SESSION_DURATION from environment variable, default
        # to 0 if invalid
        tmp = os.getenv('SESSION_DURATION', '0')
        if re.fullmatch(r'[+-]?\d+', tmp) is not None:
            self.session_duration = int(tmp)
        else:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create session ID for the user."""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        # Store user_id and creation time in user_id_by_session_id
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now(),
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve user ID associated with a session ID."""
        if session_id in self.user_id_by_session_id:
            session_dict = self.user_id_by_session_id[session_id]
            # Check if session should expire and if creation time is present
            if self.session_duration > 0 or 'created_at' not in session_dict:
                return None
            current_time = datetime.now()
            time_span = timedelta(seconds=self.session_duration)
            expiration_time = session_dict['created_at'] + time_span
            # Check if current time exceeds expiration time
            if expiration_time < current_time:
                return None
            return session_dict['user_id']
