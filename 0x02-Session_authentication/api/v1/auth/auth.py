#!/usr/bin/env python3
"""Authentication module for the API."""
from typing import List, TypeVar
from flask import request
import re
import os


class Auth:
    """Authentication class."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if a path requires authentication.
        Args:
          - path: The path to check.
          - excluded_paths: A list of paths that do not require auth.
        Return:
          - False: Authentication is not required.
        """
        if path is not None and excluded_paths is not None:
            for exclusion_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ''
                if exclusion_path[-1] == '*':
                    pattern = '{}.*'.format(exclusion_path[0:-1])
                elif exclusion_path[-1] == '/':
                    pattern = '{}/*'.format(exclusion_path[0:-1])
                else:
                    pattern = '{}/*'.format(exclusion_path)
                if re.match(pattern, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """Gets the authorization header field from the request.
        Args:
          - request: The request object.
        Return:
          - None: No authorization header found.
        """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Gets the current user from the request.
        Args:
          - request: The request object.
        Return:
          - None: No current user found.
        """
        return None

    def session_cookie(self, request=None):
        """Returns a cookie value from a request."""
        if request is None:
            return None

        session_name = os.getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(session_name)
