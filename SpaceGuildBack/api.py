# SpaceGuildBack/api.py
# Aidan Orion 24 Feb 2026
# Flask API for Space Guild game

from flask import Flask, request, jsonify
from typing import Optional, Dict, Any
import actions
import components
from program import data_handler

app = Flask(__name__)

# TODO: Implement proper authentication system
# For now, we'll use player_id directly (in production, use JWT tokens or similar)
def get_ship_id_from_player_id(player_id: int) -> Optional[int]:
    """Get the ship_id for a player.
    
    Args:
        player_id: Player ID
        
    Returns:
        Ship ID if player exists, None otherwise
    """
    try:
        player = data_handler.get_player(player_id)
        return player.get('ship_id')
    except KeyError:
        return None


@app.route('/action', methods=['POST'])
def queue_action_endpoint():
    """Queue an action for a ship to execute on the next tick.
    
    Request JSON format:
    {
        "player_id": int,
        "action_type": str,  # 'attack_ship', 'attack_ship_component', 'attack_item', 'move', 'collect'
        "target": int | str,  # ship_id/item_id (int) or location_name (str)
        "target_data": str (optional),  # e.g., component slot for attack_ship_component
        "action_hash": str (optional)  # Client-side hash for spam protection
    }
    
    Returns:
        {"status": "success"} or {"error": "message"}
    """
    try:
        data = request.json
        
        # Validate required fields
        player_id = data.get('player_id')
        action_type = data.get('action_type')
        target = data.get('target')
        
        if player_id is None or action_type is None or target is None:
            return jsonify({'error': 'Missing required fields: player_id, action_type, target'}), 400
        
        # Get ship_id from player_id
        ship_id = get_ship_id_from_player_id(player_id)
        if ship_id is None:
            return jsonify({'error': 'Invalid player_id or player has no ship'}), 404
        
        # Get optional fields
        target_data = data.get('target_data')
        action_hash = data.get('action_hash')
        
        # Queue the action
        success = actions.queue_action(ship_id, action_type, target, target_data, action_hash)
        
        if success:
            return jsonify({'status': 'success', 'message': 'Action queued'}), 200
        else:
            return jsonify({'error': 'Invalid action type or parameters'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/repair/component', methods=['POST'])
def repair_component_endpoint():
    """Repair a component by restoring health and applying multiplier reduction.
    
    Request JSON format:
    {
        "player_id": int,
        "item_id": int  # ID of the component to repair
    }
    
    Returns:
        {
            "status": "success",
            "health_restored": float,
            "multiplier_reduction": float,
            "new_multiplier": float,
            "health_percent_before": float
        } or {"error": "message"}
    """
    try:
        data = request.json
        player_id = data.get('player_id')
        item_id = data.get('item_id')
        
        if player_id is None or item_id is None:
            return jsonify({'error': 'Missing required fields: player_id, item_id'}), 400
        
        # Verify player exists (for authentication)
        ship_id = get_ship_id_from_player_id(player_id)
        if ship_id is None:
            return jsonify({'error': 'Invalid player_id or player has no ship'}), 404
        
        # Repair the component
        result = components.repair_component(item_id)
        
        return jsonify({
            'status': 'success',
            **result
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except KeyError:
        return jsonify({'error': 'Component not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'}), 200


if __name__ == '__main__':
    app.run(debug=True)