from spaceship import Ship

# Startup

# 

def Location(name):
    return {
        'name': name,
        'links': set()
    }
    
earth = Location('earth')
mars = Location('mars')

earth['links'].add('mars')
mars['links'].add('earth')

locationhandler = {
    'earth': earth,
    'mars': mars
}



def attack(attacker, target):
    atk = tokenhandler[attacker]
    tar = tokenhandler[target]
    if atk['location'] == tar['location']:
        tar['hp'] -= atk['weapon']['multiplier']

def move(mover, newlocation):
    mov = tokenhandler[mover]
    loc = locationhandler[newlocation]
    if loc['name'] in (locationhandler[mov['location']]['links']):
      mov['location'] = loc['name']

def doaction(actor, action, thing):
  actionhandler[action](actor, thing)

actionhandler = {
  'attack': attack,
  'move': move
}




myship = Ship('earth')
othership = Ship('mars')


tokenhandler = {
    'myship': myship,
    'othership': othership
}
  
print(myship['location'])
doaction('myship', 'move', 'mars')
print(myship['location'])
print(othership['hp'])
doaction('myship', 'attack', 'othership')
print(othership['hp'])