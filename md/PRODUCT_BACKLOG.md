# Space Guild - Product Backlog

**Last Updated:** 25 Feb 2026  
**Current Sprint:** Sprint 0 Completion → Sprint 1  
**Priority System:** P0 (Critical/Blocking) → P1 (High) → P2 (Medium) → P3 (Low)

---

## SPRINT 0: Critical Blockers (Fix to Run Code) [~75% COMPLETE]
**Goal:** Make the codebase executable  
**Estimated Effort:** 4-6 hours | **Remaining:** ~2 hours

### P0 - Blocking Issues

- [x] **FIX-001:** Fix import statements in `data.py` ✅
  - All imports correct: `from location import Location`, `from player import Player`, `from ship import Ship`

- [x] **FIX-002:** Fix import statements in `program.py` ✅
  - All imports correct

- [x] **FIX-003:** Fix Ship factory type definitions in `ship.py` ✅
  - Component IDs properly set to `None`

- [x] **FIX-004:** Fix Faction factory type definitions in `faction.py`
  - Lines 7, 9: Change from type placeholders to actual values
  - `'name': ""` not `'name': str`
  - `'color': ""` not `'color': str`
  - **Blocks:** Faction creation

- [X] **FIX-005:** Fix Player factory default in `player.py`
  - Line 11: Change `'faction_id': int` to `'faction_id': None`
  - **Blocks:** Player creation

- [x] **FIX-006:** Action handler decision ✅
  - Action handler exists but is unused by API
  - Decision: Keep in codebase, API directly calls `queue_action()` for now
  - Can revisit later if needed

- [ ] **RUN-001:** Add program entry point
  - Add `if __name__ == '__main__'` block to `program.py`
  - Initialize DataHandler
  - Start Flask app
  - Start tick loop (threading.Timer or asyncio)
  - **Blocks:** Running the game

- [~] **SHIP-001:** Implement basic ship creation (PARTIALLY DONE)
  - Ship factory exists ✅
  - TODO: Add tier-0 component loading and initialization helper
  - **Blocks:** Player spawning and gameplay

---

## SPRINT 1: Minimal Viable Backend (Week 1-2) [~10% COMPLETE]
**Goal:** Get a runnable backend with basic state access  
**Estimated Effort:** 20-30 hours

### P0 - Critical for MVP

#### Tick System
- [~] **TICK-001:** Complete tick loop runner (PARTIALLY DONE)
  - `process_tick()` function exists ✅
  - TODO: Add automated timer calling it every 5 seconds (threading.Timer or asyncio)
  - TODO: Add tick counter/timestamp tracking
  - **Epic:** Core Game Loop
  - **Estimate:** 2h remaining

- [ ] **TICK-002:** Add tick broadcast mechanism
  - Store tick results per location
  - Allow clients to poll for tick updates
  - Clear old tick data
  - **Epic:** Core Game Loop
  - **Estimate:** 4h

#### Basic API Expansion
- [ ] **API-001:** Add GET `/ship/<id>` endpoint
  - Return complete ship state (HP, location, components, items)
  - Include equipped component details
  - **Epic:** State Access API
  - **Estimate:** 2h

- [ ] **API-002:** Add GET `/location/<id>` endpoint
  - Return location name, links, ships present, items present
  - Include last tick events if logging implemented
  - **Epic:** State Access API
  - **Estimate:** 2h

- [ ] **API-003:** Add GET `/player/<id>` endpoint
  - Return player info and associated ship data
  - **Epic:** State Access API
  - **Estimate:** 1H

- [ ] **API-004:** Add GET `/item/<id>` endpoint
  - info about an item based on sensors
  - in general and for now just returns the item details.
  - **Epic:** State Access API
  - **Estimate:** 1h

- [ ] **API-005:** Add GET `/game/tick` endpoint (ping-pong)
  - waits for next tick to complete, and then returns location data.
  - **Epic:** State Access API
  - **Estimate:** 1h

#### Minimal World Content
- [ ] **WORLD-001:** Create starter location graph
  - Create the first system in 
  - Link them together
  - write a setup script that is called if nothing gets loaded from the json files.
  - **Epic:** SOL System Content
  - **Estimate:** 3h

