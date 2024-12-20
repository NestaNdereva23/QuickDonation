import requests
import base64
import datetime
import os
import logging

logger = logging.getLogger(__name__)

class MpesaClient:
    def __init__(self):
        self.consumer_key = os.getenv('MPESA_CONSUMER_KEY')
        self.consumer_secret = os.getenv('MPESA_CONSUMER_SECRET')
        self.shortcode = os.getenv('MPESA_SHORTCODE')
        self.passkey = os.getenv('MPESA_PASSKEY')
        self.access_token_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
        self.stk_push_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'

    def get_access_token(self):
        auth_string = f"{self.consumer_key}:{self.consumer_secret}"
        base64_bytes = base64.b64encode(auth_string.encode('ascii'))

        headers = {
            'Authorization': f'Basic {base64_bytes.decode("ascii")}'
        }

        try:
            response = requests.get(self.access_token_url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json().get('access_token')
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching access token: {e}")
            return None

    def generate_password(self):
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        password_string = f"{self.shortcode}{self.passkey}{timestamp}"
        return base64.b64encode(password_string.encode('ascii')).decode('ascii'), timestamp

    def initiate_stk_push(self, phone_number, amount, account_reference='QuickDonate'):
        access_token = self.get_access_token()
        if not access_token:
            logger.error("Failed to fetch access token.")
            return None

        password, timestamp = self.generate_password()
        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "PartyA": phone_number,
            "Amount": int(amount),
            "PartyB": self.shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": "https://c61e-41-209-57-164.ngrok-free.app/mpesa/callback",
            "AccountReference": account_reference,
            "TransactionDesc": "Donation"
        }

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(self.stk_push_url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error initiating STK push: {e}")
            return None
