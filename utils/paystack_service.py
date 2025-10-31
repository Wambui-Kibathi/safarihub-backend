import requests
import os

class PayStackService:
    def __init__(self):
        self.secret_key = os.getenv('PAYSTACK_SECRET_KEY', 'sk_test_your_secret_key_here')
        self.base_url = 'https://api.paystack.co'
        self.headers = {
            'Authorization': f'Bearer {self.secret_key}',
            'Content-Type': 'application/json'
        }

    def initialize_transaction(self, email, amount, reference, metadata=None):
        """
        Initialize a PayStack transaction
        """
        try:
            url = f'{self.base_url}/transaction/initialize'
            data = {
                'email': email,
                'amount': amount * 100,  # Convert to kobo
                'reference': reference,
                'callback_url': os.getenv('PAYSTACK_CALLBACK_URL', 'http://localhost:3000/payment/callback'),
                'metadata': metadata or {}
            }

            response = requests.post(url, json=data, headers=self.headers)
            result = response.json()

            if response.status_code == 200 and result.get('status'):
                return {
                    'success': True,
                    'authorization_url': result['data']['authorization_url'],
                    'reference': result['data']['reference'],
                    'access_code': result['data']['access_code']
                }
            else:
                return {
                    'success': False,
                    'error': result.get('message', 'Transaction initialization failed')
                }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def verify_transaction(self, reference):
        """
        Verify a PayStack transaction
        """
        try:
            url = f'{self.base_url}/transaction/verify/{reference}'
            response = requests.get(url, headers=self.headers)
            result = response.json()

            if response.status_code == 200 and result.get('status'):
                return {
                    'success': True,
                    'data': result['data']
                }
            else:
                return {
                    'success': False,
                    'error': result.get('message', 'Transaction verification failed')
                }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

paystack_service = PayStackService()
