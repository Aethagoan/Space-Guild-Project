# Aidan Orion 25 Feb 2026
# World setup script - Creates initial game world with locations and links

import os
import json
from data import DataHandler
from location import Location


def prompt_overwrite(data_dir: str) -> bool:
    """Prompt user before overwriting existing world data.
    
    Args:
        data_dir: Path to game data directory
        
    Returns:
        True if user wants to proceed, False otherwise
    """
    # Check if any data files exist
    files_to_check = ['locations.json', 'ships.json', 'items.json', 'players.json', 'factions.json']
    existing_files = [f for f in files_to_check if os.path.exists(os.path.join(data_dir, f))]
    
    if not existing_files:
        return True  # No existing data, proceed
    
    print(f"\n[!] Warning: The following data files already exist in '{data_dir}':")
    for f in existing_files:
        print(f"  - {f}")
    
    response = input("\nOverwrite existing world data? (yes/no): ").strip().lower()
    return response in ['yes', 'y']

def setup_world(data_dir: str = "game_data", force: bool = False):
    """Set up the game world with locations and links.
    
    Args:
        data_dir: Directory to store game data
        force: Skip user confirmation prompt if True
        
    Returns:
        DataHandler instance with all locations, links, and vendors created
    """
    print("=" * 70)
    print("SPACE GUILD - WORLD SETUP")
    print("=" * 70)
    
    # Check for existing data and prompt user
    if not force and not prompt_overwrite(data_dir):
        print("\n[X] Setup cancelled by user.")
        return
    
    print("\n[*] Initializing world...")
    
    # Create DataHandler
    data_handler = DataHandler(data_dir=data_dir)
    
    # Get location data
    location_metadata = create_world_locations()
    bidirectional_links, single_links = create_world_links()
    vendor_data = create_vendor_dialogue()
    
    print(f"\n[*] Creating {len(location_metadata)} locations...")
    
    # Create all locations with their metadata
    for location_name, metadata in location_metadata.items():
        data_handler.add_location(
            location_name,
            location_type=metadata.get('type', 'space'),
            controlled_by=metadata.get('controlled_by', 'ORION'),
            description=metadata.get('description', ''),
            tags=metadata.get('tags', []),
            spawnable_ids=metadata.get('spawnable_ids', []),
            resource_node_ids=metadata.get('resource_node_ids', [])
        )
        print(f"  [+] Created: {location_name} ({metadata.get('type', 'space')})")
    
    # Create bidirectional links
    print(f"\n[*] Creating {len(bidirectional_links)} bidirectional links...")
    for loc1, loc2 in bidirectional_links:
        data_handler.double_link_locations(loc1, loc2)
        print(f"  [+] Linked: {loc1} <-> {loc2}")
    
    # Create single-directional links
    if single_links:
        print(f"\n[*] Creating {len(single_links)} one-way links...")
        for source, dest, _ in single_links:
            data_handler.single_link_locations(source, dest)
            print(f"  [+] One-way: {source} -> {dest}")
    
    # Save vendor dialogue data separately (station-based structure)
    vendor_file = os.path.join(data_dir, "vendor_dialogue.json")
    print(f"\n[*] Saving vendor dialogue to {vendor_file}...")
    
    # Count total vendors across all stations
    total_vendors = sum(len(vendors) for vendors in vendor_data.values())
    
    with open(vendor_file, 'w') as f:
        json.dump(vendor_data, f, indent=2)
    print(f"  [+] Created {total_vendors} vendors across {len(vendor_data)} stations")
    
    # Save all location data
    print(f"\n[*] Saving world data...")
    data_handler.save_all()
    
    print("\n" + "=" * 70)
    print("[+] WORLD SETUP COMPLETE")
    print("=" * 70)
    print(f"\nLocations created: {len(location_metadata)}")
    print(f"Stations with vendors: {len(vendor_data)}")
    print(f"Total vendors: {total_vendors}")
    print(f"Total connections: {len(bidirectional_links) * 2 + len(single_links)}")
    print(f"\nData saved to: {data_dir}/")
    print("\n[*] World is ready for game loop startup!")
    
    return data_handler

if __name__ == '__main__':
    # Run setup
    setup_world()

