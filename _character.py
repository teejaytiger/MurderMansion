from _inventory import inventory

class character:
    def __init__(self):
        self.name = "Joaroagn"
        self.time_spellcasting = 10
        self.time_crafting = 10
        self.time_book_base = 30
        self.equipped_traps = [(None, None)]
        self.cast_spells = [None]
        self.craft_level = 0
        self.spell_level = 0
        self.murderer_skill = 0.0
        self.attributes = {
            "str":None, ## Struggle - Modifies chance of escaping conflict and performing successful close up attacks and defenses
            "pct":None, ## Perception - Modified chance of identifying hard to see objects or objects that may be of value
            "lck":None, ## Luck - Modifies the chance of getting rare items and performing spells and critical hits, affected by alignment
            "cha":None, ## Charisma - Improves difficulty modifier of certain dialogue actions
            "int":None, ## Intelligence - Improves crafting and spellcasting times
            "hps":70    ## character hit points, recovered with spells, decreased with spells and attacks, 0 is dead, no max
        }
        self.inventory = inventory()

