# NPC SHIP DIALOGUE

## Overview

This document defines dialogue interactions between players and NPC ships encountered in space. Unlike station vendors (who are always at fixed locations), these are mobile NPCs that spawn in various regions.

### Dialogue Rules
- **Player-Initiated**: Players can hail any NPC ship and attempt dialogue
- **NPC-Initiated**: Only certain NPC types can send unsolicited messages to player ships
- **Context-Dependent**: Some dialogue options only appear based on player status, location, or reputation

---

## NPC SHIP TYPES

### ORION Enforcers
**Can initiate dialogue:** Yes
**Spawn locations:** All Enforced zones (planetary orbits)
**Behavior:** Patrol and respond to player crimes

**NPC-Initiated Messages:**
```
- "ORION PATROL: This is a routine scan. Stand by."
- "ORION PATROL: You are in violation of ORION space law. Power down your weapons."
- "ORION PATROL: Unidentified ship, state your business in this sector."
```

**Player Dialogue Options:**
```
- "I'm just passing through" → Neutral response, enforcer continues patrol
- "I need assistance" → Enforcer provides info about nearest station
- "What's the situation here?" → Enforcer shares local security status
- [If wanted] "I surrender" → Initiate arrest sequence
```

---

### ORION Patrol Ships
**Can initiate dialogue:** Yes
**Spawn locations:** All Patrolled zones (Asteroid Belt, Saturn Rings, KR1)
**Behavior:** Less aggressive than enforcers, focused on deterrence

**NPC-Initiated Messages:**
```
- "ORION PATROL: We're keeping the peace out here. Move safe."
- "ORION PATROL: Report any suspicious activity to the nearest station."
- "ORION PATROL: This sector is under ORION protection."
```

**Player Dialogue Options:**
```
- "Any trouble in the area?" → Patrol shares recent activity
- "Need any help?" → Patrol may request assistance with tasks
- "I'm looking for something" → Patrol provides local intel
```

---

### Trade Vessels
**Can initiate dialogue:** No
**Spawn locations:** Earth Orbit, Venus Orbit, Mars Orbit
**Behavior:** Transport goods between stations, avoid danger

**Player Dialogue Options:**
```
- "What are you hauling?" → Trader shares cargo manifest
- "Where are you headed?" → Trader shares destination
- "Need an escort?" → May offer escort contract (if implemented)
- [If pirate] "Hand over your cargo" → Initiate piracy attempt
```

---

### Gas Haulers
**Can initiate dialogue:** No
**Spawn locations:** Jupiter Orbit, Saturn Orbit, Uranus Orbit
**Behavior:** Transport gas from atmospheric stations

**Player Dialogue Options:**
```
- "What are you hauling?" → Hauler shares cargo type
- "Where are you headed?" → Hauler shares destination
- "Any news from the stations?" → Hauler shares rumors/info
```

---

### Mining Drones
**Can initiate dialogue:** No
**Spawn locations:** All Asteroid Belt regions
**Behavior:** Automated mining, no crew

**Player Dialogue Options:**
```
- "System query" → Returns basic operational status
- [No other options - it's a drone]
```

---

### Independent Miners
**Can initiate dialogue:** No
**Spawn locations:** Asteroid Belt regions, Kuiper Region 1
**Behavior:** Mining resources, generally friendly

**Player Dialogue Options:**
```
- "How's the mining?" → Miner shares yield info
- "Seen anything unusual?" → Miner shares local sightings
- "Want to trade?" → May trade materials for supplies
- [If pirate] "Hand over your haul" → Initiate piracy attempt
```

---

### Research Vessels
**Can initiate dialogue:** Yes (sometimes)
**Spawn locations:** Jupiter Orbit, Saturn Orbit, Sun Orbit
**Behavior:** Conducting scientific research

**NPC-Initiated Messages:**
```
- "RESEARCH VESSEL: We're detecting unusual readings. Please maintain distance."
- "RESEARCH VESSEL: Our sensors indicate anomalous activity in this sector."
```

**Player Dialogue Options:**
```
- "What are you researching?" → Vessel shares research focus
- "Need any assistance?" → May request data collection help
- "Seen anything interesting?" → Shares scientific discoveries
```

---

### Ice Prospectors
**Can initiate dialogue:** No
**Spawn locations:** Neptune Orbit, Kuiper Region 1
**Behavior:** Searching for valuable ice deposits

