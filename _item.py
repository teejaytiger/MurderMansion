from abc import ABC
import random
import datetime, pytz
from enum import IntEnum
from _abstr import _abstr, compute, ingredient_name


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
        self.size ## affects where it can be spawned
        self.modifiers
        self.score
        ## Declared in _abstr.py
        ## how many uses before it breaks, -0 for n/a, -1 for ultimate robustness
        self.durability = compute().RANDOMIZE_DURABILITY()
        ## number of instances permitted for each map
        self.rarity = compute.RANDOMIZE_RARITY
        self.timestamp = datetime.datetime.now(pytz.utc).isoformat()
        self.alignment = compute().ALIGNMENT()

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
        self.status = False # you can only read books in rooms that have lights that are turned on

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
        self.max_uses = self.durability.value

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
        self.name = name
        if not name:
            self.name = compute().RANDOMIZE_INGREDIENT_NAME()
        

if __name__ == "__main__":
    books = []
    lights = []
    altars = []
    ingredients = []
    for i in range(0, 10):
        books.append(BOOK())
        lights.append(LIGHT())
        altars.append(ALTAR())
        ingredients.append(INGREDIENT())
    
    for b in books:
        print("--------book------------")
        print("size: {0}\ndblt: {1}\nrare: {2}\ngood: {3}".format(
            b.size.name, b.durability.name, b.rarity.name, b.alignment))
    for b in lights:
        print("--------light-----------")
        print("size: {0}\ndblt: {1}\nrare: {2}\ngood: {3}\nstat: {4}".format(
            b.size.name, b.durability.name, b.rarity.name, b.alignment, b.status))
    for b in altars:
        print("--------altar-----------")
        print("size: {0}\ndblt: {1}\nrare: {2}\ngood: {3}\nuses: {4}".format(
            b.size.name, b.durability.name, b.rarity.name, b.alignment, b.max_uses))
    for b in ingredients:
        print("--------ingredient------")
        print("size: {0}\ndblt: {1}\nrare: {2}\ngood: {3}\nname: {4}".format(
            b.size.name, b.durability.name, b.rarity.name, b.alignment, b.name.name))