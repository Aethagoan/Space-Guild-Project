"""
- Contains action implementations (attack, move, etc.) and the action handler mapping.
- Maintains a shared `tokenhandler` registry that systems (API, NPC runners) can reference.
- Depends on `locationhandler` from the `location` module.
"""


from typing import Callable, Dict

from location import locationhandler

from redishandler import getdictfromredis,savedicttoredis


# Actions

def attack(attacker: str, target: str) -> None:
	atk = getdictfromredis[attacker]
	tar = getdictfromredis[target]

	if atk['location'] == tar['location']:
		tar['ship']['hp'] -= atk['ship']['weapon']['multiplier']
		savedicttoredis(target,tar)


def move(mover: str, newlocation: str) -> None:

	mov = getdictfromredis[mover]
	loc = locationhandler[newlocation]

	if loc['name'] in (locationhandler[mov['location']]['links']):
		mov['location'] = loc['name']
		savedicttoredis(mover,mov)


def collect(collector: str, target:str) -> None:
	col = getdictfromredis[collector]
	tar = getdictfromredis[target]

	if col['location'] == tar['location']:

		if can_fit_item(col['cargo'], tar['weight']):

			add_item(col['cargo'])
			savedicttoredis(collector,col)



# Action Delegator

def doaction(actor: str, action: str, target: str) -> None:

	try:
		actionhandler[action](actor, target)

	except:
		pass


actionhandler = {
	'attack': attack,
	'move': move,
	'collect': collect
}


__all__ = [
	'doaction',
	'actionhandler',
]

