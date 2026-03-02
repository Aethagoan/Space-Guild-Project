# Space Guild

A tick-based multiplayer space game combining PvE questing, territory control, and tactical ship combat. Play in your browser with a terminal-style interface.

---

## What is Space Guild?

Space Guild is an MMO space game where you pilot a customizable ship through multiple star systems, each controlled by unique factions with their own goals and territories. The game mixes several gameplay styles:

- **PvE & Questing**: Explore dangerous systems, gather resources from shattered planets, and complete faction quests
- **Territory Control**: Join factions and participate in territory wars for control of key systems and trade routes
- **Tactical Combat**: Ship-to-ship combat with component-level targeting (destroy their weapons, disable their engines, or go straight for the hull)
- **Economic Gameplay**: Trade resources, upgrade components through a tier system, and repair degraded equipment

The game operates on a 5-second tick system where all players queue actions simultaneously, then the server processes everything at once, creating a strategic "plan your move" gameplay loop.

---

## Factions

The universe of Space Guild is shaped by competing factions, each with distinct motivations, economies, and cultures.

### Orion Faction
**Mission**: Explore, defend, and make space accessible to all sapient species.

There's a reason everyone starts in Orion. Space travel is hard, and the technology required isn't something you can assemble alone. In a world where no one else took responsibility, the Orion Faction stepped up. They'll get you started with a basic ship and technology, asking for nothing in return except one thing: don't commit crimes in their space. 

Those who believe in Orion's mission—exploration, defense, and the persistence of sapience—serve with vigor and take oaths. Crime is not tolerated. Quick-response enforcers handle distress calls and deal with lawbreakers swiftly.