- [ ] **WORLD-002:** Create player spawn system
  - New player spawns at Earth Orbit
  - New player gets starter ship (tier 1, basic components)
  - Initialize player credits (10,000 starting balance)
  - **Epic:** Player Progression
  - **Estimate:** 4h

### P1 - High Priority

#### Data Initialization
- [ ] **DATA-001:** Add world data loading in `program.py`
  - Load locations from JSON or create programmatically
  - Load starter stations and inventories
  - Initialize faction data
  - **Epic:** Data Management
  - **Estimate:** 3h

- [ ] **DATA-002:** Add save/autosave system
  - Auto-save every N ticks
  - Save on shutdown
  - Backup system
  - **Epic:** Data Management
  - **Estimate:** 4h

#### Error Handling
- [ ] **ERR-001:** Add Python logging throughout
  - Log all API requests
  - Log all tick executions
  - Log all errors and exceptions
  - Configure log levels
  - **Epic:** Debugging & Operations
  - **Estimate:** 3h

- [ ] **ERR-002:** Add input validation to API endpoints
  - Validate request schemas
  - Return proper error messages
  - Handle malformed data gracefully
  - **Epic:** API Robustness
  - **Estimate:** 4h

---

## SPRINT 2: Economy & Stations (Week 2-3)
**Goal:** Players can dock, buy/sell items, manage inventory  
**Estimated Effort:** 30-40 hours

### P0 - Critical for Gameplay Loop

#### Station Entity
- [ ] **STATION-001:** Create Station entity in `data.py`
  - Station ID, name, location_id
  - Faction owner
  - Station type (vendor, shipyard, research, etc.)
  - Docking bay capacity (max ships)
  - Inventory dictionary (item_id → quantity)
  - Prices dictionary (item_id → price)
  - **Epic:** Station System
  - **Estimate:** 4h

- [ ] **STATION-002:** Add Station CRUD operations to DataHandler
  - create_station, get_station, update_station, delete_station
  - Thread-safe operations with locking
  - **Epic:** Station System
  - **Estimate:** 4h

- [ ] **STATION-003:** Implement docking mechanics
  - Dock action (move ship from location to station docked list)
  - Undock action (reverse)
  - Capacity validation
  - **Epic:** Station System
  - **Estimate:** 5h

#### Station API
- [ ] **API-010:** Add GET `/station/<id>` endpoint
  - Return station details and inventory
  - Show docked ships
  - **Epic:** Station System
  - **Estimate:** 2h

- [ ] **API-011:** Add GET `/station/<id>/inventory` endpoint
  - List all items/components for sale with prices
  - Filter by type or tier
  - **Epic:** Station System
  - **Estimate:** 2h

- [ ] **API-012:** Add POST `/station/<id>/buy` endpoint
  - Player buys item from station
  - Deduct credits, add item to ship cargo
  - Validate funds, cargo space, docking status
  - **Epic:** Station System
  - **Estimate:** 5h

- [ ] **API-013:** Add POST `/station/<id>/sell` endpoint
  - Player sells item to station
  - Add credits, remove item from ship
  - Validate item ownership, docking status
  - **Epic:** Station System
  - **Estimate:** 4h

- [ ] **API-014:** Add POST `/action/dock` endpoint
  - Queue dock action for next tick
  - Validate station proximity
  - **Epic:** Station System
  - **Estimate:** 2h

- [ ] **API-015:** Add POST `/action/undock` endpoint
  - Queue undock action for next tick
  - **Epic:** Station System
  - **Estimate:** 2h

### P1 - High Priority

#### Starter Station Content
- [ ] **CONTENT-001:** Create Earth Orbital Station Zero
  - Add to Earth Orbit location
  - Populate vendor inventory (20-30 items)
  - Tier 1-3 components of all types
  - Set reasonable prices
  - **Epic:** SOL System Content
  - **Estimate:** 4h

- [ ] **CONTENT-002:** Create additional starter stations
  - Moon Ground Station (mining gear focus)
  - Earth Ground Station Zero (general purpose)
  - **Epic:** SOL System Content
  - **Estimate:** 3h

