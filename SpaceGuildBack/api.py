# SpaceGuildBack/api.py
# Aidan Orion 24 Feb 2026
# Flask API for Space Guild game
# This runs as a SEPARATE PROCESS from the game loop (program.py)

from flask import Flask, request, jsonify
from typing import Optional, Dict, Any
import os
import actions
import components
from program import data_handler

app = Flask(__name__)


def check_world_initialized(data_dir: str = "game_data") -> bool:
    """Check if the world has been initialized.
    
    Args:
        data_dir: Directory where game data should be stored
        
    Returns:
        True if world data exists, False otherwise
    """
    locations_file = os.path.join(data_dir, "locations.json")
    return os.path.exists(locations_file)


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


@app.route('/ship/log', methods=['GET'])
def get_ship_log_endpoint():
    """Get ephemeral log entries for a player's ship.
    
    Query parameters:
        player_id: int - Player ID
    
    Returns:
        {
            "entries": [
                {
                    "type": str,  # Message type (combat, action, ship_message, computer, environment)
                    "content": str,  # The log message
                    "source": str (optional)  # Source identifier (e.g., "ship:123", "location:Sol", "item:456")
                },
                ...
            ]
        } or {"error": "message"}
        
    Note: The "source" field allows the frontend to route clicks to the appropriate detail view.
          Format is "entity_type:entity_id" where entity_type is ship/location/item/faction/player.
          The frontend is responsible for calling the appropriate endpoint based on entity_type.
    """
    try:
        player_id = request.args.get('player_id', type=int)
        
        if player_id is None:
            return jsonify({'error': 'Missing required parameter: player_id'}), 400
        
        # Get ship_id from player_id
        ship_id = get_ship_id_from_player_id(player_id)
        if ship_id is None:
            return jsonify({'error': 'Invalid player_id or player has no ship'}), 404
        
        # Get ship logs
        entries = data_handler.get_ship_log(ship_id)
        
        return jsonify({'entries': entries}), 200
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


if __name__ == '__main__':
    # Check if world is initialized before starting API
    if not check_world_initialized():
        print("=" * 70)
        print("[X] ERROR: World not initialized!")
        print("=" * 70)
        print("\nPlease run 'python setup.py' first to create the game world.")
        print("Then start the game loop with 'python program.py'")
        print("Finally, start the API server with 'python api.py'\n")
        exit(1)
    
    print("=" * 70)
    print("SPACE GUILD - API SERVER")
    print("=" * 70)
    print("\n[*] Loading world data...")
    
    try:
        data_handler.load_all()
        print("  [+] World loaded successfully\n")
    except Exception as e:
        print(f"  [X] Failed to load world: {e}\n")
        exit(1)
    
    print("[*] Starting Flask API server...")
    print("=" * 70)
    print("\n[!] NOTE: This API runs separately from the game loop (program.py)")
    print("Make sure program.py is running in another terminal!\n")
    
    # Run Flask server
    app.run(debug=True, host='0.0.0.0', port=5000)
