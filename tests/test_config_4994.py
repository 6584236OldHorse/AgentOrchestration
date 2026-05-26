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
        with self.assertRaises(ValueError) as ctx:
            self.config.get("a...b")
        self.assertIn("empty segment", str(ctx.exception).lower())

    def test_whitespace_in_segment_rejected(self):
        """Key with whitespace in segment should raise ValueError."""
        with self.assertRaises(ValueError) as ctx:
            self.config.get("foo .bar")
        self.assertIn("whitespace", str(ctx.exception).lower())

    def test_leading_whitespace_rejected(self):
        """Key with leading whitespace in segment should raise ValueError."""
        with self.assertRaises(ValueError) as ctx:
            self.config.get(" foo.bar")
        self.assertIn("whitespace", str(ctx.exception).lower())

    def test_trailing_whitespace_rejected(self):
        """Key with trailing whitespace in segment should raise ValueError."""
        with self.assertRaises(ValueError) as ctx:
            self.config.get("foo.bar ")
        self.assertIn("whitespace", str(ctx.exception).lower())

    def test_set_empty_key_rejected(self):
        """set() with empty key should raise ValueError."""
        with self.assertRaises(ValueError):
            self.config.set("", "value")

    def test_set_consecutive_dots_rejected(self):
        """set() with consecutive dots should raise ValueError."""
        with self.assertRaises(ValueError):
            self.config.set("foo..bar", "value")

    def test_set_whitespace_rejected(self):
        """set() with whitespace should raise ValueError."""
        with self.assertRaises(ValueError):
            self.config.set("foo .bar", "value")

    def test_valid_key_works(self):
        """Valid key should work normally."""
        self.config.set("foo.bar", "value")
        self.assertEqual(self.config.get("foo.bar"), "value")

    def test_valid_single_key_works(self):
        """Valid single-level key should work."""
        self.config.set("foo", "value")
        self.assertEqual(self.config.get("foo"), "value")

    def test_valid_deep_key_works(self):
        """Valid deeply nested key should work."""
        self.config.set("a.b.c.d", "value")
        self.assertEqual(self.config.get("a.b.c.d"), "value")

    def test_default_returned_for_missing(self):
        """Default value should be returned for missing key."""
        result = self.config.get("missing.key", "default")
        self.assertEqual(result, "default")


if __name__ == '__main__':
    unittest.main(verbosity=2)
