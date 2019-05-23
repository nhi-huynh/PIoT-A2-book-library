# vim: set et sw=4 ts=4 sts=4:
from class_.Auth import Auth
import unittest

class AuthTest(unittest.TestCase):

    def test_encrypt_verify(self):
        test_passwd = 'test_password_1234'

        cipher = Auth.encrypt_passwd(test_passwd)

        self.assertTrue(Auth.verify_passwd(test_passwd, cipher))
        self.assertFalse(Auth.verify_passwd('test_password_123', cipher))

    def test_validate_valid_usernames(self):
        valid = [
            'David', # Min chars (5)
            'abcdeabcdeabcdeabcdeabcde', # Max chars (25)
            's3662167', # Start with letter
            'a__--013495-__-_9', # All allowed chars, end with number
        ]

        for uname in valid:
            self.assertTrue(Auth.validate_username(uname))

    def test_validate_invalid_usernames(self):
        invalid = [
            '5Davlid', # Starting with number
            'asdf', # Lower than min chars (5)
            'asdfasdfasdfasdfasdfasdfas', # Greater than max chars (25)
            'aaaaaa;%a', # Contains invalid chars
            'asdfasdf_', # Doesnt end with number/letter
        ]

        for uname in invalid:
            self.assertFalse(Auth.validate_username(uname))

    def test_validate_valid_emails(self):
        valid = [
            'valid@google.com',
            'valid@google.com.au',
            244 * 'a' + '@google.com', # Max chars (255)
            'abc123.+%%a@something-.123.com-123',
        ]

        for email in valid:
            self.assertTrue(Auth.validate_email(email))

    def test_validate_invalid_emails(self):
        invalid = [
            'invalid@google@com',
            'a~bcde@google.com',
            'invalid',
            'invalid@something',
            245 * 'a' + '@google.com', # Max chars (255) + 1
            'invalid@gmail%.com'
        ]

        for email in invalid:
            self.assertFalse(Auth.validate_email(email))