def create_world_locations():
    """Create all world locations based on sol_system.md.
    
    Returns:
        Dict of location_name -> location_metadata
    """
    locations = {
        # ============================================================================
        # INNER SYSTEM - EARTH
        # ============================================================================
        'Earth_Orbit': {
            'type': 'space',
            'controlled_by': 'ORION',
            'description': 'The place players start, floating just above the blue marble.',
            'tags': ['Safe'],
            'spawnable_ids': ['orion_enforcers', 'trade_vessels'],
        },
        'Earth_Orbital_Station_Zero': {
            'type': 'station',
            'controlled_by': 'ORION',
            'description': 'The orbital Station above earth, a full ring around the earth.',
            'tags': ['Safe'],
        },
        'Earth_Ground_Station_Zero': {
            'type': 'ground_station',
            'controlled_by': 'ORION',
            'description': "The planetary headquarters of ORION, located at the equator. A sprawling complex of hangars and trading posts.",
            'tags': ['Safe'],
        },
        
        # ============================================================================
        # INNER SYSTEM - MOON
        # ============================================================================
        'Moon_Orbit': {
            'type': 'space',
            'controlled_by': 'ORION',
            'description': "Earth's Moon looms large. Ancient landing sites are visible on the surface below.",
            'tags': ['Enforced'],
            'spawnable_ids': ['orion_enforcers', 'tourist_vessels'],
        },
        'Moon_Ground_Station': {
            'type': 'ground_station',
            'controlled_by': 'ORION',
            'description': "Humanity's first extraterrestrial colony. Now a museum and trading post for historical artifacts.",
            'tags': ['Safe'],
        },
        
        # ============================================================================
        # INNER SYSTEM - SUN
        # ============================================================================
        'Sun_Orbit': {
            'type': 'space',
            'controlled_by': 'ORION',
            'description': 'The heart of the Sol System. Extreme heat and radiation make this a challenging navigation point.',
            'tags': ['Enforced'],
            'spawnable_ids': ['orion_enforcers', 'solar_research_vessels'],
        },
        'SOL_Warp_Gates': {
            'type': 'station',
            'controlled_by': 'ORION',
            'description': 'Massive warp gate structures that connect the Sol System to distant star systems. Heavily guarded and monitored.',
            'tags': ['Enforced'],
            'spawnable_ids': ['orion_enforcers', 'customs_inspectors'],
        },
        
        # ============================================================================
        # INNER SYSTEM - MERCURY
        # ============================================================================
        'Mercury_Orbit': {
            'type': 'space',
            'controlled_by': 'ORION',
            'description': "Close to the sun, Mercury's orbit is searing hot. The planet below is pockmarked with mining operations.",
            'tags': ['Enforced'],
            'spawnable_ids': ['orion_enforcers', 'mining_transports'],
        },
        'Mercury_Ground_Station': {
            'type': 'ground_station',
            'controlled_by': 'ORION',
            'description': "A heavily shielded facility on Mercury's surface, specializing in heat-resistant components and bounty hunting operations.",
            'tags': ['Safe'],
        },
        
        # ============================================================================
        # INNER SYSTEM - VENUS
        # ============================================================================
        'Venus_Orbit': {
            'type': 'space',
            'controlled_by': 'ORION',
            'description': 'Venus hangs below, a toxic planet shrouded in acidic clouds. The orbital station is a hub for black market activity.',
            'tags': ['Enforced'],
            'spawnable_ids': ['orion_enforcers', 'trade_vessels'],
        },
        'Venus_Ground_Station': {
            'type': 'ground_station',
            'controlled_by': 'ORION',
            'description': "A fortified dome facility on Venus's surface. Known for illicit dealings and untraceable goods.",
            'tags': ['Safe'],
        },
        'Venus_Orbital_Station': {
            'type': 'station',
            'controlled_by': 'ORION',
            'description': 'An aging orbital platform with questionable security. Traders and smugglers frequent the docks.',
            'tags': ['Safe'],
        },
        
        # ============================================================================
        # INNER SYSTEM - MARS
        # ============================================================================
        'Mars_Orbit': {
            'type': 'space',
            'controlled_by': 'ORION',
            'description': 'The red planet below is dotted with terraforming projects. Mars Orbit serves as a major military and trade hub.',
            'tags': ['Enforced'],
            'spawnable_ids': ['orion_enforcers', 'military_transports', 'colonial_vessels'],
        },
        'Mars_Ground_Station': {
            'type': 'ground_station',
            'controlled_by': 'ORION',
            'description': 'Built into the Martian surface, this station is a center for colonial operations and ship manufacturing.',
            'tags': ['Safe'],
        },
        'Mars_Orbital_Station': {
            'type': 'station',
            'controlled_by': 'ORION',
            'description': 'The largest orbital facility around Mars, equipped with advanced shipyards and defensive systems.',
            'tags': ['Safe'],
        },
        'Mars_Moon_1_Ground_Station': {
            'type': 'ground_station',
            'controlled_by': 'ORION',
            'description': "Phobos Station - A weapons depot built into the moon's interior. Heavily armed and fortified.",
            'tags': ['Safe'],
        },
        'Mars_Moon_2_Ground_Station': {
            'type': 'ground_station',
            'controlled_by': 'ORION',
            'description': 'Deimos Station - A secretive research facility specializing in stealth technology and cloaking devices.',
            'tags': ['Safe'],
        },
        
        # ============================================================================
        # ASTEROID BELT REGION 1
        # ============================================================================
        'Asteroid_Belt_Region_1': {
            'type': 'space',
            'controlled_by': 'ORION',
            'description': 'The Inner belt region.',
            'tags': ['Patrolled'],
            'spawnable_ids': ['orion_patrol_ships', 'mining_drones', 'independent_miners'],
        },
        'ABR1_Resource_1': {
            'type': 'resource_node',
            'controlled_by': 'ORION',
            'description': 'Asteroids with iron and nickel.',
            'tags': ['Patrolled'],
            'resource_node_ids': ['iron', 'nickel'],
        },
        'ABR1_Resource_2': {
            'type': 'resource_node',
            'controlled_by': 'ORION',
            'description': 'Sensors have found platinum in the area.',
            'tags': ['Patrolled'],
            'resource_node_ids': ['platinum'],
        },
        'ABR1_Space_Station': {
            'type': 'station',
            'controlled_by': 'ORION',
            'description': 'Logs show encrypt coming in and out of this station frequently.',
            'tags': ['Safe'],
        },
        
        # ============================================================================
        # ASTEROID BELT REGION 2
        # ============================================================================
        'Asteroid_Belt_Region_2': {
            'type': 'space',
            'controlled_by': 'ORION',
            'description': 'The central belt region.',
            'tags': ['Patrolled'],
            'spawnable_ids': ['orion_patrol_ships', 'mining_drones', 'independent_miners'],
        },
        'ABR2_Resource_1': {
            'type': 'resource_node',
            'controlled_by': 'ORION',
            'description': 'Sensors show high carbon density here.',
            'tags': ['Patrolled'],
            'resource_node_ids': ['carbon'],
        },
        'ABR2_Resource_2': {
            'type': 'resource_node',
            'controlled_by': 'ORION',
            'description': 'Sensors indicate metal rich asteroids.',
            'tags': ['Patrolled'],
            'resource_node_ids': ['iron', 'titanium', 'nickel']
        },
        'ABR2_Space_Station': {
            'type': 'station',
            'controlled_by': 'ORION',
            'description': 'Logs indicate ORION enforcers often pass through this station.',
            'tags': ['Safe'],
        },
        
        # ============================================================================
        # ASTEROID BELT REGION 3
        # ============================================================================
        'Asteroid_Belt_Region_3': {
            'type': 'space',
            'controlled_by': 'ORION',
            'description': "The outer belt region.",
            'tags': ['Patrolled'],
            'spawnable_ids': ['orion_patrol_ships', 'mining_drones', 'salvage_vessels'],
        },
        'ABR3_Resource_1': {
            'type': 'resource_node',
            'controlled_by': 'ORION',
            'description': 'A silicate asteroid group with rare mineral deposits.',
            'tags': ['Patrolled'],
            'resource_node_ids': ['silicon', 'rare_minerals'],
        },
        'ABR3_Resource_2': {
            'type': 'resource_node',
            'controlled_by': 'ORION',
            'description': 'An asteroid field with scattered chunks of platinum and iridium.',
            'tags': ['Patrolled'],
            'resource_node_ids': ['platinum', 'iridium'],
        },
        'ABR3_Space_Station': {
            'type': 'station',
            'controlled_by': 'ORION',
            'description': 'A trading station specializing in mining explosives.',
            'tags': ['Safe'],
        },
        
        # ============================================================================
        # JUPITER SYSTEM
        # ============================================================================
        'Jupiter_Orbit': {
            'type': 'space',
            'controlled_by': 'ORION',
            'description': 'History records indicate Jupiter became ORION\'s foothold once they started facing outside threats. Many moons sell some of the best equipment you can get for several systems.',
            'tags': ['Enforced'],
            'spawnable_ids': ['orion_enforcers', 'gas_haulers', 'research_vessels'],
        },
        'Jupiter_Thunder_Station': {
            'type': 'station',
            'controlled_by': 'ORION',
            'description': 'A city floating on Jupiter\'s storms.',
            'tags': ['Safe'],
        },
        'IO_Station_Weapon_Specialist': {
            'type': 'ground_station',
            'controlled_by': 'ORION',
            'description': 'The Sol System\'s premier weapons research and manufacturing facility.',
            'tags': ['Safe'],
        },
        'Ganymede_Station_Shipwright': {
            'type': 'ground_station',
            'controlled_by': 'ORION',
            'description': 'Shipyards for miles and hull modification facilities.',
            'tags': ['Safe'],
        },
        'Europa_Station_Engine_Specialist': {
            'type': 'ground_station',
            'controlled_by': 'ORION',
            'description': 'A facility selling tried and tested booster tech, need an engine in Sol? You\'re in the right place',
            'tags': ['Safe'],
        },
        'Callisto_Station_Shield_Specialist': {
            'type': 'ground_station',
            'controlled_by': 'ORION',
            'description': "A facility who is renowned for creating superior shields.",
            'tags': ['Safe'],
        },
        'Amalthea_Station_Cargo_Specialist': {
            'type': 'ground_station',
            'controlled_by': 'ORION',
            'description': 'A logistics hub specializing in storage systems.',
            'tags': ['Safe'],
        },
        'Himalia_Station_Sensor_Specialist': {
            'type': 'ground_station',
            'controlled_by': 'ORION',
            'description': 'An facility dedicated to sensors and scanning technology.',
            'tags': ['Safe'],
        },
        'Thebe_Station_Stealth_Specialist': {
            'type': 'ground_station',
            'controlled_by': 'ORION',
            'description': 'A facility specializing in stealth cloaking technology.',
            'tags': ['Safe'],
        },
        
        # ============================================================================
        # SATURN SYSTEM
        # ============================================================================
        'Saturn_Orbit': {
            'type': 'space',
            'controlled_by': 'ORION',
            'description': 'Saturn. Some ancient species named this after their god of time.',
            'tags': ['Enforced'],
            'spawnable_ids': ['orion_enforcers', 'research_vessels', 'ring_miners'],
        },
        'Saturn_Ring_Resource_1': {
            'type': 'resource_node',
            'controlled_by': 'ORION',
            'description': "Rock particles suspended in Saturn's rings.",
            'tags': ['Patrolled'],
            'resource_node_ids': ['ring_materials', 'silicates'],
        },
        'Saturn_Ring_Resource_2': {
            'type': 'resource_node',
            'controlled_by': 'ORION',
            'description': 'Sensors indicate metalic particles.',
            'tags': ['Patrolled'],
            'resource_node_ids': ['ring_materials', 'metallic_dust', 'organic_compounds'],
        },
        'Saturn_Ring_Station_1': {
            'type': 'station',
            'controlled_by': 'ORION',
            'description': 'A research station in the rings of Saturn. Focuses on data collection of the rings.',
            'tags': ['Safe'],
        },
        'Saturn_Ring_Station_2': {
            'type': 'station',
            'controlled_by': 'ORION',
            'description': 'Offers similar services to Ring Station 1 with a focus on long-range scanning equipment.',
            'tags': ['Safe'],
        },
        'Titan_Station': {
            'type': 'ground_station',
            'controlled_by': 'ORION',
            'description': 'Logs indicate core mining of this moon.',
            'tags': ['Safe'],
        },
        'Enceladus_Station_Rare_Materials_Trading': {
            'type': 'ground_station',
            'controlled_by': 'ORION',
            'description': 'Logs indicate that rare materials come in and out of this place at astonishing rates.',
            'tags': ['Safe'],
        },
        'Rhea_Station_Advanced_Manufacturing': {
            'type': 'ground_station',
            'controlled_by': 'ORION',
            'description': 'A fabrication facility producing good components.',
            'tags': ['Safe'],
        },
        
        # ============================================================================
        # URANUS SYSTEM
        # ============================================================================
        'Uranus_Orbit': {
            'type': 'space',
            'controlled_by': 'ORION',
            'description': 'Uranus. Some call it sideways, but there\'s no \'up\' in space.',
            'tags': ['Enforced'],
            'spawnable_ids': ['orion_enforcers', 'gas_haulers'],
        },
        'Uranus_Atmo_Station': {
            'type': 'station',
            'controlled_by': 'ORION',
            'description': 'The floating city on Uranus. Yes, we get it, you\'re very funny.',
            'tags': ['Safe'],
        },
        'Titania_Station_Data_Archive': {
            'type': 'ground_station',
            'controlled_by': 'ORION',
            'description': 'A massive data archive seeking information from every corner of the Sol System. Pays well for scan data.',
            'tags': ['Safe'],
        },
        'Oberon_Station_Sample_Repository': {
            'type': 'ground_station',
            'controlled_by': 'ORION',
            'description': 'A scientific facility samples from across Sol. Seeks minerals, gases, and organic materials.',
            'tags': ['Safe'],
        },
        
        # ============================================================================
        # NEPTUNE SYSTEM
        # ============================================================================
        'Neptune_Orbit': {
            'type': 'space',
            'controlled_by': 'ORION',
            'description': 'Neptune. The furthest planet in Sol\'s grasp.',
            'tags': ['Enforced'],
            'spawnable_ids': ['orion_enforcers', 'frontier_transports', 'ice_prospectors'],
        },
        'Neptune_Orbital_Station': {
            'type': 'station',
            'controlled_by': 'ORION',
            'description': 'Logs indicate this station is mostly used as a last-stop before the Kuiper belt.',
            'tags': ['Safe'],
        },
        'Triton_Station_Cartography_Center': {
            'type': 'station',
            'controlled_by': 'ORION',
            'description': "A data center filled to capacity with navigation data.",
            'tags': ['Safe'],
        },
        'Nereid_Station_Frontier_Research': {
            'type': 'station',
            'controlled_by': 'ORION',
            'description': 'An isolated research outpost seeking materials and data from the most remote locations in Sol.',
            'tags': ['Safe'],
        },
        
        # ============================================================================
        # KUIPER BELT REGION 1
        # ============================================================================
        'Kuiper_Region_1': {
            'type': 'space',
            'controlled_by': 'ORION',
            'description': 'The kuiper belt. You probably came here for ice, because there really isn\'t much else.',
            'tags': ['Patrolled'],
            'spawnable_ids': ['orion_patrol_ships', 'exploration_drones', 'ice_prospectors'],
        },
        'KR1_Resource_1': {
            'type': 'resource_node',
            'controlled_by': 'ORION',
            'description': 'Sensors found methane ice.',
            'tags': ['Dangerous'],
            'resource_node_ids': ['rare_ice_samples', 'methane_ice'],
        },
        'KR1_Resource_2': {
            'type': 'resource_node',
            'controlled_by': 'ORION',
            'description': 'Nothing but old ice.',
            'tags': ['Dangerous'],
            'resource_node_ids': ['rare_ice_samples', 'primordial_ices'],
        },
        'KR1_Resource_3': {
            'type': 'resource_node',
            'controlled_by': 'ORION',
            'description': 'Sensors indicate water ice and organic materials. How did they get out here?',
            'tags': ['Dangerous'],
            'resource_node_ids': ['rare_ice_samples', 'water_ice', 'organic_materials'],
        },
        'KR1_Resource_4': {
            'type': 'resource_node',
            'controlled_by': 'ORION',
            'description': 'Sensors indicate Kilometer wide ice structures.',
            'tags': ['Dangerous'],
            'resource_node_ids': ['rare_ice_samples', 'exotic_ices'],
        },
        'Kuiper_Region_1_Station': {
            'type': 'station',
            'controlled_by': 'ORION',
            'description': 'One of the last stations before interstellar space.',
            'tags': ['Safe'],
        },
        
        # ============================================================================
        # KUIPER BELT REGION 2
        # ============================================================================
        'Kuiper_Region_2': {
            'type': 'space',
            'controlled_by': 'ORION',
            'description': 'Somewhere in the Kuiper belt.',
            'tags': ['Dangerous'],
            'spawnable_ids': ['ice_pirates', 'pirate_scouts', 'rogue_prospectors'],
        },
        'KR2_Resource_1': {
            'type': 'resource_node',
            'controlled_by': 'ORION',
            'description': 'Sensors have found Ice chunks.',
            'tags': ['Dangerous'],
            'resource_node_ids': ['rare_ice_samples', 'nitrogen_ice', 'ammonia_ice'],
        },
        'KR2_Resource_2': {
            'type': 'resource_node',
            'controlled_by': 'ORION',
            'description': 'The only place in the system capable of having volatiles.',
            'tags': ['Dangerous'],
            'resource_node_ids': ['rare_ice_samples', 'pristine_volatiles'],
        },
        'KR2_Resource_3': {
            'type': 'resource_node',
            'controlled_by': 'ORION',
            'description': 'Sensors indicate there are interstellar remnants here.',
            'tags': ['Dangerous'],
            'resource_node_ids': ['rare_ice_samples', 'exotic_materials', 'interstellar_dust'],
        },
        'KR2_Resource_4': {
            'type': 'resource_node',
            'controlled_by': 'ORION',
            'description': 'The sensors have picked up prescense of rare isotopes, to bad it\'s in the form of dust',
            'tags': ['Dangerous'],
            'resource_node_ids': ['rare_ice_samples', 'deuterium_dust', 'tritium_dust'],
        },
        'Kuiper_Region_2_Station': {
            'type': 'station',
            'controlled_by': 'ORION',
            'description': 'A barely-maintained outpost.',
            'tags': ['Safe'],
        },
        
        # ============================================================================
        # KUIPER BELT REGION 3
        # ============================================================================
        'Kuiper_Region_3': {
            'type': 'space',
            'controlled_by': 'ORION',
            'description': "This is pretty far out. Mostly ice and dust.",
            'tags': ['Dangerous'],
            'spawnable_ids': ['pirate_fleets', 'rogue_miners', 'outlaws'],
        },
        'KR3_Resource_1': {
            'type': 'resource_node',
            'controlled_by': 'ORION',
            'description': 'A field of ancient ice fragments from the formation of the system.',
            'tags': ['Dangerous'],
            'resource_node_ids': ['rare_ice_samples', 'ancient_ices', 'primordial_materials'],
        },
        'KR3_Resource_2': {
            'type': 'resource_node',
            'controlled_by': 'ORION',
            'description': 'An ice cloud with some strange, dense, ice.',
            'tags': ['Dangerous'],
            'resource_node_ids': ['rare_ice_samples', 'deep_ice_cores'],
        },
        'KR3_Resource_3': {
            'type': 'resource_node',
            'controlled_by': 'ORION',
            'description': 'Shattered dwarf planet remains. Rich in metallic ices.',
            'tags': ['Dangerous'],
            'resource_node_ids': ['rare_ice_samples', 'metallic_ices', 'iron_ice_compounds'],
        },
        'KR3_Resource_4': {
            'type': 'resource_node',
            'controlled_by': 'ORION',
            'description': 'Ice shards pelt the side of the ship. Other than that this region isn\'t that weird.',
            'tags': ['Dangerous'],
            'resource_node_ids': ['rare_ice_samples', 'exotic_volatiles', 'crystalline_ices'],
        },
        'Kuiper_Region_3_Station': {
            'type': 'station',
            'controlled_by': 'ORION',
            'description': 'It\'s a station. Not really remarkable in any other way. Oh, other than it\'s way out in the Kuiper regions, that too.',
            'tags': ['Safe'],
        },
        
        # ============================================================================
        # KUIPER BELT REGION 4
        # ============================================================================
        'Kuiper_Region_4': {
            'type': 'space',
            'controlled_by': 'ORION',
            'description': 'The outermost reaches of the Kuiper Belt.',
            'tags': ['Dangerous'],
            'spawnable_ids': ['pirate_fleets', 'outlaws', 'unknown_entities'],
        },
        'KR4_Resource_1': {
            'type': 'resource_node',
            'controlled_by': 'ORION',
            'description': 'Nothing but ice and dust.',
            'tags': ['Dangerous'],
            'resource_node_ids': ['rare_ice_samples', 'helium_3'],
        },
        'KR4_Resource_2': {
            'type': 'resource_node',
            'controlled_by': 'ORION',
            'description': 'A place untouched by harsh gravitational conditions.',
            'tags': ['Dangerous'],
            'resource_node_ids': ['rare_ice_samples', 'proto_comet_materials', 'primordial_volatiles'],
        },
        'KR4_Resource_3': {
            'type': 'resource_node',
            'controlled_by': 'ORION',
            'description': 'A cold desolate region of the SOL system.',
            'tags': ['Dangerous'],
            'resource_node_ids': ['rare_ice_samples', 'anomalous_materials', 'unknown_compounds'],
        },
        'KR4_Resource_4': {
            'type': 'resource_node',
            'controlled_by': 'ORION',
            'description': 'The furthest confirmed resource point in the Sol System. Only the bravest or most desperate come here.',
            'tags': ['Dangerous'],
            'resource_node_ids': ['rare_ice_samples', 'ultra_rare_volatiles', 'oort_cloud_fragments'],
        },
        'Kuiper_Region_4_Station': {
            'type': 'station',
            'controlled_by': 'ORION',
            'description': 'A mysterious station in Kyiper Region 4. Rumors say it\'s run by exiles and outcasts.',
            'tags': ['Safe'],
        },
    }
    
    return locations