---

## SPRINT 3: Location Event Logging (Week 3-4)
**Goal:** Players can see what happened at their location last tick  
**Estimated Effort:** 6-8 hours

### P1 - High Priority

#### Location Event Log System
- [ ] **LOG-001:** Implement location event log storage
  - Add event list to Location entity (max 100 messages, ephemeral)
  - Timestamp + event type + message
  - FIFO rotation when full (same as ship logs)
  - **Epic:** Logging System
  - **Estimate:** 2h

- [ ] **LOG-002:** Add event entries during tick processing
  - Movement actions: "Ship-X moved to Location-B"
  - Combat actions: "Ship-X attacked Ship-Y for Z damage"
  - Collection: "Ship-X picked up Item-Y"
  - Docking: "Ship-X docked at Station-Y"
  - **Epic:** Logging System
  - **Estimate:** 3h

- [ ] **API-020:** Add GET `/location/<id>/events` endpoint
  - Return last tick's events at location
  - Show what happened in the location
  - **Epic:** Logging System
  - **Estimate:** 1h

#### Ship Logging (Optional - for personal ship history)
- [ ] **LOG-003:** Implement ship log storage
  - Add log list to Ship entity (max 100 messages)
  - Timestamp + event type + message
  - FIFO rotation when full
  - **Epic:** Logging System
  - **Estimate:** 2h

- [ ] **API-021:** Add GET `/ship/<id>/log` endpoint
  - Return last N log entries for the ship
  - Filter by event type
  - **Epic:** Logging System
  - **Estimate:** 1h

---

## SPRINT 4: SOL System Content (Week 4-5)
**Goal:** Expand playable universe with 15-20 locations  
**Estimated Effort:** 20-30 hours

### P1 - High Priority

#### Inner System
- [ ] **SOL-001:** Implement Earth subsystem
  - Earth Orbit (done in Sprint 1)
  - Earth Orbital Station Zero (done in Sprint 2)
  - Earth Ground Station Zero
  - Moon Orbit
  - Moon Ground Station
  - Link all locations
  - **Epic:** SOL System Content
  - **Estimate:** 3h

- [ ] **SOL-002:** Implement Venus subsystem
  - Venus Orbit
  - Venus Ground Station Zero
  - Venus Orbital Station Zero
  - Link to SOL network
  - **Epic:** SOL System Content
  - **Estimate:** 2h

- [ ] **SOL-003:** Implement Mars subsystem
  - Mars Orbit
  - Mars Ground Station Zero
  - Mars Orbital Station Zero
  - Mars Moon 1 Ground Station
  - Mars Moon 2 Ground Station
  - Link to SOL network
  - **Epic:** SOL System Content
  - **Estimate:** 3h

- [ ] **SOL-004:** Implement Mercury subsystem
  - Mercury Orbit
  - Mercury Ground Station
  - Link to SOL network
  - **Epic:** SOL System Content
  - **Estimate:** 2h

#### Asteroid Belt & Outer System
- [ ] **SOL-005:** Implement Asteroid Belt
  - Belt Region 1 Orbit + Station
  - Belt Region 2 Orbit + Station
  - Belt Region 3 Orbit + Station
  - Resource gather mechanics (future epic)
  - **Epic:** SOL System Content
  - **Estimate:** 3h

- [ ] **SOL-006:** Implement Jupiter subsystem
  - Jupiter Orbit
  - Jupiter Atmosphere Station 'Thunder Station'
  - IO Station
  - Link to SOL network
  - **Epic:** SOL System Content
  - **Estimate:** 2h

- [ ] **SOL-007:** Implement Saturn subsystem
  - Saturn Orbit
  - Saturn Atmosphere Station 'Cloud Station'
  - Ring Station 1
  - Ring Station 2
  - Link to SOL network
  - **Epic:** SOL System Content
  - **Estimate:** 3h

- [ ] **SOL-008:** Implement Uranus subsystem
  - Uranus Orbit
  - Uranus Orbital Station
  - Uranus Atmosphere Station
  - Link to SOL network
  - **Epic:** SOL System Content
  - **Estimate:** 2h

