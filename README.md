# SimpleMsg SDK

`SimpleMsg` is a Python SDK designed to simplify interaction with messaging APIs. It provides an easy-to-use interface for managing contacts, sending and retrieving messages, and verifying webhook signatures.

## Features
- **Contacts Management:** Create, retrieve, update, and delete contacts effortlessly.
- **Messaging:** Send messages, retrieve message details, and list messages with pagination.
- **Webhook Security:** Verify webhook signatures using HMAC for secure communication.

## Installation
Install the package via pip:
```bash
pip install simplemsg
```

## Getting Started

### Initialization
To start using `SimpleMsg`, initialize the `Messaging` class with your API base URL and API key:
```python
from simplemsg import Messaging

# Initialize the SDK
base_url = "https://api.example.com"
api_key = "your_api_key"
messaging = Messaging(base_url, api_key)
```

### Contacts Management

#### Create a Contact
```python
response = messaging.create_contact(name="John Doe", phone="1234567890")
print(response)
```

#### Get a Contact
```python
response = messaging.get_contact(contact_id="123")
print(response)
```

#### List Contacts
```python
response = messaging.list_contacts(page_index=1, max_per_page=5)
print(response)
```

#### Update a Contact
```python
response = messaging.update_contact(contact_id="123", name="Jane Doe", phone="0987654321")
print(response)
```

#### Delete a Contact
```python
response = messaging.delete_contact(contact_id="123")
print(response)
```

### Messaging

#### Send a Message
```python
response = messaging.send_message(from_phone="1234567890", to_contact_id="123", content="Hello, World!")
print(response)
```

#### Get a Message
```python
response = messaging.get_message(message_id="msg_123")
print(response)
```

#### List Messages
```python
response = messaging.list_messages(page=1, limit=10)
print(response)
```

### Webhook Signature Validation

#### Verify Webhook Signature
```python
message = "example payload"
secret = "your_secret_key"
signature = "provided_signature"

is_valid = Messaging.verify_webhook_signature(message, secret, signature)
print("Signature is valid:", is_valid)
```

## Error Handling
The SDK raises exceptions for HTTP errors. Wrap your API calls in try-except blocks:
```python
try:
    response = messaging.create_contact(name="John Doe", phone="1234567890")
    print(response)
except requests.exceptions.HTTPError as e:
    print("API Error:", e)
```

## Dependencies
- `requests`
- `hmac`
- `hashlib`
- `json`

## Contributing
Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