**Player Dialogue Options:**
```
- "Found anything good?" → Prospector shares recent finds
- "Any dangerous spots?" → Warns about pirate activity
- "Want to trade?" → May trade ice samples
```

---

### Salvage Vessels
**Can initiate dialogue:** No
**Spawn locations:** Asteroid Belt Region 3
**Behavior:** Collecting debris and abandoned equipment

**Player Dialogue Options:**
```
- "What are you salvaging?" → Vessel shares what they found
- "Seen any wrecks?" → May share wreck locations
- "Want to sell anything?" → May offer salvaged items
```

---

### Exploration Drones
**Can initiate dialogue:** No
**Spawn locations:** Kuiper Region 1
**Behavior:** Automated exploration, minimal interaction

**Player Dialogue Options:**
```
- "System query" → Returns exploration data summary
- [No other options - it's a drone]
```

---

### Tourist Vessels
**Can initiate dialogue:** No
**Spawn locations:** Moon Orbit
**Behavior:** Sightseeing tours, harmless

**Player Dialogue Options:**
```
- "Enjoying the view?" → Tourist shares enthusiasm
- "First time out here?" → Tourist shares travel stories
- "Need directions?" → Provide navigation help
```

---

### Military Transports
**Can initiate dialogue:** Yes
**Spawn locations:** Mars Orbit
**Behavior:** ORION military logistics, heavily armed

**NPC-Initiated Messages:**
```
- "ORION MILITARY: Maintain distance. This is a restricted convoy."
- "ORION MILITARY: Unidentified vessel, state your clearance level."
```

**Player Dialogue Options:**
```
- "Just passing through" → Acknowledged, maintain distance
- [If high reputation] "Reporting for escort duty" → May accept player escort
```

---

### Colonial Vessels
**Can initiate dialogue:** No
**Spawn locations:** Mars Orbit
**Behavior:** Transporting colonists and supplies

**Player Dialogue Options:**
```
- "Where are you settling?" → Shares colony destination
- "Need supplies?" → May purchase supplies from player
- "How's the colony life?" → Shares stories
```

---

### Ring Miners
**Can initiate dialogue:** No
**Spawn locations:** Saturn Orbit
**Behavior:** Harvesting Saturn's ring materials

**Player Dialogue Options:**
```
- "How's the harvest?" → Miner shares yield
- "Dangerous work?" → Shares hazard stories
- "Want to trade?" → May trade ring materials
```

---

### Frontier Transports
**Can initiate dialogue:** No
**Spawn locations:** Neptune Orbit
**Behavior:** Resupplying outer system stations

**Player Dialogue Options:**
```
- "Heading to the Kuiper Belt?" → Shares route info
- "Any news from the inner system?" → Shares rumors
- "Need an escort?" → May hire player for protection
```

---

### Customs Inspectors
**Can initiate dialogue:** Yes
**Spawn locations:** SOL Warp Gates
**Behavior:** Inspect ships entering/leaving Sol System

**NPC-Initiated Messages:**
```
- "SOL CUSTOMS: Prepare for inspection. Transmit your cargo manifest."
- "SOL CUSTOMS: Welcome to Sol System. Please declare any restricted items."
- "SOL CUSTOMS: Routine customs check. This will only take a moment."
```

**Player Dialogue Options:**
```
- "Here's my manifest" → Submit to inspection
- "I have nothing to declare" → Quick inspection
- [If smuggling] "Everything's in order" → Attempt to bluff
- "I'm in a hurry" → May pay fast-track fee
```

---

## HOSTILE NPC TYPES (Kuiper Belt)

### Ice Pirates
**Can initiate dialogue:** Yes
**Spawn locations:** Kuiper Region 1, 2
**Behavior:** Demand cargo or attack

**NPC-Initiated Messages:**
```
- "Cut your engines and dump your cargo. You won't be harmed."
- "This is our territory. Pay the toll or suffer the consequences."
- "Nice ship you've got there. It'd be a shame if something happened to it."
```

**Player Dialogue Options:**
```
- "I don't have anything valuable" → May reduce demand
- "You don't want to do this" → Intimidation attempt
- [Pay toll] "Fine, here's your cut" → Give credits/items, they leave
- "Come and take it" → Initiate combat
```

---

### Pirate Scouts
**Can initiate dialogue:** Yes
**Spawn locations:** Kuiper Region 2
**Behavior:** Scout for valuable targets, may flee or attack

