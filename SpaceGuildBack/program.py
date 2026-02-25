"""
- Orchestrates imports from actions and location modules.
- Creates and manages the global DataHandler instance.
- Leaves example usage commented out for now.
"""

import ship
import location
import components
import actions
from data import DataHandler

# Global DataHandler singleton instance
# All modules should import this instance to access game data
data_handler = DataHandler(data_dir="game_data")



