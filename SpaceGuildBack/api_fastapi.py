# SpaceGuildBack/api_fastapi.py
# Aidan Orion - March 2026
# FastAPI async API for Space Guild game
# This runs embedded in program.py - NOT as a separate process
# Designed to scale to 1M concurrent WebSocket connections

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict, Any
import hashlib
import logging
import asyncio
import os

# Import game modules (DataHandler will be imported from program.py)
import actions
import components
from websocket_manager import connection_manager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(name)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('api_fastapi')

# Create FastAPI app
app = FastAPI(
    title="Space Guild API",
    description="Async API for Space Guild multiplayer game - designed for 1M concurrent connections",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global reference to DataHandler (will be set by program.py)
data_handler = None
current_tick_number = 0


def set_data_handler(handler):
    """Set the global data handler reference. Called by program.py on startup."""
    global data_handler
    data_handler = handler
    logger.info("DataHandler reference set in FastAPI app")


def set_current_tick(tick_num: int):
    """Update current tick number. Called by program.py after each tick."""
    global current_tick_number
    current_tick_number = tick_num


# Helper functions

def convert_ids_to_strings(obj):
    """Recursively convert all ID fields to strings to prevent JavaScript precision loss.
    
    JavaScript cannot safely handle integers larger than 2^53-1 (9007199254740991).
    Snowflake IDs and other large integers must be sent as strings.
    """
    if isinstance(obj, dict):
        result = {}
        for key, value in obj.items():
            # Convert any field ending with _id to string
            if key.endswith('_id') or key in ('id', 'owner_id', 'target_id'):
                if isinstance(value, int):
                    result[key] = str(value)
                elif isinstance(value, list):
                    result[key] = [str(v) if isinstance(v, int) else v for v in value]
                else:
                    result[key] = value
            else:
                result[key] = convert_ids_to_strings(value)
        return result
    elif isinstance(obj, list):
        return [convert_ids_to_strings(item) for item in obj]
    else:
        return obj


def check_world_initialized(data_dir: str = "game_data") -> bool:
    """Check if the world has been initialized."""
    locations_file = os.path.join(data_dir, "locations.json")
    return os.path.exists(locations_file)


async def get_ship_id_from_player_id(player_id: int) -> Optional[int]:
    """Get the ship_id for a player.
    
    Args:
        player_id: Player ID (can be int or string that will be converted to int)
    """
    try:
        # Ensure player_id is an integer (in case it comes as string from query param)
        if isinstance(player_id, str):
            player_id = int(player_id)
        
        player = await data_handler.get_player(player_id)
        ship_id = player.get('ship_id')
        logger.info(f"get_ship_id_from_player_id({player_id}) -> ship_id: {ship_id} (type: {type(ship_id).__name__})")
        logger.info(f"Player data: {player}")
        return ship_id
    except (KeyError, ValueError) as e:
        logger.error(f"get_ship_id_from_player_id({player_id}) failed: {e}")
        return None


# REST API Endpoints

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "tick": current_tick_number}


@app.post("/spawn_player")
async def spawn_player_endpoint(request: Request):
    """Create a new player with a ship and tier 0 starter components.
    
    Request JSON:
        {
            "name": str  # Player name (optional, defaults to "Pilot")
        }
    """
    logger.info("========== SPAWN_PLAYER ENDPOINT CALLED ==========")
    try:
        if data_handler is None:
            raise RuntimeError("Server is still initializing, try again in a moment")

        content_type = request.headers.get('content-type', '')
        data = await request.json() if 'application/json' in content_type else {}
        player_name = data.get('name')
        
        logger.info(f"Creating new player: {player_name}")
        
        # Call data handler to create player
        result = await data_handler.spawn_new_player(player_name=player_name)
        
        logger.info(f"Player created successfully - player_id: {result['player_id']}, ship_id: {result['ship_id']}, location: {result['location']}")
        
        # Convert IDs to strings to prevent JavaScript precision loss
        return convert_ids_to_strings(result)
        
    except Exception as e:
        import traceback
        logger.error(f"Failed to create player: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/ship")