**NPC-Initiated Messages:**
```
- "Well, well... what do we have here?"
- "You're a long way from ORION protection, friend."
```

**Player Dialogue Options:**
```
- "Keep moving" → Pirate may leave or engage
- "I'm not your friend" → Hostile response
- [If strong ship] "Leave now or I'll destroy you" → May flee
```

---

### Pirate Raiders
**Can initiate dialogue:** Yes
**Spawn locations:** Kuiper Region 2
**Behavior:** Actively hunting for cargo and ships

**NPC-Initiated Messages:**
```
- "Power down your ship. We're boarding you."
- "Your ship or your life. Choose quickly."
```

**Player Dialogue Options:**
```
- [Pay ransom] "How much to let me go?" → Negotiate payment
- "I'll fight my way out" → Initiate combat
- [If player is pirate] "I'm one of you" → May avoid fight
```

---

### Pirate Fleets
**Can initiate dialogue:** Yes
**Spawn locations:** Kuiper Region 3, 4
**Behavior:** Organized pirate groups, very dangerous

**NPC-Initiated Messages:**
```
- "FLEET LEADER: You've entered our space. Tribute is required."
- "FLEET LEADER: Surrender your ship and you may live."
- "FLEET LEADER: Join us or join the debris field."
```

**Player Dialogue Options:**
```
- [Pay tribute] "How much?" → Large payment required
- [Join them] "I want to join your fleet" → May recruit player
- "I'll take my chances" → Fight entire fleet
- [If reputation] "I have a deal to offer" → Special dialogue
```

---

### Rogue Prospectors
**Can initiate dialogue:** No
**Spawn locations:** Kuiper Region 2
**Behavior:** Independent miners, may be desperate or hostile

**Player Dialogue Options:**
```
- "How's it going out here?" → May share situation
- "Need supplies?" → May trade at high markup
- "This is a dangerous place" → Warns about pirates
```

---

### Rogue Miners
**Can initiate dialogue:** No
**Spawn locations:** Kuiper Region 3
**Behavior:** Outlaws mining in lawless space

**Player Dialogue Options:**
```
- "What are you mining?" → May share or refuse
- "Want to trade?" → May trade rare materials
- "ORION is looking for you" → May flee or attack
```

---

### Outlaws
**Can initiate dialogue:** Yes
**Spawn locations:** Kuiper Region 3, 4
**Behavior:** Criminals, smugglers, exiles - unpredictable

**NPC-Initiated Messages:**
```
- "Turn around. Nothing for you out here."
- "You see me, you saw nothing. Understand?"
```

**Player Dialogue Options:**
```
- "I didn't see anything" → Outlaw leaves
- "What are you running from?" → May share story
- "ORION would pay for your location" → Hostile response
- [If player is outlaw] "We're both hiding" → May share info
```

---

### Unknown Entities
**Can initiate dialogue:** Yes
**Spawn locations:** Kuiper Region 4
**Behavior:** Mysterious, alien, or experimental - unknown intentions

**NPC-Initiated Messages:**
```
- "..." [garbled transmission]
- "[SIGNAL CORRUPTED]"
- "Why are you here?"
```

**Player Dialogue Options:**
```
- "Who are you?" → May get cryptic response
- "What do you want?" → Unknown
- "I come in peace" → Unknown
- [Scan them] → May reveal information or provoke attack
```

---

## DIALOGUE MECHANICS

### Response Types
- **Neutral**: NPC continues current behavior
- **Friendly**: NPC may offer information, trades, or contracts
- **Hostile**: NPC becomes aggressive or attacks
- **Flee**: NPC attempts to escape
- **Trade**: Opens trade interface
- **Contract**: Offers mission or task

### Reputation Effects
- High ORION reputation: Better responses from ORION NPCs, hostile from pirates
- Low ORION reputation: ORION NPCs suspicious, pirates may be friendlier
- Pirate reputation: Pirates less likely to attack, ORION more aggressive

### Context-Based Options
Some dialogue options only appear if:
- Player has specific items in cargo
- Player has certain reputation level
- Player is in specific ship type
- Player has completed certain missions
- Player is wanted by ORION

---

## IMPLEMENTATION NOTES

- All dialogue arrays above are placeholders for the actual dialogue system
- NPC responses may vary based on RNG and player stats
- Some NPCs may remember previous interactions with the player
- Certain dialogue paths may open up side missions or unlock new vendors
- Failed dialogue attempts (intimidation, bluffing) may have consequences
