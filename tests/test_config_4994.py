"""Tests for Config empty key validation."""

import os
import sys
import unittest

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from common.config import Config


class TestConfigKeyValidation(unittest.TestCase):
    """Regression tests for Issue #4994: Reject empty dotted config keys."""

    def setUp(self):
        self.config = Config()

    def test_empty_key_rejected(self):
        """Empty string key should raise ValueError."""
        with self.assertRaises(ValueError) as ctx:
            self.config.get("")
        self.assertIn("empty", str(ctx.exception).lower())

    def test_leading_dot_rejected(self):
        """Key starting with dot should raise ValueError."""
        with self.assertRaises(ValueError) as ctx:
            self.config.get(".foo")
        self.assertIn("empty segment", str(ctx.exception).lower())

    def test_trailing_dot_rejected(self):
        """Key ending with dot should raise ValueError."""
        with self.assertRaises(ValueError) as ctx:
            self.config.get("foo.")
        self.assertIn("empty segment", str(ctx.exception).lower())

    def test_consecutive_dots_rejected(self):
        """Key with consecutive dots should raise ValueError."""
        with self.assertRaises(ValueError) as ctx:
            self.config.get("foo..bar")
        self.assertIn("empty segment", str(ctx.exception).lower())

    def test_multiple_consecutive_dots_rejected(self):
        """Key with multiple consecutive dots should raise ValueError."""
        with self.assertRaises(ValueError):
            self.config.get("a...b")

    def test_valid_key_works(self):
        """Valid dotted key should work normally."""
        self.config.set("foo.bar", "value")
        self.assertEqual(self.config.get("foo.bar"), "value")

    def test_valid_single_key_works(self):
        """Single-segment key should work."""
        self.config.set("key", "value")
        self.assertEqual(self.config.get("key"), "value")

    def test_set_empty_key_rejected(self):
        """set() with empty key should raise ValueError."""
        with self.assertRaises(ValueError):
            self.config.set("", "value")

    def test_set_consecutive_dots_rejected(self):
        """set() with consecutive dots should raise ValueError."""
        with self.assertRaises(ValueError):
            self.config.set("a..b", "value")

    def test_error_message_includes_key(self):
        """Error message should include the problematic key."""
        with self.assertRaises(ValueError) as ctx:
            self.config.get("foo..bar")
        self.assertIn("foo..bar", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
