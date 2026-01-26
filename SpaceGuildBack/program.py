"""
LLM-Dev v1: program module after refactor
- Orchestrates imports from actions and location modules.
- Leaves example usage commented out for now.
"""

import spaceship
import location
import spaceshipComponent
import actions





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