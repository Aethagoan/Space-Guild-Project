"""
LLM-Dev v1: Actions module
- Contains action implementations (attack, move, etc.) and the action handler mapping.
- Maintains a shared `tokenhandler` registry that systems (API, NPC runners) can reference.
- Depends on `locationhandler` from the `location` module.
"""

from typing import Callable, Dict
from location import locationhandler


# Public registry of tokens by token id/name
tokenhandler = {}

# Actions
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

def collect(collector: str, target:str) -> None:
	col = tokenhandler[collector]
	tar = tokenhandler[target]
	if col['location'] == tar['location']:
		if can_fit_item(col['cargo'], tar['weight']):
			add_item(col['cargo'])




# Action Delegator
def doaction(actor: str, action: str, thing: str) -> None:
	try:
		actionhandler[action](actor, thing)
	except:
		pass

actionhandler = {
	'attack': attack,
	'move': move,
	'collect': collect
}



__all__ = [
	'attack',
	'move',
	'collect',
	'doaction',
	'actionhandler',
	'tokenhandler',
]
