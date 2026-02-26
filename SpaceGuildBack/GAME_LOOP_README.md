# Space Guild - Game Loop & Setup

This document explains how to set up and run the Space Guild game server.

## Architecture Overview

Space Guild uses a **3-process architecture**:

1. **setup.py** - One-time world initialization
2. **program.py** - Main game loop (processes ticks every 5 seconds)
3. **api.py** - Flask REST API (handles player actions)

The game loop and API server run as **separate processes** that share the same game data through JSON files.

## Quick Start

### 1. Initialize the World

First, run the setup script to create the game world:

```bash
cd SpaceGuildBack
python setup.py
```

This will:
- Create 20+ locations across multiple star systems
- Link locations together (jump gates, trade routes, etc.)
- Save location dialogue data
- Generate all initial JSON data files

**Note:** If world data already exists, setup.py will prompt you before overwriting.

### 2. Start the Game Loop

In one terminal, start the main game loop:

```bash
python program.py
```

This will:
- Load the world data
- Process game ticks every 5 seconds
- Execute queued actions (combat, movement, collection)
- Auto-save world state every 60 ticks (~5 minutes)
- Display tick statistics in real-time

**Press Ctrl+C to stop the game loop gracefully.**

### 3. Start the API Server (Separate Terminal)

In another terminal, start the Flask API server:

```bash
python api.py
```

This will:
- Load the world data (read-only at startup)
- Start Flask server on `http://0.0.0.0:5000`
- Accept player action requests
- Queue actions for the next tick

## How It Works

### Game Loop (program.py)

The game loop runs continuously with these responsibilities:

- **Tick Processing**: Every 5 seconds, processes all queued actions
- **Action Execution**: Executes attacks, moves, and collections in order
- **Concurrency**: Multiple locations process actions in parallel
- **Auto-Save**: Saves world state every 60 ticks (configurable)
- **Statistics**: Displays tick stats (actions processed, duration, etc.)

### API Server (api.py)

The API runs as a separate process and handles:

- **Action Queueing**: Players queue actions via HTTP POST
- **Data Queries**: Get ship logs, location info, etc.
- **Repairs**: Process component repairs
- **Authentication**: (TODO - currently uses player_id directly)

### Data Synchronization

Both processes share data through:

- **JSON Files**: Locations, ships, items, players, factions
- **File System**: Data stored in `game_data/` directory
- **Thread-Safe DataHandler**: All modifications use fine-grained locking

**Important:** The game loop writes data every 60 ticks. The API reads data at startup and queues actions in memory (action queues are cleared each tick).

## Configuration

### Tick Interval

Default: 5 seconds

To change, edit `program.py`:

```python
run_game_loop(tick_interval=5.0)  # Change to desired seconds
```

### Auto-Save Interval

Default: 60 ticks (5 minutes at 5-second ticks)

To change, edit `program.py`:

```python
run_game_loop(save_interval=60)  # Change to desired tick count
```

### API Server Port

Default: 5000

To change, edit `api.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

## Setup.py - World Configuration

The setup script creates a multi-system world with jump gates. It's currently configured with a **template world** that includes:

- **Sol System** (Earth, Mars, Jupiter, Sol Jump Gate)
- **Alpha Centauri** (Proxima Station, Centauri Prime, multiple jump gates)
- **Sirius System** (Mining belts, trade stations)
- **Vega System** (Trading hub, shipyard, frontier gateway)
- **Frontier Space** (Pirate havens, derelicts, anomalies)

### Customizing the World

To customize locations and links, edit `setup.py`:

1. **Edit `create_world_locations()`** - Add/remove locations and dialogue
2. **Edit `create_world_links()`** - Define bidirectional and one-way links
3. Run `python setup.py` to regenerate the world

### Location Dialogue

Dialogue is stored separately in `game_data/location_dialogue.json`. Each location has a list of dialogue strings that can be displayed to players.

Format:
```json
{
  "Earth_Orbit": {
    "dialogue": [
      "Welcome to Earth Orbit Station.",
      "The blue marble below holds billions of souls."
    ]
  }
}
```

## API Endpoints

### Queue Action
```
POST /action
Content-Type: application/json

{
  "player_id": 1,
  "action_type": "move",
  "target": "Mars_Colony",
  "target_data": null,  // Optional
  "action_hash": "abc123"  // Optional (spam protection)
}

Response: {"status": "success"}
```

**Action Types:**
- `attack_ship` - Attack another ship's HP
- `attack_ship_component` - Attack a specific component
- `attack_item` - Attack an item at a location
- `move` - Move to a linked location
- `collect` - Collect an item into cargo

### Get Ship Log
```
GET /ship/log?player_id=1

Response: {
  "entries": [
    {"type": "combat", "content": "Attacked ship 42 for 10 damage"},
    {"type": "movement", "content": "Moved to Mars_Colony"}
  ]
}
```

### Health Check
```
GET /health

Response: {"status": "healthy"}
```

### Repair Component
```
POST /repair/component
Content-Type: application/json

{
  "player_id": 1,
  "item_id": 5
}

Response: {
  "status": "success",
  "health_restored": 40.0,
  "multiplier_reduction": 0.05,
  "new_multiplier": 2.95
}
```

## Troubleshooting

### "World not initialized" error

Run `python setup.py` first to create the game world.

### API can't connect to game data

Make sure `game_data/` directory exists with JSON files. Both program.py and api.py must be run from the `SpaceGuildBack` directory.

### Tick processing is slow

This is expected if many actions are queued. The game loop will log a warning if a tick takes longer than 5 seconds.

Consider:
- Reducing the number of concurrent actions
- Increasing tick interval
- Optimizing action processing

### Auto-save failed

Check file permissions on the `game_data/` directory. The game loop needs write access to save JSON files.

## Development Roadmap

### Current Status

✅ World setup with locations and links
✅ Game loop with 5-second ticks
✅ API server for player actions
✅ Auto-save functionality
✅ Tick statistics

### Future Plans

- **Admin Console**: Transform program.py into a god's-eye view console
- **Authentication**: JWT tokens for API security
- **NPC Spawning**: Dynamic ship/item spawning system
- **Faction AI**: Automated faction behavior
- **Real-time Events**: Random events during ticks
- **Web Dashboard**: Monitor game state in browser

## Known Issues

### Movement Timing

There's a potential edge case where ships moving between locations at slightly different tick times could cause odd behavior. This is being monitored but should be rare due to the per-location processing architecture.

### Flask Imports

If you see "Import 'flask' could not be resolved" warnings, make sure Flask is installed:

```bash
pip install flask
```

This is only a type-checking warning and doesn't affect runtime.

## Contact

For questions or issues, see the main project README.
