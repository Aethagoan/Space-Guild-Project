# SOL SYSTEM - Graph and Configuration

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

## SOL SYSTEM LOCATIONS

### - Earth Orbit
	Controlled by: ORION
	Description: The place players start, floating just above the blue marble.
	Tags: Safe
	Links:
		- Sun Orbit
		- Mercury Orbit
		- Mars Orbit
		- Asteroid Belt Region 1
		- Asteroid Belt Region 2
		- Asteroid Belt Region 3
		- Jupiter Orbit
		- Moon Orbit
		- Earth Orbital Station Zero
		- Earth Ground Station Zero
	Things that can spawn here:
		- ORION enforcers
		- Trade vessels

### - Earth Orbital Station Zero
	Controlled by: ORION
	Description: The orbital Station above earth, a full ring around the earth.
	Tags: Safe
	Links:
		- Earth Orbit
	Vendors:
		- earthorbit_zero_shipwright
			Entry dialogue: ""
    			Options:[]
		- earthorbit_zero_trader
			Entry dialogue: ""
    			Options:[]
		- earthorbit_zero_repairshop
			Entry dialogue: ""
    			Options:[]

### - Moon Orbit
	Controlled by: ORION
	Description: Earth's Moon looms large. Ancient landing sites are visible on the surface below.
	Tags: Enforced
	Links:
		- Earth Orbit
		- Moon Ground Station
	Things that can spawn here:
		- ORION enforcers
		- Tourist vessels

### - Moon Ground Station
	Controlled by: ORION
	Description: Humanity's first extraterrestrial colony. Now a museum and trading post for historical artifacts.
	Tags: Safe
	Links:
		- Moon Orbit
	Vendors:
		- moon_historian
			Entry dialogue: ""
    			Options:[]
		- moon_artifactdealer
			Entry dialogue: ""
    			Options:[]
		- moon_shipwright
			Entry dialogue: ""
    			Options:[]

### - Earth Ground Station Zero
	Controlled by: ORION
	Description: The planetary headquarters of ORION, located at the equator. A sprawling complex of hangars and trading posts.
	Tags: Safe
	Links:
		- Earth Orbit
	Vendors:
		- earthground_zero_shipwright
			Entry dialogue: ""
    			Options:[]
		- earthground_zero_trader
			Entry dialogue: ""
    			Options:[]

### - Sun Orbit
	Controlled by: ORION
	Description: The heart of the Sol System. Extreme heat and radiation make this a challenging navigation point.
	Tags: Enforced
	Links:
		- Earth Orbit
		- Mercury Orbit
		- Venus Orbit
		- Mars Orbit
		- Asteroid Belt Region 1
		- Asteroid Belt Region 2
		- Asteroid Belt Region 3
		- Jupiter Orbit
		- Saturn Orbit
		- SOL Warp Gates
	Things that can spawn here:
		- ORION enforcers
		- Solar research vessels

### - SOL Warp Gates
	Controlled by: ORION
	Description: Massive warp gate structures that connect the Sol System to distant star systems. Heavily guarded and monitored.
	Tags: Enforced
	Links:
		- Sun Orbit
	Vendors:
		- solgate_customs
			Entry dialogue: ""
    			Options:[]
		- solgate_navigation
			Entry dialogue: ""
    			Options:[]
	Things that can spawn here:
		- ORION enforcers
		- Customs inspectors

### - Mercury Orbit
	Controlled by: ORION
	Description: Close to the sun, Mercury's orbit is searing hot. The planet below is pockmarked with mining operations.
	Tags: Enforced
	Links:
		- Earth Orbit
		- Sun Orbit
		- Asteroid Belt Region 1
		- Asteroid Belt Region 2
		- Asteroid Belt Region 3
		- Venus Orbit
		- Mars Orbit
		- Mercury Ground Station
	Things that can spawn here:
		- ORION enforcers
		- Mining transports

### - Mercury Ground Station
	Controlled by: ORION
	Description: A heavily shielded facility on Mercury's surface, specializing in heat-resistant components and bounty hunting operations.
	Tags: Safe
	Links:
		- Mercury Orbit
	Vendors:
		- mercury_shipwright
			Entry dialogue: ""
    			Options:[]
		- mercury_hunters
			Entry dialogue: ""
    			Options:[]

### - Venus Orbit
	Controlled by: ORION
	Description: Venus hangs below, a toxic planet shrouded in acidic clouds. The orbital station is a hub for black market activity.
	Tags: Enforced
	Links:
		- Earth Orbit
		- Sun Orbit
		- Asteroid Belt Region 1
		- Asteroid Belt Region 2
		- Asteroid Belt Region 3
		- Mercury Orbit
		- Mars Orbit
		- Venus Orbital Station
		- Venus Ground Station
	Things that can spawn here:
		- ORION enforcers
		- Trade vessels

