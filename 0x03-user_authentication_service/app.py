#!/usr/bin/env python3
"""app module"""
from flask import Flask, jsonify
from auth import Auth
from flask import request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
