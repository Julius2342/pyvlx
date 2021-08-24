"""Test for slip helper functions."""
import unittest

from pyvlx.api.session_id import get_new_session_id, set_session_id


class SessionIdSlip(unittest.TestCase):
    """Test class for slip helper functions."""

    # pylint: disable=invalid-name

    def test_session_id(self):
        """Decode encoded, encode decoded and test results."""
        set_session_id(0)  # Reset session id
        self.assertEqual(get_new_session_id(), 1)
        self.assertEqual(get_new_session_id(), 2)
        self.assertEqual(get_new_session_id(), 3)
        set_session_id(65535 - 1)
        self.assertEqual(get_new_session_id(), 65535)
        self.assertEqual(get_new_session_id(), 1)