### - Venus Ground Station
	Controlled by: ORION
	Description: A fortified dome facility on Venus's surface. Known for illicit dealings and untraceable goods.
	Tags: Safe
	Links:
		- Venus Orbit
	Vendors:
		- venusground_blackmarket
			Entry dialogue: ""
    			Options:[]

### - Venus Orbital Station
	Controlled by: ORION
	Description: An aging orbital platform with questionable security. Traders and smugglers frequent the docks.
	Tags: Safe
	Links:
		- Venus Orbit
	Vendors:
		- venusorbital_trader
			Entry dialogue: ""
    			Options:[]
		- venusorbital_componentdealer
			Entry dialogue: ""
    			Options:[]

### - Mars Orbit
	Controlled by: ORION
	Description: The red planet below is dotted with terraforming projects. Mars Orbit serves as a major military and trade hub.
	Tags: Enforced
	Links:
		- Earth Orbit
		- Jupiter Orbit
		- Asteroid Belt Region 1
		- Asteroid Belt Region 2
		- Asteroid Belt Region 3
		- Sun Orbit
		- Venus Orbit
		- Mercury Orbit
		- Mars Ground Station
		- Mars Orbital Station
		- Mars Moon 1 Ground Station
		- Mars Moon 2 Ground Station
	Things that can spawn here:
		- ORION enforcers
		- Military transports
		- Colonial vessels

### - Mars Ground Station
	Controlled by: ORION
	Description: Built into the Martian surface, this station is a center for colonial operations and ship manufacturing.
	Tags: Safe
	Links:
		- Mars Orbit
	Vendors:
		- marsground_shipwright
			Entry dialogue: ""
    			Options:[]
		- marsground_colonysupplies
			Entry dialogue: ""
    			Options:[]

### - Mars Orbital Station
	Controlled by: ORION
	Description: The largest orbital facility around Mars, equipped with advanced shipyards and defensive systems.
	Tags: Safe
	Links:
		- Mars Orbit
	Vendors:
		- marsorbital_shipwright
			Entry dialogue: ""
    			Options:[]
		- marsorbital_defensesystems
			Entry dialogue: ""
    			Options:[]

### - Mars Moon 1 Ground Station
	Controlled by: ORION
	Description: Phobos Station - A weapons depot built into the moon's interior. Heavily armed and fortified.
	Tags: Safe
	Links:
		- Mars Orbit
	Vendors:
		- marsmoon1_weaponsdealer
			Entry dialogue: ""
    			Options:[]
		- marsmoon1_ammunition
			Entry dialogue: ""
    			Options:[]

### - Mars Moon 2 Ground Station
	Controlled by: ORION
	Description: Deimos Station - A secretive research facility specializing in stealth technology and cloaking devices.
	Tags: Safe
	Links:
		- Mars Orbit
	Vendors:
		- marsmoon2_stealthcloakvendor
			Entry dialogue: ""
    			Options:[]
		- marsmoon2_stealthresearch
			Entry dialogue: ""
    			Options:[]

### - Asteroid Belt Region 1
	Controlled by: ORION
	Description: The inner belt region, dense with asteroids and mining operations. ORION patrols are frequent but not constant.
	Tags: Patrolled
	Links:
		- Asteroid Belt Region 2
		- Asteroid Belt Region 3
		- Earth Orbit
		- Mars Orbit
		- Venus Orbit
		- Mercury Orbit
		- Sun Orbit
		- Jupiter Orbit
		- Saturn Orbit
		- Uranus Orbit
		- Neptune Orbit
		- ABR1 Resource 1
		- ABR1 Resource 2
		- ABR1 Space Station
	Things that can spawn here:
		- ORION patrol ships
		- Mining drones
		- Independent miners

### - ABR1 Resource 1
	Controlled by: ORION
	Description: A large metallic asteroid rich in precious metals. Mining equipment is scattered across its surface.
	Tags: Patrolled
	Links:
		- Asteroid Belt Region 1
	Resources gatherable:
		- Precious metals
		- Iron ore
		- Nickel

### - ABR1 Resource 2
	Controlled by: ORION
	Description: A cluster of smaller asteroids with high concentrations of rare earth elements.
	Tags: Patrolled
	Links:
		- Asteroid Belt Region 1
	Resources gatherable:
		- Precious metals
		- Platinum
		- Rare earth elements

### - ABR1 Space Station
	Controlled by: ORION
	Description: A small outpost serving miners and traders in the belt. Known for mail delivery contracts.
	Tags: Safe
	Links:
		- Asteroid Belt Region 1
	Vendors:
		- abr1station_maildelivery
			Entry dialogue: ""
    			Options:[]
		- abr1station_miningequipment
			Entry dialogue: ""
    			Options:[]

