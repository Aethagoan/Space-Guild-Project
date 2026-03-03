# SpaceGuildBack/api.py
# Aidan Orion 24 Feb 2026
# Flask API for Space Guild game
# This runs as a SEPARATE PROCESS from the game loop (program.py)

from flask import Flask, request, jsonify
from typing import Optional, Dict, Any
from threading import Condition, Lock
import os
import hashlib
import actions
import components
from program import data_handler, tick_completion_event

app = Flask(__name__)

# Pending updates registry: ship_id -> Condition for efficient blocking
# When a new /updates request comes in, we cancel the old one and create a new condition
# Threads will wait() on their condition and be notified when tick completes
pending_updates: Dict[int, Condition] = {}
pending_updates_lock = Lock()


def trigger_ship_update(ship_id: int):
    """Trigger immediate update for a ship (used for out-of-tick messages).
    
    This function is called when a message is added to a ship's log outside of
    tick processing (e.g., private messages, admin broadcasts). It signals any
    waiting /updates request for this ship to return immediately.
    
    Args:
        ship_id: Ship ID to trigger update for
    """
    with pending_updates_lock:
        if ship_id in pending_updates:
            # Notify the waiting thread via condition variable
            with pending_updates[ship_id]:
                pending_updates[ship_id].notify_all()


def notify_all_waiting_clients():
    """Notify all waiting /updates requests that a tick has completed.
    
    This should be called by program.py after tick_completion_event.set().
    It wakes up all threads waiting on their ship-specific conditions.
    
    PERFORMANCE: With 100k players, this acquires 100k condition locks and notifies.
    Each notify is O(1), so total is O(n) where n = number of waiting requests.
    This is acceptable since it happens once per tick (every 5 seconds).
    """
    with pending_updates_lock:
        # Get snapshot of all conditions to avoid holding lock during notification
        conditions_to_notify = list(pending_updates.values())
    
    # Notify all waiting threads (released lock first to avoid blocking tick processing)
    for condition in conditions_to_notify:
        with condition:
            condition.notify_all()


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
        "action_type": str,  # 'scan', 'attack_ship', 'attack_ship_component', 'attack_item', 'move', 'collect'
        "target": int | str,  # ship_id/item_id (int) or location_name (str)
        "target_data": str (optional)  # e.g., component slot for attack_ship_component, or scan type ('ship', 'item', 'location')
    }
    
    Returns:
        {"status": "success"} or {"error": "message"}
        
    Note: Action hash is computed server-side for spam protection based on 
          (ship_id, action_type, target, target_data) to detect duplicate actions.
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
        
        # Compute action hash server-side for spam protection
        # Hash is based on: ship_id + action_type + target + target_data
        hash_input = f"{ship_id}:{action_type}:{target}:{target_data or ''}"
        action_hash = hashlib.sha256(hash_input.encode()).hexdigest()
        
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


