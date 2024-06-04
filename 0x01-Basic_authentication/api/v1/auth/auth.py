#!/usr/bin/env python3
""" Auth module"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Auth class for handling authentication and authorization.

    Methods:
    - require_auth(path: str, excluded_paths: List[str]) -> bool: Checks if authentication is required for the given path.
    - authorization_header(request=None) -> str: Retrieves the authorization header from the request.
    - current_user(request=None) -> TypeVar('User'): Retrieves the current user based on the request.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if authentication is required for the given path.

        Args:
        - path (str): The path to check.
        - excluded_paths (List[str]): List of paths that are excluded from authentication.

        Returns:
        - bool: True if authentication is required, False otherwise.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the request.

        Args:
        - request (optional): The request object.

        Returns:
        - str: The authorization header.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user based on the request.

        Args:
        - request (optional): The request object.

        Returns:
        - TypeVar('User'): The current user.
        """
        return None
