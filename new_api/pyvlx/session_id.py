"""Module for generating a unique session_id."""


LAST_SESSION_ID = 0
MAX_SESSION_ID = 65535


def get_new_session_id():
    """Generate new session_id."""
    global LAST_SESSION_ID  # pylint: disable=global-statement
    LAST_SESSION_ID = LAST_SESSION_ID + 1
    if LAST_SESSION_ID > MAX_SESSION_ID:
        LAST_SESSION_ID = 1
    return LAST_SESSION_ID


def set_session_id(session_id):
    """Set session id to value."""
    global LAST_SESSION_ID  # pylint: disable=global-statement
    LAST_SESSION_ID = session_id
