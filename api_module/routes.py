from flask import redirect, request, jsonify
import os

from sessionholder import UuidStorage

from . import app
from .accountholder import AccountCommand

storage = UuidStorage(f"{os.environ['BASE_DB_URL']}{os.environ['DB_PORTS']}{os.environ['DB_NAME']}")
storage.connect()
account_command = AccountCommand(storage)


@app.route("os.environ['BASE_URL']}/<uuid:wallet_uuid>", methods=['GET'])
def get_balance(wallet_uuid):
    balance = storage.get_balance_by_uuid(wallet_uuid)
    if balance is not None:
        return jsonify({'balance': balance}), 200
    else:
        return jsonify({'error': 'User not found'}), 404


@app.route(f"{os.environ['BASE_URL']}/<uuid:wallet_uuid>/operation", methods=['POST'])
def execute_operation(wallet_uuid):  # Renamed for clarity
    data = request.get_json()
    if not data or 'action' not in data or 'amount' not in data:
        return jsonify({'error': 'Invalid request data'}), 400

    action = data['action'].upper()
    amount = data['amount']

    if not isinstance(amount, (int, float)):
        return jsonify({'error': 'Amount must be a number'}), 400

    new_balance = account_command.take_action(wallet_uuid, action, amount)

    if new_balance is not False:
        storage.update_balance_by_uuid(wallet_uuid, new_balance)
        return jsonify({'message': 'Operation successful', 'balance': new_balance}), 200
    else:
        return jsonify({'error': 'Operation failed',
                        'balance': storage.get_balance_by_uuid(wallet_uuid)}), 400