- [ ] **SOL-009:** Implement Kuiper Belt regions
  - Kuiper Region 1 Orbit + Station
  - Kuiper Region 2 Orbit + Station
  - Kuiper Region 3 Orbit + Station
  - Kuiper Region 4 Orbit + Station
  - Link to SOL network
  - **Epic:** SOL System Content
  - **Estimate:** 3h

- [ ] **SOL-010:** Implement special locations
  - Sun Orbital location
  - SOL -> ALPHA Warp Gate Orbital
  - **Epic:** SOL System Content
  - **Estimate:** 2h

### P2 - Medium Priority

#### Station Content
- [ ] **CONTENT-010:** Populate all SOL stations with inventories
  - Create 15-20 station inventories
  - Specialize by location (mining, military, research, etc.)
  - Balance component tier availability
  - **Epic:** SOL System Content
  - **Estimate:** 6h

- [ ] **CONTENT-011:** Add location descriptions and metadata
  - Lore text for each location
  - Danger levels
  - Faction ownership
  - Visual descriptions
  - **Epic:** SOL System Content
  - **Estimate:** 4h

---

## SPRINT 5: Testing & Stability (Week 5-6)
**Goal:** Comprehensive test coverage and performance validation  
**Estimated Effort:** 20-25 hours

### P0 - Critical

#### Test Infrastructure
- [ ] **TEST-001:** Rewrite test suite for current codebase
  - Remove all old tests (currently broken)
  - Set up pytest properly
  - Create test fixtures for DataHandler, locations, ships, players
  - **Epic:** Testing Infrastructure
  - **Estimate:** 5h

#### Unit Tests
- [ ] **TEST-010:** DataHandler unit tests
  - Test all CRUD operations for each entity type
  - Test locking mechanisms
  - Test JSON save/load
  - **Epic:** Testing Infrastructure
  - **Estimate:** 5h

- [ ] **TEST-011:** Components unit tests
  - Test stat calculations for all component types
  - Test repair mechanics and degradation
  - Test equipment/unequipment
  - **Epic:** Testing Infrastructure
  - **Estimate:** 3h

- [ ] **TEST-012:** Actions unit tests
  - Test all action types
  - Test action queue operations
  - Test tick processing
  - Test spam protection
  - **Epic:** Testing Infrastructure
  - **Estimate:** 5h

#### Integration Tests
- [ ] **TEST-020:** Full tick cycle integration test
  - Multiple players queue actions
  - Process tick
  - Verify correct execution order
  - Verify state changes
  - **Epic:** Testing Infrastructure
  - **Estimate:** 4h

- [ ] **TEST-021:** Combat scenario integration test
  - Two ships attack each other
  - Verify damage calculations
  - Verify shield mechanics
  - Verify component destruction
  - **Epic:** Testing Infrastructure
  - **Estimate:** 3h

#### Performance Tests
- [ ] **TEST-030:** Load test with 100+ ships
  - Create 100 ships in same location
  - Queue various actions
  - Measure tick processing time
  - Ensure < 1 second tick processing
  - **Epic:** Testing Infrastructure
  - **Estimate:** 4h

- [ ] **TEST-031:** Lock contention test
  - Concurrent API requests
  - Verify no deadlocks
  - Verify data consistency
  - **Epic:** Testing Infrastructure
  - **Estimate:** 3h

---

## BACKLOG: Authentication & Security
**Priority:** P1 (Required for multiplayer)  
**Epic:** Authentication System

- [ ] **AUTH-001:** Design authentication system
  - JWT tokens vs sessions
  - Password hashing strategy (bcrypt)
  - Token refresh mechanism
  - **Estimate:** 2h

- [ ] **AUTH-002:** Add User entity
  - username, email, password_hash
  - created_at, last_login
  - player_id reference
  - **Estimate:** 2h

- [ ] **AUTH-003:** Implement user registration
  - POST `/register` endpoint
  - Validate email/username uniqueness
  - Hash password
  - Create associated Player and Ship
  - **Estimate:** 5h

- [ ] **AUTH-004:** Implement login system
  - POST `/login` endpoint
  - Verify credentials
  - Generate JWT token
  - Return token + player info
  - **Estimate:** 4h

