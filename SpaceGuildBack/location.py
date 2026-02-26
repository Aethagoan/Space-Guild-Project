# Aidan Orion 23 Feb 2026
# Location Creator/Recreator

from typing import Dict, Set
import json

# in this case there's nothing to specially handle. The links of the dict are meant to be a set, but it doesn't really matter because they'll be handled by setup only.
def Location(name: str, location_type: str = 'space'):
    return {
        'name': name,
        'type': location_type,  # 'space', 'station', 'starport'
        'description':"",
        'links': [],
        'logs': [],
        'ship_ids': [],
        'items': [],
        'vendors': [],
    }

