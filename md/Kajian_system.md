# KAJIAN SYSTEM - Graph and Configuration

## Legend

### Safety Tags
- **Safe** – No PvP allowed
- **Enforced** – PvP at own risk, responders arrive immediately
- **Patrolled** – PvP allowed, someone might show up though
- **Dangerous** – Things can and will attack you without consequences

### Template Structure
```
- Location Name
	Controlled by: <Faction>
	Description: <Description text>
	Tags: <Safety tag>
	Links:
		- Location 2
		- Location 3
	Vendors (optional):
		- vendor_type
			Entry dialogue: "..."
			Options: [
				- "dialogue":requirements:reward
				- "dialogue":requirements:reward
			]
	Resources gatherable:
		- Resource name
	Things that can spawn here:
		- NPC/item name
```

---

## KAJIAN SYSTEM LOCATIONS

### - Primary Star Orbit
	Controlled by: Scavenger Guild
	Description: The larger, brighter star of the binary system. Massive stellar mass and intense radiation dominate this region.
	Tags: Patrolled
	Links:
		- Secondary Star Orbit
		- Primary Star Orbital Station
		- Gas Giant Orbit
		- Inner Asteroid Belt Region
		- Outer Asteroid Belt Region
		- Shattered Planet 1 Orbit
		- Shattered Planet 2 Orbit
		- Synthetic Planet Orbit
	Things that can spawn here:
		- Scavenger Guild patrols
		- Salvage vessels
		- Independent traders

### - Primary Star Orbital Station
	Controlled by: Scavenger Guild
	Description: A heavily shielded orbital platform circling the primary star. Salvagers use this as a base for operations throughout the system.
	Tags: Safe
	Links:
		- Primary Star Orbit
	Vendors:
		- primarystar_trader
			Entry dialogue: "Welcome to Primary Station. Got salvage to trade?"
    			Options:[]
		- primarystar_salvagebuyer
			Entry dialogue: "I buy anything you pull from wrecks or ruins. Show me what you've got."
    			Options:[]
		- primarystar_heatshielding
			Entry dialogue: "This close to the star, you need the best heat protection. I've got what you need."
    			Options:[]

### - Secondary Star Orbit
	Controlled by: Scavenger Guild
	Description: The smaller, denser companion star. More compact and hotter per unit volume, this white dwarf remnant pulses with exotic energy.
	Tags: Patrolled
	Links:
		- Primary Star Orbit
		- Secondary Star Orbital Station
		- Secondary Star Warp Gate
		- Gas Giant Orbit
		- Inner Asteroid Belt Region
		- Outer Asteroid Belt Region
		- Shattered Planet 1 Orbit
		- Shattered Planet 2 Orbit
		- Synthetic Planet Orbit
	Things that can spawn here:
		- Scavenger Guild patrols
		- Salvage vessels
		- Independent traders

### - Secondary Star Orbital Station
	Controlled by: Scavenger Guild
	Description: A compact, dense station orbiting the white dwarf. The exotic radiation environment makes salvaged materials particularly valuable.
	Tags: Safe
	Links:
		- Secondary Star Orbit
	Vendors:
		- secondarystar_trader
			Entry dialogue: "The density of this star allows for some unique salvage. Interested?"
    			Options:[]
		- secondarystar_repairshop
			Entry dialogue: "Ships take a beating in this environment. Let me fix you up."
    			Options:[]
		- secondarystar_shipwright
			Entry dialogue: "I build ships from salvaged parts and scrap. Tough as nails."
    			Options:[]
		- secondarystar_exoticmaterials
			Entry dialogue: "The white dwarf's radiation transforms salvage into something special. I'll pay top credit."
    			Options:[]

### - Secondary Star Warp Gate
	Controlled by: Scavenger Guild
	Description: Massive warp gate anchored in the gravitational field of the dense secondary star. The primary connection point to other systems.
	Tags: Patrolled
	Links:
		- Secondary Star Orbit
	Vendors:
		- warpgate_gatekeeper
			Entry dialogue: "Transit fee required. No exceptions."
    			Options:[]
		- warpgate_navigation
			Entry dialogue: "I can help you plot courses to connected systems."
    			Options:[]
	Things that can spawn here:
		- Scavenger Guild patrols
		- Gate guards
		- Interstellar transports

