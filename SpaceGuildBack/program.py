"""
Main async program for Space Guild.
- Manages the global DataHandler instance.
- Runs async tick processing every 5 seconds.
- Runs FastAPI/Uvicorn server for WebSocket and REST API.
- Single process architecture for 1M concurrent connections.
"""

import asyncio
import sys
import os
from datetime import datetime
from typing import Optional
import uvicorn
from uvicorn import Config, Server

import ship
import location
import components
import actions
from data import DataHandler

# Global DataHandler singleton instance
# All modules should import this instance to access game data
data_handler = DataHandler(data_dir="game_data")

# Tick signaling system for real-time updates
current_tick_number = 0
tick_number_lock = asyncio.Lock()


def check_world_initialized(data_dir: str = "game_data") -> bool:
    """Check if the world has been initialized by setup.py.
    
    Args:
        data_dir: Directory where game data should be stored
        
    Returns:
        True if world data exists, False otherwise
    """
    locations_file = os.path.join(data_dir, "locations.json")
    return os.path.exists(locations_file)


def print_tick_stats(tick_number: int, stats: dict, duration: float):
    """Print statistics for a completed tick.
    
    Args:
        tick_number: Current tick number
        stats: Dictionary of action counts from process_tick()
        duration: Time taken to process tick in seconds
    """
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    print(f"\n{'='*70}")
    print(f"[{timestamp}] TICK #{tick_number} completed in {duration:.3f}s")
    print(f"{'='*70}")
    
    # Only print non-zero stats
    actions_processed = []
    if stats['scans'] > 0:
        actions_processed.append(f"  • Scans: {stats['scans']}")
    if stats['attack_ship'] > 0:
        actions_processed.append(f"  • Ship attacks: {stats['attack_ship']}")
    if stats['attack_ship_component'] > 0:
        actions_processed.append(f"  • Component attacks: {stats['attack_ship_component']}")
    if stats['attack_item'] > 0:
        actions_processed.append(f"  • Item attacks: {stats['attack_item']}")
    if stats['moves'] > 0:
        actions_processed.append(f"  • Moves: {stats['moves']}")
    if stats['collects'] > 0:
        actions_processed.append(f"  • Collects: {stats['collects']}")
    if stats['drops'] > 0:
        actions_processed.append(f"  • Drops: {stats['drops']}")
    if stats['stealth_activations'] > 0:
        actions_processed.append(f"  • Stealth activations: {stats['stealth_activations']}")
    if stats['stealth_deactivations'] > 0:
        actions_processed.append(f"  • Stealth deactivations: {stats['stealth_deactivations']}")
    
    if actions_processed:
        print("ACTIONS PROCESSED:")
        print('\n'.join(actions_processed))
    else:
        print("  No actions processed this tick")
    
    print(f"{'='*70}\n")


async def save_world_data(save_interval: int, tick_number: int, data_handler: DataHandler):
    """Save world data at regular intervals.
    
    Args:
        save_interval: Number of ticks between saves
        tick_number: Current tick number
        data_handler: DataHandler instance to save
    """
    if tick_number % save_interval == 0:
        print(f"\n[*] Auto-saving world data (tick #{tick_number})...")
        try:
            data_handler.save_dynamic()
            print("  [+] Save complete")
        except Exception as e:
            print(f"  [X] Save failed: {e}")


