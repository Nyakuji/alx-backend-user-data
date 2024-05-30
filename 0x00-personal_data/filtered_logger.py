#!/usr/bin/env python3
"""Regex-ing"""
import os
import re
import mysql.connector
import logging
from mysql.connector.connection import MySQLConnection
from typing import List

# Define PII fields
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """
    Obfuscates specified fields in a log message.

    Args:
        fields (list[str]): List of strings representing fields to obfuscate.
        redaction (str): String representing the obfuscation value.
        message (str): Log line to process.
        separator (str): Character separating fields in the log line.

    Returns:
        str: Obfuscated log message.
    """
    return re.sub(r'({})=(.*?){}'.format('|'.join(fields), separator),
                  r'\1={}{}'.format(redaction, separator), message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record and redact sensitive information.

            Args:
                record (logging.LogRecord): The log record to be formatted.

            Returns:
                str: The formatted log record with redacted
                sensitive information.

        """
        original_message = super().format(record)
        return filter_datum(
            self.fields,
            self.REDACTION,
            original_message,
            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    Creates and returns a logger object with specific configuration.

    Returns:
        logging.Logger: Configured logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(list(PII_FIELDS))
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def get_db() -> MySQLConnection:
    """
    Creates and returns a connection to the database using credentials
    from environment variables.

    Returns:
        MySQLConnection: A MySQL connection object.
    """
    # Retrieve database credentials from environment variables
    db_username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    # Establish and return the database connection
    connection = mysql.connector.connect(
        user=db_username,
        password=db_password,
        host=db_host,
        database=db_name
    )
    return connection


def main() -> None:
    """
    Main function that retrieves all rows in the users table
    and displays each row under a filtered format.
    """
    # Get database connection
    db_connection = get_db()
    cursor = db_connection.cursor(dictionary=True)

    # Execute query to retrieve all rows from the users table
    cursor.execute("SELECT * FROM users")

    # Get logger
    logger = get_logger()

    # Fetch and log each row
    for row in cursor:
        message = "; ".join([f"{key}={value}" for key, value in row.items()])
        logger.info(message)

    # Close cursor and connection
    cursor.close()
    db_connection.close()


if __name__ == "__main__":
    main()