### - Asteroid Belt Region 2
	Controlled by: ORION
	Description: The central belt region with the highest density of asteroids. Navigation requires skill and caution.
	Tags: Patrolled
	Links:
		- Asteroid Belt Region 1
		- Asteroid Belt Region 3
		- Earth Orbit
		- Mars Orbit
		- Venus Orbit
		- Mercury Orbit
		- Sun Orbit
		- Jupiter Orbit
		- Saturn Orbit
		- Uranus Orbit
		- Neptune Orbit
		- ABR2 Resource 1
		- ABR2 Resource 2
		- ABR2 Space Station
	Things that can spawn here:
		- ORION patrol ships
		- Mining drones
		- Independent miners

### - ABR2 Resource 1
	Controlled by: ORION
	Description: A carbonaceous asteroid with valuable organic compounds and water ice deposits.
	Tags: Patrolled
	Links:
		- Asteroid Belt Region 2
	Resources gatherable:
		- Precious metals
		- Water ice
		- Carbon compounds

### - ABR2 Resource 2
	Controlled by: ORION
	Description: A massive iron-nickel asteroid, one of the most profitable mining sites in the belt.
	Tags: Patrolled
	Links:
		- Asteroid Belt Region 2
	Resources gatherable:
		- Precious metals
		- Iron ore
		- Titanium

### - ABR2 Space Station
	Controlled by: ORION
	Description: A fortified station known for weapons trafficking. ORION turns a blind eye in exchange for information.
	Tags: Safe
	Links:
		- Asteroid Belt Region 2
	Vendors:
		- abr2station_weapontraffickers
			Entry dialogue: ""
    			Options:[]
		- abr2station_informationbroker
			Entry dialogue: ""
    			Options:[]

### - Asteroid Belt Region 3
	Controlled by: ORION
	Description: The outer belt region, bordering Jupiter's influence. Less dense but still profitable for experienced miners.
	Tags: Patrolled
	Links:
		- Asteroid Belt Region 1
		- Asteroid Belt Region 2
		- Earth Orbit
		- Mars Orbit
		- Venus Orbit
		- Mercury Orbit
		- Sun Orbit
		- Jupiter Orbit
		- Saturn Orbit
		- Uranus Orbit
		- Neptune Orbit
		- ABR3 Resource 1
		- ABR3 Resource 2
		- ABR3 Space Station
	Things that can spawn here:
		- ORION patrol ships
		- Mining drones
		- Salvage vessels

### - ABR3 Resource 1
	Controlled by: ORION
	Description: A silicate asteroid with rare mineral deposits, popular with independent prospectors.
	Tags: Patrolled
	Links:
		- Asteroid Belt Region 3
	Resources gatherable:
		- Precious metals
		- Silicon
		- Rare minerals

### - ABR3 Resource 2
	Controlled by: ORION
	Description: An asteroid field with scattered chunks of high-grade platinum and iridium.
	Tags: Patrolled
	Links:
		- Asteroid Belt Region 3
	Resources gatherable:
		- Precious metals
		- Platinum
		- Iridium

### - ABR3 Space Station
	Controlled by: ORION
	Description: A research and trading station specializing in shield technology and experimental explosives.
	Tags: Safe
	Links:
		- Asteroid Belt Region 3
	Vendors:
		- abr3station_shieldspecialists
			Entry dialogue: ""
    			Options:[]
		- abr3station_explosives
			Entry dialogue: ""
    			Options:[]
		- abr3station_researchdata
			Entry dialogue: ""
    			Options:[]

### - Jupiter Orbit
	Controlled by: ORION
	Description: The massive gas giant dominates the view. Orbital traffic is heavy with gas haulers and research vessels.
	Tags: Enforced
	Links:
		- Asteroid Belt Region 1
		- Asteroid Belt Region 2
		- Asteroid Belt Region 3
		- Mars Orbit
		- Earth Orbit
		- Saturn Orbit
		- Uranus Orbit
		- Neptune Orbit
		- Sun Orbit
		- Jupiter Thunder Station
		- IO Station - Weapon Specialist
		- Ganymede Station - Shipwright
		- Europa Station - Engine Specialist
		- Callisto Station - Shield Specialist
		- Amalthea Station - Cargo Specialist
		- Himalia Station - Sensor Specialist
		- Thebe Station - Stealth Specialist
	Things that can spawn here:
		- ORION enforcers
		- Gas haulers
		- Research vessels

### - Jupiter Thunder Station
	Controlled by: ORION
	Description: Atmospheric station in Jupiter's storms. A dangerous posting that pays well for gas collection and storm data.
	Tags: Safe
	Links:
		- Jupiter Orbit
	Vendors:
		- jupiterthunder_gasshipments
			Entry dialogue: ""
    			Options:[]
		- jupiterthunder_stormdata
			Entry dialogue: ""
    			Options:[]
		- jupiterthunder_hazardpay
			Entry dialogue: ""
    			Options:[]

