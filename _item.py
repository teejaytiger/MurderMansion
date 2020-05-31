from abc import ABC
from math import ceil
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
        self.badge = ""
        self.countdown = ""

    def __str__(self): 
        wid = 40
        s1 = " {} {} {}".format(self.icon, self.durability.name, self.name.name)
        s2 = "({}, {})".format(self.size.name, self.rarity.name)
        g1 = wid-len(s1)-len(str(self.badge))
        g2 = wid-len(s2)-len(str(self.countdown))
        return "".join(
            [ch.DOUBLE_LEFT_TOP]+[ch.DOUBLE_HORIZ_PIPE]*wid+[ch.DOUBLE_RIGHT_TOP]+["\n"]+\
            [ch.DOUBLE_VERTI_PIPE]+[s1]+[" "]*g1+[str(self.badge), ch.DOUBLE_VERTI_PIPE]+["\n"]+\
            [ch.DOUBLE_VERTI_PIPE]+[s2]+[" "]*g2+[str(self.countdown), ch.DOUBLE_VERTI_PIPE]+["\n"]+\
            [ch.DOUBLE_LEFT_BOTTOM]+[ch.DOUBLE_HORIZ_PIPE]*wid+[ch.DOUBLE_RIGHT_BOTTOM]
            )
    #def __repr__(self): return "".join([ch.DOUBLE_LEFT_TOP]+[ch.DOUBLE_HORIZ_PIPE]*30+[ch.DOUBLE_RIGHT_TOP])
    def get_uses(self):
        fac = (self.durability.value+1)/4 + (self.rarity.value+1)/4
        return ceil(fac + self.alignment*fac)
        
class WEAPON(_item):
    def __init__(self):
        self.modifiers = {}
        self.size = compute().RANDOMIZE_SIZE_BOOK()
        self.durability = compute().RANDOMIZE_DURABILITY()
        self.rarity = compute().RANDOMIZE_RARITY()
        self.timestamp = datetime.datetime.now(pytz.utc).isoformat()
        self.alignment = compute().ALIGNMENT()
        self.name = compute().RANDOMIZE_WEAPON_NAME()
        self.icon = ch.SWORD_ICON
        self.extras = {"damage_per_turn":compute().RANDOMIZE_WEAPON_DPS()}
        self.score = self.get_uses()
        self.badge = "DPS "+str(self.compute_dps())
        self.countdown = self.score
    def __str__(self): return super().__str__()
    def get_uses(self): return super().get_uses()
    def compute_dps(self): return self.score*ceil((self.alignment+self.score)//2+(self.rarity.value+1))

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
        self.badge = str(random.choice([6, 7, 8, 9, 10]))+"s"
        self.countdown = 1
    def __str__(self): return super().__str__()
    def time_to_read(self): pass
    def quality(self): pass
        
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
        self.status = compute().RANDOMIZE_LIGHT_STATUS().value
        self.badge = ["off", "on"][self.status]
        self.countdown = ""
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
        self.badge = ""
        self.countdown = str(self.get_uses())
    def __str__(self): return super().__str__()
    def get_uses(self): return super().get_uses()

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
        self.badge = ""
        self.countdown = 1
    def __str__(self): return super().__str__()
        
if __name__ == "__main__":
    books = []
    lights = []
    altars = []
    ingredients = []
    weapons = []
    for i in range(0, 1):
        books.append(BOOK())
        lights.append(LIGHT())
        altars.append(ALTAR())
        ingredients.append(INGREDIENT())
        weapons.append(WEAPON())
    
    for b in books:
        print(b)
    for b in lights:
        print(b)
    for b in altars:
        print(b)
    for b in ingredients:
        print(b)
    for b in weapons:
        print(b)
    for i in range(0, 20):
        w = WEAPON()
        #print("(Alignment + item score)/2 + (rarity + 1)")
        #print ("DPS: ({}+{})/2+({}+1) = {}".format(w.alignment, w.score, w.rarity.value, w.compute_dps()))
        print(w)