

class Location(canMove):
    def __init__(self):
        self.links:Location = []
        # self.player_tokens:str = []

    def add_link(self, location):
        self.links.append(location)

    def remove_link(self, location):
        if location in self.links:
            self.links.remove(location)

    # def receive_token(self, token):
    #     self.player_tokens.append(token)

    # def move(self, token, destination):
    #     if destination in self.links and token in self.player_tokens:
    #         self.player_tokens.remove(token)
    #         destination.receive_token(token)





class Orbit(Location,canScan,canAttack):
    pass

class Station(Location,canRepair,canMarket):
    pass

class Resource(Location,canGather,canScan):
    pass





class canScan:
    pass

class canGather:
    @staticmethod
    def gather():
        pass

class canAttack:
    @staticmethod
    def attack():
        pass

class canRepair:
    @staticmethod
    def repair():
        pass

class canMissions:
    def missions(self):
        print("printing missions!")

class canMarket:
    @staticmethod
    def market():
        pass