### - IO Station - Weapon Specialist
	Controlled by: ORION
	Description: Built on Jupiter's volcanic moon Io. The intense geothermal activity powers the Sol System's premier weapons research and manufacturing facility.
	Tags: Safe
	Links:
		- Jupiter Orbit
	Vendors:
		- io_weapon_upgrades
			Entry dialogue: ""
    			Options:[]
		- io_ballistics_expert
			Entry dialogue: ""
    			Options:[]

### - Ganymede Station - Shipwright
	Controlled by: ORION
	Description: The largest moon in the solar system hosts extensive shipyards and hull modification facilities.
	Tags: Safe
	Links:
		- Jupiter Orbit
	Vendors:
		- ganymede_shipwright
			Entry dialogue: ""
    			Options:[]
		- ganymede_hull_specialist
			Entry dialogue: ""
    			Options:[]

### - Europa Station - Engine Specialist
	Controlled by: ORION
	Description: Deep beneath Europa's ice sheets, this facility specializes in engine and propulsion system upgrades.
	Tags: Safe
	Links:
		- Jupiter Orbit
	Vendors:
		- europa_engine_upgrades
			Entry dialogue: ""
    			Options:[]
		- europa_propulsion_engineer
			Entry dialogue: ""
    			Options:[]

### - Callisto Station - Shield Specialist
	Controlled by: ORION
	Description: Far from Jupiter's radiation, Callisto Station is renowned for shield generator research and upgrades.
	Tags: Safe
	Links:
		- Jupiter Orbit
	Vendors:
		- callisto_shield_upgrades
			Entry dialogue: ""
    			Options:[]
		- callisto_energy_systems
			Entry dialogue: ""
    			Options:[]

### - Amalthea Station - Cargo Specialist
	Controlled by: ORION
	Description: A logistics hub specializing in cargo hold expansion and storage optimization systems.
	Tags: Safe
	Links:
		- Jupiter Orbit
	Vendors:
		- amalthea_cargo_upgrades
			Entry dialogue: ""
    			Options:[]
		- amalthea_storage_engineer
			Entry dialogue: ""
    			Options:[]

### - Himalia Station - Sensor Specialist
	Controlled by: ORION
	Description: An outer moon facility dedicated to sensor arrays, scanning technology, and long-range detection systems.
	Tags: Safe
	Links:
		- Jupiter Orbit
	Vendors:
		- himalia_sensor_upgrades
			Entry dialogue: ""
    			Options:[]
		- himalia_detection_specialist
			Entry dialogue: ""
    			Options:[]

### - Thebe Station - Stealth Specialist
	Controlled by: ORION
	Description: A secretive facility specializing in stealth cloaking technology and signature dampening systems.
	Tags: Safe
	Links:
		- Jupiter Orbit
	Vendors:
		- thebe_stealth_upgrades
			Entry dialogue: ""
    			Options:[]
		- thebe_cloak_specialist
			Entry dialogue: ""
    			Options:[]

### - Saturn Orbit
	Controlled by: ORION
	Description: Saturn's rings create a spectacular backdrop. The orbit is a hub for ring mining and research operations.
	Tags: Enforced
	Links:
		- Asteroid Belt Region 1
		- Asteroid Belt Region 2
		- Asteroid Belt Region 3
		- Earth Orbit
		- Mars Orbit
		- Jupiter Orbit
		- Neptune Orbit
		- Uranus Orbit
		- Saturn Ring Resource 1
		- Saturn Ring Resource 2
		- Saturn Ring Station 1
		- Saturn Ring Station 2
		- Titan Station - Elite Outfitter
		- Enceladus Station - Rare Materials Trading
		- Rhea Station - Advanced Manufacturing
	Things that can spawn here:
		- ORION enforcers
		- Research vessels
		- Ring miners

### - Saturn Ring Resource 1
	Controlled by: ORION
	Description: Ice and rock particles suspended in Saturn's rings. Harvesting requires specialized equipment.
	Tags: Patrolled
	Links:
		- Saturn Orbit
	Resources gatherable:
		- Ring materials
		- Water ice
		- Silicates

### - Saturn Ring Resource 2
	Controlled by: ORION
	Description: A denser section of the rings with higher concentrations of metallic particles.
	Tags: Patrolled
	Links:
		- Saturn Orbit
	Resources gatherable:
		- Ring materials
		- Metallic dust
		- Organic compounds

### - Saturn Ring Station 1
	Controlled by: ORION
	Description: A research station embedded in the ring system. Focuses on data collection and ship modifications.
	Tags: Safe
	Links:
		- Saturn Orbit
	Vendors:
		- saturnring1_datacollection
			Entry dialogue: ""
    			Options:[]
		- saturnring1_shipwright
			Entry dialogue: ""
    			Options:[]

