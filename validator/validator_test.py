import unittest
import validator

class TestValidator(unittest.TestCase):
    def test_validate_password(self):
        self.assertTrue(validator.validate_password('password123&'))
        self.assertFalse(validator.validate_password('password123'))
        self.assertFalse(validator.validate_password('pass123'))
        self.assertFalse(validator.validate_password('password123А'))



