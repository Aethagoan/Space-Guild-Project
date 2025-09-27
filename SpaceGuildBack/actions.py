"""
LLM-Dev v1: Actions module
- Contains action implementations (attack, move, etc.) and the action handler mapping.
- Maintains a shared `tokenhandler` registry that systems (API, NPC runners) can reference.
- Depends on `locationhandler` from the `location` module.
"""

from typing import Callable, Dict

# LLM-Dev v1: Prefer package-relative import; fall back to local when run as script.
try:
    from .location import locationhandler  # type: ignore
except ImportError:  # pragma: no cover
    from location import locationhandler  # type: ignore


# Public registry of tokens (ships, NPCs, etc.) by token id/name
# Token schema (dict) expected by actions today:
# {
#   'location': str,
#   'hp': int,
#   'weapon': { 'multiplier': int | float }
# }
# LLM-Dev v1: Keeping schema as dict for compatibility; consider Pydantic/dataclasses later.
tokenhandler: Dict[str, dict] = {}


def attack(attacker: str, target: str) -> None:
    atk = tokenhandler[attacker]
    tar = tokenhandler[target]
    if atk['location'] == tar['location']:
        tar['hp'] -= atk['weapon']['multiplier']


def move(mover: str, newlocation: str) -> None:
    mov = tokenhandler[mover]
    loc = locationhandler[newlocation]
    if loc['name'] in (locationhandler[mov['location']]['links']):
        mov['location'] = loc['name']


def doaction(actor: str, action: str, thing: str) -> None:
    actionhandler[action](actor, thing)


# Mapping of action name -> callable
actionhandler: Dict[str, Callable[..., None]] = {
    'attack': attack,
    'move': move,
}


__all__ = [
    'attack',
    'move',
    'doaction',
    'actionhandler',
    'tokenhandler',
]