### - Saturn Ring Station 2
	Controlled by: ORION
	Description: Sister station to Ring Station 1. Offers similar services with a focus on long-range scanning equipment.
	Tags: Safe
	Links:
		- Saturn Orbit
	Vendors:
		- saturnring2_datacollection
			Entry dialogue: ""
    			Options:[]
		- saturnring2_shipwright
			Entry dialogue: ""
    			Options:[]
		- saturnring2_scanningtech
			Entry dialogue: ""
    			Options:[]

### - Titan Station - Elite Outfitter
	Controlled by: ORION
	Description: Saturn's largest moon hosts the most prestigious ship outfitting facility in the outer system. Only the finest equipment.
	Tags: Safe
	Links:
		- Saturn Orbit
	Vendors:
		- titan_elite_weapons
			Entry dialogue: ""
    			Options:[]
		- titan_elite_defense
			Entry dialogue: ""
    			Options:[]
		- titan_premium_outfitter
			Entry dialogue: ""
    			Options:[]

### - Enceladus Station - Rare Materials Trading
	Controlled by: ORION
	Description: Built above the geysers of Enceladus, this station is the premier exchange for rare materials and exotic compounds.
	Tags: Safe
	Links:
		- Saturn Orbit
	Vendors:
		- enceladus_rare_materials
			Entry dialogue: ""
    			Options:[]
		- enceladus_exotic_trader
			Entry dialogue: ""
    			Options:[]
		- enceladus_material_exchange
			Entry dialogue: ""
    			Options:[]

### - Rhea Station - Advanced Manufacturing
	Controlled by: ORION
	Description: A cutting-edge fabrication facility producing top-tier ship components and experimental technology.
	Tags: Safe
	Links:
		- Saturn Orbit
	Vendors:
		- rhea_advanced_manufacturing
			Entry dialogue: ""
    			Options:[]
		- rhea_prototype_components
			Entry dialogue: ""
    			Options:[]
		- rhea_experimental_tech
			Entry dialogue: ""
    			Options:[]

### - Uranus Orbit
	Controlled by: ORION
	Description: The ice giant rotates on its side, creating unique atmospheric phenomena. A remote but profitable posting.
	Tags: Enforced
	Links:
		- Neptune Orbit
		- Jupiter Orbit
		- Saturn Orbit
		- Asteroid Belt Region 1
		- Asteroid Belt Region 2
		- Asteroid Belt Region 3
		- Uranus Atmo Station
		- Titania Station - Data Archive
		- Oberon Station - Sample Repository
	Things that can spawn here:
		- ORION enforcers
		- Gas haulers

### - Uranus Atmo Station
	Controlled by: ORION
	Description: An atmospheric processing station harvesting rare gases from Uranus's atmosphere.
	Tags: Safe
	Links:
		- Uranus Orbit
	Vendors:
		- uranusatmo_gasharvesting
			Entry dialogue: ""
    			Options:[]
		- uranusatmo_raregases
			Entry dialogue: ""
    			Options:[]

### - Titania Station - Data Archive
	Controlled by: ORION
	Description: A massive data archive seeking information from every corner of the Sol System. Pays well for scan data, research, and discoveries.
	Tags: Safe
	Links:
		- Uranus Orbit
	Vendors:
		- titania_data_collector
			Entry dialogue: ""
    			Options:[]
		- titania_research_buyer
			Entry dialogue: ""
    			Options:[]
		- titania_exploration_records
			Entry dialogue: ""
    			Options:[]

### - Oberon Station - Sample Repository
	Controlled by: ORION
	Description: A scientific facility collecting physical samples from across Sol. Seeks minerals, gases, ice, and organic materials.
	Tags: Safe
	Links:
		- Uranus Orbit
	Vendors:
		- oberon_sample_collector
			Entry dialogue: ""
    			Options:[]
		- oberon_material_analyst
			Entry dialogue: ""
    			Options:[]
		- oberon_specimen_buyer
			Entry dialogue: ""
    			Options:[]

### - Neptune Orbit
	Controlled by: ORION
	Description: The furthest major planet from the sun. Neptune Orbit serves as the gateway to the Kuiper Belt.
	Tags: Enforced
	Links:
		- Saturn Orbit
		- Uranus Orbit
		- Asteroid Belt Region 1
		- Asteroid Belt Region 2
		- Asteroid Belt Region 3
		- Kuiper Region 1
		- Kuiper Region 2
		- Kuiper Region 3
		- Kuiper Region 4
		- Neptune Orbital Station
		- Triton Station - Cartography Center
		- Nereid Station - Frontier Research
	Things that can spawn here:
		- ORION enforcers
		- Frontier transports
		- Ice prospectors

### - Neptune Orbital Station
	Controlled by: ORION
	Description: The last major outpost before the Kuiper Belt. A waystation for explorers and prospectors heading into the outer system.
	Tags: Safe
	Links:
		- Neptune Orbit
	Vendors:
		- neptuneorbital_explorer_supplies
			Entry dialogue: ""
    			Options:[]
		- neptuneorbital_deepspace_outfitter
			Entry dialogue: ""
    			Options:[]

