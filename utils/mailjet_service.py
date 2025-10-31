from mailjet_rest import Client
from config import Config

mailjet = Client(auth=(Config.MAILJET_API_KEY, Config.MAILJET_SECRET_KEY), version='v3.1')

def send_email(to_email, to_name, subject, text_content, html_content=None):
    """
    Send an email using Mailjet API.

    :param to_email: Recipient's email address
    :param to_name: Recipient's name
    :param subject: Email subject
    :param text_content: Plain text content
    :param html_content: HTML content (optional)
    :return: Response from Mailjet API
    """
    data = {
        'Messages': [
            {
                "From": {
                    "Email": Config.SENDER_EMAIL,
                    "Name": Config.SENDER_NAME
                },
                "To": [
                    {
                        "Email": to_email,
                        "Name": to_name
                    }
                ],
                "Subject": subject,
                "TextPart": text_content,
                "HTMLPart": html_content
            }
        ]
    }

    result = mailjet.send.create(data=data)
    return result.status_code, result.json()

def send_booking_confirmation(user_email, user_name, booking_details):
    """
    Send booking confirmation email.

    :param user_email: User's email
    :param user_name: User's name
    :param booking_details: Dictionary with booking info
    """
    subject = "Booking Confirmation - SafariHub"
    text_content = f"""
    Dear {user_name},

    Your booking has been confirmed!

    Details:
    - Destination: {booking_details.get('destination', 'N/A')}
    - Travel Date: {booking_details.get('travel_date', 'N/A')}
    - Number of People: {booking_details.get('number_of_people', 'N/A')}
    - Total Amount: ${booking_details.get('total_amount', 'N/A')}

    Thank you for choosing SafariHub!

    Best regards,
    SafariHub Team
    """

    html_content = f"""
    <html>
    <body>
        <h2>Booking Confirmation</h2>
        <p>Dear {user_name},</p>
        <p>Your booking has been confirmed!</p>
        <ul>
            <li><strong>Destination:</strong> {booking_details.get('destination', 'N/A')}</li>
            <li><strong>Travel Date:</strong> {booking_details.get('travel_date', 'N/A')}</li>
            <li><strong>Number of People:</strong> {booking_details.get('number_of_people', 'N/A')}</li>
            <li><strong>Total Amount:</strong> ${booking_details.get('total_amount', 'N/A')}</li>
        </ul>
        <p>Thank you for choosing SafariHub!</p>
        <p>Best regards,<br>SafariHub Team</p>
    </body>
    </html>
    """

    return send_email(user_email, user_name, subject, text_content, html_content)
