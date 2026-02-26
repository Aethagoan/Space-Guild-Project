# Aidan Orion 23 Feb 2026
# Location Creator/Recreator

from typing import Dict, Set, List, Optional
import json

# in this case there's nothing to specially handle. The links of the dict are meant to be a set, but it doesn't really matter because they'll be handled by setup only.
def Location(
    name: str, 
    location_type: str = 'space',
    controlled_by: str = 'ORION',
    description: str = '',
    tags: Optional[List[str]] = None,
    spawnable_ids: Optional[List[str]] = None,
    resource_node_ids: Optional[List[str]] = None,
):
    """Create a location dict with all metadata.
    
    Args:
        name: Location name (e.g., 'Earth_Orbit')
        location_type: 'space', 'station', 'ground_station', 'resource_node'
        controlled_by: Faction controlling this location (default 'ORION')
        description: Descriptive text about the location
        tags: Safety/danger tags ['Safe', 'Enforced', 'Patrolled', 'Dangerous']
        spawnable_ids: List of IDs for NPCs/ships that can spawn here
        resource_node_ids: List of IDs for resources that can be gathered here
    
    Returns:
        Dict representing a location
    """
    return {
        'name': name,
        'type': location_type,
        'controlled_by': controlled_by,
        'description': description,
        'tags': tags if tags is not None else [],
        'links': [],
        'logs': [],
        'ship_ids': [],
        'visible_ship_ids': [],  # Cached list of visible ships (filtered by stealth), updated each tick
        'items': [],
        'spawnable_ids': spawnable_ids if spawnable_ids is not None else [],
        'resource_node_ids': resource_node_ids if resource_node_ids is not None else [],
    }