- [ ] **AUTH-005:** Add authentication middleware
  - Verify JWT on protected endpoints
  - Extract player_id from token
  - Return 401 on invalid token
  - **Estimate:** 3h

- [ ] **AUTH-006:** Implement logout/token revocation
  - Token blacklist or expiration
  - POST `/logout` endpoint
  - **Estimate:** 3h

- [ ] **AUTH-007:** Add password reset flow
  - Email-based reset (future)
  - Admin password reset
  - **Estimate:** 4h

---

## BACKLOG: Component Mechanics
**Priority:** P2 (Enhance gameplay depth)  
**Epic:** Component Systems

### Engine Mechanics
- [ ] **COMP-001:** Implement engine-based movement range
  - Define speed stat per engine tier (how many graph nodes can you cross at once?)
  - Limit moves per tick based on engine
  - Multi-tick travel for long distances
  - **Estimate:** 6h

### Sensor Mechanics
- [ ] **COMP-010:** Implement sensor-based cargo detection
  - Define sensor range per tier
  - What kinds of cargo can you detect?
  - What details can you see on the navigation page?
  - Ships/items outside range provide less information
  - **Estimate:** 8h

### Stealth Cloak Mechanics
- [ ] **COMP-020:** Implement basic cloaking system
  - "Cloak" action to enable stealth
  - "Uncloak" action or auto-uncloak on action
  - How many ticks can you go unnoticed?
  - Basic stealth duration mechanics
  - **Estimate:** 6h

---

## BACKLOG: Faction System & NPC Ships
**Priority:** P1 (Expand endgame content - player factions are the next step when gameloop becomes routine)  
**Epic:** Faction Politics

### Player Faction Creation
- [ ] **FACTION-001:** Implement player faction/guild creation
  - Players can create guilds/factions
  - Guild membership management
  - Guild banks, shared resources
  - Guild territory claims
  - **Estimate:** 20h

### NPC Ship Behaviors (Simple Boid-like AI)
- [ ] **NPC-001:** Design simple NPC ship behavior system
  - Mathematical boid-like movement (not CPU intensive)
  - Basic patrol behaviors
  - Territorial presence calculations
  - **Estimate:** 8h

- [ ] **NPC-002:** Implement faction territory presence
  - Calculate faction presence by counting ships per location
  - Display dominant faction at locations
  - No complex warfare mechanics - just analytical presence
  - **Estimate:** 4h

- [ ] **NPC-003:** Create patrol ship spawning
  - Spawn NPC ships at faction territories
  - Simple patrol routes between locations
  - Basic combat engagement rules
  - **Estimate:** 8h

- [ ] **NPC-004:** Add pirate NPC ships
  - Spawn pirates in certain locations (e.g., asteroid belts)
  - Simple aggression behavior
  - Attack ships based on simple rules
  - **Estimate:** 6h

---

## BACKLOG: Ship Progression
**Priority:** P1 (Core gameplay loop)  
**Epic:** Player Progression

- [ ] **PROG-001:** Implement ship tier upgrade system
  - Upgrade ship to next tier via station quest
  - Quest-based upgrade (return X items for tier upgrade)
  - Simple tier increase mechanic
  - **Estimate:** 4h

- [ ] **PROG-002:** Add ship symbol customization
  - Player can pick a symbol for their ship
  - Display symbol in game UI
  - **Estimate:** 2h

---

## BACKLOG: Combat Mechanics
**Priority:** P2 (Keep it simple)  
**Epic:** Combat Systems

- [ ] **COMBAT-001:** Add component targeting
  - Target specific ship components (engine, weapons, shields, etc.)
  - Damage directed at specific component
  - Component destruction mechanics
  - **Estimate:** 6h

- [ ] **COMBAT-002:** Add simple NPC combat AI
  - NPC ships can attack players
  - Simple targeting logic (closest, weakest, etc.)
  - Basic threat assessment
  - **Estimate:** 8h

- [ ] **COMBAT-003:** Add shields regeneration
  - Shields regen X per tick when not in combat
  - Combat flag prevents regen
  - **Estimate:** 4h

---

