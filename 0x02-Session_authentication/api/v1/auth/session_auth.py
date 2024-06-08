#!/usr/bin/env python3
"""Basic authentication module for the API.
"""
from uuid import uuid4

from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """Basic authentication class.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session id for the user.
        """
        if type(user_id) is str:
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on a Session ID
        """
        if isinstance(session_id, str):
            return self.user_id_by_session_id.get(session_id)
