from flask import Blueprint, jsonify, request
from utils.mailjet_service import send_email, send_booking_confirmation
from utils.jwt_service import token_required

email_bp = Blueprint('email_bp', __name__)

@email_bp.route('/send', methods=['POST'])
@token_required
def send_custom_email(current_user_id, current_user_role):
    """
    Send a custom email.
    Expects JSON: {"to_email": "user@example.com", "to_name": "User Name", "subject": "Subject", "text_content": "Content", "html_content": "Optional HTML"}
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    to_email = data.get('to_email')
    to_name = data.get('to_name')
    subject = data.get('subject')
    text_content = data.get('text_content')
    html_content = data.get('html_content')

    if not all([to_email, to_name, subject, text_content]):
        return jsonify({"error": "Missing required fields: to_email, to_name, subject, text_content"}), 400

    status_code, response = send_email(to_email, to_name, subject, text_content, html_content)

    if status_code == 200:
        return jsonify({"message": "Email sent successfully", "response": response}), 200
    else:
        return jsonify({"error": "Failed to send email", "response": response}), 500

@email_bp.route('/test', methods=['POST'])
@token_required
def send_test_email(current_user_id, current_user_role):
    """
    Send a test email to verify Mailjet integration.
    Expects JSON: {"to_email": "test@example.com", "to_name": "Test User"}
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    to_email = data.get('to_email')
    to_name = data.get('to_name')

    if not to_email or not to_name:
        return jsonify({"error": "Missing to_email or to_name"}), 400

    subject = "Test Email from SafariHub"
    text_content = f"Hello {to_name}, this is a test email from SafariHub to verify Mailjet integration."
    html_content = f"<h1>Test Email</h1><p>Hello {to_name}, this is a test email from SafariHub to verify Mailjet integration.</p>"

    status_code, response = send_email(to_email, to_name, subject, text_content, html_content)

    if status_code == 200:
        return jsonify({"message": "Test email sent successfully", "response": response}), 200
    else:
        return jsonify({"error": "Failed to send test email", "response": response}), 500