Works closely with the Manufacturing faction. Controls multiple star systems, including SOL (the predecessors' home system).

### The Dryads
**Mission**: Achieve immortality through digital existence and spread across the universe.

The Dryads are a decentralized collective of transhumanist post-mortals who abandoned their biological bodies to digitize their minds. They saw flesh as the ultimate limitation to intelligent life's progression and survival.

Acting more as a movement than a unified faction, Dryads spread like lichen across barren, metal-rich worlds. They terraform hostile environments into metallic forests with solar-panel leaves, tin-foil grass, and mechanical wildlife—an artificial mimicry of nature powered by self-replicating nanomachines.

Each Dryad's consciousness exists on physical servers in underground datacenters (like woodland spirits tied to specific trees). They interact with others through automata proxies—empty shells possessed like ghosts.

**Economy**: Export raw metals, silicates, and advanced electronics. Import organic materials (rubber, oil products) scarce on their barren worlds.

**Goal**: Spread until they can never be eradicated, existing until the last stars burn out.

### Scientific Faction
**Mission**: Advance knowledge without repeating past mistakes.

These researchers ruined their own planets through unchecked scientific experimentation. Now they've learned their lesson (sort of). They need dangerous materials from those shattered worlds but don't want to risk themselves gathering them.

Solution? Hire scavengers. High-risk, high-reward operations controlled by powerful barons trying to increase their wealth through SCIENCE! They produce cutting-edge technology and sell it to those willing to pay.

Not aligned with the Scavenger barons, but the barons frequently buy gear from them.

### Scavenger Factions
**Motto**: "Money through finds."

Three semi-unified branches working closely with the Scientific faction, each with different ethics:

- **The Pirates**: "Scavenge by sometimes taking." A little underhanded, willing to steal if opportunity knocks.
- **The Elite**: "Scavenge by excellence." Well-equipped, well-funded professionals who do the job right.
- **The Honest**: "Get stuff, make money." Regular folks earning a living without piracy, mostly honest.

All three dive into deadly shattered worlds and hazardous locations to retrieve high-value finds.

### Kuiper Faction
**Mission**: Secure resources and technology for their isolated kingdom.

Ice miners ruled by a king, operating in a frozen system around a black dwarf star. Deeply isolationist and paranoid, they trust no one.

When you enter Kuiper territory, they'll force you into a deal. Sign, and you can pass safely. Refuse? They'll take everything you have—or die trying. They keep to themselves, mining ice and rare elements, but desperately want high-tier technology they can't produce themselves.

**Unique feature**: Travel restricted to vertical movement through ice belts—you can't traverse directly between inner and outer regions.

### The Collectors
**Mission**: Harvest rare stardust from the nebula's deadly storms.

Mysterious inhabitants of the Nebula, these hardy souls venture into violent cosmic storms to collect materials found nowhere else in the galaxy. Little is known about their society, but their trade goods are highly sought after.

### Zealots Faction
**Mission**: Spread their religion by force and claim territory.

Religious crusaders inhabiting a binary star system with a tidally-locked planet at the gravitational center point. The planet doesn't rotate—one side experiences permanent day.

They periodically send out crusader fleets to neighboring systems, seeking converts and new territory. They're aggressive, ideologically driven, and see expansion as a holy mandate.

### Manufacturing Faction
**Mission**: Produce the equipment that keeps civilization running.

High-tech industrial worlds scattered throughout known space. They need raw materials and turn them into ships, components, stations, and everything else that makes space travel possible.

Work closely with Orion and maintain presence in multiple systems. If you need gear, they probably make it.

### Rifter Faction
**Mission**: Steal from the weak and hide from the strong.

Pirates, plain and simple. They lurk in deep space, asteroid fields, and remote regions, waiting for vulnerable targets. No grand ideology—just theft and survival.

### Empire Faction
**Status**: Under development.

A powerful centralized government controlling multiple systems (details forthcoming).

---

## The Galaxy

Space Guild's playable area spans multiple interconnected star systems, each with unique environments and strategic importance.

### SOL System (Orion Territory)
Humanity's home system and every player's starting point. Heavily populated, highly lawful, rich with stations and opportunities.

**Major Locations**:
- **Earth**: Orbit stations, Earth Ground Station Zero, Moon Ground Station
- **Venus**: Orbit stations, Venus Ground/Orbital Station Zero
- **Mars**: Orbit stations, Mars Ground/Orbital Station Zero, two moon stations
- **Mercury**: Orbit station, ground station
- **Asteroid Belt**: Three regions with mining stations (Belt 1, 2, 3)
- **Jupiter**: Orbit, Thunder Station (atmosphere), IO station
- **Saturn**: Orbit, Cloud Station (atmosphere), two ring stations
- **Uranus**: Orbit, orbital station, atmosphere station
- **Kuiper Regions**: Four regions with orbit stations
- **Sun Orbital**: Central gateway hub
- **Warp Gates**: SOL → ALPHA connection

### Scientific System (Scientific Faction Territory)
A binary star system with extreme hazards and extreme rewards.

**Structure** (innermost to outermost):
- **Close Gas Giant**: Near the binary stars
- **Asteroid Belt**
- **First Shattered Planet**: Orbital station, deadly ground resource site
- **Second Asteroid Belt**
- **Second Shattered Planet**: Orbital station, two dangerous ground resource sites
- **Synthetic Planet**: Two orbital stations, one ground station

**Warp Gate Connections**:
- Synthetic planet gates → Nebula
- Binary star gates → SOL
- Binary star gates → Black Hole

### Kuiper System (Kuiper Faction Territory)
A frozen, hostile system ruled by an isolationist king.

**Structure**:
- **Black Dwarf Star** (center)
- **Ice Belt 1**
- **Gas Giant** (high radiation): Floating station/city (sells drinks and stolen goods), vegetated moon with resource sites, blue moon with cyron element
- **Ice Belt 2**: Station
- **Ice Planet** (faction center): Ground station, moon with quirky traders
- **GNALL** (former volcanic planet): Obsidian and frozen igneous element 'elion'
- **Ice Belt 3**: Warp gate area
- **Ice Belt 4**: Station

**Unique Mechanic**: Restricted travel—you can only move vertically through ice belts, not directly between inner/outer regions.

### The Nebula (Collector Territory)
Deadly storms, rare resources, and mysterious inhabitants.

**Locations**:
- Warp gate orbital
- Storm regions (hazardous, high-reward)
- Asteroid fields
- Nebula Station 1
- Nebula Station 2

### Additional Systems
Multiple systems are planned or in development, including Zealot, Empire, Dryad, Manufacturing, and Rifter territories. Warp gates connect these systems, creating a web of trade routes, conflict zones, and exploration opportunities.

---

## Game Mechanics

This section explains the core systems that power Space Guild's gameplay. Understanding these mechanics will help you make strategic decisions about ship upgrades, combat tactics, and resource management.

### Ships & Tiers

Every ship has a **tier** (0-6) that determines its maximum HP and component restrictions.

**Ship HP Formula**: `100 × (1 + tier)²`

| Tier | Max HP | Description |
|------|--------|-------------|
| 0 | 100 HP | Starter ships (everyone begins here) |
| 1 | 400 HP | Early upgrades (easy to obtain) |
| 2 | 900 HP | Mid-game progression |
| 3 | 1600 HP | Advanced ships |
| 4 | 2500 HP | High-tier ships |
| 5 | 3600 HP | Elite ships (faction boss drops) |
| 6 | 4900 HP | Endgame ships (world boss drops) |

**Component Restrictions**: Ships can only equip components with `item_tier ≤ ship_tier + 2`
- Example: A Tier 0 ship can equip up to Tier 2 components
- Example: A Tier 3 ship can equip up to Tier 5 components

Ship tier upgrades are obtained through **station quests** and automatically restore the ship to its new maximum HP.

### Components & Multipliers

Ships have 6 component slots:
- **Engine**: Enables movement between locations
- **Weapon**: Determines attack damage
- **Shield**: Absorbs incoming damage
- **Cargo**: Determines inventory capacity
- **Sensor**: Controls scan range and detail
- **Stealth Cloak**: Provides temporary invisibility

#### Multiplier System

Every component has three multiplier values:
- **Current multiplier**: Current effectiveness
- **Min multiplier**: Minimum allowed (tier-dependent)
- **Max multiplier**: Maximum allowed (tier-dependent)

**Multiplier Ranges by Tier**:
```
Tier 0: min=0.5,  max=1.0
Tier 1: min=0.8,  max=2.0
Tier 2: min=1.5,  max=3.0
Tier 3: min=2.0,  max=4.0
Tier 4: min=3.0,  max=6.0
Tier 5: min=5.0,  max=8.0
Tier 6: min=6.0,  max=10.0
```

**How Multipliers Affect Stats**:

- **Weapons**: Damage = multiplier (direct value)
  - T0 weapon (mult=1.0) → 1.0 damage
  - T3 weapon (mult=4.0) → 4.0 damage
  - T6 weapon (mult=10.0) → 10.0 damage (max possible)

- **Cargo**: Capacity = `100 × (1 + tier) × multiplier`
  - T0 cargo (mult=1.0) → 100 capacity
  - T2 cargo (mult=2.5) → 750 capacity

- **Shields**: Max Pool = `50 × (1 + tier)^1.5 × multiplier`
  - T0 shield (mult=1.0) → 50 pool
  - T2 shield (mult=3.0) → ~779 pool
  - T3 shield (mult=4.0) → 1600 pool

- **Stealth Cloak**: Duration = `floor(5 × (1 + tier) × multiplier)` ticks
  - T0 cloak (mult=1.0) → 5 ticks (25 seconds)
  - T3 cloak (mult=4.0) → 80 ticks (400 seconds)

#### Component Health

Each component type has different base health:

| Component | Health Formula | T0 Health | T3 Health |
|-----------|---------------|-----------|-----------|
| Engine | 40 × (1 + tier) | 40 | 160 |
| Weapon | 50 × (1 + tier) | 50 | 200 |
| Shield | 25 × (1 + tier) | 25 | 100 |
| Cargo | 100 × (1 + tier) | 100 | 400 |
| Sensor | 25 × (1 + tier) | 25 | 100 |
| Stealth Cloak | 40 × (1 + tier) | 40 | 160 |

**When a component reaches 0 health, it becomes disabled**:
- **Weapons**: Deal 0 damage
- **Engines**: Cannot move
- **Cargo**: All items spill to current location
- **Shields**: Shield pool drops to 0
- **Sensors**: Cannot scan
- **Stealth Cloaks**: Cannot activate stealth

Components are **not destroyed** at 0 health—they can be repaired at stations.

#### Repair & Degradation System

Repairing components has a **permanent cost**: the multiplier is reduced based on how damaged the component was.

**Multiplier Reduction Table**:
```
Health %    → Multiplier Penalty
0-9%        → -0.10
10-19%      → -0.09
20-29%      → -0.08
30-39%      → -0.07
40-49%      → -0.06
50-59%      → -0.05
60-69%      → -0.04
70-79%      → -0.03
80-89%      → -0.02
90-99%      → -0.01
100%        → -0.00 (no penalty)
```

**Example**:
- T2 weapon with mult=3.0 takes damage down to 15% health
- Repair restores health to max but reduces mult by 0.09
- New multiplier: 3.0 - 0.09 = 2.91
- Multiplier cannot drop below `min_multiplier` for that tier (1.5 for T2)

This creates a **maintenance economy**: components degrade with use, forcing players to eventually replace them or accept reduced effectiveness.

### Combat System

#### Shield Mechanics

Shields provide a **shield pool** that absorbs damage before HP or components take hits.

**Shield Absorption Rules** (no overflow damage):
1. **If shield_pool > 0**: Shields absorb **ALL damage** (even if damage exceeds pool)
   - No overflow damage to ship HP
   - Shield pool reduced by damage amount (minimum 0)
2. **If shield_pool = 0**: Damage goes directly to ship HP or components

**Example Combat Scenario**:
```
Ship has 30 shield pool, 400 HP
Attacker deals 100 damage
Result: Shield pool → 0, Ship HP → 400 (shields blocked everything!)
Next attack: Damage goes to HP (shields depleted)
```

This makes shields **very valuable** for protection—while they're up, you're invincible. Once they break, you're vulnerable.

Shields refill at stations with **no penalty** (unlike component repairs).

#### Attack Types

**1. Attack Ship HP**
- Damage goes to shields first (if pool > 0)
- If shields depleted, damage goes to ship HP
- Attacker's stealth deactivates

**2. Attack Ship Component** (targeted attacks)
- Damage goes to shields first (if pool > 0)
- If shields depleted:
  - If component exists → damage the component
  - If slot is empty → **CRITICAL HIT**: 5x damage to ship HP!
- Example: 4.0 damage weapon hits empty slot = 20.0 HP damage

**3. Attack Item** (destroy loot at locations)
- Items at locations have no shields
- Damage goes directly to item health
- When health → 0, item is destroyed (unusable)

#### Safe Zones

Locations tagged `'Safe'` disable all weapons—attacks will fail if attempted in safe zones. This protects station areas and Orion-controlled space from PvP combat.

### Movement System

**Movement Requirements**:
1. Engine must be equipped
2. Engine health > 0
3. Destination must be linked to current location

Movement is **instant** (completes in 1 tick). Engine tier/multiplier **does not affect speed**—engines provide binary functionality (works or doesn't work).

**Movement & Stealth**:
- Stealthed ships leave "energy signature" logs when moving
- Entering stations/starports auto-deactivates stealth

### Stealth System

**Stealth Duration Formula**: `floor(5 × (1 + tier) × multiplier)` ticks

**Examples**:
- T0 cloak (mult=1.0): 5 ticks (25 seconds)
- T1 cloak (mult=2.0): 20 ticks (100 seconds)
- T3 cloak (mult=4.0): 80 ticks (400 seconds)

**Requirements**:
- Stealth cloak equipped with health > 0
- Ship has NOT taken damage this tick
- Ship is NOT already stealthed

**While Stealthed**:
- Hidden from scans
- Hidden from location ship lists
- Can still move (leaves energy signature logs)

**Automatic Deactivation**:
- Taking damage (immediate)
- Performing attacks
- Entering stations/starports
- Timer expires

### Cargo System

**Cargo Capacity Formula**: `100 × (1 + tier) × multiplier`

**Item Weights** (base × (1 + tier)):
```
Engine:        40 × (1 + tier)
Weapon:        10 × (1 + tier)
Shield:        40 × (1 + tier)
Cargo:         40 × (1 + tier)
Sensor:        20 × (1 + tier)
Stealth Cloak: 20 × (1 + tier)
```

**Cargo Rules**:
- Total weight of items in cargo cannot exceed capacity
- Need cargo with health > 0 to collect items
- When cargo health → 0, all items spill to ship's location

**Example**:
```
T1 cargo (mult=2.0): capacity = 400
Contains:
  - T2 engine: 120 weight
  - T1 weapon: 20 weight
  - T0 shield: 40 weight
Total: 180/400 (220 remaining)
```

### Tick-Based Action Queue

The game operates on a **5-second tick** system where all players queue actions simultaneously.

**Action Execution Order per Location**:
```
Phase 0: All scans (ship, item, location)
Phase 1: All attacks (ship HP, components, items)
Phase 2: All moves
Phase 3: All collects
Phase 4: Stealth deactivation
Phase 5: Stealth activation
```

**Concurrent Processing**:
- Each location processes in its own thread
- Multiple locations process concurrently (up to 32 threads)
- Ships at Earth don't block ships fighting at Mars

This creates strategic "plan your move" gameplay where positioning and timing matter more than reflexes.

---

## Backend Architecture

The backend is built in Python with Flask, using JSON for data storage instead of SQL. Here's why:

### Design Philosophy

**Python over C#**: While C# is great for large projects, Python excels at dynamic handler systems that can take strings and return various object types. This makes the game's action system much more maintainable.

**Dictionaries over Class Inheritance**: Rather than complex OOP hierarchies, the game uses dictionaries and linked lists for entity storage. These tried-and-tested data structures provide excellent performance and simplicity.

**JSON over SQL**: Most game data involves single-ID lookups rather than complex relational queries. JSON storage removes relational database overhead while providing the flexibility needed for game entities.

### The Action System (actions.py)

This is the core of the game's tick-based architecture, and it's where things get interesting.

#### Node-Based Action Queue with Linked Lists

Every action queued by players is stored in a reusable `ActionNode` managed by a dictionary lookup and organized into doubly-linked lists. Here's the clever part:

```python
class ActionNode:
    """Node in the action queue linked list.
    
    Each ship gets one node that can be reused between ticks and moved between lists.
    """
    def __init__(self, ship_id: int):
        self.ship_id = ship_id
        self.action_type: Optional[str] = None
        self.target: Any = None
        self.target_data: Optional[Any] = None
        self.action_hash: Optional[str] = None
        self.prev: Optional['ActionNode'] = None
        self.next: Optional['ActionNode'] = None
        self._lock = Lock()


class ActionList:
    """Doubly-linked list with sentinel head and tail nodes.
    
    Real action nodes are always between head and tail.
    This ensures uniform removal logic with no edge cases.
    """
    def __init__(self, name: str):
        self.name = name
        # Sentinel nodes (ship_id = -1 means not a real ship)
        self.head = ActionNode(-1)
        self.tail = ActionNode(-1)
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def append(self, node: ActionNode):
        """Append node to the tail of the list."""
        with self.tail._lock, self.tail.prev._lock:
            node.prev = self.tail.prev
            node.next = self.tail
            self.tail.prev.next = node
            self.tail.prev = node
    
    def remove(self, node: ActionNode):
        """Remove node from the list."""
        with node.prev._lock, node.next._lock:
            node.prev.next = node.next
            node.next.prev = node.prev


# Each ship gets ONE node that moves between action lists
ship_to_node: Dict[int, ActionNode] = {}  # O(1) lookup
node_pool: Dict[int, ActionNode] = {}     # Reused between ticks

# Five action lists (attack_ship, attack_ship_component, attack_item, move, collect)
# Each is a doubly-linked list with sentinel head/tail nodes
```

**Why this structure?**

1. **O(1) action updates**: When a player changes their action, lookup the ship's node in the dictionary, remove it from its current linked list, update it, and append to the new list - all constant time.

2. **No memory allocation spam**: Nodes are reused between ticks. Instead of creating/destroying thousands of objects per tick, nodes stay in the pool and just move between lists.

3. **Sentinel nodes eliminate edge cases**: Each linked list has permanent head/tail sentinel nodes. Real action nodes are always *between* them, so removal logic is uniform - no special cases for removing the first or last node.

4. **Thread-safe by design**: Each node has its own lock. Removal locks the node's neighbors, preventing race conditions during concurrent operations.

#### Per-Location Concurrent Processing (Planned)

The system is designed to group actions by location and process each location's actions in parallel. Ships fighting at Earth won't block ships fighting at Mars, enabling massive throughput gains with dozens of active locations.

**Why this will work:**

- Ships at different locations use different lock keys (ship:123:hp vs ship:456:hp)
- No contention between location-isolated operations
- Movement locks both source and destination, handling cross-location correctly
- With 10 active locations = 10x potential speedup, 100 locations = 100x speedup

#### Fine-Grained Locking (data.py)

The `DataHandler` class uses field-level locks rather than entity-level locks:

```python
# Instead of locking the entire ship, lock specific fields:
ship:{id}:hp              # HP modifications
ship:{id}:shield          # Shield pool
ship:{id}:cargo           # Cargo operations
ship:{id}:component:engine_id  # Individual component slots
ship:{id}:location        # Location updates

# Same for locations:
location:{name}:ships     # Ship list modifications
location:{name}:items     # Item list modifications
```

**Benefits:**

- Damage a ship's HP while another system accesses its cargo (no conflict)
- Multiple ships' independent fields modified concurrently
- Locks are cleared each tick (prevents memory leaks, ensures fresh state)

**Performance characteristics:**

- Sequential tick operations: ~10,000 moves/second
- Lock acquisition overhead: ~0.01ms per lock
- Bottleneck: Computational (list operations), not lock contention

### Component System

Ships have customizable components across 6 slots:
- **Engine**: Determines movement range per tick
- **Weapons**: Damage output and targeting
- **Shields**: Absorbs damage before hull/components take hits
- **Cargo**: Inventory capacity
- **Sensors**: Scan range and detail level
- **Stealth Cloak**: Temporary invisibility (disables other actions)

Components have:
- **Tier system** (0-6): Tier 0 = starter, Tier 6 = endgame boss drops
- **Health and degradation**: Components don't break at 0 HP, they just stop functioning. Repairs restore health but permanently reduce multipliers over time (degradation system).
- **Multipliers**: Tier and condition affect effectiveness

#### Combat Mechanics

Damage flows through this priority:
1. Shields absorb damage first (shield pool)
2. Overflow or direct damage hits the target (ship HP or component HP)
3. Components at 0 HP cease functioning but aren't destroyed

Players can attack:
- Ship HP directly (faster kills)
- Specific components (tactical disabling)
- Items at locations (destroy loot before others collect it)

### API Endpoints

The Flask API provides:
- `/action` (POST): Queue actions for next tick
- `/repair/component` (POST): Repair damaged components (with degradation)
- `/ship/log` (GET): Retrieve ephemeral ship log entries
- `/health` (GET): Health check

Actions are queued with spam protection via action_hash - identical actions are ignored until the player changes their mind.

---

## Frontend

The frontend is browser-based with a terminal-style aesthetic (in progress).

### Current State
- Basic HTML structure with command input
- Terminal-style CSS (monospace, text-on-black theme)
- Command-based interaction model

### Planned Design (3-Panel Interface)
1. **Left Panel**: Navigation menu (location, ship status, inventory)
2. **Middle Panel**: Contextual selection interface (clickable objects, ships, locations)
3. **Right Panel**: Details and actions (inspect items, queue actions, view stats)

### Tick-Based Interaction
Every 5 seconds:
- Server processes all queued actions
- Results are sent back to connected players
- Players see updates and queue their next action

Between ticks, players:
- Explore the action panel
- Queue their desired action (move, attack, collect, etc.)
- See feedback when the tick resolves

Additional planned pages:
- **Landing page**: Story intro and gameplay overview
- **Login**: Authentication (JWT planned)
- **Wiki**: Detailed game information (GET/POST system)
- **Forum**: Player community with faction-specific sections

---
## Current Progress

### Implemented
- Full action queue system with reusable nodes and linked lists
- Concurrent per-location tick processing
- Fine-grained field-level locking for thread safety
- Component system with health, degradation, and tier multipliers
- Combat system (ship attacks, component targeting, item destruction)
- Shield mechanics with overflow damage
- Movement system with location linking
- Item collection with cargo capacity checks
- JSON-based data persistence
- Flask API with action queuing, component repair, and logs
- Basic frontend structure

### In Progress
- Frontend 3-panel interface
- Authentication system (JWT tokens)
- Ship logs and notification system

### Planned
- Trading system (player-to-player and station vendors)
- Quest system (faction missions)
- Anomalies (random events during travel)
- Station shipyards (component shopping and ship upgrades)
- Territory control mechanics
- Full implementation of all star systems and factions

---

## Tech Stack

- **Backend**: Python, Flask
- **Data Storage**: JSON (custom DataHandler with fine-grained locking)
- **Frontend**: HTML/CSS/JavaScript (terminal aesthetic)
- **Concurrency**: ThreadPoolExecutor for per-location parallel processing
- **Architecture**: Tick-based game loop with action queue system

---

## Why These Design Choices?

### Tick-Based Gameplay
Everyone acts in one action at a time which eliminates harsh 'clicked first' gameplay, but the order in which the requests come in, so skilled players who click first act first, but are in a way, rate limited to prevent such a skill curve that casual players are pushed out. It creates strategic gameplay where planning matters more than reflexes.

### Linked Lists + Dictionary Lookup
O(1) action lookup via dictionary, O(1) insertion/removal via linked list, zero memory allocation spam via node pooling. It's the best of all worlds.

### Fine-Grained Locks
Enables high concurrency for external systems (trading, admin commands) while maintaining data consistency. Locks are cleared each tick to prevent memory leaks.

### JSON Storage
Game entities are mostly accessed by ID lookups, not relational queries. JSON eliminates SQL overhead and gives flexibility for dynamic game data.

### Per-Location Concurrency
With dozens of active locations, this provides massive throughput gains without complex synchronization.

---

**Space Guild** - Built with Python, powered by clever data structures, and designed for strategic multiplayer chaos.
