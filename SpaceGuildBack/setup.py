# Aidan Orion 25 Feb 2026
# World setup script - Creates initial game world with locations, links, vendors, spawnables_ids

import os
import json
from data import DataHandler
from location import Location


def prompt_overwrite(data_dir: str, systems: list[str]) -> bool:
    """Prompt user before overwriting existing world data.
    
    Args:
        data_dir: Path to game data directory
        systems: List of system setup files being loaded
        
    Returns:
        True if user wants to proceed, False otherwise
    """
    # Load all system data to determine what will be created
    will_have_locations = False
    will_have_vendors = False
    
    for system_file in systems:
        setup_file = os.path.join('setup_data', system_file)
        if os.path.exists(setup_file):
            with open(setup_file, 'r') as f:
                system_data = json.load(f)
                if system_data.get('locations'):
                    will_have_locations = True
                if system_data.get('vendors'):
                    will_have_vendors = True
    
    # Check which files will be affected
    files_to_check = []
    if will_have_locations:
        files_to_check.append('locations.json')
    if will_have_vendors:
        files_to_check.append('vendor_dialogue.json')
    
    existing_files = [f for f in files_to_check if os.path.exists(os.path.join(data_dir, f))]
    
    if not existing_files:
        return True  # No existing data, proceed
    
    print(f"\n[!] Warning: The following data files already exist in '{data_dir}':")
    for f in existing_files:
        print(f"  - {f}")
    
    response = input("\nOverwrite existing world data? (yes/no): ").strip().lower()
    return response in ['yes', 'y']

def load_system_setup(file_name: str) -> dict:
    """Load system setup data from JSON file.
    
    Args:
        file_name: Name of the setup file (e.g., 'sol_setup.json')
        
    Returns:
        Dict containing locations, links, and vendors for the system
    """
    setup_file = os.path.join('setup_data/systems', file_name)
    
    if not os.path.exists(setup_file):
        raise FileNotFoundError(f"Setup file not found: {setup_file}")
    
    with open(setup_file, 'r') as f:
        return json.load(f)


def load_spawnable_resources(file_name: str) -> dict:
    """Load resource item definitions from setup data.
    
    Returns:
        Dict containing resource item templates
    """
    setup_file = os.path.join('setup_data/spawnable_items', file_name)
    
    if not os.path.exists(setup_file):
        raise FileNotFoundError(f"resources file not found: {setup_file}")
    
    with open(setup_file, 'r') as f:
        return json.load(f)

def load_spawnable_deliverables(file_name: str) -> dict:
    """Load deliverable item definitions from setup data.
    
    Returns:
        Dict containing deliverable item templates
    """
    setup_file = os.path.join('setup_data/spawnable_items', file_name)
    
    if not os.path.exists(setup_file):
        raise FileNotFoundError(f"deliverables file not found: {setup_file}")
    
    with open(setup_file, 'r') as f:
        return json.load(f)

def load_spawnable_interactables(file_name: str) -> dict:
    """Load interactable item definitions from setup data.
    
    Returns:
        Dict containing interactable item templates
    """
    setup_file = os.path.join('setup_data/spawnable_items', file_name)
    
    if not os.path.exists(setup_file):
        raise FileNotFoundError(f"interactables file not found: {setup_file}")
    
    with open(setup_file, 'r') as f:
        return json.load(f)

def load_spawnable_components(file_name: str) -> dict:
    """Loads the spawnable components from setup data.
    
    Returns:
        Dict containing spawnable component templates.
    """
    setup_file = os.path.join('setup_data/spawnable_items', file_name)
    
    if not os.path.exists(setup_file):
        raise FileNotFoundError(f"Components file not found: {setup_file}")
    
    with open(setup_file, 'r') as f:
        return json.load(f)


def load_spawnable_ships(file_name: str) -> dict:
    """Load spawnable ship definitions from setup data.
    
    Returns:
        Dict containing spawnable ship templates
    """
    setup_file = os.path.join('setup_data/spawnable_ships', file_name)
    
    if not os.path.exists(setup_file):
        raise FileNotFoundError(f"Spawnable ships file not found: {setup_file}")
    
    with open(setup_file, 'r') as f:
        return json.load(f)


def load_npc_factions(file_name: str) -> dict:
    """Load NPC faction definitions from setup data.
    
    Returns:
        Dict containing NPC faction data
    """
    setup_file = os.path.join('setup_data/npc_factions', file_name)
    
    if not os.path.exists(setup_file):
        raise FileNotFoundError(f"NPC factions file not found: {setup_file}")
    
    with open(setup_file, 'r') as f:
        return json.load(f)


