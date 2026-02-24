# Aidan Orion 23 Feb 2026
# Location Creator/Recreator

from typing import Dict, Set
import json

# in this case there's nothing to specially handle. The links of the dict are meant to be a set, but it doesn't really matter because they'll be handled by setup only.
def Location(name: str):
    return {
        'name': name,
        'links': [],
        'logs': [],
        'ship_ids': [],
        'items': [],
    }