## BACKLOG: Quest & Barter Economy
**Priority:** P2 (Simple barter economy)  
**Epic:** Economy System

- [ ] **ECON-001:** Remove currency system
  - Remove all credit/money references from codebase
  - Stations don't buy/sell for money
  - **Estimate:** 2h

- [ ] **ECON-002:** Implement station quest system
  - Each station has quests: "Bring X of item Y, receive Z of item A"
  - Quest board at stations
  - Quest completion mechanics
  - **Estimate:** 10h

- [ ] **ECON-010:** Implement resource gathering
  - Mining actions at asteroid belts
  - Gas harvesting at gas giants
  - Resources as tradeable items
  - **Estimate:** 8h

- [ ] **ECON-011:** Add drop/pickup for player-to-player trading
  - One player drops item at location
  - Another player picks it up
  - No facilitated trading system
  - Risky but possible
  - **Estimate:** 3h

---

## BACKLOG: World Events (Not Player-Triggered)
**Priority:** P3 (Flavor content)  
**Epic:** World Events

- [ ] **EVENT-001:** Design in-world event system
  - Events happen in the world naturally, not triggered by players
  - No forced dialogue or completion requirements
  - Examples: pirates spawn at certain locations, derelict ships appear, etc.
  - **Estimate:** 4h

- [ ] **EVENT-002:** Implement location-based spawning
  - Pirates spawn in asteroid belts
  - Traders appear at trade routes
  - Derelict ships in certain zones
  - **Estimate:** 6h

- [ ] **EVENT-003:** Add environmental hazards
  - Cosmic storms in certain regions
  - Naturally occurring damage zones
  - **Estimate:** 4h

---

## BACKLOG: Admin Console
**Priority:** P2 (Debugging and monitoring)  
**Epic:** Admin Tools

- [ ] **ADMIN-001:** Create admin console web interface
  - View all ships in DataHandler
  - View all locations and their contents
  - View all players
  - View all items
  - **Estimate:** 10h

- [ ] **ADMIN-002:** Add admin monitoring features
  - Real-time tick monitoring
  - Performance metrics display
  - Error log viewing
  - **Estimate:** 6h

- [ ] **ADMIN-003:** Add admin actions
  - Manually spawn ships/items
  - Manually trigger ticks
  - Force save/load data
  - **Estimate:** 8h

---

## BACKLOG: Multi-System Expansion
**Priority:** P2 (Post-v0.3.0)  
**Epic:** Universe Expansion

### Outer System 1 - Science/Scavengers (Binary System)
- [ ] **OUTER1-001:** Implement Binary Star system core
  - Two stars, close gas giant
  - Warp gate connections to SOL, Nebula, Black Hole
  - **Estimate:** 3h

- [ ] **OUTER1-002:** Implement Shattered Planet 1
  - Deadly ground resource gather site
  - Orbital station
  - High risk/reward resources
  - **Estimate:** 4h

- [ ] **OUTER1-003:** Implement Shattered Planet 2
  - Two dangerous ground resource sites
  - Orbital station
  - **Estimate:** 4h

- [ ] **OUTER1-004:** Implement Synthetic Planet
  - 2 orbital stations, 1 ground station
  - Scientific faction HQ
  - Research facilities
  - **Estimate:** 4h

- [ ] **OUTER1-005:** Add Scavenger faction mechanics
  - Three baron branches
  - Reputation system
  - Specialized gear/ships
  - **Estimate:** 8h

### Other Outer Systems (2-7)
- [ ] **OUTER2-001:** Design and implement Empire system
  - Per design doc (to be created)
  - **Estimate:** 20h

- [ ] **OUTER3-001:** Design and implement Outer System 3
  - Per design doc (to be created)
  - **Estimate:** 20h

- [ ] **OUTER4-001:** Design and implement Outer System 4
  - Per design doc (to be created)
  - **Estimate:** 20h

- [ ] **OUTER5-001:** Design and implement Outer System 5
  - Per design doc (to be created)
  - **Estimate:** 20h

- [ ] **OUTER6-001:** Design and implement Outer System 6
  - Per design doc (to be created)
  - **Estimate:** 20h

