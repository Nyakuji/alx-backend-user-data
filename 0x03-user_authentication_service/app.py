#!/usr/bin/env python3
"""app module"""
from flask import Flask, jsonify, request, abort
from auth import Auth
from typing import Dict, Union, Tuple


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def welcome() -> str:
    """Returns a JSON payload with a welcome message"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user() -> Union[Dict[str, str], Tuple[Dict[str, str], int]]:
    """Registers a new user"""
    try:
        email = request.form.get("email")
        password = request.form.get("password")
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login() -> Union[Dict[str, str], Tuple[Dict[str, str], int]]:
    """Logs in a user"""
    try:
        email = request.form.get("email")
        password = request.form.get("password")
        if not AUTH.valid_login(email, password):
            abort(401)
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    except ValueError:
        abort(401)


@app.route("/sessions", methods=["DELETE"])
def logout() -> Union[Dict[str, str], Tuple[Dict[str, str], int]]:
    """Logs out a user"""
    session_id = request.cookies.get("session_id")
    if session_id is None:
        abort(403)
    email = AUTH.get_user_from_session_id(session_id)
    if email is None:
        abort(403)
    AUTH.destroy_session(email)
    response = jsonify({"message": "logout successful"})
    response.delete_cookie("session_id")
    return response

    redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
