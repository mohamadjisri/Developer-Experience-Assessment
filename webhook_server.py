from flask import Flask, request, jsonify
from sinch_sdk import SinchSDK

app = Flask(__name__)

# Initialize the SDK
sdk = SinchSDK(base_url="http://localhost:3000", api_key="there-is-no-key")

WEBHOOK_SECRET = "mySecret"


@app.route("/webhooks", methods=["POST"])
def handle_webhook():
    # Validate Signature
    signature = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not sdk.verify_webhook_signature(
        request.data.decode("utf-8"), WEBHOOK_SECRET, signature
    ):
        return jsonify({"error": "Invalid signature"}), 403

    # Process Event
    event = request.json
    print("Received Webhook Event:", event)
    return jsonify({"status": "Received"}), 200


if __name__ == "__main__":
    app.run(port=3010)