- [ ] **OUTER7-001:** Design and implement Zealots system
  - Binary system with planet at gravity center
  - Constant day mechanics
  - Crusader NPC ships
  - Aggressive expansion behavior
  - **Estimate:** 20h

### Special Regions
- [ ] **NEBULA-001:** Implement Nebula region
  - Gate/warp orbit entrance
  - Storm regions with navigation hazard
  - Asteroid fields
  - Nebula Station 1 & 2
  - Collector faction
  - Star dust resource gathering
  - **Estimate:** 12h

- [ ] **BLACKHOLE-001:** Implement Black Hole region
  - Gate/warp orbit entrance
  - Black hole orbit with hazards
  - Unique physics/mechanics
  - **Estimate:** 8h

- [ ] **WARP-001:** Implement warp gate travel
  - Warp action between systems
  - Travel time/cooldowns
  - Gate access restrictions
  - **Estimate:** 6h

---

## BACKLOG: Frontend Development
**Priority:** P1 (Post-v0.1.0, for v0.2.0)  
**Epic:** Frontend

### Core Pages
- [ ] **FE-001:** Create landing page
  - Game pitch and story intro
  - Feature overview
  - Call-to-action to register
  - Terminal aesthetic styling
  - **Estimate:** 8h

- [ ] **FE-002:** Create login page
  - Username/password form
  - Register link
  - JWT token handling
  - **Estimate:** 4h

- [ ] **FE-003:** Create registration page
  - Username, email, password fields
  - Validation
  - Spawn player on success
  - **Estimate:** 5h

- [ ] **FE-004:** Create game page layout
  - Three-panel interface
  - Left: Navigation menu
  - Center: Interactive area
  - Right: Details and actions
  - **Estimate:** 8h

### Game Interface
- [ ] **FE-010:** Implement navigation panel
  - Current location display
  - Available travel destinations
  - Docked status
  - Quick stats (HP, credits, cargo)
  - **Estimate:** 6h

- [ ] **FE-011:** Implement center interaction panel
  - Show ships at location
  - Show items at location
  - Show station (if present)
  - Clickable elements
  - **Estimate:** 10h

- [ ] **FE-012:** Implement details/actions panel
  - Selected target details
  - Available actions (attack, collect, move, dock, etc.)
  - Action confirmation
  - **Estimate:** 8h

- [ ] **FE-013:** Implement ship management panel
  - Ship stats display
  - Component slots with details
  - Cargo inventory
  - **Estimate:** 6h

- [ ] **FE-014:** Implement station interface
  - Station inventory browser
  - Buy/sell forms
  - Shipyard ship browser
  - **Estimate:** 10h

### Real-time Updates
- [ ] **FE-020:** Implement tick polling system
  - Poll `/game/tick` every 5 seconds
  - Detect new tick
  - Fetch updated game state
  - Update UI
  - **Estimate:** 6h

- [ ] **FE-021:** Implement ship log display
  - Scrolling combat log
  - Event notifications
  - Color-coded messages
  - **Estimate:** 4h

- [ ] **FE-022:** Implement regional events display
  - Show other players' actions
  - Notification system
  - **Estimate:** 4h

### Additional Pages
- [ ] **FE-030:** Create Wiki page
  - Game mechanics documentation
  - Ship/component reference
  - Location guide
  - Simple CMS backend
  - **Estimate:** 12h

- [ ] **FE-031:** Create Forum page
  - Post/reply system
  - Faction-specific sections
  - User profiles
  - **Estimate:** 15h

---

## BACKLOG: Deployment
**Priority:** P3 (Nice to have)  
**Epic:** Production Readiness

### Docker
- [ ] **DEPLOY-001:** Create Docker configuration
  - Dockerfile for backend
  - docker-compose for full stack
  - **Estimate:** 5h

---

## TECHNICAL DEBT REGISTER