async def get_ship_endpoint(player_id: int = Query(..., description="Player ID")):
    """Get the player's ship information."""
    logger.info(f"========== GET /ship - player_id: {player_id} ==========")
    try:
        if player_id is None:
            raise HTTPException(status_code=400, detail="Missing required parameter: player_id")
        
        # Get ship_id from player_id
        ship_id = await get_ship_id_from_player_id(player_id)
        
        logger.info(f"Player {player_id} has ship_id: {ship_id}")
        
        if ship_id is None:
            logger.warning(f"Invalid player_id {player_id} or player has no ship")
            raise HTTPException(status_code=404, detail="Invalid player_id or player has no ship")
        
        # Get ship data
        ship = await data_handler.get_ship(ship_id)
        
        logger.info(f"Retrieved ship {ship_id} data successfully")
        
        # Get component details for all equipped components
        component_data = {}
        component_slots = ['engine_id', 'weapon_id', 'shield_id', 'cargo_id', 'sensor_id', 'stealth_cloak_id']
        
        for slot in component_slots:
            component_id = ship.get(slot)
            if component_id:
                try:
                    component = await data_handler.get_item(component_id)
                    # Include only relevant fields: health, maxhealth, tier, multiplier
                    component_data[slot] = {
                        'id': component_id,
                        'name': component.get('name', 'Unknown'),
                        'type': component.get('type', 'unknown'),
                        'health': component.get('health', 0),
                        'maxhealth': component.get('maxhealth', 0),
                        'tier': component.get('tier', 0),
                        'multiplier': component.get('multiplier', 1.0)
                    }
                except KeyError:
                    # Component doesn't exist, skip it
                    pass
        
        # Return ship data with ship_id, stealth status, and component details
        # Convert IDs to strings to prevent JavaScript precision loss
        result = {
            'ship_id': ship_id,
            'is_stealthed': await actions.is_ship_stealthed(ship_id),
            'components': component_data,
            **ship
        }
        return convert_ids_to_strings(result)
        
    except KeyError:
        logger.error(f"Ship not found for player {player_id}")
        raise HTTPException(status_code=404, detail="Ship not found")
    except Exception as e:
        import traceback
        logger.error(f"Error in get_ship_endpoint: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/location")
async def get_location_endpoint(player_id: int = Query(..., description="Player ID")):
    """Get the player's current location information including visible ships and items."""
    try:
        logger.info(f"GET /location - player_id: {player_id}")
        
        if player_id is None:
            logger.info(f"player_id {player_id} was NONE.")
            raise HTTPException(status_code=400, detail="Missing required parameter: player_id")
        
        # Get ship_id from player_id
        ship_id = await get_ship_id_from_player_id(player_id)
        if ship_id is None:
            logger.warning(f"Invalid player_id {player_id} or player has no ship")
            raise HTTPException(status_code=404, detail="Invalid player_id or player has no ship")
        
        # Get ship's current location
        ship = await data_handler.get_ship(ship_id)
        if ship is None:
            logger.info(f"{player_id} had no ship")
            raise HTTPException(status_code=404, detail=f"No ship for {player_id}")

        location_name = ship.get('location')
        
        logger.info(f"Player {player_id} (ship {ship_id}) is at location: {location_name}")
        
        if location_name is None:
            raise HTTPException(status_code=500, detail="Ship has no location")
        
        # Get location data
        location = await data_handler.get_location(location_name)
        
        # Use pre-cached enriched data (computed once per tick in update_all_location_visibility)
        # This is O(1) lookup instead of O(n) iteration per request
        ships_info = location.get('cached_ships_info', [])
        items_info = location.get('cached_items_info', [])
        
        # Enrich links with location type information for frontend sorting
        links_with_types = []
        for link_name in location.get('links', []):
            try:
                linked_location = await data_handler.get_location(link_name)
                links_with_types.append({
                    'name': link_name,
                    'type': linked_location.get('type', 'space')
                })
            except KeyError:
                # Location doesn't exist, add with unknown type
                links_with_types.append({
                    'name': link_name,
                    'type': 'unknown'
                })
        
        result = {
            'name': location.get('name'),
            'description': location.get('description'),
            'links': links_with_types,
            'ships': ships_info,
            'items': items_info
        }
        # Convert IDs to strings to prevent JavaScript precision loss
        return convert_ids_to_strings(result)
        
    except KeyError:
        raise HTTPException(status_code=404, detail="Location not found")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Action failed")