@app.route('/ship', methods=['GET'])
def get_ship_endpoint():
    """Get the player's ship information.
    
    Returns all ship data including HP, tier, components, cargo, shield pool, and location.
    
    Query parameters:
        player_id: int - Player ID
    
    Returns:
        {
            "ship_id": int,
            "is_stealthed": bool,
            "hp": float,
            "tier": int,
            "location": str,
            "shield_pool": float,
            "engine_id": int | null,
            "weapon_id": int | null,
            "shield_id": int | null,
            "cargo_id": int | null,
            "sensor": int | null,
            "stealth_cloak_id": int | null,
            "items": [int]  # Item IDs in cargo
        } or {"error": "message"}
    """
    try:
        player_id = request.args.get('player_id', type=int)
        
        if player_id is None:
            return jsonify({'error': 'Missing required parameter: player_id'}), 400
        
        # Get ship_id from player_id
        ship_id = get_ship_id_from_player_id(player_id)
        if ship_id is None:
            return jsonify({'error': 'Invalid player_id or player has no ship'}), 404
        
        # Get ship data
        ship = data_handler.get_ship(ship_id)
        
        # Return ship data with ship_id and stealth status included
        return jsonify({
            'ship_id': ship_id,
            'is_stealthed': actions.is_ship_stealthed(ship_id),
            **ship
        }), 200
        
    except KeyError:
        return jsonify({'error': 'Ship not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/location', methods=['GET'])
def get_location_endpoint():
    """Get the player's current location information including visible ships and items.
    
    This endpoint returns the "situation" at the player's current location - what ships 
    and items are present. Ships with active stealth cloaks are filtered out. This is 
    used when entering a location or refreshing the current view. Stations disable 
    sensors, so this should not be used there.
    
    PERFORMANCE NOTE: visible_ship_ids is pre-computed during tick processing (O(n) once per tick)
    rather than filtering in real-time (O(n²) total across all player requests). This ensures
    the endpoint remains fast even with thousands of players at the same location.
    
    Query parameters:
        player_id: int - Player ID
    
    Returns:
        {
            "name": str,
            "description": str,
            "links": [str],
            "ships": [
                {
                    "ship_id": int,
                    "name": str,
                    "player_name": str,
                    "symbol": str
                }
            ],
            "items": [
                {
                    "item_id": int,
                    "name": str
                }
            ]
        } or {"error": "message"}
        
    Note: Only ship IDs, names, player names, and symbols are returned. 
          Use scan action to get full ship details.
    """
    try:
        player_id = request.args.get('player_id', type=int)
        
        if player_id is None:
            return jsonify({'error': 'Missing required parameter: player_id'}), 400
        
        # Get ship_id from player_id
        ship_id = get_ship_id_from_player_id(player_id)
        if ship_id is None:
            return jsonify({'error': 'Invalid player_id or player has no ship'}), 404
        
        # Get ship's current location
        ship = data_handler.get_ship(ship_id)
        location_name = ship.get('location')
        
        if location_name is None:
            return jsonify({'error': 'Ship has no location'}), 500
        
        # Get location data
        location = data_handler.get_location(location_name)
        
        # Use pre-computed visible_ship_ids from tick processing (avoids O(n²) problem)
        # If visible_ship_ids doesn't exist (old save file), fall back to ship_ids
        visible_ship_ids = location.get('visible_ship_ids', location.get('ship_ids', []))
        
        # Get ship names and player names for visible ships
        ships_info = []
        for visible_ship_id in visible_ship_ids:
            try:
                vis_ship = data_handler.get_ship(visible_ship_id)
                # Get player name if ship has an owner
                player_name = "NPC"
                if 'owner_id' in vis_ship and vis_ship['owner_id'] is not None:
                    try:
                        player = data_handler.get_player(vis_ship['owner_id'])
                        player_name = player.get('name', 'Unknown')
                    except KeyError:
                        pass
                
                ships_info.append({
                    'ship_id': visible_ship_id,
                    'name': vis_ship.get('name', 'Unknown Ship'),
                    'player_name': player_name,
                    'symbol': vis_ship.get('symbol', '?')
                })
            except KeyError:
                # Ship doesn't exist anymore, skip
                pass
        
        # Get item names for items at location
        items_info = []
        for item_id in location.get('items', []):
            try:
                item = data_handler.get_item(item_id)
                items_info.append({
                    'item_id': item_id,
                    'name': item.get('name', 'Unknown Item')
                })
            except KeyError:
                # Item doesn't exist anymore, skip
                pass
        
        return jsonify({
            'name': location.get('name'),
            'description': location.get('description'),
            'links': location.get('links', []),
            'ships': ships_info,
            'items': items_info
        }), 200
        
    except KeyError:
        return jsonify({'error': 'Location not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/vendors', methods=['GET'])
def get_vendors_endpoint():
    """Get all vendors at the player's current location.
    
    Returns vendor dialogue and options for all vendors at the player's current location.
    This is typically called when the player is at a station or ground_station.
    
    Query parameters:
        player_id: int - Player ID
    
    Returns:
        {
            "location_name": str,
            "vendors": {
                "vendor_id": {
                    "vendor_type": str,
                    "entry_dialogue": str,
                    "options": []
                },
                ...
            }
        } or {"error": "message"}
        
    Note: If no vendors exist at the location, returns an empty vendors dict.
    """
    try:
        player_id = request.args.get('player_id', type=int)
        
        if player_id is None:
            return jsonify({'error': 'Missing required parameter: player_id'}), 400
        
        # Get ship_id from player_id
        ship_id = get_ship_id_from_player_id(player_id)
        if ship_id is None:
            return jsonify({'error': 'Invalid player_id or player has no ship'}), 404
        
        # Get ship's current location
        ship = data_handler.get_ship(ship_id)
        location_name = ship.get('location')
        
        if location_name is None:
            return jsonify({'error': 'Ship has no location'}), 500
        
        # Get vendors at this location
        vendors = data_handler.get_vendors_at_location(location_name)
        
        return jsonify({
            'location_name': location_name,
            'vendors': vendors
        }), 200
        
    except KeyError:
        return jsonify({'error': 'Location not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/updates', methods=['GET'])
def get_updates_endpoint():
    """Long-polling endpoint that waits for next tick completion or ship log update.
    
    This endpoint supports multiple signal sources:
    - Tick completion (most common - happens every 5 seconds)
    - Ship log updates (messages between ticks)
    
    The endpoint will block until one of these events occurs, then return:
    - Current ship state
    - Current location info
    - New ship log entries
    - Action results (scans, attacks, moves, collects)
    
    If multiple requests come from the same player, only the latest is kept active.
    
    Query parameters:
        player_id: int - Player ID
    
    Returns:
        {
            "ship_state": {
                "ship_id": int,
                "is_stealthed": bool,
                "hp": float,
                "tier": int,
                ...
            },
            "location_state": {...},
            "ship_log": [...],
            "scan_data": {...} or null,
            "attack_result": {...} or null,
            "collect_result": {...} or null,
            "move_result": {...} or null
        } or {"error": "message"}
    """
    try:
        player_id = request.args.get('player_id', type=int)
        
        if player_id is None:
            return jsonify({'error': 'Missing required parameter: player_id'}), 400
        
        # Get ship_id from player_id
        ship_id = get_ship_id_from_player_id(player_id)
        if ship_id is None:
            return jsonify({'error': 'Invalid player_id or player has no ship'}), 404
        
        # Cancel any existing pending request for this ship
        # This ensures only one active /updates request per player at a time
        ship_condition = None
        with pending_updates_lock:
            if ship_id in pending_updates:
                # Cancel old request by notifying it (it will check if it's been replaced)
                old_condition = pending_updates[ship_id]
                with old_condition:
                    old_condition.notify_all()
            
            # Create new condition for this request (ship-specific)
            ship_condition = Condition()
            pending_updates[ship_id] = ship_condition
        
        # Wait for tick completion event to be set by program.py
        # We need to wait on BOTH tick_completion_event AND ship_condition
        # Strategy: We'll wait on ship_condition, and program.py will notify all conditions
        timeout = 30.0  # 30 second timeout to prevent hanging forever
        
        event_triggered = False
        with ship_condition:
            # Check if tick already completed before we registered
            if tick_completion_event.is_set():
                event_triggered = True
            else:
                # Wait for notification (thread truly sleeps here - no busy wait!)
                # Returns True if notified, False if timeout
                event_triggered = ship_condition.wait(timeout=timeout)
        
        # Check if we were cancelled by a newer request
        with pending_updates_lock:
            if ship_id in pending_updates and pending_updates[ship_id] != ship_condition:
                # We were replaced by a newer request - return empty/stale response
                return jsonify({'error': 'Request superseded by newer request'}), 409
            
            # Remove ourselves from pending updates
            pending_updates.pop(ship_id, None)
        
        if not event_triggered:
            # Timeout occurred
            return jsonify({'error': 'Request timed out waiting for tick'}), 408
        
        # Tick completed! Gather all update data
        
        # Get ship state
        ship = data_handler.get_ship(ship_id)
        ship_state = {
            'ship_id': ship_id,
            'is_stealthed': actions.is_ship_stealthed(ship_id),
            **ship
        }
        
        # Get location state
        location_name = ship.get('location')
        if location_name is None:
            return jsonify({'error': 'Ship has no location'}), 500
        
        location = data_handler.get_location(location_name)
        visible_ship_ids = location.get('visible_ship_ids', location.get('ship_ids', []))
        
        # Get ship names and player names for visible ships
        ships_info = []
        for visible_ship_id in visible_ship_ids:
            try:
                vis_ship = data_handler.get_ship(visible_ship_id)
                # Get player name if ship has an owner
                player_name = "NPC"
                if 'owner_id' in vis_ship and vis_ship['owner_id'] is not None:
                    try:
                        player = data_handler.get_player(vis_ship['owner_id'])
                        player_name = player.get('name', 'Unknown')
                    except KeyError:
                        pass
                
                ships_info.append({
                    'ship_id': visible_ship_id,
                    'name': vis_ship.get('name', 'Unknown Ship'),
                    'player_name': player_name,
                    'symbol': vis_ship.get('symbol', '?')
                })
            except KeyError:
                # Ship doesn't exist anymore, skip
                pass
        
        # Get item names for items at location
        items_info = []
        for item_id in location.get('items', []):
            try:
                item = data_handler.get_item(item_id)
                items_info.append({
                    'item_id': item_id,
                    'name': item.get('name', 'Unknown Item')
                })
            except KeyError:
                # Item doesn't exist anymore, skip
                pass
        
        location_state = {
            'name': location.get('name'),
            'description': location.get('description'),
            'links': location.get('links', []),
            'ships': ships_info,
            'items': items_info
        }
        
        # Get ship log entries
        ship_log = data_handler.get_ship_log(ship_id)
        
        # Get and clear action results
        action_results_data = actions.get_and_clear_action_results(ship_id)
        
        if action_results_data is None:
            # No action results - initialize empty structure
            action_results_data = {
                "ship_log": [],
                "ship_state": None,
                "scan_data": None,
                "attack_result": None,
                "collect_result": None,
                "move_result": None
            }
        
        # Build response
        response = {
            'ship_state': ship_state,
            'location_state': location_state,
            'ship_log': ship_log,
            'scan_data': action_results_data.get('scan_data'),
            'attack_result': action_results_data.get('attack_result'),
            'collect_result': action_results_data.get('collect_result'),
            'move_result': action_results_data.get('move_result')
        }
        
        return jsonify(response), 200
        
    except KeyError:
        return jsonify({'error': 'Entity not found'}), 404
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Server error: {str(e)}'}), 500


if __name__ == '__main__':
    # DEPLOYMENT NOTE:
    # - Development: python api.py (uses Flask threaded=True, good for ~1k concurrent)
    # - Production Linux: gunicorn -w 4 -k gevent --worker-connections 25000 api:app
    # - Production Windows: waitress-serve --host=0.0.0.0 --port=5000 --threads=100 api:app
    # - Docker: See Dockerfile for containerized deployment
    
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
    
    # Run Flask server with threading enabled for concurrent request handling
    # threaded=True allows handling multiple simultaneous /updates requests
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