def create_world_links():
    """Define all location links based on sol_system.md.
    
    Returns:
        List of tuples (location1, location2) for bidirectional links
        List of tuples (source, dest) with 'single' marker for one-way links
    """
    # Bidirectional links (normal travel routes)
    bidirectional_links = [
        # ============================================================================
        # EARTH ORBIT CONNECTIONS
        # ============================================================================
        ('Earth_Orbit', 'Sun_Orbit'),
        ('Earth_Orbit', 'Mercury_Orbit'),
        ('Earth_Orbit', 'Mars_Orbit'),
        ('Earth_Orbit', 'Asteroid_Belt_Region_1'),
        ('Earth_Orbit', 'Asteroid_Belt_Region_2'),
        ('Earth_Orbit', 'Asteroid_Belt_Region_3'),
        ('Earth_Orbit', 'Jupiter_Orbit'),
        ('Earth_Orbit', 'Moon_Orbit'),
        ('Earth_Orbit', 'Earth_Orbital_Station_Zero'),
        ('Earth_Orbit', 'Earth_Ground_Station_Zero'),
        
        # ============================================================================
        # MOON CONNECTIONS
        # ============================================================================
        ('Moon_Orbit', 'Moon_Ground_Station'),
        
        # ============================================================================
        # SUN ORBIT CONNECTIONS
        # ============================================================================
        ('Sun_Orbit', 'Mercury_Orbit'),
        ('Sun_Orbit', 'Venus_Orbit'),
        ('Sun_Orbit', 'Mars_Orbit'),
        ('Sun_Orbit', 'Asteroid_Belt_Region_1'),
        ('Sun_Orbit', 'Asteroid_Belt_Region_2'),
        ('Sun_Orbit', 'Asteroid_Belt_Region_3'),
        ('Sun_Orbit', 'Jupiter_Orbit'),
        ('Sun_Orbit', 'Saturn_Orbit'),
        ('Sun_Orbit', 'SOL_Warp_Gates'),
        
        # ============================================================================
        # MERCURY CONNECTIONS
        # ============================================================================
        ('Mercury_Orbit', 'Asteroid_Belt_Region_1'),
        ('Mercury_Orbit', 'Asteroid_Belt_Region_2'),
        ('Mercury_Orbit', 'Asteroid_Belt_Region_3'),
        ('Mercury_Orbit', 'Venus_Orbit'),
        ('Mercury_Orbit', 'Mars_Orbit'),
        ('Mercury_Orbit', 'Mercury_Ground_Station'),
        
        # ============================================================================
        # VENUS CONNECTIONS
        # ============================================================================
        ('Venus_Orbit', 'Asteroid_Belt_Region_1'),
        ('Venus_Orbit', 'Asteroid_Belt_Region_2'),
        ('Venus_Orbit', 'Asteroid_Belt_Region_3'),
        ('Venus_Orbit', 'Mars_Orbit'),
        ('Venus_Orbit', 'Venus_Orbital_Station'),
        ('Venus_Orbit', 'Venus_Ground_Station'),
        
        # ============================================================================
        # MARS CONNECTIONS
        # ============================================================================
        ('Mars_Orbit', 'Jupiter_Orbit'),
        ('Mars_Orbit', 'Asteroid_Belt_Region_1'),
        ('Mars_Orbit', 'Asteroid_Belt_Region_2'),
        ('Mars_Orbit', 'Asteroid_Belt_Region_3'),
        ('Mars_Orbit', 'Mars_Ground_Station'),
        ('Mars_Orbit', 'Mars_Orbital_Station'),
        ('Mars_Orbit', 'Mars_Moon_1_Ground_Station'),
        ('Mars_Orbit', 'Mars_Moon_2_Ground_Station'),
        
        # ============================================================================
        # ASTEROID BELT REGION 1 CONNECTIONS
        # ============================================================================
        ('Asteroid_Belt_Region_1', 'Asteroid_Belt_Region_2'),
        ('Asteroid_Belt_Region_1', 'Asteroid_Belt_Region_3'),
        ('Asteroid_Belt_Region_1', 'Jupiter_Orbit'),
        ('Asteroid_Belt_Region_1', 'Saturn_Orbit'),
        ('Asteroid_Belt_Region_1', 'Uranus_Orbit'),
        ('Asteroid_Belt_Region_1', 'Neptune_Orbit'),
        ('Asteroid_Belt_Region_1', 'ABR1_Resource_1'),
        ('Asteroid_Belt_Region_1', 'ABR1_Resource_2'),
        ('Asteroid_Belt_Region_1', 'ABR1_Space_Station'),
        
        # ============================================================================
        # ASTEROID BELT REGION 2 CONNECTIONS
        # ============================================================================
        ('Asteroid_Belt_Region_2', 'Asteroid_Belt_Region_3'),
        ('Asteroid_Belt_Region_2', 'Jupiter_Orbit'),
        ('Asteroid_Belt_Region_2', 'Saturn_Orbit'),
        ('Asteroid_Belt_Region_2', 'Uranus_Orbit'),
        ('Asteroid_Belt_Region_2', 'Neptune_Orbit'),
        ('Asteroid_Belt_Region_2', 'ABR2_Resource_1'),
        ('Asteroid_Belt_Region_2', 'ABR2_Resource_2'),
        ('Asteroid_Belt_Region_2', 'ABR2_Space_Station'),
        
        # ============================================================================
        # ASTEROID BELT REGION 3 CONNECTIONS
        # ============================================================================
        ('Asteroid_Belt_Region_3', 'Jupiter_Orbit'),
        ('Asteroid_Belt_Region_3', 'Saturn_Orbit'),
        ('Asteroid_Belt_Region_3', 'Uranus_Orbit'),
        ('Asteroid_Belt_Region_3', 'Neptune_Orbit'),
        ('Asteroid_Belt_Region_3', 'ABR3_Resource_1'),
        ('Asteroid_Belt_Region_3', 'ABR3_Resource_2'),
        ('Asteroid_Belt_Region_3', 'ABR3_Space_Station'),
        
        # ============================================================================
        # JUPITER ORBIT CONNECTIONS
        # ============================================================================
        ('Jupiter_Orbit', 'Saturn_Orbit'),
        ('Jupiter_Orbit', 'Uranus_Orbit'),
        ('Jupiter_Orbit', 'Neptune_Orbit'),
        ('Jupiter_Orbit', 'Jupiter_Thunder_Station'),
        ('Jupiter_Orbit', 'IO_Station_Weapon_Specialist'),
        ('Jupiter_Orbit', 'Ganymede_Station_Shipwright'),
        ('Jupiter_Orbit', 'Europa_Station_Engine_Specialist'),
        ('Jupiter_Orbit', 'Callisto_Station_Shield_Specialist'),
        ('Jupiter_Orbit', 'Amalthea_Station_Cargo_Specialist'),
        ('Jupiter_Orbit', 'Himalia_Station_Sensor_Specialist'),
        ('Jupiter_Orbit', 'Thebe_Station_Stealth_Specialist'),
        
        # ============================================================================
        # SATURN ORBIT CONNECTIONS
        # ============================================================================
        ('Saturn_Orbit', 'Neptune_Orbit'),
        ('Saturn_Orbit', 'Uranus_Orbit'),
        ('Saturn_Orbit', 'Saturn_Ring_Resource_1'),
        ('Saturn_Orbit', 'Saturn_Ring_Resource_2'),
        ('Saturn_Orbit', 'Saturn_Ring_Station_1'),
        ('Saturn_Orbit', 'Saturn_Ring_Station_2'),
        ('Saturn_Orbit', 'Titan_Station'),
        ('Saturn_Orbit', 'Enceladus_Station_Rare_Materials_Trading'),
        ('Saturn_Orbit', 'Rhea_Station_Advanced_Manufacturing'),
        
        # ============================================================================
        # URANUS ORBIT CONNECTIONS
        # ============================================================================
        ('Uranus_Orbit', 'Neptune_Orbit'),
        ('Uranus_Orbit', 'Uranus_Atmo_Station'),
        ('Uranus_Orbit', 'Titania_Station_Data_Archive'),
        ('Uranus_Orbit', 'Oberon_Station_Sample_Repository'),
        
        # ============================================================================
        # NEPTUNE ORBIT CONNECTIONS
        # ============================================================================
        ('Neptune_Orbit', 'Kuiper_Region_1'),
        ('Neptune_Orbit', 'Neptune_Orbital_Station'),
        ('Neptune_Orbit', 'Triton_Station_Cartography_Center'),
        ('Neptune_Orbit', 'Nereid_Station_Frontier_Research'),
        
        # ============================================================================
        # KUIPER REGION 1 CONNECTIONS
        # ============================================================================
        ('Kuiper_Region_1', 'KR1_Resource_1'),
        ('Kuiper_Region_1', 'KR1_Resource_2'),
        ('Kuiper_Region_1', 'KR1_Resource_3'),
        ('Kuiper_Region_1', 'KR1_Resource_4'),
        ('Kuiper_Region_1', 'Kuiper_Region_1_Station'),
        ('Kuiper_Region_1', 'Kuiper_Region_2'),
        
        # ============================================================================
        # KUIPER REGION 2 CONNECTIONS
        # ============================================================================
        ('Kuiper_Region_2', 'KR2_Resource_1'),
        ('Kuiper_Region_2', 'KR2_Resource_2'),
        ('Kuiper_Region_2', 'KR2_Resource_3'),
        ('Kuiper_Region_2', 'KR2_Resource_4'),
        ('Kuiper_Region_2', 'Kuiper_Region_2_Station'),
        ('Kuiper_Region_2', 'Kuiper_Region_3'),
        
        # ============================================================================
        # KUIPER REGION 3 CONNECTIONS
        # ============================================================================
        ('Kuiper_Region_3', 'KR3_Resource_1'),
        ('Kuiper_Region_3', 'KR3_Resource_2'),
        ('Kuiper_Region_3', 'KR3_Resource_3'),
        ('Kuiper_Region_3', 'KR3_Resource_4'),
        ('Kuiper_Region_3', 'Kuiper_Region_3_Station'),
        ('Kuiper_Region_3', 'Kuiper_Region_4'),
        
        # ============================================================================
        # KUIPER REGION 4 CONNECTIONS
        # ============================================================================
        ('Kuiper_Region_4', 'KR4_Resource_1'),
        ('Kuiper_Region_4', 'KR4_Resource_2'),
        ('Kuiper_Region_4', 'KR4_Resource_3'),
        ('Kuiper_Region_4', 'KR4_Resource_4'),
        ('Kuiper_Region_4', 'Kuiper_Region_4_Station'),
    ]
    
    # One-way links (special routes, traps, etc.)
    single_directional_links = []
    
    return bidirectional_links, single_directional_links


