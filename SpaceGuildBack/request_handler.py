# request_handler.py

# per tick, one token can do one thing
player_actions: dict[str,(str,str)]

def handle_request(player_token:str, action:str, target:str):
    player_actions.add((player_token, (action, target)))