### - Gas Giant Orbit
	Controlled by: Scavenger Guild
	Description: A massive gas giant orbits close to both stars, its atmosphere churning with violent storms. Deep within lie valuable resources.
	Tags: Patrolled
	Links:
		- Primary Star Orbit
		- Secondary Star Orbit
		- Gas Giant Orbital Station
		- Gas Giant Deep Storm Site 1
		- Gas Giant Deep Storm Site 2
		- Inner Asteroid Belt Region
		- Outer Asteroid Belt Region
	Things that can spawn here:
		- Scavenger Guild patrol ships
		- Gas haulers
		- Storm divers

### - Gas Giant Orbital Station
	Controlled by: Scavenger Guild
	Description: A refueling and salvage station in high orbit above the gas giant. Storm-diving operations are coordinated from here.
	Tags: Safe
	Links:
		- Gas Giant Orbit
	Vendors:
		- gasgiant_storm_salvager
			Entry dialogue: "The storms below hide wrecks and treasures. I buy whatever you bring up."
    			Options:[]
		- gasgiant_gas_trader
			Entry dialogue: "I process gases from the atmosphere. Premium fuel at fair prices."
    			Options:[]
		- gasgiant_storm_equipment
			Entry dialogue: "Planning to dive into those storms? You'll need specialized gear."
    			Options:[]

### - Gas Giant Deep Storm Site 1
	Controlled by: Scavenger Guild
	Description: A raging tempest in the lower atmosphere. Special extraction equipment required - deploy storm probes to gather exotic materials.
	Tags: Dangerous
	Links:
		- Gas Giant Orbit
	Resources gatherable:
		- Storm-forged crystals
		- Exotic atmospheric compounds
		- High-pressure gases
		- Plasma-charged particles

### - Gas Giant Deep Storm Site 2
	Controlled by: Scavenger Guild
	Description: An even more violent storm system deeper in the atmosphere. Greater rewards for those brave enough to deploy extraction probes.
	Tags: Dangerous
	Links:
		- Gas Giant Orbit
	Resources gatherable:
		- Storm-forged crystals
		- Rare atmospheric materials
		- Supercritical fluids
		- Lightning-infused elements

### - Inner Asteroid Belt Region
	Controlled by: Scavenger Guild
	Description: A dense asteroid field between the gas giant and inner system. Rich in metallic ores and salvageable materials.
	Tags: Patrolled
	Links:
		- Primary Star Orbit
		- Secondary Star Orbit
		- Gas Giant Orbit
		- Shattered Planet 1 Orbit
		- Shattered Planet 2 Orbit
		- Inner Belt Resource Site 1
		- Inner Belt Resource Site 2
	Things that can spawn here:
		- Scavenger Guild patrol ships
		- Salvage vessels
		- Independent prospectors

### - Inner Belt Resource Site 1
	Controlled by: Scavenger Guild
	Description: A massive metallic asteroid with exposed ore veins. Mining and salvage operations are straightforward but competitive.
	Tags: Patrolled
	Links:
		- Inner Asteroid Belt Region
	Resources gatherable:
		- Iron ore
		- Nickel
		- Cobalt
		- Titanium

### - Inner Belt Resource Site 2
	Controlled by: Scavenger Guild
	Description: A carbonaceous asteroid cluster rich in rare earth elements and organic compounds.
	Tags: Patrolled
	Links:
		- Inner Asteroid Belt Region
	Resources gatherable:
		- Rare earth elements
		- Carbon compounds
		- Platinum group metals
		- Water ice

### - Shattered Planet 1 Orbit
	Controlled by: Scavenger Guild
	Description: The remnants of a destroyed world float in orbit. Planetary fragments drift among the debris field - a salvager's paradise.
	Tags: Patrolled
	Links:
		- Primary Star Orbit
		- Secondary Star Orbit
		- Inner Asteroid Belt Region
		- Outer Asteroid Belt Region
		- Shattered Planet 1 Orbital Station
		- Shattered Planet 1 Surface Site
	Things that can spawn here:
		- Scavenger Guild patrol ships
		- Salvage vessels
		- Wreck hunters

