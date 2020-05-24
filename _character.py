

class _character:
    def __init__(self):
        self.name = "Joaroagn"
        self.attributes = {
            "str":None, ## Struggle - Modifies chance of escaping conflict and performing successful close up attacks and defenses
            "pct":None, ## Perception - Modified chance of identifying hard to see objects or objects that may be of value
            "lck":None, ## Luck - Modifies the chance of getting rare items and performing spells and critical hits, affected by alignment
            "cha":None, ## Charisma - Improves difficulty modifier of certain dialogue actions
            "int":None, ## Intelligence - Improves crafting and spellcasting ability
            "hps":70    ## character hit points, recovered with spells, decreased with spells and attacks, 0 is dead, no max
        }
        self.inventory = [] ## list of items


    def add2inv(self, item):
        self.inventory += [item]
    
    def display_inv(self):
        for item in self.inventory:

