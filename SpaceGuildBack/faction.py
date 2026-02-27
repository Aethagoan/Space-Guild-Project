# Aidan Orion 24 Feb 2026
# The faction dict creator

# player factions
def Faction():
    return {
        'name':"",
        'player_ids': [],
        'color':"", # hex code
        
    }

# npc factions
def NpcFaction(ID,name="",description="",color=""):
    return {
        'ID':ID,
        'name':name,
        'description':description,
        'color':color,
    }