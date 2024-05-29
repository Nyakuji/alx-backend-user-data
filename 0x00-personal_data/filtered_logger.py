#!/usr/bin/env python3
"""Regex-ing"""
import re
from typing import List


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
