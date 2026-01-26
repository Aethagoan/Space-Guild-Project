# request_handler.py

player_actions: Dict[str, str] = {}

def handle_request(player_token:str, action:str):
    player_actions.add((player_token, action))