### - Shattered Planet 1 Orbital Station
	Controlled by: Scavenger Guild
	Description: A station built into the largest remaining fragment of the destroyed planet. Serves as a base for salvage operations.
	Tags: Safe
	Links:
		- Shattered Planet 1 Orbit
	Vendors:
		- shattered1_salvage_trader
			Entry dialogue: "The planet below is full of salvage. I buy whatever you find."
    			Options:[]
		- shattered1_wreck_buyer
			Entry dialogue: "Pre-shattering artifacts are worth a fortune. Show me what you've pulled from the ruins."
    			Options:[]
		- shattered1_hazard_equipment
			Entry dialogue: "The surface is deadly. Don't go down without proper protection."
    			Options:[]

### - Shattered Planet 1 Surface Site
	Controlled by: Scavenger Guild
	Description: A treacherous landing zone on the largest fragment. Unstable terrain and extreme conditions make this a deadly salvage location.
	Tags: Dangerous
	Links:
		- Shattered Planet 1 Orbit
	Resources gatherable:
		- Ancient artifacts
		- Rare planetary minerals
		- Crystalline formations
		- Pre-shattering technology fragments
	Things that can spawn here:
		- Unstable terrain hazards
		- Radiation storms
		- Hostile automated defenses

### - Outer Asteroid Belt Region
	Controlled by: Scavenger Guild
	Description: A wider, less dense asteroid field in the outer system. Contains more exotic salvage but requires longer travel times.
	Tags: Patrolled
	Links:
		- Primary Star Orbit
		- Secondary Star Orbit
		- Gas Giant Orbit
		- Shattered Planet 1 Orbit
		- Shattered Planet 2 Orbit
		- Synthetic Planet Orbit
		- Outer Belt Resource Site 1
		- Outer Belt Resource Site 2
		- Outer Belt Resource Site 3
		- Outer Belt Resource Site 4
	Things that can spawn here:
		- Scavenger Guild patrol ships
		- Salvage vessels
		- Explorers

### - Outer Belt Resource Site 1
	Controlled by: Scavenger Guild
	Description: A silicate asteroid rich in construction materials and industrial compounds.
	Tags: Patrolled
	Links:
		- Outer Asteroid Belt Region
	Resources gatherable:
		- Silicon
		- Aluminum
		- Industrial metals
		- Glass-forming compounds

### - Outer Belt Resource Site 2
	Controlled by: Scavenger Guild
	Description: An ice-rich asteroid with valuable volatile compounds frozen in its core.
	Tags: Patrolled
	Links:
		- Outer Asteroid Belt Region
	Resources gatherable:
		- Water ice
		- Ammonia
		- Methane ice
		- Frozen volatiles

### - Outer Belt Resource Site 3
	Controlled by: Scavenger Guild
	Description: A metallic asteroid with high concentrations of precious metals embedded in its structure.
	Tags: Patrolled
	Links:
		- Outer Asteroid Belt Region
	Resources gatherable:
		- Gold
		- Platinum
		- Palladium
		- Silver

### - Outer Belt Resource Site 4
	Controlled by: Scavenger Guild
	Description: A rare radioactive asteroid containing uranium and thorium deposits. Requires specialized extraction equipment.
	Tags: Patrolled
	Links:
		- Outer Asteroid Belt Region
	Resources gatherable:
		- Uranium
		- Thorium
		- Radioactive isotopes
		- Heavy metals

### - Shattered Planet 2 Orbit
	Controlled by: Scavenger Guild
	Description: The second destroyed world in the system. This planet's fragments are more scattered and the debris field more dangerous - but the salvage is richer.
	Tags: Dangerous
	Links:
		- Primary Star Orbit
		- Secondary Star Orbit
		- Inner Asteroid Belt Region
		- Outer Asteroid Belt Region
		- Synthetic Planet Orbit
		- Shattered Planet 2 Orbital Station
		- Shattered Planet 2 Surface Site 1
		- Shattered Planet 2 Surface Site 2
	Things that can spawn here:
		- Scavenger Guild patrol ships
		- Salvage hunters
		- Rogue scavengers
		- Debris hazards

