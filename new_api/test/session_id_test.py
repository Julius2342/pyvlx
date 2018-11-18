"""Test for slip helper functions."""
import unittest
from pyvlx.session_id import get_new_session_id, set_session_id


class SessionIdSlip(unittest.TestCase):
    """Test class for slip helper functions."""

    # pylint: disable=invalid-name

    def test_session_id(self):
        """Decode encoded, encode decoded and test results."""
        self.assertEqual(get_new_session_id(), 1)
        self.assertEqual(get_new_session_id(), 2)
        self.assertEqual(get_new_session_id(), 3)
        set_session_id(65535 - 1)
        self.assertEqual(get_new_session_id(), 65535)
        self.assertEqual(get_new_session_id(), 1)