async def setup_world(data_dir: str = "game_data", 
    systems: list[str] | None = None, 
    resources: list[str] | None = None,
    deliverables: list[str] | None = None,
    interactables: list[str] | None = None,
    components: list[str] | None = None, 
    factions: list[str] | None = None,
    ships: list[str] | None = None):

    """Set up the game world with locations and links.
    
    Args:
        data_dir: Directory to store game data
        systems: List of setup file names to load
        
    Returns:
        DataHandler instance with all locations, links, and vendors created
    """
    if systems is None:
        raise ValueError("No system files provided. Please specify at least one setup file.")
    
    print("=" * 70)
    print("SPACE GUILD - WORLD SETUP")
    print("=" * 70)
    
    # Check for existing data and prompt user
    if not prompt_overwrite(data_dir, systems):
        print("\n[X] Setup cancelled by user.")
        return
    
    print("\n[*] Initializing world...")
    
    # Create DataHandler
    data_handler = DataHandler(data_dir=data_dir)
    
    # Load system data
    all_locations = {}
    all_bidirectional_links = []
    all_single_links = []
    all_vendors = {}
    
    for system_file in systems:
        print(f"\n[*] Loading {system_file}...")
        system_data = load_system_setup(system_file)
        
        all_locations.update(system_data['locations'])
        all_bidirectional_links.extend([tuple(link) for link in system_data['bidirectional_links']])
        all_single_links.extend([tuple(link) for link in system_data.get('single_directional_links', [])])
        all_vendors.update(system_data['vendors'])
    
    print(f"\n[*] Creating {len(all_locations)} locations...")
    
    # Create all locations with their metadata
    for location_name, metadata in all_locations.items():
        await data_handler.add_location(
            location_name,
            location_type=metadata.get('type', 'space'),
            controlled_by=metadata.get('controlled_by', 'ORION'),
            description=metadata.get('description', ''),
            tags=metadata.get('tags', []),
            spawnable_ships=metadata.get('spawnable_ships', []),
            spawnable_resources=metadata.get('spawnable_resources', [])
        )
        print(f"  [+] Created: {location_name} ({metadata.get('type', 'space')})")
    
    # Create bidirectional links
    print(f"\n[*] Creating {len(all_bidirectional_links)} bidirectional links...")
    for loc1, loc2 in all_bidirectional_links:
        await data_handler.double_link_locations(loc1, loc2)
        print(f"  [+] Linked: {loc1} <-> {loc2}")
    
    # Create single-directional links
    print(f"\n[*] Creating {len(all_single_links)} one-way links...")
    for source, dest, _ in all_single_links:
        await data_handler.single_link_locations(source, dest)
        print(f"  [+] One-way: {source} -> {dest}")
    
    # Save vendor dialogue data separately (station-based structure)
    vendor_file = os.path.join(data_dir, "vendor_dialogue.json")
    print(f"\n[*] Saving vendor dialogue to {vendor_file}...")
    
    # Count total vendors across all stations
    total_vendors = sum(len(vendors) for vendors in all_vendors.values())
    
    with open(vendor_file, 'w') as f:
        json.dump(all_vendors, f, indent=2)
    print(f"  [+] Created {total_vendors} vendors across {len(all_vendors)} stations")
    
    # Load and save resource items
    if resources:
        print(f"\n[*] Loading resource item definitions...")
        for resource_file in resources:
            resource_items = load_spawnable_resources(resource_file)
            data_handler.ResourceItems.update(resource_items)
        print(f"  [+] Loaded {len(data_handler.ResourceItems)} resource types")
    
    # Load and save deliverable items
    if deliverables:
        print(f"\n[*] Loading deliverable item definitions...")
        for deliverable_file in deliverables:
            deliverable_items = load_spawnable_deliverables(deliverable_file)
            data_handler.DeliverableItems.update(deliverable_items)
        print(f"  [+] Loaded {len(data_handler.DeliverableItems)} deliverable types")
    
    # Load and save interactable items
    if interactables:
        print(f"\n[*] Loading interactable item definitions...")
        for interactable_file in interactables:
            interactable_items = load_spawnable_interactables(interactable_file)
            data_handler.InteractableItems.update(interactable_items)
        print(f"  [+] Loaded {len(data_handler.InteractableItems)} interactable types")
    
    # Load and save spawnable components
    if components:
        print(f"\n[*] Loading spawnable component templates...")
        for component_file in components:
            spawnable_components = load_spawnable_components(component_file)
            data_handler.SpawnableComponents.update(spawnable_components)
        print(f"  [+] Loaded {len(data_handler.SpawnableComponents)} component templates")
    
    # Load and save spawnable ships
    if ships:
        print(f"\n[*] Loading spawnable ship templates...")
        for ship_file in ships:
            spawnable_ships = load_spawnable_ships(ship_file)
            data_handler.SpawnableShips.update(spawnable_ships)
        print(f"  [+] Loaded {len(data_handler.SpawnableShips)} ship templates")
    
    # Load and save NPC factions
    if factions:
        print(f"\n[*] Loading NPC faction data...")
        for faction_file in factions:
            npc_factions = load_npc_factions(faction_file)
            data_handler.NPCFactions.update(npc_factions)
        print(f"  [+] Loaded {len(data_handler.NPCFactions)} NPC factions")
    
    # Save all location data
    print(f"\n[*] Saving world data...")
    data_handler.save_all()
    
    print("\n" + "=" * 70)
    print("[+] WORLD SETUP COMPLETE")
    print("=" * 70)
    print(f"\nLocations created: {len(all_locations)}")
    print(f"Stations with vendors: {len(all_vendors)}")
    print(f"Total vendors: {total_vendors}")
    print(f"Total connections: {len(all_bidirectional_links) * 2 + len(all_single_links)}")
    print(f"\nData saved to: {data_dir}/")
    print("\n[*] World is ready for game loop startup!")
    
    return data_handler

if __name__ == '__main__':
    import sys
    import asyncio
    
    # Parse command line arguments
    systems_setup_files = ['sol_setup.json',]
    resources_setup_files = ['spawnable_resources.json',]
    deliverables_setup_files = ['spawnable_deliverables.json',]
    interactables_setup_files = ['spawnable_interactables.json',]
    components_setup_files = ['spawnable_components.json',]
    factions_setup_files = ['npc_factions.json',]
    ships_setup_files = ['sol_ships.json',]

    # Run setup
    asyncio.run(setup_world(
        systems=systems_setup_files,
        resources=resources_setup_files,
        deliverables=deliverables_setup_files,
        interactables=interactables_setup_files,
        components=components_setup_files,
        factions=factions_setup_files,
        ships=ships_setup_files
    ))

