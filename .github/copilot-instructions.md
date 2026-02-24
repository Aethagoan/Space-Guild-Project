for human hands only do not touch {

Use maintainable code. If you write a function, make it only have one purpose with no side effects.
DO NOT edit the human hands only section of the copilot-instructions.md file.

Update the copilot-instructions in short form for important discoveries and bug fixes as well as short hand knowledge towards best security practices and decisions.

Architecture stack
front end - html, javascript, css.
backend - python, postgresql with UNLOGGED tables for speed, and for use as storage.


}


for use by copilot {

Core Tables
player
  id (PK)
  username (unique)
  password_hash
  email
  created_at
  faction_id (FK to factions, nullable)

faction
  id (PK)
  name (unique)
  symbol
  color
  description

location
  id (PK)
  name
  description
  artwork

location_link (association table for location connections)
  from_location_id (FK to locations)
  to_location_id (FK to locations)

item
  id (PK)
  name
  description
  type
  properties (JSONB)

spaceship
  id (PK)
  player_id (FK to players)
  name
  location_id (FK to locations)
  ship_type
  created_at

spaceship_component
  id (PK)
  name

spaceship_component_link
  spaceship_id (FK to spaceships)
  component_id (FK to spaceship_components)
  slot
  status
  PRIMARY KEY (spaceship_id, component_id, slot)


UNLOGGED Tables (for high-churn, transient data)

ship_state (UNLOGGED)
  ship_id (FK to spaceships)
  player_id (FK to players)
  health
  status_effects (JSONB)
  PRIMARY KEY (ship_id)

ship_component (UNLOGGED)
  

ship_cargo (UNLOGGED)
  ship_id (FK to spaceships)
  item_id (FK to items)
  quantity
  PRIMARY KEY (ship_id, item_id)

}