"""Unit test for roller shutter."""
import unittest

from pyvlx.exception import PyVLXException


# pylint: disable=too-many-public-methods,invalid-name
class TestException(unittest.TestCase):
    """Test class for roller shutter."""

    def test_str(self):
        """Test string representation of PyVLXException."""
        exception = PyVLXException("fnord fnord")
        self.assertEqual(str(exception), '<PyVLXException description="fnord fnord" />')

    def test_str_with_parameter(self):
        """Test string representation of PyVLXException with parameter."""
        exception = PyVLXException("fnord fnord", fnord="fnord", bla="blub")
        self.assertEqual(
            str(exception),
            '<PyVLXException description="fnord fnord" bla="blub" fnord="fnord"/>',
        )
