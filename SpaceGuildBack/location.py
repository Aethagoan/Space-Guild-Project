"""
LLM-Dev v1: Location module
- Provides a simple Location factory and the location registry/handler.
- Keeps initial sample locations (earth, mars) with bidirectional links.
- Actions and other systems should import `locationhandler` from here.
"""

from typing import Dict, Set


def Location(name: str) -> Dict[str, object]:
    """Create a basic location record.

    Keys:
    - name: str
    - links: set[str] of adjacent location names

    LLM-Dev v1: Keeping as dict for compatibility with existing code.
    """
    return {
        'name': name,
        'links': set(),  # type: Set[str]
    }


# Sample locations and links
earth = Location('earth')
mars = Location('mars')

earth['links'].add('mars')
mars['links'].add('earth')


# Public registry for locations by name
locationhandler: Dict[str, Dict[str, object]] = {
    'earth': earth,
    'mars': mars,
}


__all__ = [
    'Location',
    'locationhandler',
]
