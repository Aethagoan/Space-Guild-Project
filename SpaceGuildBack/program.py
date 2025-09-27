"""
LLM-Dev v1: program module after refactor
- Orchestrates imports from actions and location modules.
- Leaves example usage commented out for now.
"""

from spaceship import Ship  # existing import kept if used elsewhere

# Import the refactored modules (prefer relative; fallback to absolute for direct runs)
try:
	from .location import locationhandler, Location  # type: ignore
	from .actions import attack, move, doaction, actionhandler, tokenhandler  # type: ignore
except ImportError:  # pragma: no cover
	from location import locationhandler, Location  # type: ignore
	from actions import attack, move, doaction, actionhandler, tokenhandler  # type: ignore


# Example usage (kept commented)
# myship = Ship('earth')
# othership = Ship('mars')
# tokenhandler['myship'] = {
#     'location': 'earth',
#     'hp': 100,
#     'weapon': {'multiplier': 10},
# }
# tokenhandler['othership'] = {
#     'location': 'mars',
#     'hp': 100,
#     'weapon': {'multiplier': 8},
# }
# print(tokenhandler['myship']['location'])
# doaction('myship', 'move', 'mars')
# print(tokenhandler['myship']['location'])
# print(othership['hp'])
# doaction('myship', 'attack', 'othership')
# print(othership['hp'])