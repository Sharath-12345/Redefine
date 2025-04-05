# api/index.py

import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def send_notification():
    try:
        data = request.json
        fcm_token = data.get('fcm_token')
        title = data.get('title', 'Default Title')
        message = data.get('message', 'Default Message')

        if not fcm_token:
            return jsonify({'error': 'Missing FCM token'}), 400

        # Get FCM server key from environment variables
        server_key = os.environ.get('FCM_SERVER_KEY')
        if not server_key:
            return jsonify({'error': 'Missing FCM_SERVER_KEY'}), 500

        # Construct FCM payload
        payload = {
            'to': fcm_token,
            'notification': {
                'title': title,
                'body': message,
                'sound': 'default'
            },
            'priority': 'high'
        }

        # Send POST request to FCM
        headers = {
            'Authorization': f'key={server_key}',
            'Content-Type': 'application/json'
        }

        response = requests.post('https://fcm.googleapis.com/fcm/send',
                                 headers=headers,
                                 json=payload)

        return jsonify({
            'status': 'success',
            'fcm_response': response.json()
        }), response.status_code

    except Exception as e:
        return jsonify({'error': str(e)}), 500