### Current Known Issues
1. ~~**Import inconsistencies**~~ - ✅ Fixed (Sprint 0)
2. **Outdated test suite** - All tests broken and reference old code (P0, Sprint 5)
3. **No requirements.txt** - Dependencies undocumented (P1, Sprint 0)
4. **Magic numbers everywhere** - Formulas hardcoded in code (acceptable per scope decision)
5. **Limited error handling** - Many functions return False without logging (P1, Sprint 1)
6. **No input validation** - API accepts malformed data (P1, Sprint 1)
7. **Thread safety questions** - Lock cache clearing during tick (P2, investigate)
8. **No logging infrastructure** - Cannot debug production issues (P0, Sprint 1)
9. **Faction factory types** - Still using type placeholders instead of default values (P0, Sprint 0)
10. **Player factory types** - Still using type placeholders instead of default values (P0, Sprint 0)

---

## EPIC SUMMARY

| Epic | Total Tasks | Est. Hours | Priority | Status |
|------|-------------|------------|----------|--------|
| **Critical Blockers** | 8 | 2h remain | P0 | Sprint 0 (~75% done) |
| **Core Game Loop** | 2 | 6h | P0 | Sprint 1 |
| **State Access API** | 5 | 7h | P0 | Sprint 1 |
| **SOL System Content** | 13 | 31h | P1 | Sprints 1-4 |
| **Player Progression** | 2 | 6h | P1 | Backlog (simplified) |
| **Data Management** | 2 | 7h | P1 | Sprint 1 |
| **API Robustness** | 2 | 7h | P1 | Sprint 1 |
| **Station System** | 8 | 23h | P0 | Sprint 2 (no currency) |
| **Location Event Logging** | 5 | 9h | P1 | Sprint 3 (simplified) |
| **Testing Infrastructure** | 9 | 32h | P0 | Sprint 5 |
| **Authentication System** | 7 | 23h | P1 | Backlog |
| **Component Systems** | 3 | 20h | P2 | Backlog (simplified) |
| **Faction & NPC Ships** | 5 | 46h | P1 | Backlog (redesigned) |
| **Combat Systems** | 3 | 18h | P2 | Backlog (simplified) |
| **Quest & Barter Economy** | 4 | 23h | P2 | Backlog (redesigned) |
| **World Events** | 3 | 14h | P3 | Backlog (simplified) |
| **Admin Tools** | 3 | 24h | P2 | Backlog |
| **Universe Expansion** | 20+ | 200h+ | P2 | Backlog |
| **Frontend** | 15+ | 120h+ | P1 | Backlog |
| **Deployment** | 1 | 5h | P3 | Backlog |

---

## NOTES

### Scope Changes Summary (Feb 25, 2026)
**Removed/Simplified:**
- Reputation system (not needed)
- Faction missions/quests (separate from station quests)
- Complex faction warfare (replaced with simple presence calculation)
- Currency/money system (replaced with barter quests)
- Crafting system
- Dynamic pricing
- Player XP/leveling system
- Multiple ship ownership
- Complex weapon types and targeting locks
- Complex random event triggers
- Game configuration system (keeping code-based balance)
- Most deployment/operations items (except Docker)
- CI/CD pipeline (for now)

**Kept/Redesigned:**
- Player factions (for endgame)
- Simple NPC AI (boid-like, not CPU intensive)
- Station quest system (barter economy)
- Basic component targeting in combat
- Engine movement range, sensor detection, stealth duration
- Location event logs (not DevOps logs - player-visible game events)
- Admin console (for monitoring)
- All frontend work
- All outer systems expansion
- Full authentication system
- Performance tests

### Backlog Management
- Review backlog bi-weekly
- Prioritize based on user feedback and testing
- Re-estimate as needed
- Move items to sprints when ready

### Definition of Done
- Code written and reviewed
- Unit tests passing
- Integration tests passing (if applicable)
- Documentation updated
- No blocking bugs introduced
- API documented (if new endpoints)

### Sprint Planning
- Each sprint = 1-2 weeks
- Pick ~20-40 hours of work per sprint (adjust to team size)
- Focus on completing epics, not starting many things

---

**Total Estimated Work to v1.0.0:** ~500-700 hours (4-8 months solo, 2-3 months with team)  
**Scope Reduction:** ~300 hours removed/simplified

**Current Progress:** 
- Sprint 0: ~75% complete
- Overall to v0.1.0: ~30%
- Overall to v1.0.0: ~15%
