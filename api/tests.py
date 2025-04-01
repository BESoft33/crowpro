from django.test import TestCase
from unittest.mock import patch
from .auth import Staff


def mock_resolve_user(auth_header):
    if auth_header == "ValidToken":
        return "mock_user"
    return None


class StaffAuthenticationTest(TestCase):
    @patch('api.auth.resolve_user', side_effect=mock_resolve_user)
    def test_authenticate_valid_user(self, mock_resolve):
        request = type('Request', (object,), {"headers": {"Authorization": "ValidToken"}})()
        auth = Staff()
        user, _ = auth.authenticate(request)
        self.assertEqual(user, "mock_user")

    @patch('api.auth.resolve_user', side_effect=mock_resolve_user)
    def test_authenticate_invalid_user(self, mock_resolve):
        request = type('Request', (object,), {"headers": {"Authorization": "InvalidToken"}})()
        auth = Staff()
        result = auth.authenticate(request)
        self.assertIsNone(result)

    @patch('api.auth.resolve_user', side_effect=mock_resolve_user)
    def test_authenticate_no_auth_header(self, mock_resolve):
        request = type('Request', (object,), {"headers": {}})()
        auth = Staff()
        result = auth.authenticate(request)
        self.assertIsNone(result)