async def run_tick_loop(tick_interval: float = 5.0, save_interval: int = 60):
    """Async game loop - processes ticks every tick_interval seconds.
    
    Args:
        tick_interval: Time between ticks in seconds (default: 5.0)
        save_interval: Number of ticks between auto-saves (default: 60 = every 5 minutes)
    """
    global current_tick_number
    
    print("=" * 70)
    print("SPACE GUILD - ASYNC TICK LOOP")
    print("=" * 70)
    
    # Check if world is initialized
    if not check_world_initialized():
        print("\n[X] ERROR: World not initialized!")
        print("Please run 'python setup.py' first to create the game world.")
        return
    
    print(f"\n[*] Loading world data...")
    try:
        data_handler.load_all()
        print("  [+] World loaded successfully")
    except Exception as e:
        print(f"  [X] Failed to load world: {e}")
        return
    
    # Validate and repair ship locations (failsafe for data integrity)
    print(f"\n[*] Validating ship locations...")
    try:
        repair_stats = await data_handler.validate_and_repair_ship_locations(default_location='Earth_Orbit')
        print(f"  [+] Validation complete:")
        print(f"    Ships checked: {repair_stats['ships_checked']}")
        if repair_stats['ships_repaired'] > 0:
            print(f"    Ships with no location: {repair_stats['ships_with_no_location']}")
            print(f"    Ships with invalid location: {repair_stats['ships_with_invalid_location']}")
            print(f"    Ships not in location list: {repair_stats['ships_not_in_location_list']}")
            print(f"    Ships repaired: {repair_stats['ships_repaired']}")
        else:
            print(f"    All ships have valid locations")
    except Exception as e:
        print(f"  [!] Warning: Ship location validation failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Print loaded data stats
    num_locations = len(data_handler.Locations)
    num_ships = len(data_handler.Ships)
    num_items = len(data_handler.Items)
    num_players = len(data_handler.Players)
    num_factions = len(data_handler.Factions)
    
    print(f"\n[*] World Statistics:")
    print(f"  Locations: {num_locations}")
    print(f"  Ships: {num_ships}")
    print(f"  Items: {num_items}")
    print(f"  Players: {num_players}")
    print(f"  Factions: {num_factions}")
    
    # Initialize location visibility cache
    print(f"\n[*] Initializing location visibility cache...")
    await actions.update_all_location_visibility()
    print("  [+] Visibility cache initialized")
    
    print(f"\n[*] Tick loop configuration:")
    print(f"  Tick interval: {tick_interval}s")
    print(f"  Auto-save: Every {save_interval} ticks ({save_interval * tick_interval / 60:.1f} minutes)")
    
    print("\n[*] Starting async tick loop...")
    print("=" * 70)
    
    tick_number = 0
    
    try:
        while True:
            tick_number += 1
            tick_start = asyncio.get_event_loop().time()
            
            # Process game tick
            try:
                stats = await actions.process_tick()
                tick_duration = asyncio.get_event_loop().time() - tick_start
                
                # Update global tick number
                async with tick_number_lock:
                    current_tick_number = tick_number
                
                # Broadcast tick updates to all connected WebSocket clients
                try:
                    from api_fastapi import broadcast_tick_updates
                    await broadcast_tick_updates(tick_number)
                except ImportError:
                    # API module not loaded (e.g., running standalone game loop)
                    pass
                
                # Print tick statistics
                print_tick_stats(tick_number, stats, tick_duration)
                
                # Auto-save at intervals
                await save_world_data(save_interval, tick_number, data_handler)
                
            except Exception as e:
                print(f"\n[X] ERROR during tick #{tick_number}: {e}")
                import traceback
                traceback.print_exc()
                
                # Still broadcast update even on error
                try:
                    from api_fastapi import broadcast_tick_updates
                    await broadcast_tick_updates(tick_number)
                except ImportError:
                    pass
            
            # Sleep until next tick
            elapsed = asyncio.get_event_loop().time() - tick_start
            sleep_time = max(0, tick_interval - elapsed)
            
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
            else:
                # Tick took longer than interval - log warning
                print(f"  [!] Warning: Tick took {elapsed:.3f}s (>{tick_interval}s interval)")
    
    except asyncio.CancelledError:
        print("\n\n" + "=" * 70)
        print("[!] Tick loop stopped")
        print("=" * 70)
        
        # Final save
        print("\n[*] Saving final world state...")
        try:
            data_handler.save_dynamic()
            print("  [+] Final save complete")
        except Exception as e:
            print(f"  [X] Final save failed: {e}")
        
        print(f"\n[*] Final Statistics:")
        print(f"  Total ticks processed: {tick_number}")
        print(f"  Total runtime: {tick_number * tick_interval / 60:.1f} minutes")
        print("\n[*] Goodbye!")


async def run_server_and_tick_loop(
    tick_interval: float = 5.0,
    save_interval: int = 60,
    host: str = "0.0.0.0",
    port: int = 8000
):
    """Run both the Uvicorn FastAPI server AND the tick loop in one process.
    
    Args:
        tick_interval: Time between ticks in seconds (default: 5.0)
        save_interval: Number of ticks between auto-saves (default: 60)
        host: API server host (default: 0.0.0.0)
        port: API server port (default: 8000)
    """
    # Import and configure FastAPI app
    from api_fastapi import app, set_data_handler
    import actions
    import components
    
    # Set the DataHandler reference in api_fastapi, actions, and components modules
    set_data_handler(data_handler)
    actions._set_data_handler(data_handler)
    components._set_data_handler(data_handler)
    
    # Configure Uvicorn server
    config = Config(
        app=app,
        host=host,
        port=port,
        log_level="info",
        access_log=True
    )
    server = Server(config)
    
    print("=" * 70)
    print("SPACE GUILD - ASYNC SERVER + TICK LOOP")
    print("=" * 70)
    print(f"\n[*] Starting FastAPI server on {host}:{port}")
    print(f"[*] WebSocket endpoint: ws://{host}:{port}/ws/{{ship_id}}")
    print(f"[*] Tick interval: {tick_interval}s")
    print("=" * 70 + "\n")
    
    # Run both the server and tick loop concurrently
    await asyncio.gather(
        server.serve(),  # FastAPI server
        run_tick_loop(tick_interval, save_interval)  # Tick loop
    )


if __name__ == '__main__':
    # Run everything under one async event loop
    try:
        asyncio.run(run_server_and_tick_loop(tick_interval=5.0, save_interval=60))
    except KeyboardInterrupt:
        print("\n[!] Shutting down...")


