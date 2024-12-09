"""
Messaging Module
=================
This module provides a `Messaging` class to interact with an API for managing contacts and messages. It also includes a utility method for validating webhook signatures.

Features:
- Create, retrieve, update, and delete contacts.
- Send and retrieve messages.
- Verify webhook signatures using HMAC.
"""

import requests
import hmac
import hashlib
import json

class Messaging:
    """
    Messaging Class
    ================
    A class to handle communication with a messaging API, providing methods to manage contacts and messages.

    Attributes:
        base_url (str): The base URL of the API.
        headers (dict): The headers used for API requests, including the authorization token.
    """

    def __init__(self, base_url: str, api_key: str):
        """
        Initializes the Messaging class.

        Args:
            base_url (str): The base URL of the messaging API.
            api_key (str): The API key for authentication.
        """
        self.base_url = base_url.rstrip("/")
        self.headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    def _make_request(self, method: str, endpoint: str, params=None, data=None):
        """
        Makes a request to the API.

        Args:
            method (str): HTTP method (e.g., GET, POST, PATCH, DELETE).
            endpoint (str): The API endpoint.
            params (dict, optional): Query parameters for the request.
            data (dict, optional): JSON payload for the request.

        Returns:
            dict: The JSON response from the API.

        Raises:
            requests.exceptions.HTTPError: If the request returns an HTTP error status code.
        """
        url = f"{self.base_url}{endpoint}"
        
        response = requests.request(
            method, url, headers=self.headers, params=params, data=json.dumps(data) if data else data
        )
        
        response.raise_for_status()
        return None if method == "DELETE" else response.json()

    # Contacts
    def create_contact(self, name: str, phone: str):
        """
        Creates a new contact in the API.

        Args:
            name (str): The name of the contact.
            phone (str): The phone number of the contact.

        Returns:
            dict: The created contact details.
        """
        return self._make_request(
            "POST", "/contacts", data={"name": name, "phone": phone}
        )

    def get_contact(self, contact_id: str):
        """
        Retrieves details of a specific contact by ID.

        Args:
            contact_id (str): The ID of the contact to retrieve.

        Returns:
            dict: The contact details.
        """
        return self._make_request("GET", f"/contacts/{contact_id}")

    def list_contacts(self, page_index=0, max_per_page=10):
        """
        Lists all contacts with pagination.

        Args:
            page_index (int, optional): The page index (default is 0).
            max_per_page (int, optional): The maximum number of contacts per page (default is 10).

        Returns:
            dict: The paginated list of contacts.
        """
        return self._make_request(
            "GET", "/contacts", params={"pageIndex": page_index, "max": max_per_page}
        )

    def update_contact(self, contact_id: str, name: str = None, phone: str = None):
        """
        Updates an existing contact's details.

        Args:
            contact_id (str): The ID of the contact to update.
            name (str, optional): The updated name of the contact.
            phone (str, optional): The updated phone number of the contact.

        Returns:
            dict: The updated contact details.
        """
        update_data = {"name": name, "phone": phone}
        return self._make_request("PATCH", f"/contacts/{contact_id}", data=update_data)

    def delete_contact(self, contact_id: str):
        """
        Deletes a contact by ID.

        Args:
            contact_id (str): The ID of the contact to delete.

        Returns:
            dict: A message indicating successful deletion.
        """
        self._make_request("DELETE", f"/contacts/{contact_id}")
        return {"message": "Contact deleted successfully"}

    # Messages
    def send_message(self, from_phone: str, to_contact_id: str, content: str):
        """
        Sends a message to a specific contact.

        Args:
            from_phone (str): The sender's phone number.
            to_contact_id (str): The recipient contact's ID.
            content (str): The message content.

        Returns:
            dict: The details of the sent message.
        """
        return self._make_request(
            "POST",
            "/messages",
            data={"from": from_phone, "to": {"id": to_contact_id}, "content": content},
        )

    def get_message(self, message_id: str):
        """
        Retrieves details of a specific message by ID.

        Args:
            message_id (str): The ID of the message to retrieve.

        Returns:
            dict: The message details.
        """
        return self._make_request("GET", f"/messages/{message_id}")

    def list_messages(self, page=1, limit=100):
        """
        Lists all messages with pagination.

        Args:
            page (int, optional): The page number (default is 1).
            limit (int, optional): The maximum number of messages per page (default is 100).

        Returns:
            dict: The paginated list of messages.
        """
        return self._make_request("GET", "/messages", params={"page": page, "limit": limit})

    # Webhook Signature Validation
    @staticmethod
    def verify_webhook_signature(message: str, secret: str, signature: str) -> bool:
        """
        Verifies the signature of a webhook request using HMAC.

        Args:
            message (str): The webhook request body.
            secret (str): The secret key used to generate the signature.
            signature (str): The signature to verify.

        Returns:
            bool: True if the signature is valid, False otherwise.
        """
        computed_signature = hmac.new(
            secret.encode(), message.encode(), hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(computed_signature, signature)