### - Triton Station - Cartography Center
	Controlled by: ORION
	Description: The Sol System's premier mapping facility. Purchases navigation data, system charts, and location discoveries from across all regions.
	Tags: Safe
	Links:
		- Neptune Orbit
	Vendors:
		- triton_cartographer
			Entry dialogue: ""
    			Options:[]
		- triton_navigation_data_buyer
			Entry dialogue: ""
    			Options:[]
		- triton_stellar_mapping
			Entry dialogue: ""
    			Options:[]

### - Nereid Station - Frontier Research
	Controlled by: ORION
	Description: An isolated research outpost seeking materials and data from the most remote locations in Sol. The further out, the better they pay.
	Tags: Safe
	Links:
		- Neptune Orbit
	Vendors:
		- nereid_frontier_researcher
			Entry dialogue: ""
    			Options:[]
		- nereid_remote_samples
			Entry dialogue: ""
    			Options:[]
		- nereid_deep_space_data
			Entry dialogue: ""
    			Options:[]

### - Kuiper Region 1
	Controlled by: ORION
	Description: The inner edge of the Kuiper Belt. Icy bodies drift in the darkness, rich with rare materials.
	Tags: Patrolled
	Links:
		- KR1 Resource 1
		- KR1 Resource 2
		- KR1 Resource 3
		- KR1 Resource 4
		- Kuiper Region 1 Station
		- Neptune Orbit
		- Kuiper Region 2
	Things that can spawn here:
		- ORION patrol ships
		- Exploration drones
		- Ice prospectors

### - KR1 Resource 1
	Controlled by: ORION
	Description: A frozen dwarf planet with exposed ice deposits. Rich in rare volatiles.
	Tags: Dangerous
	Links:
		- Kuiper Region 1
	Resources gatherable:
		- Rare ice samples
		- Frozen volatiles
		- Methane ice

### - KR1 Resource 2
	Controlled by: ORION
	Description: A cluster of icy cometary bodies with pristine samples from the early solar system.
	Tags: Dangerous
	Links:
		- Kuiper Region 1
	Resources gatherable:
		- Rare ice samples
		- Primordial ices
		- Deuterium

### - KR1 Resource 3
	Controlled by: ORION
	Description: A large trans-Neptunian object with subsurface water ice and organic compounds.
	Tags: Dangerous
	Links:
		- Kuiper Region 1
	Resources gatherable:
		- Rare ice samples
		- Water ice
		- Organic materials

### - KR1 Resource 4
	Controlled by: ORION
	Description: An isolated ice field far from patrol routes. High risk, high reward.
	Tags: Dangerous
	Links:
		- Kuiper Region 1
	Resources gatherable:
		- Rare ice samples
		- Exotic ices
		- Heavy water

### - Kuiper Region 1 Station
	Controlled by: ORION
	Description: A remote outpost for ice traders and prospectors. The last safe harbor before venturing deeper into the belt.
	Tags: Safe
	Links:
		- Kuiper Region 1
	Vendors:
		- kr1station_icegathering
			Entry dialogue: ""
    			Options:[]
		- kr1station_icetrader
			Entry dialogue: ""
    			Options:[]
		- kr1station_coldweather_gear
			Entry dialogue: ""
    			Options:[]

### - Kuiper Region 2
	Controlled by: ORION
	Description: Deeper into the Kuiper Belt. ORION patrols are infrequent, and pirate activity increases.
	Tags: Dangerous
	Links:
		- KR2 Resource 1
		- KR2 Resource 2
		- KR2 Resource 3
		- KR2 Resource 4
		- Kuiper Region 2 Station
		- Kuiper Region 1
		- Kuiper Region 3
		- Neptune Orbit
	Things that can spawn here:
		- Ice pirates
		- Pirate scouts
		- Rogue prospectors

### - KR2 Resource 1
	Controlled by: ORION
	Description: A binary system of icy planetoids orbiting each other in the void.
	Tags: Dangerous
	Links:
		- Kuiper Region 2
	Resources gatherable:
		- Rare ice samples
		- Nitrogen ice
		- Ammonia ice

### - KR2 Resource 2
	Controlled by: ORION
	Description: A shattered comet with exposed interior materials. Extremely valuable for research.
	Tags: Dangerous
	Links:
		- Kuiper Region 2
	Resources gatherable:
		- Rare ice samples
		- Comet fragments
		- Pristine volatiles

### - KR2 Resource 3
	Controlled by: ORION
	Description: A rogue planetoid that drifted into the Kuiper Belt from elsewhere in the galaxy.
	Tags: Dangerous
	Links:
		- Kuiper Region 2
	Resources gatherable:
		- Rare ice samples
		- Exotic materials
		- Interstellar dust

