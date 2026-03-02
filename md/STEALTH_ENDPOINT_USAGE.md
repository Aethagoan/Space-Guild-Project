# Stealth Operations via /action Endpoint

## Overview
Stealth operations (activate/deactivate) are now handled through the standard `/action` endpoint instead of dedicated `/stealth/*` endpoints.

## Activate Stealth

**Endpoint:** `POST /action`

**Request Body:**
```json
{
  "player_id": 123,
  "action_type": "activate_stealth",
  "target": 0
}
```

**Note:** The `target` field is required by the endpoint but not used for stealth activation. You can pass `0` or any placeholder value.

**Response (Success):**
```json
{
  "status": "success",
  "message": "Action queued"
}
```

**Response (Error):**
```json
{
  "error": "Invalid player_id or player has no ship"
}
```

## Deactivate Stealth

**Endpoint:** `POST /action`

**Request Body:**
```json
{
  "player_id": 123,
  "action_type": "deactivate_stealth",
  "target": 0
}
```

**Note:** The `target` field is required by the endpoint but not used for stealth deactivation. You can pass `0` or any placeholder value.

**Response (Success):**
```json
{
  "status": "success",
  "message": "Action queued"
}
```

## How Stealth Works

### Activation Requirements:
1. Ship must have a stealth cloak component installed
2. Stealth cloak must have health > 0
3. Ship must NOT have taken damage this tick
4. Ship must not already be stealthed

### Duration Calculation:
```
duration_ticks = floor(5 * (1 + tier) * multiplier)
```

Where:
- `tier` = stealth cloak tier (0-9)
- `multiplier` = component multiplier (starts at 1.0, degrades with repairs)

### Automatic Deactivation:
Stealth is automatically deactivated when:
1. Duration expires (ticks down each game tick)
2. Ship takes damage from any source
3. Ship enters a station or starport location
4. Ship performs an attack action

### Processing Order:
Each tick, stealth operations are processed in this order:
1. Tick down all active stealth timers (expirations)
2. Process all game actions (scans, attacks, moves, collects)
3. Process stealth deactivations
4. Process stealth activations

This ensures that:
- You can deactivate and reactivate stealth in the same tick
- Attacks properly disable stealth before stealth activation phase
- Ships that took damage cannot activate stealth

## Check Stealth Status

Stealth status is automatically included in all ship state responses:

**Via `/updates` endpoint:**
```json
{
  "ship_state": {
    "ship_id": 123,
    "is_stealthed": true,
    "hp": 100.0,
    "tier": 0,
    // ... other ship data
  },
  "location_state": {...},
  "ship_log": [...],
  // ... action results
}
```

**Via `/ship` endpoint:**
```json
{
  "ship_id": 123,
  "is_stealthed": true,
  "hp": 100.0,
  "tier": 0,
  // ... other ship data
}
```

**Note:** Ships with active stealth are automatically filtered from:
- `/location` endpoint ship lists
- Ship scan results
- Visible ship IDs in location data

## Example Workflow

```javascript
// 1. Activate stealth before entering hostile territory
fetch('/action', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    player_id: 123,
    action_type: 'activate_stealth',
    target: 0
  })
})

// 2. Wait for next tick to get updated state
const updates = await fetch('/updates?player_id=123')
const state = await updates.json()

// 3. Check if stealth is active
if (state.ship_state.is_stealthed) {
  console.log('Stealth active!')
}

// 4. Deactivate when ready to attack
fetch('/action', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    player_id: 123,
    action_type: 'deactivate_stealth',
    target: 0
  })
})
```

## Deprecated Endpoints

The following endpoints have been removed:
- ❌ `POST /stealth/activate`
- ❌ `POST /stealth/deactivate`
- ❌ `GET /stealth/status`

Use the `/action` endpoint with `activate_stealth` or `deactivate_stealth` action types instead.
