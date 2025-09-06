class Location:
    def __init__(self):
        self.links:Location = []
        self.player_tokens:str = []

    def add_link(self, location):
        self.links.append(location)

    def remove_link(self, location):
        if location in self.links:
            self.links.remove(location)

    def receive_token(self, token):
        self.player_tokens.append(token)

    def move(self, token, destination):
        if destination in self.links and token in self.player_tokens:
            self.player_tokens.remove(token)
            destination.receive_token(token)


class Orbit(Location):
    pass


class Station(Location):
    pass