@app.get("/vendors")
async def get_vendors_endpoint(player_id: int = Query(..., description="Player ID")):
    """Get all vendors at the player's current location."""
    try:
        if player_id is None:
            raise HTTPException(status_code=400, detail="Missing required parameter: player_id")
        
        # Get ship_id from player_id
        ship_id = await get_ship_id_from_player_id(player_id)
        if ship_id is None:
            raise HTTPException(status_code=404, detail="Invalid player_id or player has no ship")
        
        # Get ship's current location
        ship = await data_handler.get_ship(ship_id)
        location_name = ship.get('location')
        
        if location_name is None:
            raise HTTPException(status_code=500, detail="Ship has no location")
        
        # Get vendors at this location - O(1) dict lookup
        vendors = data_handler.Vendors.get(location_name)
        
        result = {
            'location_name': location_name,
            'vendors': vendors if vendors is not None else {}
        }
        
        # Convert IDs to strings to prevent JavaScript precision loss
        return convert_ids_to_strings(result)
        
    except KeyError:
        raise HTTPException(status_code=404, detail="Location not found")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Action failed")


@app.post("/action")
async def queue_action_endpoint(request: Request):
    """Queue an action for a ship to execute on the next tick."""
    try:
        data = await request.json()
        logger.info(f"POST /action - Received data: {data}")
        
        # Validate required fields
        player_id = data.get('player_id')
        action_type = data.get('action_type')
        target = data.get('target')
        
        if player_id is None or action_type is None or target is None:
            raise HTTPException(status_code=400, detail="Missing required fields: player_id, action_type, target")
        
        # Convert string IDs to integers
        try:
            if isinstance(player_id, str):
                player_id = int(player_id)
            if isinstance(target, str) and target.isdigit():
                target = int(target)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid ID format")
        
        logger.info(f"After conversion - player_id: {player_id} (type: {type(player_id)}), action_type: {action_type}, target: {target} (type: {type(target)})")
        
        # Get ship_id from player_id
        ship_id = await get_ship_id_from_player_id(player_id)
        logger.info(f"Got ship_id: {ship_id} for player_id: {player_id}")
        if ship_id is None:
            raise HTTPException(status_code=404, detail="Invalid player_id or player has no ship")
        
        # Get optional fields
        target_data = data.get('target_data')
        
        # Compute action hash server-side for spam protection
        hash_input = f"{ship_id}:{action_type}:{target}:{target_data or ''}"
        action_hash = hashlib.sha256(hash_input.encode()).hexdigest()
        
        logger.info(f"Calling queue_action with ship_id={ship_id}, action_type={action_type}, target={target}, target_data={target_data}")
        
        # Queue the action
        success = await actions.queue_action(ship_id, action_type, target, target_data, action_hash)
        
        if success:
            return {'status': 'success', 'message': 'Action queued'}
        else:
            raise HTTPException(status_code=400, detail="Invalid action type or parameters")
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Action failed")


