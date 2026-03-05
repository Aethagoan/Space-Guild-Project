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
    # Keys whose values are IDs (int or list of ints) that must become strings
    ID_VALUE_KEYS = {'id', 'owner_id', 'target_id'}
    ID_SUFFIX = '_id'
    # Keys whose values are lists of IDs (bare ints) that must all become strings
    ID_LIST_KEYS = {'items', 'ship_ids', 'item_ids'}

    if isinstance(obj, dict):
        result = {}
        for key, value in obj.items():
            if key.endswith(ID_SUFFIX) or key in ID_VALUE_KEYS:
                # Single ID field or list of IDs
                if isinstance(value, int):
                    result[key] = str(value)
                elif isinstance(value, list):
                    result[key] = [str(v) if isinstance(v, int) else convert_ids_to_strings(v) for v in value]
                else:
                    result[key] = value
            elif key in ID_LIST_KEYS:
                # Field is a list of bare integer IDs (e.g. ship['items'] = [id1, id2, ...])
                if isinstance(value, list):
                    result[key] = [str(v) if isinstance(v, int) else convert_ids_to_strings(v) for v in value]
                else:
                    result[key] = convert_ids_to_strings(value)
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
    try:
        if data_handler is None:
            raise RuntimeError("Server is still initializing, try again in a moment")

        content_type = request.headers.get('content-type', '')
        data = await request.json() if 'application/json' in content_type else {}
        player_name = data.get('name')
        
        # Call data handler to create player
        result = await data_handler.spawn_new_player(player_name=player_name)
        
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
    try:
        if player_id is None:
            raise HTTPException(status_code=400, detail="Missing required parameter: player_id")
        
        # Get ship_id from player_id
        ship_id = await get_ship_id_from_player_id(player_id)
        
        if ship_id is None:
            logger.warning(f"Invalid player_id {player_id} or player has no ship")
            raise HTTPException(status_code=404, detail="Invalid player_id or player has no ship")
        
        # Get ship data
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
                        'name': component.get('name'),
                        'type': component.get('type'),
                        'health': component.get('health'),
                        'maxhealth': component.get('maxhealth'),
                        'tier': component.get('tier'),
                        'multiplier': component.get('multiplier')
                    }
                except KeyError:
                    # Component doesn't exist, skip it
                    pass
        
        # Enrich cargo items with full item data
        cargo_items_enriched = []
        for item_id in ship.get('items', []):
            try:
                item = await data_handler.get_item(item_id)
                cargo_items_enriched.append({
                    'id': str(item_id), # turn it into a string or javascript will round the damn id.
                    'name': item.get('name'),
                    'type': item.get('type'),
                    'health': item.get('health'),
                    'maxhealth': item.get('maxhealth'),
                    'tier': item.get('tier'),
                    'multiplier': item.get('multiplier')
                })
            except KeyError:
                # Item doesn't exist, skip it
                pass
        
        # Return ship data with ship_id, stealth status, and component details
        # Convert IDs to strings to prevent JavaScript precision loss
        result = {
            'ship_id': ship_id,
            'is_stealthed': await actions.is_ship_stealthed(ship_id),
            'components': component_data,
            'cargo_items_enriched': cargo_items_enriched,
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
            raise HTTPException(status_code=400, detail="Missing required parameter: player_id")
        
        # Get ship_id from player_id
        ship_id = await get_ship_id_from_player_id(player_id)
        if ship_id is None:
            logger.warning(f"Invalid player_id {player_id} or player has no ship")
            raise HTTPException(status_code=404, detail="Invalid player_id or player has no ship")
        
        # Get ship's current location
        ship = await data_handler.get_ship(ship_id)
        if ship is None:
            raise HTTPException(status_code=404, detail=f"No ship for {player_id}")

        location_name = ship.get('location')
        
        if location_name is None:
            raise HTTPException(status_code=500, detail="Ship has no location")
        
        # Get location data
        location = await data_handler.get_location(location_name)
        
        # Use pre-cached enriched data (computed once per tick in update_all_location_visibility)
        # This is O(1) lookup instead of O(n) iteration per request
        ships_info = location.get('cached_ships_info', [])
        items_info = location.get('cached_items_info', [])
        
        location_type = location.get('type')
        
        # Only hide ship details at stations (station, ground_station)
        # At other locations (space, resource_node, etc.), show full ship data
        if location_type in ['station', 'ground_station']:
            result = {
                'name': location.get('name'),
                'type': location_type,
                'description': location.get('description'),
                'links': location.get('links'),
                'ship_count': len(ships_info),
                'items': items_info
            }
        else:
            # Show full ship data at space, resource nodes, and other locations
            result = {
                'name': location.get('name'),
                'type': location_type,
                'description': location.get('description'),
                'links': location.get('links'),
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
        
        result = vendors if vendors is not None else {}
        
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
        
        # Get ship_id from player_id
        ship_id = await get_ship_id_from_player_id(player_id)
        if ship_id is None:
            raise HTTPException(status_code=404, detail="Invalid player_id or player has no ship")
        
        # Get optional fields
        target_data = data.get('target_data')
        
        # Compute action hash server-side for spam protection
        hash_input = f"{ship_id}:{action_type}:{target}:{target_data or ''}"
        action_hash = hashlib.sha256(hash_input.encode()).hexdigest()
        
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
        slot_name = data.get('slot_name')
        
        if player_id is None or slot_name is None:
            raise HTTPException(status_code=400, detail="Missing required fields: player_id, slot_name")
        
        # Convert string IDs to integers
        try:
            if isinstance(player_id, str):
                player_id = int(player_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid ID format")
        
        # Verify player exists
        ship_id = await get_ship_id_from_player_id(player_id)
        if ship_id is None:
            raise HTTPException(status_code=404, detail="Invalid player_id or player has no ship")
        
        try:
            await data_handler.repair_ship_component(ship_id,slot_name) # this method adds the ship log as well as doing the repair
            response = {'status':'success'}
        except ValueError:
            # when there's an error, the shiplog should be updated.
            await data_handler.add_ship_log(ship_id,'environment',f"Strange request. Nothing happens.")
            response = {'status':'failure'}
        except KeyError:
            await data_handler.add_ship_log(ship_id,'environment',f"The item in the request could not be repaired because the item or ship the item was supposed to be on didn't exist...")
            response = {'status':'failure'}
        
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


@app.post("/equip")
async def equip_item_endpoint(request: Request):
    """Equip an item from ship's cargo to appropriate component slot."""
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
        
        # Get ship_id from player_id
        ship_id = await get_ship_id_from_player_id(player_id)
        if ship_id is None:
            raise HTTPException(status_code=404, detail="Invalid player_id or player has no ship")
        
        # Get item details for logging
        item = await data_handler.get_item(item_id)
        item_name = item.get('name', 'Unknown')
        item_type = item.get('type', 'unknown')
        
        # Equip the item
        await data_handler.equip_item_to_ship(ship_id, item_id)
        
        # Add ship log message
        await data_handler.add_ship_log(
            ship_id,
            'action',
            f'Equipped {item_name} ({item_type})',
            f'item:{item_id}'
        )

        # Push instant update so the client sees the new log/ship state immediately
        await push_update_to_ship(ship_id)

        return {'status': 'success', 'message': 'Item equipped successfully'}
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Equip failed")


@app.post("/unequip")
async def unequip_item_endpoint(request: Request):
    """Unequip an item from a component slot to ship's cargo."""
    try:
        data = await request.json()
        player_id = data.get('player_id')
        slot_name = data.get('slot_name')
        
        if player_id is None or slot_name is None:
            raise HTTPException(status_code=400, detail="Missing required fields: player_id, slot_name")
        
        # Convert string IDs to integers
        try:
            if isinstance(player_id, str):
                player_id = int(player_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid ID format")
        
        # Get ship_id from player_id
        ship_id = await get_ship_id_from_player_id(player_id)
        if ship_id is None:
            raise HTTPException(status_code=404, detail="Invalid player_id or player has no ship")
        
        # Get current ship state to retrieve item details before unequipping
        ship = await data_handler.get_ship(ship_id)
        item_id = ship.get(slot_name)
        
        # Unequip the item
        await data_handler.unequip_item_from_ship(ship_id, slot_name)
        
        # Add ship log message
        if item_id:
            item = await data_handler.get_item(item_id)
            item_name = item.get('name', 'Unknown')
            await data_handler.add_ship_log(
                ship_id,
                'action',
                f'Unequipped {item_name} from {slot_name}',
                f'item:{item_id}'
            )

        # Push instant update so the client sees the new log/ship state immediately
        await push_update_to_ship(ship_id)

        return {'status': 'success', 'message': 'Item unequipped successfully'}
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Unequip failed")


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
        
        return convert_ids_to_strings(stats)
        
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
    
    try:
        # Keep connection alive and listen for client messages
        while True:
            # Wait for messages from client (ping/pong, disconnect, etc.)
            data = await websocket.receive_text()
            
            # Handle client messages if needed
            # For now, we just acknowledge receipt
            logger.debug(f"Received from ship {ship_id_int}: {data}")
            
    except WebSocketDisconnect:
        await connection_manager.disconnect(ship_id_int)
    except Exception as e:
        logger.error(f"WebSocket error for ship {ship_id_int}: {e}")
        await connection_manager.disconnect(ship_id_int)


# Broadcast function to be called by program.py after each tick

async def build_ship_update(ship_id: int) -> dict:
    """Build the update payload for a single ship.

    Returns a convert_ids_to_strings-ready dict, or raises on error.
    Does NOT clear action results — that is only done during a tick broadcast.
    """
    ship = await data_handler.get_ship(ship_id)

    # Get component details for all equipped components
    component_data = {}
    component_slots = ['engine_id', 'weapon_id', 'shield_id', 'cargo_id', 'sensor_id', 'stealth_cloak_id']

    for slot in component_slots:
        component_id = ship.get(slot)
        if component_id:
            try:
                component = await data_handler.get_item(component_id)
                component_data[slot] = {
                    'id': str(component_id),
                    'name': component.get('name', 'Unknown'),
                    'type': component.get('type', 'unknown'),
                    'health': component.get('health', 0),
                    'maxhealth': component.get('maxhealth', 0),
                    'tier': component.get('tier', 0),
                    'multiplier': component.get('multiplier', 1.0)
                }
            except KeyError:
                pass

    # Enrich cargo items with full item data
    cargo_items_enriched = []
    for item_id in ship.get('items', []):
        try:
            item = await data_handler.get_item(item_id)
            cargo_items_enriched.append({
                'id': str(item_id),
                'name': item.get('name', 'Unknown'),
                'type': item.get('type', 'unknown'),
                'health': item.get('health', 0),
                'maxhealth': item.get('maxhealth', 0),
                'tier': item.get('tier', 0),
                'multiplier': item.get('multiplier', 1.0)
            })
        except KeyError:
            pass

    ship_state = {
        'ship_id': ship_id,
        'is_stealthed': await actions.is_ship_stealthed(ship_id),
        'components': component_data,
        'cargo_items_enriched': cargo_items_enriched,
        **ship
    }

    # Get location state
    location_name = ship.get('location')
    if location_name:
        location = await data_handler.get_location(location_name)

        ships_info = location.get('cached_ships_info', [])
        items_info = location.get('cached_items_info', [])

        links_with_types = []
        for link_name in location.get('links', []):
            try:
                linked_location = await data_handler.get_location(link_name)
                links_with_types.append({
                    'name': link_name,
                    'type': linked_location.get('type', 'space')
                })
            except KeyError:
                links_with_types.append({
                    'name': link_name,
                    'type': 'unknown'
                })

        location_type = location.get('type', 'space')

        if location_type in ['station', 'ground_station']:
            location_state = {
                'name': location.get('name'),
                'type': location_type,
                'description': location.get('description'),
                'links': links_with_types,
                'ship_count': len(ships_info),
                'items': items_info
            }
        else:
            location_state = {
                'name': location.get('name'),
                'type': location_type,
                'description': location.get('description'),
                'links': links_with_types,
                'ships': ships_info,
                'items': items_info
            }
    else:
        location_state = None

    # Get ship log
    ship_log = await data_handler.get_ship_log(ship_id)

    return convert_ids_to_strings({
        'ship_state': ship_state,
        'location_state': location_state,
        'ship_log': ship_log,
        'scan_data': None
    })


async def push_update_to_ship(ship_id: int):
    """Push an immediate state update to a single connected ship.

    Used by instant-action endpoints (equip, unequip, send_message) so the
    client sees the result right away without waiting for the next tick.
    Safe to call even if the ship is not currently connected.
    """
    if not connection_manager.is_connected(ship_id):
        return
    try:
        update = await build_ship_update(ship_id)
        await connection_manager.send_to_ship(ship_id, {
            'type': 'tick_complete',
            'tick': None,
            'data': update
        })
        logger.debug(f"Pushed instant update to ship {ship_id}")
    except Exception as e:
        logger.error(f"Failed to push instant update to ship {ship_id}: {e}")


async def broadcast_tick_updates(tick_number: int):
    """Broadcast tick completion to all connected WebSocket clients.

    Called by program.py after each tick completes.
    """
    connected_ships = list(connection_manager.active_connections.keys())

    if not connected_ships:
        return

    logger.debug(f"Broadcasting tick {tick_number} to {len(connected_ships)} connected ships")

    ship_updates = {}

    for ship_id in connected_ships:
        try:
            update = await build_ship_update(ship_id)

            # Tick broadcast also clears pending action results (scan data etc.)
            action_results_data = await actions.get_and_clear_action_results(ship_id)
            scan_data = None
            if action_results_data:
                scan_data = action_results_data.get('scan_data')
            update['scan_data'] = scan_data

            ship_updates[ship_id] = update

        except KeyError:
            logger.warning(f"Ship {ship_id} not found during broadcast")
        except Exception as e:
            logger.error(f"Error building update for ship {ship_id}: {e}")

    await connection_manager.broadcast_tick(tick_number, ship_updates)


# Startup logging

logger.info("=" * 70)
logger.info("FastAPI app initialized - ready to be started by program.py")
logger.info("Designed for 100k-200k concurrent WebSocket connections per server")
logger.info("=" * 70)