### - Shattered Planet 2 Orbital Station
	Controlled by: Scavenger Guild
	Description: A larger station than its counterpart at Shattered Planet 1, built to support multiple dangerous salvage operations.
	Tags: Safe
	Links:
		- Shattered Planet 2 Orbit
	Vendors:
		- shattered2_salvage_trader
			Entry dialogue: "Two surface sites means double the salvage. And double the danger."
    			Options:[]
		- shattered2_salvage_coordinator
			Entry dialogue: "I organize salvage teams. Looking to join one, or hire protection?"
    			Options:[]
		- shattered2_medical_facility
			Entry dialogue: "Surface injuries are common. I patch up survivors."
    			Options:[]
		- shattered2_advanced_equipment
			Entry dialogue: "This planet's sites are more dangerous. You'll need the best gear available."
    			Options:[]

### - Shattered Planet 2 Surface Site 1
	Controlled by: Scavenger Guild
	Description: An exposed underground facility from before the shattering. Automated defenses remain active. Extreme danger, extreme salvage.
	Tags: Dangerous
	Links:
		- Shattered Planet 2 Orbit
	Resources gatherable:
		- Pre-war technology
		- Advanced components
		- Experimental materials
		- Ancient data cores
	Things that can spawn here:
		- Hostile defense drones
		- Security robots
		- Environmental hazards
		- Unstable energy fields

### - Shattered Planet 2 Surface Site 2
	Controlled by: Scavenger Guild
	Description: A massive crater exposing the planet's mantle. Rich in exotic minerals but plagued by volcanic activity and toxic gases.
	Tags: Dangerous
	Links:
		- Shattered Planet 2 Orbit
	Resources gatherable:
		- Mantle minerals
		- Exotic crystals
		- Volcanic glass
		- Rare geological specimens
	Things that can spawn here:
		- Lava flows
		- Toxic gas vents
		- Seismic activity
		- Extreme temperatures

### - Synthetic Planet Orbit
	Controlled by: Scientific Guild
	Description: An artificially constructed world, a marvel of ancient engineering. The planet's surface gleams with metallic structures and megacity complexes.
	Tags: Enforced
	Links:
		- Primary Star Orbit
		- Secondary Star Orbit
		- Outer Asteroid Belt Region
		- Shattered Planet 2 Orbit
		- Synthetic Planet Orbital Station 1
		- Synthetic Planet Orbital Station 2
		- Synthetic Planet Ground Station
	Things that can spawn here:
		- Scientific Guild enforcers
		- Commercial transports
		- Research expeditions
		- Synthetic planet security forces

### - Synthetic Planet Orbital Station 1
	Controlled by: Scientific Guild
	Description: The primary orbital hub for the synthetic planet. A massive ring station handling the majority of commercial and scientific traffic.
	Tags: Safe
	Links:
		- Synthetic Planet Orbit
	Vendors:
		- synthetic_orbital1_shipwright
			Entry dialogue: "Welcome to the finest shipyard in the system. What can I build for you?"
    			Options:[]
		- synthetic_orbital1_advanced_trader
			Entry dialogue: "The synthetic planet produces unique goods. Take a look at my inventory."
    			Options:[]
		- synthetic_orbital1_technology_dealer
			Entry dialogue: "Ancient technology, reverse-engineered and improved. Very expensive, very effective."
    			Options:[]
		- synthetic_orbital1_component_specialist
			Entry dialogue: "I specialize in ship components enhanced with synthetic planet technology."
    			Options:[]

### - Synthetic Planet Orbital Station 2
	Controlled by: Scientific Guild
	Description: A secondary station focusing on research and experimental technologies. Access is more restricted than Station 1.
	Tags: Safe
	Links:
		- Synthetic Planet Orbit
	Vendors:
		- synthetic_orbital2_research_vendor
			Entry dialogue: "Our experiments push the boundaries of known science. Results available for purchase."
    			Options:[]
		- synthetic_orbital2_prototype_dealer
			Entry dialogue: "Prototype equipment, fresh from the labs. Powerful but sometimes unstable."
    			Options:[]
		- synthetic_orbital2_data_broker
			Entry dialogue: "I trade in information about the synthetic planet's construction and purpose."
    			Options:[]

