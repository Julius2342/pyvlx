"""Module for generating a unique session_id."""


_last_session_id = 0  # pylint: disable=invalid-name; ignore this false positive until https://github.com/pylint-dev/pylint/issues/10768 is resolved
MAX_SESSION_ID = 65535


def get_new_session_id() -> int:
    """Generate new session_id."""
    global _last_session_id  # pylint: disable=global-statement
    _last_session_id = _last_session_id + 1
    if _last_session_id > MAX_SESSION_ID:
        _last_session_id = 1
    return _last_session_id


def set_session_id(session_id: int) -> None:
    """Set session id to value."""
    global _last_session_id  # pylint: disable=global-statement
    _last_session_id = session_id
