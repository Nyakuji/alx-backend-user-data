#!/usr/bin/env python3
"""Hash password"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password with a salt using bcrypt.

    Args:
        password (str): The plain text password to hash.

    Returns:
        bytes: The salted, hashed password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates whether the provided password matches the hashed password.

    Args:
        hashed_password (bytes): The salted, hashed password.
        password (str): The plain text password to validate.

    Returns:
        bool: True if the provided password matches
        the hashed password, False otherwise.
    """
    # Use bcrypt's checkpw function to verify the password
    return bcrypt.checkpw(password.encode(), hashed_password)
