class canScan:
    @staticmethod
    def scan():
        pass

class canGather:
    @staticmethod
    def gather():
        pass

class canAttack:
    @staticmethod
    def attack():
        pass

class canMove:
    @staticmethod
    def move(token, destination):
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

class StationCanMove(canMove):
    pass

class StationCanMarket(StationCanMove):
    pass