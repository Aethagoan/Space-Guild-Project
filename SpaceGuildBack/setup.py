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


def create_world_locations():
    """Create all world locations (just names, no dialogue).
    
    TODO: Replace this with your actual location list.
    
    Returns:
        List of location names
    """
    # This is a TEMPLATE. Replace with your 20-30 location names.
    locations = [
        # ============================================================================
        # SOL SYSTEM
        # ============================================================================
        'Earth_Orbit',
        'Mars_Colony',
        'Jupiter_Station',
        'Sol_JumpGate',
        
        # ============================================================================
        # ALPHA CENTAURI SYSTEM
        # ============================================================================
        'Proxima_Centauri_Station',
        'Centauri_Prime',
        'Alpha_JumpGate_1',
        'Alpha_JumpGate_2',
        
        # ============================================================================
        # SIRIUS SYSTEM
        # ============================================================================
        'Sirius_A_Station',
        'Sirius_Mining_Belt',
        'Sirius_JumpGate',
        
        # ============================================================================
        # VEGA SYSTEM
        # ============================================================================
        'Vega_Trading_Hub',
        'Vega_Shipyard',
        'Vega_Outpost_7',
        'Vega_JumpGate_Alpha',
        'Vega_JumpGate_Frontier',
        
        # ============================================================================
        # FRONTIER SYSTEMS (Unregulated space)
        # ============================================================================
        'Frontier_Station_Delta',
        'Dead_Space_Graveyard',
        'Pirate_Haven',
        'Abandoned_Research_Facility',
        'Unknown_Anomaly',
    ]
    
    return locations


def create_world_links():
    """Define all location links (connections between locations).
    
    TODO: Replace with your actual world map structure.
    
    Returns:
        List of tuples (location1, location2) for bidirectional links
        List of tuples (source, dest) with 'single' marker for one-way links
    """
    # Bidirectional links (normal travel routes)
    bidirectional_links = [
        # Sol System internal connections
        ('Earth_Orbit', 'Mars_Colony'),
        ('Mars_Colony', 'Jupiter_Station'),
        ('Jupiter_Station', 'Sol_JumpGate'),
        ('Earth_Orbit', 'Sol_JumpGate'),  # Direct route too
        
        # Sol to Alpha Centauri via jump gate
        ('Sol_JumpGate', 'Proxima_Centauri_Station'),
        
        # Alpha Centauri internal connections
        ('Proxima_Centauri_Station', 'Centauri_Prime'),
        ('Proxima_Centauri_Station', 'Alpha_JumpGate_1'),
        ('Proxima_Centauri_Station', 'Alpha_JumpGate_2'),
        
        # Alpha Centauri to Sirius
        ('Alpha_JumpGate_1', 'Sirius_A_Station'),
        
        # Sirius internal connections
        ('Sirius_A_Station', 'Sirius_Mining_Belt'),
        ('Sirius_Mining_Belt', 'Sirius_JumpGate'),
        ('Sirius_JumpGate', 'Proxima_Centauri_Station'),  # Back to Alpha Centauri
        
        # Alpha Centauri to Vega
        ('Alpha_JumpGate_2', 'Vega_Trading_Hub'),
        
        # Vega internal connections
        ('Vega_Trading_Hub', 'Vega_Shipyard'),
        ('Vega_Shipyard', 'Vega_Outpost_7'),
        ('Vega_Trading_Hub', 'Vega_JumpGate_Alpha'),
        ('Vega_Outpost_7', 'Vega_JumpGate_Frontier'),
        
        # Vega back to Alpha Centauri
        ('Vega_JumpGate_Alpha', 'Proxima_Centauri_Station'),
        
        # Vega to Frontier space
        ('Vega_JumpGate_Frontier', 'Frontier_Station_Delta'),
        
        # Frontier internal connections
        ('Frontier_Station_Delta', 'Dead_Space_Graveyard'),
        ('Frontier_Station_Delta', 'Pirate_Haven'),
        ('Dead_Space_Graveyard', 'Abandoned_Research_Facility'),
        ('Pirate_Haven', 'Unknown_Anomaly'),
    ]
    
    # One-way links (special routes, traps, etc.)
    single_directional_links = [
        # Example: Anomaly might pull ships in but not let them out easily
        # ('Some_Location', 'Unknown_Anomaly', 'single'),
    ]
    
    return bidirectional_links, single_directional_links