### - KR2 Resource 4
	Controlled by: ORION
	Description: An ice field rich with deuterium and tritium. Perfect for fusion fuel production.
	Tags: Dangerous
	Links:
		- Kuiper Region 2
	Resources gatherable:
		- Rare ice samples
		- Deuterium
		- Tritium

### - Kuiper Region 2 Station
	Controlled by: ORION
	Description: A barely-maintained outpost run by independent operators. ORION presence is minimal.
	Tags: Safe
	Links:
		- Kuiper Region 2
	Vendors:
		- kr2station_independenttrader
			Entry dialogue: ""
    			Options:[]
		- kr2station_fuelprocessing
			Entry dialogue: ""
    			Options:[]
		- kr2station_blackmarket
			Entry dialogue: ""
    			Options:[]

### - Kuiper Region 3
	Controlled by: ORION
	Description: Far beyond Neptune's influence. This region is lawless and dangerous.
	Tags: Dangerous
	Links:
		- KR3 Resource 1
		- KR3 Resource 2
		- KR3 Resource 3
		- KR3 Resource 4
		- Kuiper Region 3 Station
		- Kuiper Region 2
		- Kuiper Region 4
		- Neptune Orbit
	Things that can spawn here:
		- Pirate fleets
		- Rogue miners
		- Outlaws

### - KR3 Resource 1
	Controlled by: ORION
	Description: A field of ancient ice fragments from the formation of the solar system.
	Tags: Dangerous
	Links:
		- Kuiper Region 3
	Resources gatherable:
		- Rare ice samples
		- Ancient ices
		- Primordial materials

### - KR3 Resource 2
	Controlled by: ORION
	Description: A massive ice moon ejected from Neptune's orbit eons ago.
	Tags: Dangerous
	Links:
		- Kuiper Region 3
	Resources gatherable:
		- Rare ice samples
		- Deep ice cores
		- Xenon ice

### - KR3 Resource 3
	Controlled by: ORION
	Description: A debris field from a shattered dwarf planet. Rich in metallic ices.
	Tags: Dangerous
	Links:
		- Kuiper Region 3
	Resources gatherable:
		- Rare ice samples
		- Metallic ices
		- Iron ice compounds

### - KR3 Resource 4
	Controlled by: ORION
	Description: An uncharted ice field discovered by prospectors. Potentially the richest deposit in the belt.
	Tags: Dangerous
	Links:
		- Kuiper Region 3
	Resources gatherable:
		- Rare ice samples
		- Exotic volatiles
		- Crystalline ices

### - Kuiper Region 3 Station
	Controlled by: ORION
	Description: A pirate haven disguised as a legitimate trading post. ORION has no authority here.
	Tags: Safe
	Links:
		- Kuiper Region 3
	Vendors:
		- kr3station_fencedgoods
			Entry dialogue: ""
    			Options:[]
		- kr3station_piratequartermaster
			Entry dialogue: ""
    			Options:[]
		- kr3station_shady_shipwright
			Entry dialogue: ""
    			Options:[]

### - Kuiper Region 4
	Controlled by: ORION
	Description: The outermost reaches of the Kuiper Belt, bordering the Oort Cloud. No patrols, no laws.
	Tags: Dangerous
	Links:
		- KR4 Resource 1
		- KR4 Resource 2
		- KR4 Resource 3
		- KR4 Resource 4
		- Kuiper Region 4 Station
		- Kuiper Region 3
		- Neptune Orbit
	Things that can spawn here:
		- Pirate fleets
		- Outlaws
		- Unknown entities

### - KR4 Resource 1
	Controlled by: ORION
	Description: A lonely ice dwarf at the edge of the solar system. Few dare to venture this far.
	Tags: Dangerous
	Links:
		- Kuiper Region 4
	Resources gatherable:
		- Rare ice samples
		- Helium-3
		- Dark matter traces

### - KR4 Resource 2
	Controlled by: ORION
	Description: A field of proto-comets waiting to fall toward the sun. Millions of years of potential.
	Tags: Dangerous
	Links:
		- Kuiper Region 4
	Resources gatherable:
		- Rare ice samples
		- Proto-comet materials
		- Primordial volatiles

### - KR4 Resource 3
	Controlled by: ORION
	Description: An anomalous ice formation that defies conventional physics. Origin unknown.
	Tags: Dangerous
	Links:
		- Kuiper Region 4
	Resources gatherable:
		- Rare ice samples
		- Anomalous materials
		- Unknown compounds

### - KR4 Resource 4
	Controlled by: ORION
	Description: The furthest confirmed resource point in the Sol System. Only the bravest or most desperate come here.
	Tags: Dangerous
	Links:
		- Kuiper Region 4
	Resources gatherable:
		- Rare ice samples
		- Ultra-rare volatiles
		- Oort Cloud fragments

