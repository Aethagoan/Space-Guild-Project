# SpaceGuildBack/api.py

from flask import Flask, request, jsonify
import actions  # Assuming actions are defined in actions.py
from SpaceGuildBack.request_handler import handle_request

app = Flask(__name__)

@app.route('/move', methods=['POST'])
def move_spaceship():
    data = request.json
    player_token = data.get('player_token')
    action = 'move'
    
    if not player_token:
        return jsonify({"error": "Missing player_token"}), 400
    
    if not target_token:
        return jsonify({"error": "Target token is not present"}), 400
    
    result = actions.move(player_token, target_token)
    return jsonify(result)

@app.route('/attack', methods=['POST'])
def attack_spaceship():
    data = request.json
    player_token = data.get('player_token')
    action = 'attack'
    
    if not player_token:
        return jsonify({"error": "Missing player_token"}), 400
    
    if not target_token:
        return jsonify({"error": "Target token is not present"}), 400
    
    result = actions.attack(player_token, target_token)
    return jsonify(result)

@app.route('/collect', methods=['POST'])
def heal_spaceship():
    data = request.json
    player_token = data.get('player_token')
    action = 'collect'
    
    if not player_token:
        return jsonify({"error": "Missing player_token"}), 400
    
    if not target_token:
        return jsonify({"error": "Target token is not present"}), 400
    
    result = actions.collect(player_token, target_token)
    return jsonify(result)

@app.route('/action', methods=['POST'])
def action():
    data = request.json
    player_token = data.get('player_token')
    action = data.get('action')
    if player_token and action:
        handle_request(player_token, action)
        return {'status': 'success'}, 200
    else:
        return {'error': 'Missing player token or action'}, 400

if __name__ == '__main__':
    app.run(debug=True)