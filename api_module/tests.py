import unittest
import json
from __init__ import app  # Import your Flask app instance
import os
from sessionholder import SessionHolder


class TestEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.db_address = f"{os.environ['BASE_DB_URL']}{os.environ['DB_PORTS']}{os.environ['DB_NAME']}"
        self.session_holder = SessionHolder(self.db_address)
        self.session = self.session_holder.create_session()

    def tearDown(self):
        pass

    def test_get_balance_success(self):
        response = self.app.get('/api/v1/wallets/test_uuid')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['balance'], 100)

    def test_get_balance_not_found(self):
        response = self.app.get('/api/v1/wallets/nonexistent_uuid')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'User not found')

    def test_deposit_success(self):
        data = {'action': 'DEPOSIT', 'amount': 50}
        response = self.app.post('/api/v1/wallets/test_uuid/operation', json=data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['balance'], 150)

    def test_withdraw_success(self):
        data = {'action': 'WITHDRAW', 'amount': 20}
        response = self.app.post('/api/v1/wallets/test_uuid/operation', json=data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['balance'], 80)

    def test_withdraw_insufficient_funds(self):
        data = {'action': 'WITHDRAW', 'amount': 150}
        response = self.app.post('/api/v1/wallets/test_uuid/operation', json=data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Operation failed')

    def test_invalid_request_data(self):
        # Missing 'action'
        data = {'amount': 50}
        response = self.app.post('/api/v1/wallets/test_uuid/operation', json=data)
        self.assertEqual(response.status_code, 400)

        # Missing 'amount'
        data = {'action': 'DEPOSIT'}
        response = self.app.post('/api/v1/wallets/test_uuid/operation', json=data)
        self.assertEqual(response.status_code, 400)

        # Invalid amount type
        data = {'action': 'DEPOSIT', 'amount': 'fifty'}
        response = self.app.post('/api/v1/wallets/test_uuid/operation', json=data)
        self.assertEqual(response.status_code, 400)