def create_vendor_dialogue():
    """Create vendor NPCs and their dialogue at various locations.
    
    Vendor naming convention: locationname_vendortype
    Examples: earthorbit_shipwright, vegahub_trader, etc.
    
    Returns:
        Dict mapping vendor_name -> vendor_data
    """
    vendors = {
        # ============================================================================
        # EARTH ORBIT VENDORS
        # ============================================================================
        'earthorbit_shipwright': {
            'location': 'Earth_Orbit',
            'vendor_type': 'shipwright',
            'name': 'Marcus Steel',
            'dialogue': [
                "Welcome to Steel's Shipyard. Best ships in Sol system.",
                "Need an upgrade? I've got engines that'll make Mars look close.",
                "Every component I sell comes with a lifetime guarantee. Well, YOUR lifetime anyway.",
            ]
        },
        'earthorbit_trader': {
            'location': 'Earth_Orbit',
            'vendor_type': 'trader',
            'name': 'Sarah Kim',
            'dialogue': [
                "Fresh off Earth - rare goods and supplies.",
                "Looking to sell? I buy at fair prices. Unlike those Vega crooks.",
                "Rumor has it the Frontier has some wild salvage opportunities...",
            ]
        },
        'earthorbit_repairshop': {
            'location': 'Earth_Orbit',
            'vendor_type': 'repair_shop',
            'name': 'Engineer Dale',
            'dialogue': [
                "Repair shop open for business.",
                "Components looking rough? I can fix that. For a price.",
                "Pro tip: Don't let your shields drop to zero. Bad for business. Yours, not mine.",
            ]
        },
        
        # ============================================================================
        # VEGA TRADING HUB VENDORS
        # ============================================================================
        'vegahub_trader': {
            'location': 'Vega_Trading_Hub',
            'vendor_type': 'trader',
            'name': 'Xalen the Broker',
            'dialogue': [
                "Xalen knows all, sees all, sells all.",
                "You want it? I have it. You need it? I know someone.",
                "Credits talk, spacer. What are you buying?",
            ]
        },
        'vegahub_blackmarket': {
            'location': 'Vega_Trading_Hub',
            'vendor_type': 'black_market',
            'name': 'Unknown Contact',
            'dialogue': [
                "No names. No questions.",
                "I've got items that fell off the back of a cargo hauler. Interested?",
                "Sector police don't patrol here. Make it quick.",
            ]
        },
        
        # ============================================================================
        # VEGA SHIPYARD VENDORS
        # ============================================================================
        'vegashipyard_shipwright': {
            'location': 'Vega_Shipyard',
            'vendor_type': 'shipwright',
            'name': 'Chief Engineer Torres',
            'dialogue': [
                "Vega Shipyards - we build what others can't.",
                "Custom ship builds, tier upgrades, you name it.",
                "If you've got the credits, we've got the tech.",
            ]
        },
        'vegashipyard_componentdealer': {
            'location': 'Vega_Shipyard',
            'vendor_type': 'component_dealer',
            'name': 'Parts Specialist',
            'dialogue': [
                "Highest quality components in the sector.",
                "Military-grade shields, experimental weapons, custom engines.",
                "These aren't your standard Earth Orbit parts, friend.",
            ]
        },
        
        # ============================================================================
        # FRONTIER STATION VENDORS
        # ============================================================================
        'frontierdelta_trader': {
            'location': 'Frontier_Station_Delta',
            'vendor_type': 'trader',
            'name': 'Rusty',
            'dialogue': [
                "Out here, we trade in survival. And salvage.",
                "You look new. Word of advice: don't trust anyone. Especially me.",
                "Need supplies? I've got rations, fuel, and ammunition. In that order of importance.",
            ]
        },
        'frontierdelta_repairshop': {
            'location': 'Frontier_Station_Delta',
            'vendor_type': 'repair_shop',
            'name': 'Doc Welder',
            'dialogue': [
                "Station's repair tech. I keep ships flying. Barely.",
                "Out here, repairs are expensive. But getting stranded is worse.",
                "I've seen things you wouldn't believe. Most of them damaged beyond repair.",
            ]
        },
        
        # ============================================================================
        # PIRATE HAVEN VENDORS
        # ============================================================================
        'piratehaven_blackmarket': {
            'location': 'Pirate_Haven',
            'vendor_type': 'black_market',
            'name': 'The Fence',
            'dialogue': [
                "Stolen goods, military surplus, experimental tech. I don't ask where you got it.",
                "Cash only. No records. No witnesses.",
                "You didn't hear this from me, but there's a derelict carrier near the Graveyard...",
            ]
        },
    }
    
    return vendors


def setup_world(data_dir: str = "game_data", force: bool = False):
    """Set up the game world with locations and links.
    
    Args:
        data_dir: Directory to store game data
        force: Skip user confirmation prompt if True
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
    location_names = create_world_locations()
    bidirectional_links, single_links = create_world_links()
    vendor_data = create_vendor_dialogue()
    
    print(f"\n[*] Creating {len(location_names)} locations...")
    
    # Create all locations
    for location_name in location_names:
        data_handler.add_location(location_name)
        print(f"  [+] Created: {location_name}")
    
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
    
    # Save vendor dialogue data separately
    vendor_file = os.path.join(data_dir, "vendor_dialogue.json")
    print(f"\n[*] Saving vendor dialogue to {vendor_file}...")
    with open(vendor_file, 'w') as f:
        json.dump(vendor_data, f, indent=2)
    print(f"  [+] Created {len(vendor_data)} vendors")
    
    # Save all location data
    print(f"\n[*] Saving world data...")
    data_handler.save_all()
    
    print("\n" + "=" * 70)
    print("[+] WORLD SETUP COMPLETE")
    print("=" * 70)
    print(f"\nLocations created: {len(location_names)}")
    print(f"Vendors created: {len(vendor_data)}")
    print(f"Total connections: {len(bidirectional_links) * 2 + len(single_links)}")
    print(f"\nData saved to: {data_dir}/")
    print("\n[*] World is ready for game loop startup!")


if __name__ == '__main__':
    # Run setup
    setup_world()
