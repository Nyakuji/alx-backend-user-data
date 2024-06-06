#!/usr/bin/env python3
""" Module for Session Authentication Views """
from flask import jsonify, request
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ POST /api/v1/auth_session/login
    Handle user login and session creation
    """
    from api.v1.app import auth

    email: str = request.form.get('email')
    password: str = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    user: User = User.search({"email": email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    user = user[0]  # assuming search returns a list of users
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id: str = auth.create_session(user.id)
    user_json: dict = user.to_json()

    response: str = jsonify(user_json)
    session_name: str = getenv("SESSION_NAME")
    response.set_cookie(session_name, session_id)

    return response
