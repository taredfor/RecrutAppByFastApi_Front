import unittest
import validator

class TestValidator(unittest.TestCase):
    def test_validate_password(self):
        self.assertTrue(validator.validate_password('password123&'))
        self.assertFalse(validator.validate_password('password123'))
        self.assertFalse(validator.validate_password('pass123'))
        self.assertFalse(validator.validate_password('password123А'))
    def test_validate_email(self):
        self.assertTrue(validator.validate_email('is-email@qwerty.ru'))
        #self.assertFalse(validator.validate_email('йцйуц@dsds.com'))
        self.assertFalse(validator.validate_email(''))


