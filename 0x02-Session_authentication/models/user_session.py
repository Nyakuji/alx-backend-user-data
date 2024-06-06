#!/usr/bin/env python3
""" Module for User Session """
from sqlalchemy import Column, String
from models.base import Base


class UserSession(Base):
    __tablename__ = 'user_sessions'

    user_id = Column(String(60), nullable=False)
    session_id = Column(String(60), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
