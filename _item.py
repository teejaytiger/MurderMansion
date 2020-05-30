from abc import ABC
import sys
import random
import datetime, pytz
from enum import IntEnum
from _abstr import _abstr, compute, ingredient_name, chars as ch, item_type


"""
Book - read books to gain int
light - you can only read books in rooms with lights
weapon - use to improve struggle
altar - 
ingredient - used together to create spells, traps, weapons, and tools
"""

class _item (_abstr):
    """
    Abstract item class used to 
    """
    def __init__(self):
        ## Defined locally
        self.size = None ## affects where it can be spawned
        self.modifiers = {}
        self.score = 0
        ## Declared in _abstr.py
        ## how many uses before it breaks, -0 for n/a, -1 for ultimate robustness
        self.durability = compute().RANDOMIZE_DURABILITY()
        ## number of instances permitted for each map
        self.rarity = compute.RANDOMIZE_RARITY
        self.timestamp = datetime.datetime.now(pytz.utc).isoformat()
        self.alignment = compute().ALIGNMENT()
        self.name = None
        self.icon = ""
        self.extras = {}

    def __str__(self): 
        wid = 40
        s1 = " {} {} {}".format(self.icon, self.durability.name, self.name.name)
        s2 = "({}, {})".format(self.size.name, self.rarity.name)
        return "".join(
            [ch.DOUBLE_LEFT_TOP]+[ch.DOUBLE_HORIZ_PIPE]*wid+[ch.DOUBLE_RIGHT_TOP]+["\n"]+\
            [ch.DOUBLE_VERTI_PIPE]+[s1]+[" "]*(wid-len(s1))+[ch.DOUBLE_VERTI_PIPE]+["\n"]+\
            [ch.DOUBLE_VERTI_PIPE]+[s2]+[" "]*(wid-len(s2))+[ch.DOUBLE_VERTI_PIPE]+["\n"]+\
            [ch.DOUBLE_LEFT_BOTTOM]+[ch.DOUBLE_HORIZ_PIPE]*wid+[ch.DOUBLE_RIGHT_BOTTOM]
            )
    #def __repr__(self): return "".join([ch.DOUBLE_LEFT_TOP]+[ch.DOUBLE_HORIZ_PIPE]*30+[ch.DOUBLE_RIGHT_TOP])
            

class WEAPON(_item):
    def __init__(self):
        self.modifiers = {}
        self.score = 0
        self.size = compute().RANDOMIZE_SIZE_BOOK()
        self.durability = compute().RANDOMIZE_DURABILITY()
        self.rarity = compute().RANDOMIZE_RARITY()
        self.timestamp = datetime.datetime.now(pytz.utc).isoformat()
        self.alignment = compute().ALIGNMENT()
        self.name = item_type.WEAPON
        self.icon = name.name
        self.extras = {"damage_per_turn":compute().RANDOMIZE_WEAPON_DPS()}
    def __str__(self): return super().__str__()

class BOOK (_item):
    """
    Increses int when read. Bigger books take longer to read, but grant higher int
    Small books perform a special character buff (new spell, new craft, etc)
    """
    def __init__(self):
        self.modifiers = {}
        self.score = 0
        self.size = compute().RANDOMIZE_SIZE_BOOK()
        self.durability = compute().RANDOMIZE_DURABILITY()
        self.rarity = compute().RANDOMIZE_RARITY()
        self.timestamp = datetime.datetime.now(pytz.utc).isoformat()
        self.alignment = compute().ALIGNMENT()
        self.name = item_type.BOOK
        self.icon = ch.BOOK_ICON
    def __str__(self): return super().__str__()
        
class LIGHT (_item):
    """
    Improves pct, and allows books to be read in rooms where a light is present.
    Lamp size affects reading speed. 
    """
    def __init__(self):
        self.modifiers = {}
        self.score = 0
        self.size = compute().RANDOMIZE_SIZE_LAMP()
        self.durability = compute().RANDOMIZE_DURABILITY()
        self.rarity = compute().RANDOMIZE_RARITY()
        self.timestamp = datetime.datetime.now(pytz.utc).isoformat()
        self.alignment = compute().ALIGNMENT()
        self.name = compute().RANDOMIZE_STYLE_LAMP()
        self.icon = ch.LIGHT_ICON
        self.extras = {
            "status":compute().RANDOMIZE_LIGHT_STATUS} # you can only read books in rooms that have lights that are turned on
    def __str__(self): return super().__str__()

class ALTAR (_item):
    """
    Portable item used for spellcrafting. Alignment affects quality of spells. 
    Has a max number of uses based on durability
    """
    def __init__(self):
        self.modifiers = {}
        self.score = 0
        self.size = compute().RANDOMIZE_SIZE_ALTAR()
        self.durability = compute().RANDOMIZE_DURABILITY()
        self.rarity = compute().RANDOMIZE_RARITY()
        self.timestamp = datetime.datetime.now(pytz.utc).isoformat()
        self.alignment = compute().ALIGNMENT()
        self.name = item_type.ALTAR
        self.icon = ch.ALTAR_ICON
    def __str__(self): return super().__str__()

class INGREDIENT(_item):
    """
    Used in spellcasting and weapon crafting
    """
    def __init__(self, name=None):
        self.modifiers = {}
        self.score = 0
        self.size = compute().RANDOMIZE_SIZE_INGREDIENT()
        self.durability = compute().RANDOMIZE_DURABILITY()
        self.rarity = compute().RANDOMIZE_RARITY()
        self.timestamp = datetime.datetime.now(pytz.utc).isoformat()
        self.alignment = compute().ALIGNMENT()
        self.name = compute().RANDOMIZE_INGREDIENT_NAME()
        self.icon = ch.CRAFT_ICON
    def __str__(self): return super().__str__()
        
if __name__ == "__main__":
    books = []
    lights = []
    altars = []
    ingredients = []
    for i in range(0, 1):
        books.append(BOOK())
        lights.append(LIGHT())
        altars.append(ALTAR())
        ingredients.append(INGREDIENT())
    
    for b in books:
        print(b)
    for b in lights:
        print(b)
    for b in altars:
        print(b)
    for b in ingredients:
        print(b)