### - Synthetic Planet Ground Station
	Controlled by: Scientific Guild
	Description: The central hub on the synthetic planet's surface. A sprawling complex where ancient architecture meets modern civilization.
	Tags: Safe
	Links:
		- Synthetic Planet Orbit
	Vendors:
		- synthetic_ground_cultural_exchange
			Entry dialogue: "The history of this world is fascinating. I can teach you much... for a price."
    			Options:[]
		- synthetic_ground_master_shipwright
			Entry dialogue: "The ground facilities allow me to build ships nowhere else in the system can match."
    			Options:[]
		- synthetic_ground_megacity_trader
			Entry dialogue: "Millions live on this planet. I have connections to get you anything you need."
    			Options:[]
		- synthetic_ground_ancient_technology
			Entry dialogue: "Deep below the surface lie the planet's original systems. I've salvaged some... pieces."
    			Options:[]
		- synthetic_ground_colony_administrator
			Entry dialogue: "I manage resource distribution for the colony. Perhaps we can make a deal."
    			Options:[]

---

## LOCATION SUMMARY

**Binary Stars (Enforced):**
- Primary Star Orbit, Secondary Star Orbit
- 2 Orbital Stations (1 per star)
- 1 Warp Gate (Secondary Star)

**Gas Giant System (Patrolled/Dangerous):**
- Gas Giant Orbit (Patrolled)
- 1 Orbital Station
- 2 Deep Storm Resource Sites (Dangerous, requires special extraction equipment)

**Asteroid Belts (Patrolled):**
- 2 Belt Regions (Inner, Outer)
- 6 Resource Sites (2 in Inner, 4 in Outer)

**Shattered Planets (Patrolled/Dangerous):**
- Shattered Planet 1: Orbit (Patrolled), 1 Orbital Station, 1 Deadly Surface Site
- Shattered Planet 2: Orbit (Dangerous), 1 Orbital Station, 2 Dangerous Surface Sites

**Synthetic Planet (Enforced/Safe):**
- Synthetic Planet Orbit (Enforced)
- 2 Orbital Stations
- 1 Ground Station

**Total Locations:** 32

---

## VENDOR SUMMARY

**Total Vendors:** 29

**By Category:**
- Shipwrights: 4
- Traders/General: 5
- Research/Data: 5
- Salvage/Archaeological: 3
- Equipment/Gear: 4
- Technology Specialists: 4
- Specialized Services: 4

**By Location Type:**
- Star Stations: 6 vendors
- Gas Giant Station: 3 vendors
- Shattered Planet Stations: 7 vendors
- Synthetic Planet Stations: 13 vendors

---

## NOTES

- Binary star system creates unique gravitational and radiation dynamics
- Secondary star (white dwarf) enables exotic research and manufacturing
- Warp gate positioned at secondary star for gravitational stability
- Gas Giant deep storms require special extraction items (deployable probes)
- Two shattered planets suggest ancient catastrophic events
- Shattered Planet 2 more dangerous with two surface sites vs one for Planet 1
- Synthetic Planet is the system's crown jewel - artificial world with advanced technology
- Progression from Safe (stations) → Patrolled (belts, orbits) → Dangerous (storms, surfaces)

### Spawn Distribution Philosophy:
- **Divided system** - Scavenger Guild controls most of the system, Scientific Guild controls only the Synthetic Planet
- **Patrolled zones** (stellar orbits, asteroid belts, shattered planets, gas giant): Scavenger patrols + salvagers
- **Enforced zones** (synthetic planet orbit): Scientific Guild enforcers + research vessels
- **Dangerous zones** (deep storms, surface sites, shattered planet 2 orbit): Environmental hazards + hostile defenses
- **Limited pirate presence** - Both guilds maintain reasonable security
- PvP opportunities exist in Patrolled and Dangerous zones

### Resource Gathering Design:
- **Standard mining**: Asteroid belt sites (6 total)
- **Specialized extraction**: Gas giant storms require deployment of special equipment items
- **High-risk, high-reward**: Shattered planet surface sites (3 total)
- **Resource tier progression**: Belts (common) → Storms (rare) → Surfaces (exotic/ancient)

### Synthetic Planet Lore:
- Artificially constructed world - ancient megastructure
- Two orbital stations (commercial + research focused)
- Ground station with access to underground ancient systems
- Highest concentration of advanced vendors in system
- **Only location controlled by Scientific Guild** - they claimed it for research purposes
- Represents pinnacle of system's technological achievement
- Scavenger Guild controls the rest of the system, making this a unique political situation