### - Kuiper Region 4 Station
	Controlled by: ORION
	Description: A mysterious station at the edge of known space. Rumors say it's run by exiles and outcasts.
	Tags: Safe
	Links:
		- Kuiper Region 4
	Vendors:
		- kr4station_exile_trader
			Entry dialogue: ""
    			Options:[]
		- kr4station_frontier_supplies
			Entry dialogue: ""
    			Options:[]
		- kr4station_mysterious_vendor
			Entry dialogue: ""
    			Options:[]

---

## LOCATION SUMMARY

**Inner System (Safe/Enforced):**
- Earth Orbit, Moon Orbit, Sun Orbit, Mercury Orbit, Venus Orbit, Mars Orbit

**Inner System Stations (Safe):**
- Earth Orbital Station Zero, Moon Ground Station, Earth Ground Station Zero
- Mercury Ground Station, Venus Orbital Station, Venus Ground Station
- Mars Ground Station, Mars Orbital Station, Mars Moon 1 Ground Station, Mars Moon 2 Ground Station
- SOL Warp Gates (Enforced but has vendors)

**Asteroid Belt (Patrolled):**
- 3 Belt Regions (ABR1, ABR2, ABR3)
- 6 Resource nodes (2 per region)
- 3 Belt Stations

**Jupiter System (Enforced):**
- Jupiter Orbit, Jupiter Thunder Station
- 7 Component Specialist Moon Stations:
  - IO (Weapon), Ganymede (Shipwright/Hull), Europa (Engine), Callisto (Shield)
  - Amalthea (Cargo), Himalia (Sensor), Thebe (Stealth)

**Saturn System (Patrolled/Enforced):**
- Saturn Orbit, 2 Ring Resources, 2 Ring Stations
- 3 Elite Moon Stations:
  - Titan (Elite Outfitter), Enceladus (Rare Materials), Rhea (Advanced Manufacturing)

**Uranus System (Enforced):**
- Uranus Orbit, Uranus Atmo Station
- 2 Collection Moon Stations:
  - Titania (Data Archive), Oberon (Sample Repository)

**Neptune System (Enforced):**
- Neptune Orbit, Neptune Orbital Station
- 2 Research Moon Stations:
  - Triton (Cartography Center), Nereid (Frontier Research)

**Kuiper Belt (Dangerous/Patrolled):**
- 4 Kuiper Regions (KR1, KR2, KR3, KR4)
- 16 Resource nodes (4 per region)
- 4 Kuiper Stations

**Total Locations:** 110

---

## VENDOR SUMMARY

**Total Vendors:** 105

**By Category:**
- Component Specialists (Jupiter moons): 14
- Elite Equipment (Saturn moons): 9
- Data/Research Collectors (Uranus/Neptune moons): 12
- Shipwrights: 10
- Traders/General: 8
- Weapons/Military: 7
- Gas/Fuel Operations: 6
- Ice/Resource Trading: 8
- Black Market/Illicit: 5
- Repair/Maintenance: 2
- Mining/Exploration Support: 6
- Specialized Services: 18

---

## NOTES

- All vendor dialogue arrays are empty and ready to be populated
- All resource nodes have specific gatherable materials listed
- Station descriptions provide thematic context for vendors
- Kuiper Belt progression shows increasing lawlessness from KR1 to KR4
- SOL Warp Gates added as interstellar connection point

### Spawn Distribution Philosophy:
- **SOL is a safe, civilized system** - ORION maintains strong control
- **Enforced zones** (all planetary orbits): ORION enforcers + civilian traffic
- **Patrolled zones** (Asteroid Belt, Saturn Rings, KR1): ORION patrols + miners/explorers
- **Dangerous zones** (KR2, KR3, KR4): Pirates and outlaws - the lawless frontier
- **No smugglers in SOL** - smuggling belongs in less controlled systems
- Players wanting PvP combat in SOL should head to the Kuiper Belt regions

### Outer System Station Design:
- **Jupiter Moons (7 stations)**: Each specializes in ONE major ship component
  - IO: Weapons - geothermal-powered weapons research
  - Ganymede: Shipwright/Hull - largest moon, largest shipyards
  - Europa: Engine - beneath the ice, propulsion specialists
  - Callisto: Shield - far from radiation, shield research
  - Amalthea: Cargo - logistics and storage optimization
  - Himalia: Sensor - outer moon, long-range detection
  - Thebe: Stealth - cloaking and signature dampening
- **Saturn Moons (3 stations)**: Elite equipment and top-tier items
  - Titan: Elite weapons and defense systems
  - Enceladus: Rare materials trading hub
  - Rhea: Advanced manufacturing and prototypes
- **Uranus Moons (2 stations)**: Data and sample collection hubs
  - Titania: Pays for scan data, research, discoveries from anywhere in Sol
  - Oberon: Buys physical samples (minerals, gases, ice, organics)
- **Neptune Moons (2 stations)**: Frontier research and mapping
  - Triton: Cartography center, buys navigation data and system charts
  - Nereid: Frontier research, pays MORE for materials from remote locations
