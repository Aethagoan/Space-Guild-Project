# Space Guild - Product Backlog

**Last Updated:** 24 Feb 2026  
**Current Sprint:** Pre-v0.1.0 Foundation  
**Priority System:** P0 (Critical/Blocking) → P1 (High) → P2 (Medium) → P3 (Low)

---

## SPRINT 0: Critical Blockers (Fix to Run Code)
**Goal:** Make the codebase executable  
**Estimated Effort:** 4-6 hours

### P0 - Blocking Issues

- [ ] **FIX-001:** Fix import statements in `data.py`
  - Change `from Location import Location` → `from location import Location`
  - Change `from Player import Player` → `from player import Player`
  - Change `from spaceship import Ship` → `from ship import Ship`
  - **Blocks:** Everything - code won't run

- [ ] **FIX-002:** Fix import statements in `program.py`
  - Remove or fix `import spaceship` and `import spaceshipComponent` (files don't exist)
  - Update to use `ship` module instead
  - **Blocks:** Program entry point

- [ ] **FIX-003:** Fix Ship factory type definitions in `ship.py`
  - Lines 12-17: Change component IDs from `int` to `None`
  - Example: `'engine_id': None` not `'engine_id': int`
  - **Blocks:** Ship creation

- [ ] **FIX-004:** Fix Faction factory type definitions in `faction.py`
  - Lines 7, 9: Change from type placeholders to actual values
  - `'name': ""` not `'name': str`
  - **Blocks:** Faction creation

- [ ] **FIX-005:** Fix Player factory default in `player.py`
  - Line 11: Change `'faction_id': int` to `'faction_id': None`
  - **Blocks:** Player creation

- [ ] **DEP-001:** Create `requirements.txt`
  - Add Flask
  - Add any other dependencies (pytest, etc.)
  - **Blocks:** Installation and deployment

- [ ] **RUN-001:** Add program entry point
  - Add `if __name__ == '__main__'` block to `program.py`
  - Initialize DataHandler
  - Start Flask app
  - Start tick loop
  - **Blocks:** Running the game

---

## SPRINT 1: Minimal Viable Backend (Week 1-2)
**Goal:** Get a runnable backend with basic state access  
**Estimated Effort:** 20-30 hours

### P0 - Critical for MVP

#### Tick System
- [ ] **TICK-001:** Implement tick loop runner
  - Timer that calls `process_tick()` every 5 seconds
  - Thread-safe tick execution
  - Tick counter/timestamp
  - **Epic:** Core Game Loop
  - **Estimate:** 3h

- [ ] **TICK-002:** Add tick broadcast mechanism
  - Store tick results per player/location
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
  - **Estimate:** 1h

- [ ] **API-004:** Add GET `/game/tick` endpoint
  - Return current tick number and timestamp
  - **Epic:** State Access API
  - **Estimate:** 1h

#### Minimal World Content
- [ ] **WORLD-001:** Create starter location graph
  - Earth Orbit (starter hub)
  - Earth Orbital Station Zero location
  - Moon Orbit
  - Link them together
  - Add to `program.py` initialization
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

#### Currency System
- [ ] **ECON-001:** Add credits field to Player entity
  - Update `player.py` factory
  - Add to DataHandler CRUD operations
  - **Epic:** Economy System
  - **Estimate:** 2h

- [ ] **ECON-002:** Implement transaction system
  - Debit/credit player accounts
  - Thread-safe currency operations
  - Transaction logging
  - Rollback on failure
  - **Epic:** Economy System
  - **Estimate:** 5h

- [ ] **ECON-003:** Define item/component pricing
  - Price formulas based on tier and type
  - Base prices for all 6 component types
  - Rarity modifiers
  - **Epic:** Economy System
  - **Estimate:** 3h

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

## SPRINT 3: Logging & Events (Week 3-4)
**Goal:** Players can see combat logs, movement notifications, regional activity  
**Estimated Effort:** 15-20 hours

### P1 - High Priority

#### Ship Logging
- [ ] **LOG-001:** Implement ship log storage
  - Add log list to Ship entity (max 100 messages)
  - Timestamp + event type + message
  - FIFO rotation when full
  - **Epic:** Logging System
  - **Estimate:** 3h

- [ ] **LOG-002:** Add log entries in action processing
  - Combat actions: "You attacked Ship-X for Y damage"
  - Damage taken: "Ship-Z attacked you for Y damage"
  - Movement: "Moved from Location-A to Location-B"
  - Collection: "Picked up Item-X"
  - **Epic:** Logging System
  - **Estimate:** 4h

- [ ] **API-020:** Add GET `/ship/<id>/log` endpoint
  - Return last N log entries
  - Filter by event type
  - Pagination support
  - **Epic:** Logging System
  - **Estimate:** 2h

#### Regional Event System
- [ ] **LOG-003:** Implement regional event logging
  - Per-location event list (cleared each tick)
  - Events visible to all ships in location
  - Event types: ship_enter, ship_leave, combat, item_drop, item_pickup
  - **Epic:** Logging System
  - **Estimate:** 4h

- [ ] **LOG-004:** Add regional event generation
  - Movement actions append to origin/destination
  - Combat actions append to location
  - Collection actions append to location
  - **Epic:** Logging System
  - **Estimate:** 3h

- [ ] **API-021:** Add GET `/location/<id>/events` endpoint
  - Return last tick's events at location
  - Show what other players did
  - **Epic:** Logging System
  - **Estimate:** 2h

### P2 - Medium Priority

- [ ] **LOG-005:** Add subscriber pattern for real-time events
  - Ships can subscribe to location events
  - Push notifications on tick
  - Unsubscribe on move
  - **Epic:** Logging System
  - **Estimate:** 5h

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
**Goal:** Comprehensive test coverage and bug fixes  
**Estimated Effort:** 20-30 hours

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
  - Test all 5 action types
  - Test action queue operations
  - Test tick processing
  - Test spam protection
  - **Epic:** Testing Infrastructure
  - **Estimate:** 5h

- [ ] **TEST-013:** Station system unit tests
  - Test buy/sell transactions
  - Test docking/undocking
  - Test inventory management
  - **Epic:** Testing Infrastructure
  - **Estimate:** 4h

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

- [ ] **TEST-022:** Economy integration test
  - Player docks at station
  - Buys components
  - Sells items
  - Verify credit transactions
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

### P1 - High Priority

- [ ] **TEST-040:** Add CI/CD pipeline
  - GitHub Actions or similar
  - Run tests on every commit
  - Code coverage reporting
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
  - Define speed stat per engine tier
  - Limit moves per tick based on engine
  - Multi-tick travel for long distances
  - **Estimate:** 6h

- [ ] **COMP-002:** Add engine damage effects
  - Damaged engine reduces speed
  - Destroyed engine prevents movement
  - **Estimate:** 2h

### Sensor Mechanics
- [ ] **COMP-010:** Implement sensor-based visibility
  - Define sensor range per tier
  - Ships outside range are hidden
  - "Scan" action to reveal ships
  - **Estimate:** 8h

- [ ] **COMP-011:** Add sensor vs stealth mechanics
  - Stealth cloak reduces detection range
  - High-tier sensors counter stealth
  - **Estimate:** 5h

### Stealth Cloak Mechanics
- [ ] **COMP-020:** Implement cloaking system
  - "Cloak" action to enable stealth
  - "Uncloak" action or auto-uncloak on action
  - Cloaked ships harder to detect
  - **Estimate:** 6h

- [ ] **COMP-021:** Add cloak power/duration mechanics
  - Cloak drains power/fuel (future resource)
  - Limited cloak duration
  - **Estimate:** 4h

---

## BACKLOG: Faction System
**Priority:** P2 (Expand endgame content)  
**Epic:** Faction Politics

- [ ] **FACTION-001:** Implement reputation system
  - Player reputation per faction (-100 to +100)
  - Actions affect reputation
  - Reputation thresholds for access
  - **Estimate:** 6h

- [ ] **FACTION-002:** Add faction-owned territories
  - Locations have faction owner
  - Restrictions based on reputation
  - Hostile factions attack on sight
  - **Estimate:** 5h

- [ ] **FACTION-003:** Implement faction missions/quests
  - Mission board at faction stations
  - Combat missions, delivery missions, etc.
  - Reputation rewards
  - **Estimate:** 10h

- [ ] **FACTION-004:** Add faction warfare mechanics
  - Territory control system
  - Faction vs faction combat
  - Player alignment and participation
  - **Estimate:** 15h

- [ ] **FACTION-005:** Implement player faction creation
  - Players can create guilds/factions
  - Guild banks, shared resources
  - Guild territory claims
  - **Estimate:** 20h

---

## BACKLOG: Ship Progression
**Priority:** P1 (Core gameplay loop)  
**Epic:** Player Progression

- [ ] **PROG-001:** Implement ship purchase system
  - Stations sell ships (tier 1-5)
  - Expensive ship prices based on tier
  - Player can own multiple ships
  - Switch between ships at stations
  - **Estimate:** 6h

- [ ] **PROG-002:** Add ship tier upgrade system
  - Upgrade ship to next tier at shipyard
  - Cost = new ship price - trade-in value
  - Preserve components or lose them
  - **Estimate:** 5h

- [ ] **PROG-003:** Implement player experience/leveling
  - XP gained from combat, trading, exploration
  - Level unlocks higher tier access
  - **Estimate:** 6h

- [ ] **PROG-004:** Add ship customization
  - Ship names
  - Ship colors/cosmetics (future)
  - **Estimate:** 3h

---

## BACKLOG: Advanced Combat
**Priority:** P2 (Depth and balance)  
**Epic:** Combat Systems

- [ ] **COMBAT-001:** Add weapon types with different mechanics
  - Lasers (shield damage bonus)
  - Ballistics (armor piercing)
  - Missiles (delayed AOE damage)
  - **Estimate:** 10h

- [ ] **COMBAT-002:** Implement target locking
  - Lock-on action before attack
  - Sensors affect lock time
  - **Estimate:** 5h

- [ ] **COMBAT-003:** Add shields regeneration
  - Shields regen X per tick when not in combat
  - Combat flag prevents regen
  - **Estimate:** 4h

- [ ] **COMBAT-004:** Implement escape mechanics
  - "Warp out" action with charge time
  - Interrupted by damage
  - **Estimate:** 6h

- [ ] **COMBAT-005:** Add NPC ships and AI
  - Patrol ships at faction borders
  - Pirates in asteroid belts
  - Basic AI behaviors (attack, flee, patrol)
  - **Estimate:** 15h

---

## BACKLOG: Economy & Resources
**Priority:** P2 (Depth)  
**Epic:** Economy System

- [ ] **ECON-010:** Implement resource gathering
  - Mining actions at asteroid belts
  - Gas harvesting at gas giants
  - Resources as tradeable items
  - **Estimate:** 8h

- [ ] **ECON-011:** Add crafting/manufacturing system
  - Combine resources to create components
  - Manufacturing stations
  - Blueprints and skill requirements
  - **Estimate:** 12h

- [ ] **ECON-012:** Implement dynamic pricing
  - Station prices affected by supply/demand
  - Trade routes between stations
  - **Estimate:** 8h

- [ ] **ECON-013:** Add contracts and player trading
  - Player-to-player item sales
  - Contract system for jobs
  - Escrow for safe trading
  - **Estimate:** 10h

---

## BACKLOG: Anomalies & Random Events
**Priority:** P3 (Flavor content)  
**Epic:** Random Events

- [ ] **EVENT-001:** Design anomaly system
  - Random event triggers (on move, on tick, etc.)
  - Event types and outcomes
  - Rarity tiers
  - **Estimate:** 4h

- [ ] **EVENT-002:** Implement travel anomalies
  - Ship damage during travel
  - Discover derelict ships
  - Cosmic storms
  - Wormholes to random locations
  - **Estimate:** 8h

- [ ] **EVENT-003:** Add location-based events
  - Pirate ambushes
  - Trader encounters
  - Distress signals
  - **Estimate:** 6h

---

## BACKLOG: Configuration & Balance
**Priority:** P1 (Essential for tuning)  
**Epic:** Game Balance

- [ ] **CONFIG-001:** Create game configuration system
  - YAML or JSON config file
  - Load on startup
  - Hot-reload capability (future)
  - **Estimate:** 4h

- [ ] **CONFIG-002:** Externalize all balance formulas
  - Damage multipliers
  - Repair costs and degradation rates
  - HP/shield formulas
  - Component stat formulas
  - Price formulas
  - **Estimate:** 6h

- [ ] **CONFIG-003:** Add admin API for balance adjustments
  - Update config values without code changes
  - Apply changes on next tick
  - **Estimate:** 5h

- [ ] **CONFIG-004:** Create balance testing tools
  - Combat simulator
  - Economy simulator
  - Progression calculator
  - **Estimate:** 10h

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

## BACKLOG: Polish & Operations
**Priority:** P2-P3 (Ongoing)  
**Epic:** Production Readiness

### Documentation
- [ ] **DOC-001:** Write comprehensive API documentation
  - All endpoints with examples
  - Request/response schemas
  - Error codes reference
  - **Estimate:** 8h

- [ ] **DOC-002:** Write developer setup guide
  - Installation instructions
  - Running locally
  - Running tests
  - **Estimate:** 3h

- [ ] **DOC-003:** Write game design document
  - Complete game mechanics reference
  - Balance philosophy
  - Progression design
  - **Estimate:** 10h

- [ ] **DOC-004:** Add inline code documentation
  - Docstrings for all functions
  - Complex logic explanations
  - Architecture overview
  - **Estimate:** 6h

### Deployment
- [ ] **DEPLOY-001:** Create Docker configuration
  - Dockerfile for backend
  - docker-compose for full stack
  - **Estimate:** 5h

- [ ] **DEPLOY-002:** Set up hosting infrastructure
  - Choose hosting provider
  - Database setup (if switching from JSON)
  - SSL/domain configuration
  - **Estimate:** 8h

- [ ] **DEPLOY-003:** Add monitoring and alerting
  - Server health monitoring
  - Error tracking (Sentry or similar)
  - Performance metrics
  - **Estimate:** 6h

- [ ] **DEPLOY-004:** Create deployment pipeline
  - Automated deployments
  - Staging environment
  - Rollback capability
  - **Estimate:** 8h

### Performance
- [ ] **PERF-001:** Profile and optimize tick processing
  - Identify bottlenecks
  - Optimize hot paths
  - Target: < 500ms for 100 ships
  - **Estimate:** 8h

- [ ] **PERF-002:** Optimize data serialization
  - JSON parsing performance
  - Consider msgpack or protobuf
  - **Estimate:** 6h

- [ ] **PERF-003:** Add caching layer
  - Cache frequently accessed data
  - Redis integration (if needed)
  - **Estimate:** 8h

- [ ] **PERF-004:** Evaluate database migration
  - If JSON becomes bottleneck
  - Migrate to PostgreSQL or Redis
  - Maintain compatibility
  - **Estimate:** 20h

### Security
- [ ] **SEC-001:** Add rate limiting
  - Prevent API abuse
  - Per-user action limits per tick
  - **Estimate:** 4h

- [ ] **SEC-002:** Add CORS configuration
  - Proper origin restrictions
  - Preflight handling
  - **Estimate:** 2h

- [ ] **SEC-003:** Security audit
  - SQL injection (if using SQL)
  - XSS prevention
  - CSRF protection
  - Input sanitization
  - **Estimate:** 6h

- [ ] **SEC-004:** Add admin authentication
  - Separate admin roles
  - Protected admin endpoints
  - **Estimate:** 5h

---

## TECHNICAL DEBT REGISTER

### Current Known Issues
1. **Import inconsistencies** - Multiple files have broken imports (P0, Sprint 0)
2. **Outdated test suite** - All tests broken and reference old code (P0, Sprint 5)
3. **No requirements.txt** - Dependencies undocumented (P0, Sprint 0)
4. **Magic numbers everywhere** - Formulas hardcoded, not configurable (P1, Backlog)
5. **Limited error handling** - Many functions return False without logging (P1, Sprint 1)
6. **No input validation** - API accepts malformed data (P1, Sprint 1)
7. **Thread safety questions** - Lock cache clearing during tick (P2, investigate)
8. **No logging infrastructure** - Cannot debug production issues (P0, Sprint 1)

---

## EPIC SUMMARY

| Epic | Total Tasks | Est. Hours | Priority | Status |
|------|-------------|------------|----------|--------|
| **Critical Blockers** | 7 | 4-6h | P0 | Sprint 0 |
| **Core Game Loop** | 2 | 7h | P0 | Sprint 1 |
| **State Access API** | 4 | 6h | P0 | Sprint 1 |
| **SOL System Content** | 13 | 31h | P1 | Sprints 1-4 |
| **Player Progression** | 5 | 20h | P1 | Sprints 1, Backlog |
| **Data Management** | 2 | 7h | P1 | Sprint 1 |
| **API Robustness** | 2 | 7h | P1 | Sprint 1 |
| **Economy System** | 6 | 25h | P0 | Sprint 2 |
| **Station System** | 9 | 30h | P0 | Sprint 2 |
| **Logging System** | 6 | 18h | P1 | Sprint 3 |
| **Testing Infrastructure** | 10 | 37h | P0 | Sprint 5 |
| **Authentication System** | 7 | 23h | P1 | Backlog |
| **Component Systems** | 6 | 31h | P2 | Backlog |
| **Faction Politics** | 5 | 56h | P2 | Backlog |
| **Combat Systems** | 5 | 40h | P2 | Backlog |
| **Random Events** | 3 | 18h | P3 | Backlog |
| **Game Balance** | 4 | 25h | P1 | Backlog |
| **Universe Expansion** | 20+ | 200h+ | P2 | Backlog |
| **Frontend** | 15+ | 120h+ | P1 | Backlog |
| **Production Readiness** | 15+ | 100h+ | P2-P3 | Backlog |

---

## NOTES

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

**Total Estimated Work to v1.0.0:** ~800-1000 hours (6-12 months solo, 2-4 months with team)

**Current Progress:** ~25-30% to v0.1.0, ~10% to v1.0.0
