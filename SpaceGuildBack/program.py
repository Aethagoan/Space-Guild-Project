"""
Main game loop for Space Guild.
- Manages the global DataHandler instance.
- Runs tick processing every 5 seconds.
- Eventually will become admin console with god's eye view.
"""

import time
import sys
import os
from datetime import datetime
from typing import Optional
from threading import Event, Lock

import ship
import location
import components
import actions
from data import DataHandler

# Global DataHandler singleton instance
# All modules should import this instance to access game data
data_handler = DataHandler(data_dir="game_data")

# Tick signaling system for /updates endpoint
current_tick_number = 0
tick_number_lock = Lock()
tick_completion_event = Event()  # Set when tick completes, signals waiting clients


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
    
    print(f"\n[{timestamp}] Tick #{tick_number} completed in {duration:.3f}s")
    
    # Only print non-zero stats
    actions_processed = []
    if stats['attack_ship'] > 0:
        actions_processed.append(f"Ship attacks: {stats['attack_ship']}")
    if stats['attack_ship_component'] > 0:
        actions_processed.append(f"Component attacks: {stats['attack_ship_component']}")
    if stats['attack_item'] > 0:
        actions_processed.append(f"Item attacks: {stats['attack_item']}")
    if stats['moves'] > 0:
        actions_processed.append(f"Moves: {stats['moves']}")
    if stats['collects'] > 0:
        actions_processed.append(f"Collects: {stats['collects']}")
    
    if actions_processed:
        print(f"  Actions: {', '.join(actions_processed)}")
    else:
        print("  No actions processed this tick")


def save_world_data(save_interval: int, tick_number: int, data_handler: DataHandler):
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


def run_game_loop(tick_interval: float = 5.0, save_interval: int = 60):
    """Main game loop - processes ticks every tick_interval seconds.
    
    Args:
        tick_interval: Time between ticks in seconds (default: 5.0)
        save_interval: Number of ticks between auto-saves (default: 60 = every 5 minutes)
    """
    global current_tick_number, tick_completion_event
    
    print("=" * 70)
    print("SPACE GUILD - GAME LOOP")
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
    
    print(f"\n[*] Game loop configuration:")
    print(f"  Tick interval: {tick_interval}s")
    print(f"  Auto-save: Every {save_interval} ticks ({save_interval * tick_interval / 60:.1f} minutes)")
    
    print("\n[*] Starting game loop... (Press Ctrl+C to stop)")
    print("=" * 70)
    
    tick_number = 0
    
    try:
        while True:
            tick_number += 1
            tick_start = time.time()
            
            # Clear the tick completion event before processing
            tick_completion_event.clear()
            
            # Process game tick
            try:
                stats = actions.process_tick()
                tick_duration = time.time() - tick_start
                
                # Update global tick number
                with tick_number_lock:
                    current_tick_number = tick_number
                
                # Signal all waiting clients that tick is complete
                tick_completion_event.set()
                
                # Notify all /updates endpoints waiting on condition variables
                # Import here to avoid circular dependency if api.py imports program
                try:
                    import api
                    api.notify_all_waiting_clients()
                except ImportError:
                    # API module not loaded (e.g., running standalone game loop)
                    pass
                
                # Print tick statistics
                print_tick_stats(tick_number, stats, tick_duration)
                
                # Auto-save at intervals
                save_world_data(save_interval, tick_number, data_handler)
                
            except Exception as e:
                print(f"\n[X] ERROR during tick #{tick_number}: {e}")
                import traceback
                traceback.print_exc()
                # Still signal completion even on error
                tick_completion_event.set()
                
                # Notify waiting clients even on error
                try:
                    import api
                    api.notify_all_waiting_clients()
                except ImportError:
                    pass
            
            # Sleep until next tick
            elapsed = time.time() - tick_start
            sleep_time = max(0, tick_interval - elapsed)
            
            if sleep_time > 0:
                time.sleep(sleep_time)
            else:
                # Tick took longer than interval - log warning
                print(f"  [!] Warning: Tick took {elapsed:.3f}s (>{tick_interval}s interval)")
    
    except KeyboardInterrupt:
        print("\n\n" + "=" * 70)
        print("[!] Game loop stopped by user")
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


if __name__ == '__main__':
    # Run the game loop with default settings (5 second ticks)
    run_game_loop(tick_interval=5.0, save_interval=60)


