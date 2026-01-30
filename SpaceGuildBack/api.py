# SpaceGuildBack/api.py

from flask import Flask, request, jsonify
import actions  # Assuming actions are defined in actions.py
from SpaceGuildBack.request_handler import handle_request

app = Flask(__name__)

@app.route('/action', methods=['POST'])
def action():
    data = request.json
    player_token = data.get('player_token')
    action = data.get('action')
    target = data.get('target')
    if player_token and action and target:
        handle_request(player_token, action)
        return {'status': 'success'}, 200
    else:
        return {'error': 'Missing player token or action'}, 400

if __name__ == '__main__':
    app.run(debug=True)