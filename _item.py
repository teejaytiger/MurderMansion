from abc import ABC
from math import ceil
import sys
import random
import datetime, pytz
from enum import IntEnum
from _abstr import _abstr, compute, ingredient_name, chars as ch, item_type, durability, rarity, craft_engine


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
        self.size = None ## affects where it can be spawned
        self.modifiers = {}
        self.score = 0
        self.durability = durability.FRAGILE
        self.rarity = rarity.COMMON
        self.timestamp = datetime.datetime.now(pytz.utc).isoformat()
        self.alignment = 0
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
            [ch.DOUBLE_LEFT_BOTTOM]+[ch.DOUBLE_HORIZ_PIPE]*wid+[ch.DOUBLE_RIGHT_BOTTOM])
    def get_uses(self):
        fac = (self.durability.value+1)/4 + (self.rarity.value+1)/4
        return ceil(fac + self.alignment*fac)

class _craft(_abstr):
    def __init__(self, item_t=item_type.UNSET):
        self.craft_type = item_t
        self.craft_name = item_t
        self.timestamp = datetime.datetime.now(pytz.utc).isoformat()
        self.modifiers = { # set by the game engine
            "str":None, ## Struggle - Modifies chance of escaping conflict and performing successful close up attacks and defenses
            "pct":None, ## Perception - Modified chance of identifying hard to see objects or objects that may be of value
            "lck":None, ## Luck - Modifies the chance of getting rare items and performing spells and critical hits, affected by alignment
            "cha":None, ## Charisma - Improves difficulty modifier of certain dialogue actions
            "int":None, ## Intelligence - Improves crafting and spellcasting ability
            "hps":70    ## character hit points, recovered with spells, decreased with spells and attacks, 0 is dead, no max
        }
        self.effect_funcs = [] # set by the game engine
        self.ingredients = [] # populated by the craft engine
        self.badge = ""
        self.quantity = ""
        self.text = ""
        self.subtext = ""
        self.compute_alignment()
        self.name = ""
    def __str__(self): 
        iconmap = {
            item_type.WEAPON:ch.WEAPON_ICON,
            item_type.SPELL:ch.SPELL_ICON,
            item_type.TOOL:ch.TOOL_ICON,
            item_type.TRAP:ch.TRAP_ICON,
            item_type.UNSET:ch.UNSET_ICON}
        wid = max([len(ing.name.name) for ing in self.ingredients])+2
        ing_print = []
        for ing in self.ingredients:
            ing_print.append("+ "+ing.name.name) if self.alignment>=0 else ing_print.append("- "+ing.name.name)
        # print(ing_print) # debug
        s = "╔═══════╗\n"+"║   "+\
            iconmap[self.craft_type]+"   ╠══╗ "
        s+= "+ " if self.alignment>=0 else "- "
        s+= self.text+"\n"
        s+= "╚╦══════╝  ║ "+self.subtext+"\n"
        s+= " ║         ╚══════════════╗ {}\n".format(self.badge)
        s+= " ║  STR: {}{}CHA: {}{}║\n".format(
            self.modifiers["str"]," "*(6-len(str(self.modifiers["str"]))), 
            self.modifiers["cha"]," "*(6-len(str(self.modifiers["cha"]))))
        s+= " ║  PCT: {}{}INT: {}{}║ {}\n".format(
            self.modifiers["pct"]," "*(6-len(str(self.modifiers["pct"]))), 
            self.modifiers["int"]," "*(6-len(str(self.modifiers["int"]))), self.badge)
        s+= " ║  LCK: {}{}HPS: {}{}╔══╩{}\n".format(
            self.modifiers["lck"]," "*(6-len(str(self.modifiers["lck"]))), 
            self.modifiers["hps"]," "*(3-len(str(self.modifiers["hps"]))),
            "═"*wid+"╗")
        ing = ing_print.pop()
        s+= " ╚═════════════════════╣ "+ing+" "*(wid+2-len(ing))+"║\n"
        while ing_print:
            ing = ing_print.pop()
            s+= "                       ║ "+ing+" "*(wid+2-len(ing))+"║\n"
        s+="                       ╚═══"+"═"*wid+"╝"
            
        return s

    def compute_alignment(self):
        total = 0.0
        for ingredient in self.ingredients:
            total+=ingredient.alignment
        if self.ingredients: self.alignment = total/len(self.ingredients)
        else: self.alignment = -1
    def compute_score(self):
        total = 0.0
        for ingredient in self.ingredients:
            total+=ingredient.score
        if self.ingredients: self.score = total/len(self.ingredients)
    def compute_damage(self):
        return self.score*ceil((self.alignment+self.score)//2+(self.rarity.value+1))
    def randomize(self):
        self.timestamp = datetime.datetime.now(pytz.utc).isoformat()
        self.compute_alignment()
        self.modifiers = { # set by the game engine
            "str":random.randrange(-1, 2), ## Struggle - Modifies chance of escaping conflict and performing successful close up attacks and defenses
            "pct":random.randrange(-1, 2), ## Perception - Modified chance of identifying hard to see objects or objects that may be of value
            "lck":random.randrange(-1, 2), ## Luck - Modifies the chance of getting rare items and performing spells and critical hits, affected by alignment
            "cha":random.randrange(-1, 2), ## Charisma - Improves difficulty modifier of certain dialogue actions
            "int":random.randrange(-1, 2), ## Intelligence - Improves crafting and spellcasting ability
            "hps":random.randrange(-1, 2)    ## character hit points, recovered with spells, decreased with spells and attacks, 0 is dead, no max
        }
        for i in range(0, random.randrange(2, 5)):
            self.ingredients.append(INGREDIENT())
        self.badge = ""
        self.quantity = 0


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
        self.badge = str(random.choice([6, 7, 8, 9, 10]))+"s" # time to reads
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
    def __init__(self):
        self.modifiers = {}
        self.size = compute().RANDOMIZE_SIZE_INGREDIENT()
        self.durability = compute().RANDOMIZE_DURABILITY()
        self.rarity = compute().RANDOMIZE_RARITY()
        self.timestamp = datetime.datetime.now(pytz.utc).isoformat()
        self.alignment = compute().ALIGNMENT()
        self.score = super().get_uses()
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
    for i in range(0, 1):
        books.append(BOOK())
        lights.append(LIGHT())
        altars.append(ALTAR())
    for i in range(0, 30):
        ingredients.append(INGREDIENT())
    
    for b in books:
        print(b)
    for b in lights:
        print(b)
    for b in altars:
        print(b)
    for b in ingredients:
        print(b)

    # randomize a weapon from craft_engine