@app.post("/repair/component")
async def repair_component_endpoint(request: Request):
    """Repair a component by restoring health and applying multiplier reduction."""
    try:
        data = await request.json()
        player_id = data.get('player_id')
        item_id = data.get('item_id')
        
        if player_id is None or item_id is None:
            raise HTTPException(status_code=400, detail="Missing required fields: player_id, item_id")
        
        # Convert string IDs to integers
        try:
            if isinstance(player_id, str):
                player_id = int(player_id)
            if isinstance(item_id, str):
                item_id = int(item_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid ID format")
        
        # Verify player exists
        ship_id = await get_ship_id_from_player_id(player_id)
        if ship_id is None:
            raise HTTPException(status_code=404, detail="Invalid player_id or player has no ship")
        
        # Repair the component
        result = await components.repair_component(item_id)
        
        response = {
            'status': 'success',
            **result
        }
        # Convert IDs to strings to prevent JavaScript precision loss
        return convert_ids_to_strings(response)
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid repair request")
    except KeyError:
        raise HTTPException(status_code=404, detail="Component not found")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Action failed")


@app.get("/admin/game_stats")
async def admin_game_stats():
    """Get statistics about the current game state."""
    try:
        stats = {
            "locations_count": len(data_handler.Locations),
            "ships_count": len(data_handler.Ships),
            "items_count": len(data_handler.Items),
            "players_count": len(data_handler.Players),
            "factions_count": len(data_handler.Factions),
            "players": [],
            "ships": [],
            "locations": []
        }
        
        # Get player details
        for player_id, player_data in data_handler.Players.items():
            stats["players"].append({
                "id": player_id,
                "name": player_data.get('name', 'Unknown'),
                "ship_id": player_data.get('ship_id'),
                "faction_id": player_data.get('faction_id')
            })
        
        # Get ship details
        for ship_id, ship_data in data_handler.Ships.items():
            stats["ships"].append({
                "id": ship_id,
                "owner_id": ship_data.get('owner_id'),
                "name": ship_data.get('name', 'Unknown'),
                "location": ship_data.get('location', 'Unknown'),
                "hp": ship_data.get('hp', 0),
                "tier": ship_data.get('tier', 0)
            })
        
        # Get location details
        for location_name, location_data in data_handler.Locations.items():
            stats["locations"].append({
                "name": location_name,
                "ships_count": len(location_data.get('ship_ids', [])),
                "items_count": len(location_data.get('item_ids', []))
            })
        
        return stats
        
    except Exception as e:
        import traceback
        logger.error(f"Failed to get game stats: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to get game stats")


# WebSocket endpoint (replaces /updates long-polling)

@app.websocket("/ws/{ship_id}")
async def websocket_endpoint(websocket: WebSocket, ship_id: str):
    """WebSocket endpoint for real-time game updates.
    
    Replaces the /updates long-polling endpoint with efficient WebSocket connection.
    Clients connect once and receive tick updates pushed from the server.
    
    Args:
        ship_id: Ship ID as string (will be converted to int internally)
    """
    # Convert ship_id from string to int for internal use
    try:
        ship_id_int = int(ship_id)
    except ValueError:
        logger.error(f"Invalid ship_id format: {ship_id}")
        # Must accept before we can close
        await websocket.accept()
        await websocket.close(code=1003, reason="Invalid ship_id format")
        return
    
    # Accept the WebSocket connection first
    await connection_manager.connect(ship_id_int, websocket)
    logger.info(f"WebSocket connected for ship {ship_id_int}")
    
    try:
        # Keep connection alive and listen for client messages
        while True:
            # Wait for messages from client (ping/pong, disconnect, etc.)
            data = await websocket.receive_text()
            
            # Handle client messages if needed
            # For now, we just acknowledge receipt
            logger.debug(f"Received from ship {ship_id_int}: {data}")
            
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for ship {ship_id_int}")
        await connection_manager.disconnect(ship_id_int)
    except Exception as e:
        logger.error(f"WebSocket error for ship {ship_id_int}: {e}")
        await connection_manager.disconnect(ship_id_int)


# Broadcast function to be called by program.py after each tick

async def broadcast_tick_updates(tick_number: int):
    """Broadcast tick completion to all connected WebSocket clients.
    
    This is called by program.py after each tick completes.
    It gathers update data for all connected ships and broadcasts via WebSocket.
    """
    # Get all connected ship IDs
    connected_ships = list(connection_manager.active_connections.keys())
    
    if not connected_ships:
        return  # No one connected
    
    logger.debug(f"Broadcasting tick {tick_number} to {len(connected_ships)} connected ships")
    
    # Build updates for each connected ship
    ship_updates = {}
    
    for ship_id in connected_ships:
        try:
            # Get ship state
            ship = await data_handler.get_ship(ship_id)
            
            # Get component details for all equipped components
            component_data = {}
            component_slots = ['engine_id', 'weapon_id', 'shield_id', 'cargo_id', 'sensor_id', 'stealth_cloak_id']
            
            for slot in component_slots:
                component_id = ship.get(slot)
                if component_id:
                    try:
                        component = await data_handler.get_item(component_id)
                        # Include only relevant fields: health, maxhealth, tier, multiplier
                        component_data[slot] = {
                            'id': component_id,
                            'name': component.get('name', 'Unknown'),
                            'type': component.get('type', 'unknown'),
                            'health': component.get('health', 0),
                            'maxhealth': component.get('maxhealth', 0),
                            'tier': component.get('tier', 0),
                            'multiplier': component.get('multiplier', 1.0)
                        }
                    except KeyError:
                        # Component doesn't exist, skip it
                        pass
            
            ship_state = {
                'ship_id': ship_id,
                'is_stealthed': await actions.is_ship_stealthed(ship_id),
                'components': component_data,
                **ship
            }
            
            # Get location state
            location_name = ship.get('location')
            if location_name:
                location = await data_handler.get_location(location_name)
                
                # Use pre-cached enriched data (O(1) instead of O(n) per connected client)
                ships_info = location.get('cached_ships_info', [])
                items_info = location.get('cached_items_info', [])
                
                # Enrich links with location type information for frontend sorting
                links_with_types = []
                for link_name in location.get('links', []):
                    try:
                        linked_location = await data_handler.get_location(link_name)
                        links_with_types.append({
                            'name': link_name,
                            'type': linked_location.get('type', 'space')
                        })
                    except KeyError:
                        # Location doesn't exist, add with unknown type
                        links_with_types.append({
                            'name': link_name,
                            'type': 'unknown'
                        })
                
                location_state = {
                    'name': location.get('name'),
                    'description': location.get('description'),
                    'links': links_with_types,
                    'ships': ships_info,
                    'items': items_info
                }
            else:
                location_state = None
            
            # Get ship log
            ship_log = await data_handler.get_ship_log(ship_id)
            
            # Get and clear action results
            action_results_data = await actions.get_and_clear_action_results(ship_id)
            
            if action_results_data is None:
                action_results_data = {
                    "scan_data": None,
                    "attack_result": None,
                    "collect_result": None,
                    "move_result": None
                }
            
            # Build update for this ship
            ship_updates[ship_id] = convert_ids_to_strings({
                'ship_state': ship_state,
                'location_state': location_state,
                'ship_log': ship_log,
                'scan_data': action_results_data.get('scan_data'),
                'attack_result': action_results_data.get('attack_result'),
                'collect_result': action_results_data.get('collect_result'),
                'move_result': action_results_data.get('move_result')
            })
            
        except KeyError:
            logger.warning(f"Ship {ship_id} not found during broadcast")
        except Exception as e:
            logger.error(f"Error building update for ship {ship_id}: {e}")
    
    # Broadcast to all connected clients
    await connection_manager.broadcast_tick(tick_number, ship_updates)


# Startup logging

logger.info("=" * 70)
logger.info("FastAPI app initialized - ready to be started by program.py")
logger.info("Designed for 100k-200k concurrent WebSocket connections per server")
logger.info("=" * 70)