def create_vendor_dialogue():
    """Create vendor NPCs and their dialogue at various locations.
    
    Station-based structure: Each station is a top-level key containing its vendors.
    Vendor options use dict format with 'dialogue', 'requirements', and 'reward'.
    
    Returns:
        Dict mapping station_name -> {vendor_id -> vendor_data}
    """
    vendors = {
        # ============================================================================
        # EARTH ORBITAL STATION ZERO
        # ============================================================================
        'Earth_Orbital_Station_Zero': {
            'earthorbit_zero_shipwright': {
                'vendor_type': 'shipwright',
                'entry_dialogue': "Welcome to Orbital Zero's premier shipyard.",
                'options': []
            },
            'earthorbit_zero_trader': {
                'vendor_type': 'trader',
                'entry_dialogue': "Fresh goods from Earth. What are you looking for?",
                'options': []
            },
            'earthorbit_zero_repairshop': {
                'vendor_type': 'repair_shop',
                'entry_dialogue': "Repair bay open. Let me take a look at your ship.",
                'options': []
            },
        },
        
        # ============================================================================
        # MOON GROUND STATION
        # ============================================================================
        'Moon_Ground_Station': {
            'moon_historian': {
                'vendor_type': 'historian',
                'entry_dialogue': "Welcome to humanity's first extraterrestrial colony.",
                'options': []
            },
            'moon_artifactdealer': {
                'vendor_type': 'artifact_dealer',
                'entry_dialogue': "I deal in historical artifacts from the early space age.",
                'options': []
            },
            'moon_shipwright': {
                'vendor_type': 'shipwright',
                'entry_dialogue': "Moon Shipyard. We've been building ships since the 2040s.",
                'options': []
            },
        },
        
        # ============================================================================
        # EARTH GROUND STATION ZERO
        # ============================================================================
        'Earth_Ground_Station_Zero': {
            'earthground_zero_shipwright': {
                'vendor_type': 'shipwright',
                'entry_dialogue': "ORION headquarters shipyard. Top-tier vessels only.",
                'options': []
            },
            'earthground_zero_trader': {
                'vendor_type': 'trader',
                'entry_dialogue': "Official ORION trade depot. State your business.",
                'options': []
            },
        },
        
        # ============================================================================
        # SOL WARP GATES
        # ============================================================================
        'SOL_Warp_Gates': {
            'solgate_customs': {
                'vendor_type': 'customs',
                'entry_dialogue': "Customs inspection required for all interstellar travel.",
                'options': []
            },
            'solgate_navigation': {
                'vendor_type': 'navigation',
                'entry_dialogue': "Warp gate navigation services. Destination?",
                'options': []
            },
        },
        
        # ============================================================================
        # MERCURY GROUND STATION
        # ============================================================================
        'Mercury_Ground_Station': {
            'mercury_shipwright': {
                'vendor_type': 'shipwright',
                'entry_dialogue': "Heat-resistant components are our specialty.",
                'options': []
            },
            'mercury_hunters': {
                'vendor_type': 'bounty_office',
                'entry_dialogue': "Looking for work? We've got bounties that pay well.",
                'options': []
            },
        },
        
        # ============================================================================
        # VENUS GROUND STATION
        # ============================================================================
        'Venus_Ground_Station': {
            'venusground_blackmarket': {
                'vendor_type': 'black_market',
                'entry_dialogue': "No questions asked. Cash only.",
                'options': []
            },
        },
        
        # ============================================================================
        # VENUS ORBITAL STATION
        # ============================================================================
        'Venus_Orbital_Station': {
            'venusorbital_trader': {
                'vendor_type': 'trader',
                'entry_dialogue': "Trading post open for business.",
                'options': []
            },
            'venusorbital_componentdealer': {
                'vendor_type': 'component_dealer',
                'entry_dialogue': "I've got components you won't find anywhere else.",
                'options': []
            },
        },
        
        # ============================================================================
        # MARS GROUND STATION
        # ============================================================================
        'Mars_Ground_Station': {
            'marsground_shipwright': {
                'vendor_type': 'shipwright',
                'entry_dialogue': "Mars Colony Shipyard. Building the future.",
                'options': []
            },
            'marsground_colonysupplies': {
                'vendor_type': 'trader',
                'entry_dialogue': "Colonial supplies and equipment.",
                'options': []
            },
        },
        
        # ============================================================================
        # MARS ORBITAL STATION
        # ============================================================================
        'Mars_Orbital_Station': {
            'marsorbital_shipwright': {
                'vendor_type': 'shipwright',
                'entry_dialogue': "Advanced shipyard facilities at your service.",
                'options': []
            },
            'marsorbital_defensesystems': {
                'vendor_type': 'defense_systems',
                'entry_dialogue': "Military-grade defensive systems available.",
                'options': []
            },
        },
        
        # ============================================================================
        # MARS MOON 1 (PHOBOS)
        # ============================================================================
        'Mars_Moon_1_Ground_Station': {
            'marsmoon1_weaponsdealer': {
                'vendor_type': 'weapons_dealer',
                'entry_dialogue': "Phobos Arsenal. The finest weapons in the system.",
                'options': []
            },
            'marsmoon1_ammunition': {
                'vendor_type': 'ammunition',
                'entry_dialogue': "Ammunition depot. What caliber?",
                'options': []
            },
        },
        
        # ============================================================================
        # MARS MOON 2 (DEIMOS)
        # ============================================================================
        'Mars_Moon_2_Ground_Station': {
            'marsmoon2_stealthcloakvendor': {
                'vendor_type': 'stealth_vendor',
                'entry_dialogue': "Stealth technology and cloaking devices.",
                'options': []
            },
            'marsmoon2_stealthresearch': {
                'vendor_type': 'research',
                'entry_dialogue': "Deimos Research. Our work is... classified.",
                'options': []
            },
        },
        
        # ============================================================================
        # ASTEROID BELT REGION 1 STATION
        # ============================================================================
        'ABR1_Space_Station': {
            'abr1station_maildelivery': {
                'vendor_type': 'mail_delivery',
                'entry_dialogue': "Mail delivery contracts available.",
                'options': []
            },
            'abr1station_miningequipment': {
                'vendor_type': 'mining_equipment',
                'entry_dialogue': "Mining equipment and supplies.",
                'options': []
            },
        },
        
        # ============================================================================
        # ASTEROID BELT REGION 2 STATION
        # ============================================================================
        'ABR2_Space_Station': {
            'abr2station_weapontraffickers': {
                'vendor_type': 'weapons_dealer',
                'entry_dialogue': "HELLO, SAPIENT. WE HAVE SHIPMENT ORDERS, CARE TO TAKE ONE?",
                'options': []
            },
            'abr2station_informationbroker': {
                'vendor_type': 'information_broker',
                'entry_dialogue': "Scan any mining drones recently? We're interested in that sort of thing.",
                'options': []
            },
        },
        
        # ============================================================================
        # ASTEROID BELT REGION 3 STATION
        # ============================================================================
        'ABR3_Space_Station': {
            'abr3station_shieldspecialists': {
                'vendor_type': 'shield_specialist',
                'entry_dialogue': "Shield technology and upgrades.",
                'options': []
            },
            'abr3station_explosives': {
                'vendor_type': 'explosives',
                'entry_dialogue': "Experimental explosives. Handle with care.",
                'options': []
            },
            'abr3station_researchdata': {
                'vendor_type': 'research_data',
                'entry_dialogue': "Research data exchange. What have you discovered?",
                'options': []
            },
        },
        
        # ============================================================================
        # JUPITER THUNDER STATION
        # ============================================================================
        'Jupiter_Thunder_Station': {
            'jupiterthunder_gasshipments': {
                'vendor_type': 'gas_trader',
                'entry_dialogue': "Gas collection contracts. Dangerous but profitable.",
                'options': []
            },
            'jupiterthunder_stormdata': {
                'vendor_type': 'data_buyer',
                'entry_dialogue': "We buy storm data from Jupiter's atmosphere.",
                'options': []
            },
            'jupiterthunder_hazardpay': {
                'vendor_type': 'contractor',
                'entry_dialogue': "Hazard pay jobs available. High risk, high reward.",
                'options': []
            },
        },
        
        # ============================================================================
        # IO STATION - WEAPON SPECIALIST
        # ============================================================================
        'IO_Station_Weapon_Specialist': {
            'io_weapon_upgrades': {
                'vendor_type': 'weapon_upgrades',
                'entry_dialogue': "Io Weapons Research. Premier weapons facility in Sol.",
                'options': []
            },
            'io_ballistics_expert': {
                'vendor_type': 'ballistics',
                'entry_dialogue': "Ballistics specialist. Let's upgrade your firepower.",
                'options': []
            },
        },
        
        # ============================================================================
        # GANYMEDE STATION - SHIPWRIGHT
        # ============================================================================
        'Ganymede_Station_Shipwright': {
            'ganymede_shipwright': {
                'vendor_type': 'shipwright',
                'entry_dialogue': "Ganymede Shipyards. The largest in the outer system.",
                'options': []
            },
            'ganymede_hull_specialist': {
                'vendor_type': 'hull_specialist',
                'entry_dialogue': "Hull modifications and reinforcement.",
                'options': []
            },
        },
        
        # ============================================================================
        # EUROPA STATION - ENGINE SPECIALIST
        # ============================================================================
        'Europa_Station_Engine_Specialist': {
            'europa_engine_upgrades': {
                'vendor_type': 'engine_upgrades',
                'entry_dialogue': "Engine and propulsion upgrades. Make your ship fly.",
                'options': []
            },
            'europa_propulsion_engineer': {
                'vendor_type': 'propulsion',
                'entry_dialogue': "Propulsion engineering. Speed is survival.",
                'options': []
            },
        },
        
        # ============================================================================
        # CALLISTO STATION - SHIELD SPECIALIST
        # ============================================================================
        'Callisto_Station_Shield_Specialist': {
            'callisto_shield_upgrades': {
                'vendor_type': 'shield_upgrades',
                'entry_dialogue': "Shield generator research and upgrades.",
                'options': []
            },
            'callisto_energy_systems': {
                'vendor_type': 'energy_systems',
                'entry_dialogue': "Energy systems and power management.",
                'options': []
            },
        },
        
        # ============================================================================
        # AMALTHEA STATION - CARGO SPECIALIST
        # ============================================================================
        'Amalthea_Station_Cargo_Specialist': {
            'amalthea_cargo_upgrades': {
                'vendor_type': 'cargo_upgrades',
                'entry_dialogue': "Cargo hold expansion and storage optimization.",
                'options': []
            },
            'amalthea_storage_engineer': {
                'vendor_type': 'storage',
                'entry_dialogue': "Storage solutions for every ship class.",
                'options': []
            },
        },
        
        # ============================================================================
        # HIMALIA STATION - SENSOR SPECIALIST
        # ============================================================================
        'Himalia_Station_Sensor_Specialist': {
            'himalia_sensor_upgrades': {
                'vendor_type': 'sensor_upgrades',
                'entry_dialogue': "Sensor arrays and detection systems.",
                'options': []
            },
            'himalia_detection_specialist': {
                'vendor_type': 'detection',
                'entry_dialogue': "Long-range detection technology.",
                'options': []
            },
        },
        
        # ============================================================================
        # THEBE STATION - STEALTH SPECIALIST
        # ============================================================================
        'Thebe_Station_Stealth_Specialist': {
            'thebe_stealth_upgrades': {
                'vendor_type': 'stealth_upgrades',
                'entry_dialogue': "Stealth cloaking technology.",
                'options': []
            },
            'thebe_cloak_specialist': {
                'vendor_type': 'cloaking',
                'entry_dialogue': "Signature dampening and cloaking systems.",
                'options': []
            },
        },
        
        # ============================================================================
        # SATURN RING STATION 1
        # ============================================================================
        'Saturn_Ring_Station_1': {
            'saturnring1_datacollection': {
                'vendor_type': 'data_collector',
                'entry_dialogue': "Ring research data collection.",
                'options': []
            },
            'saturnring1_shipwright': {
                'vendor_type': 'shipwright',
                'entry_dialogue': "Ring Station shipyard services.",
                'options': []
            },
        },
        
        # ============================================================================
        # SATURN RING STATION 2
        # ============================================================================
        'Saturn_Ring_Station_2': {
            'saturnring2_datacollection': {
                'vendor_type': 'data_collector',
                'entry_dialogue': "Ring data analysis and collection.",
                'options': []
            },
            'saturnring2_shipwright': {
                'vendor_type': 'shipwright',
                'entry_dialogue': "Shipyard and modification services.",
                'options': []
            },
            'saturnring2_scanningtech': {
                'vendor_type': 'scanning',
                'entry_dialogue': "Long-range scanning equipment.",
                'options': []
            },
        },
        
        # ============================================================================
        # TITAN STATION - ELITE OUTFITTER
        # ============================================================================
        'Titan_Station': {
            'titan_elite_weapons': {
                'vendor_type': 'elite_weapons',
                'entry_dialogue': "Titan Elite Arsenal. Only the finest.",
                'options': []
            },
            'titan_elite_defense': {
                'vendor_type': 'elite_defense',
                'entry_dialogue': "Elite defensive systems.",
                'options': []
            },
            'titan_premium_outfitter': {
                'vendor_type': 'premium_outfitter',
                'entry_dialogue': "Premium ship outfitting. If you can afford it.",
                'options': []
            },
        },
        
        # ============================================================================
        # ENCELADUS STATION - RARE MATERIALS
        # ============================================================================
        'Enceladus_Station_Rare_Materials_Trading': {
            'enceladus_rare_materials': {
                'vendor_type': 'rare_materials',
                'entry_dialogue': "Rare materials exchange.",
                'options': []
            },
            'enceladus_exotic_trader': {
                'vendor_type': 'exotic_trader',
                'entry_dialogue': "Exotic compounds and materials.",
                'options': []
            },
            'enceladus_material_exchange': {
                'vendor_type': 'material_exchange',
                'entry_dialogue': "Material exchange and trading.",
                'options': []
            },
        },
        
        # ============================================================================
        # RHEA STATION - ADVANCED MANUFACTURING
        # ============================================================================
        'Rhea_Station_Advanced_Manufacturing': {
            'rhea_advanced_manufacturing': {
                'vendor_type': 'advanced_manufacturing',
                'entry_dialogue': "Advanced fabrication services.",
                'options': []
            },
            'rhea_prototype_components': {
                'vendor_type': 'prototype_components',
                'entry_dialogue': "Prototype components and experimental tech.",
                'options': []
            },
            'rhea_experimental_tech': {
                'vendor_type': 'experimental_tech',
                'entry_dialogue': "Experimental technology. Buyer beware.",
                'options': []
            },
        },
        
        # ============================================================================
        # URANUS ATMO STATION
        # ============================================================================
        'Uranus_Atmo_Station': {
            'uranusatmo_gasharvesting': {
                'vendor_type': 'gas_harvesting',
                'entry_dialogue': "Gas harvesting contracts available.",
                'options': []
            },
            'uranusatmo_raregases': {
                'vendor_type': 'rare_gases',
                'entry_dialogue': "Rare gas trading.",
                'options': []
            },
        },
        
        # ============================================================================
        # TITANIA STATION - DATA ARCHIVE
        # ============================================================================
        'Titania_Station_Data_Archive': {
            'titania_data_collector': {
                'vendor_type': 'data_collector',
                'entry_dialogue': "Data archive. We pay for information.",
                'options': []
            },
            'titania_research_buyer': {
                'vendor_type': 'research_buyer',
                'entry_dialogue': "Research and discovery purchases.",
                'options': []
            },
            'titania_exploration_records': {
                'vendor_type': 'exploration_records',
                'entry_dialogue': "Exploration records and discoveries.",
                'options': []
            },
        },
        
        # ============================================================================
        # OBERON STATION - SAMPLE REPOSITORY
        # ============================================================================
        'Oberon_Station_Sample_Repository': {
            'oberon_sample_collector': {
                'vendor_type': 'sample_collector',
                'entry_dialogue': "Sample repository. Bring us materials.",
                'options': []
            },
            'oberon_material_analyst': {
                'vendor_type': 'material_analyst',
                'entry_dialogue': "Material analysis and evaluation.",
                'options': []
            },
            'oberon_specimen_buyer': {
                'vendor_type': 'specimen_buyer',
                'entry_dialogue': "We purchase physical samples from across Sol.",
                'options': []
            },
        },
        
        # ============================================================================
        # NEPTUNE ORBITAL STATION
        # ============================================================================
        'Neptune_Orbital_Station': {
            'neptuneorbital_explorer_supplies': {
                'vendor_type': 'explorer_supplies',
                'entry_dialogue': "Explorer supplies for deep space travel.",
                'options': []
            },
            'neptuneorbital_deepspace_outfitter': {
                'vendor_type': 'deepspace_outfitter',
                'entry_dialogue': "Deep space outfitting services.",
                'options': []
            },
        },
        
        # ============================================================================
        # TRITON STATION - CARTOGRAPHY
        # ============================================================================
        'Triton_Station_Cartography_Center': {
            'triton_cartographer': {
                'vendor_type': 'cartographer',
                'entry_dialogue': "Cartography center. We map the stars.",
                'options': []
            },
            'triton_navigation_data_buyer': {
                'vendor_type': 'navigation_data',
                'entry_dialogue': "Navigation data purchases.",
                'options': []
            },
            'triton_stellar_mapping': {
                'vendor_type': 'stellar_mapping',
                'entry_dialogue': "Stellar mapping and charting services.",
                'options': []
            },
        },
        
        # ============================================================================
        # NEREID STATION - FRONTIER RESEARCH
        # ============================================================================
        'Nereid_Station_Frontier_Research': {
            'nereid_frontier_researcher': {
                'vendor_type': 'frontier_researcher',
                'entry_dialogue': "Frontier research. The further out, the better we pay.",
                'options': []
            },
            'nereid_remote_samples': {
                'vendor_type': 'remote_samples',
                'entry_dialogue': "Remote sample collection.",
                'options': []
            },
            'nereid_deep_space_data': {
                'vendor_type': 'deep_space_data',
                'entry_dialogue': "Deep space data purchases.",
                'options': []
            },
        },
        
        # ============================================================================
        # KUIPER REGION 1 STATION
        # ============================================================================
        'Kuiper_Region_1_Station': {
            'kr1station_icegathering': {
                'vendor_type': 'ice_gathering',
                'entry_dialogue': "Ice gathering contracts.",
                'options': []
            },
            'kr1station_icetrader': {
                'vendor_type': 'ice_trader',
                'entry_dialogue': "Ice and volatiles trading.",
                'options': []
            },
            'kr1station_coldweather_gear': {
                'vendor_type': 'cold_weather_gear',
                'entry_dialogue': "Cold weather equipment and gear.",
                'options': []
            },
        },
        
        # ============================================================================
        # KUIPER REGION 2 STATION
        # ============================================================================
        'Kuiper_Region_2_Station': {
            'kr2station_independenttrader': {
                'vendor_type': 'independent_trader',
                'entry_dialogue': "Independent trader. ORION doesn't come out here.",
                'options': []
            },
            'kr2station_fuelprocessing': {
                'vendor_type': 'fuel_processing',
                'entry_dialogue': "Fuel processing and refining.",
                'options': []
            },
            'kr2station_blackmarket': {
                'vendor_type': 'black_market',
                'entry_dialogue': "Black market goods. No questions.",
                'options': []
            },
        },
        
        # ============================================================================
        # KUIPER REGION 3 STATION
        # ============================================================================
        'Kuiper_Region_3_Station': {
            'kr3station_fencedgoods': {
                'vendor_type': 'fence',
                'entry_dialogue': "Fenced goods. Don't ask where they came from.",
                'options': []
            },
            'kr3station_piratequartermaster': {
                'vendor_type': 'pirate_quartermaster',
                'entry_dialogue': "Pirate supplies and equipment.",
                'options': []
            },
            'kr3station_shady_shipwright': {
                'vendor_type': 'shady_shipwright',
                'entry_dialogue': "Ship modifications. No records kept.",
                'options': []
            },
        },
        
        # ============================================================================
        # KUIPER REGION 4 STATION
        # ============================================================================
        'Kuiper_Region_4_Station': {
            'kr4station_exile_trader': {
                'vendor_type': 'exile_trader',
                'entry_dialogue': "Exile trading post. We don't judge.",
                'options': []
            },
            'kr4station_frontier_supplies': {
                'vendor_type': 'frontier_supplies',
                'entry_dialogue': "Frontier supplies. Edge of known space.",
                'options': []
            },
            'kr4station_mysterious_vendor': {
                'vendor_type': 'mysterious_vendor',
                'entry_dialogue': "...",
                'options': []
            },
        },
    }
    
    return vendors


