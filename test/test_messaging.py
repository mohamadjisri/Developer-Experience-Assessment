import unittest
from unittest.mock import patch, Mock
import hmac
import hashlib
from simplemsg.messaging import Messaging

class TestMessaging(unittest.TestCase):

    def setUp(self):
        self.base_url = "https://api.example.com"
        self.api_key = "test_api_key"
        self.messaging = Messaging(self.base_url, self.api_key)

    @patch("simplemsg.messaging.requests.request")
    def test_create_contact(self, mock_request):
        mock_response = Mock()
        mock_response.json.return_value = {"id": "123", "name": "John Doe", "phone": "1234567890"}
        mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response

        response = self.messaging.create_contact("John Doe", "1234567890")

        self.assertEqual(response, {"id": "123", "name": "John Doe", "phone": "1234567890"})
        mock_request.assert_called_once_with(
            "POST",
            f"{self.base_url}/contacts",
            headers=self.messaging.headers,
            params=None,
            json={"name": "John Doe", "phone": "1234567890"},
        )

    @patch("simplemsg.messaging.requests.request")
    def test_get_contact(self, mock_request):
        mock_response = Mock()
        mock_response.json.return_value = {"id": "123", "name": "John Doe", "phone": "1234567890"}
        mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response

        response = self.messaging.get_contact("123")

        self.assertEqual(response, {"id": "123", "name": "John Doe", "phone": "1234567890"})
        mock_request.assert_called_once_with(
            "GET",
            f"{self.base_url}/contacts/123",
            headers=self.messaging.headers,
            params=None,
            json=None,
        )

    @patch("simplemsg.messaging.requests.request")
    def test_list_contacts(self, mock_request):
        mock_response = Mock()
        mock_response.json.return_value = {"contacts": []}
        mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response

        response = self.messaging.list_contacts(page_index=1, max_per_page=5)

        self.assertEqual(response, {"contacts": []})
        mock_request.assert_called_once_with(
            "GET",
            f"{self.base_url}/contacts",
            headers=self.messaging.headers,
            params={"pageIndex": 1, "max": 5},
            json=None,
        )

    @patch("simplemsg.messaging.requests.request")
    def test_update_contact(self, mock_request):
        mock_response = Mock()
        mock_response.json.return_value = {"id": "123", "name": "Jane Doe", "phone": "0987654321"}
        mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response

        response = self.messaging.update_contact("123", name="Jane Doe", phone="0987654321")

        self.assertEqual(response, {"id": "123", "name": "Jane Doe", "phone": "0987654321"})
        mock_request.assert_called_once_with(
            "PATCH",
            f"{self.base_url}/contacts/123",
            headers=self.messaging.headers,
            params=None,
            json={"name": "Jane Doe", "phone": "0987654321"},
        )

    @patch("simplemsg.messaging.requests.request")
    def test_delete_contact(self, mock_request):
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response

        response = self.messaging.delete_contact("123")

        self.assertEqual(response, {"message": "Contact deleted successfully"})
        mock_request.assert_called_once_with(
            "DELETE",
            f"{self.base_url}/contacts/123",
            headers=self.messaging.headers,
            params=None,
            json=None,
        )

    @patch("simplemsg.messaging.requests.request")
    def test_send_message(self, mock_request):
        mock_response = Mock()
        mock_response.json.return_value = {"id": "msg_123", "status": "sent"}
        mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response

        response = self.messaging.send_message("1234567890", "123", "Hello, world!")

        self.assertEqual(response, {"id": "msg_123", "status": "sent"})
        mock_request.assert_called_once_with(
            "POST",
            f"{self.base_url}/messages",
            headers=self.messaging.headers,
            params=None,
            json={"from": "1234567890", "to": {"id": "123"}, "content": "Hello, world!"},
        )

    @patch("simplemsg.messaging.requests.request")
    def test_get_message(self, mock_request):
        mock_response = Mock()
        mock_response.json.return_value = {"id": "msg_123", "status": "sent"}
        mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response

        response = self.messaging.get_message("msg_123")

        self.assertEqual(response, {"id": "msg_123", "status": "sent"})
        mock_request.assert_called_once_with(
            "GET",
            f"{self.base_url}/messages/msg_123",
            headers=self.messaging.headers,
            params=None,
            json=None,
        )

    @patch("simplemsg.messaging.requests.request")
    def test_list_messages(self, mock_request):
        mock_response = Mock()
        mock_response.json.return_value = {"messages": []}
        mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response

        response = self.messaging.list_messages(page=2, limit=50)

        self.assertEqual(response, {"messages": []})
        mock_request.assert_called_once_with(
            "GET",
            f"{self.base_url}/messages",
            headers=self.messaging.headers,
            params={"page": 2, "limit": 50},
            json=None,
        )

    def test_verify_webhook_signature(self):
        message = "test message"
        secret = "test_secret"
        signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()

        self.assertTrue(self.messaging.verify_webhook_signature(message, secret, signature))
        self.assertFalse(self.messaging.verify_webhook_signature(message, secret, "invalid_signature"))

if __name__ == "__main__":
    unittest.main()
