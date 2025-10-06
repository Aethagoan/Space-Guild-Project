"""
Location module
- Provides a simple Location factory and the location registry/handler.
- Keeps initial sample locations (earth, mars) with bidirectional links.
- Actions and other systems should import `locationhandler` from here.
"""

from typing import Dict, Set


def Location(name: str):
    """Create a location.

    Keys:
    - name: str
    - links: set[str] of adjacent location names

    LLM-Dev v1: Keeping as dict for compatibility with existing code.
    """
    
    return {
        'name': name,
        'links': set(),  # type: Set[str]
    }



# a dict that is supposed to have 'string': Location dict
locationhandler = { }

# functions that help to quickly add the locations to the handler
def addnewlocation(name:str):
    locationhandler[name] = Location(name)

def linklocations(name:str,name2:str):
    locationhandler[name]['links'].add(name2)
    locationhandler[name2]['links'].add(name)
    

addnewlocation('earth')
addnewlocation('mars')
linklocations('earth','mars')


__all__ = [
    'Location',
    'locationhandler',
]
