#!/usr/bin/env python3
"""Module of session authenticating views.
"""
import os
from typing import Tuple
from flask import abort, jsonify, request

from models.user import User
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """POST /api/v1/auth_session/login
    Return:
      - JSON representation of a User object.
    """
    not_found_res = { "error": "no user found for this email" }
    # Retrieve email from the request form
    email = request.form.get('email')
    if email is None or len(email.strip()) == 0:
        return jsonify({ "error": "email missing" }), 400
    # Retrieve password from the request form
    password = request.form.get('password')
    if password is None or len(password.strip()) == 0:
        return jsonify({ "error": "password missing" }), 400
    try:
        # Search for users with the given email
        users = User.search({'email': email})
    except Exception:
        return jsonify(not_found_res), 404
    # If no user is found
    if len(users) <= 0:
        return jsonify(not_found_res), 404
    # Validate the password for the found user
    if users[0].is_valid_password(password):
        from api.v1.app import auth  # Import auth only when needed
        # Create a session ID for the user
        sessiond_id = auth.create_session(getattr(users[0], 'id'))
        # Create a response with the user data in JSON format
        res = jsonify(users[0].to_json())
        # Set the session ID in the response cookie
        res.set_cookie(os.getenv("SESSION_NAME"), sessiond_id)
        return res
    # Return error if the password is incorrect
    return jsonify({ "error": "wrong password" }), 401


@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout() -> Tuple[str, int]:
    """DELETE /api/v1/auth_session/logout
    Return:
      - An empty JSON object.
    """
    from api.v1.app import auth
    is_destroyed = auth.destroy_session(request)
    if not is_destroyed:
        abort(404)
    return jsonify({})
