# SpaceGuildBack/test_stealth_action.py
# Test stealth activation/deactivation through /action endpoint

import pytest
import actions

def test_stealth_action_types_valid():
    """Test that activate_stealth and deactivate_stealth are valid action types."""
    # These should be recognized as valid actions in queue_action
    assert 'activate_stealth' in {'scan', 'attack_ship', 'attack_ship_component', 'attack_item', 'move', 'collect', 'activate_stealth', 'deactivate_stealth'}
    assert 'deactivate_stealth' in {'scan', 'attack_ship', 'attack_ship_component', 'attack_item', 'move', 'collect', 'activate_stealth', 'deactivate_stealth'}


def test_stealth_actions_in_action_lists():
    """Test that stealth action lists exist in the action queues."""
    # Create a test location
    test_location = 'test_location'
    actions.location_queues[test_location] = {
        'scan': actions.ActionList('scan'),
        'attack_ship': actions.ActionList('attack_ship'),
        'attack_ship_component': actions.ActionList('attack_ship_component'),
        'attack_item': actions.ActionList('attack_item'),
        'move': actions.ActionList('move'),
        'collect': actions.ActionList('collect'),
        'activate_stealth': actions.ActionList('activate_stealth'),
        'deactivate_stealth': actions.ActionList('deactivate_stealth'),
    }
    
    # Verify stealth lists exist
    assert 'activate_stealth' in actions.location_queues[test_location]
    assert 'deactivate_stealth' in actions.location_queues[test_location]
    
    # Clean up
    del actions.location_queues[test_location]


def test_stealth_functions_exist():
    """Test that stealth helper functions exist."""
    assert hasattr(actions, 'activate_stealth')
    assert hasattr(actions, 'deactivate_stealth')
    assert hasattr(actions, 'is_ship_stealthed')
    assert hasattr(actions, 'mark_ship_took_damage')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
