from abc import ABC
from math import ceil
import sys
import random
import datetime, pytz
from enum import IntEnum
from _abstr import _abstr, compute, ingredient_name, chars as ch, item_type, durability, rarity, craft_engine, color, size


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
    def __init__(self,
    craft_type = None,
    craft_name = None,
    size = size.MEDUIM,
    effect_funcs = [],
    quantity = "",
    ingredients_list = []):
        self.size = size
        self.modifiers = {}
        self.functions = []
        choices = [f for k,f in craft_engine().__dict__.items()]
        self.craft_type = craft_type if craft_type else random.choice(choices) # returns a dictionary
        choices = [k for k in self.craft_type if type(k)!=type("")]
        self.craft_name = random.choice(choices) if not craft_name else craft_name
        self.timestamp = datetime.datetime.now(pytz.utc).isoformat()
        self.effect_funcs = effect_funcs
        self.text, self.subtext, modifiers, self.functions, inglist = self.craft_type[self.craft_name]
        self.craft_type = self.craft_type["type"]
        self.modifiers["str"] = modifiers[0]
        self.modifiers["pct"] = modifiers[1]
        self.modifiers["lck"] = modifiers[2]
        self.modifiers["cha"] = modifiers[3]
        self.modifiers["int"] = modifiers[4]
        self.modifiers["hps"] = modifiers[5]
        self.ingredients = ingredients_list
        if not ingredients_list:
            for ing in inglist:
                randomized = INGREDIENT()
                randomized.name = ing
                self.ingredients.append(randomized)
        else:
            try:
                #print([x.name for x in ingredients_list])
                #print([x for x in inglist])
                assert all(x in [e.name for e in ingredients_list] for x in inglist) # just make sure everything is there

            except:
                print("there was a failure to validate the ingredients list in the craft assembly")

        self.badge = "badge"
        self.quantity = quantity
        self.score = 0
        self.alignment = 0.0
        self.compute_alignment()
        self.compute_score()
        self.name = self.craft_name

    def __str__(self): #TODO fix the explicit pipe characters
        iconmap = {
            item_type.WEAPON:ch.WEAPON_ICON,
            item_type.INGREDIENT:ch.CRAFT_ICON,
            item_type.SPELL:ch.SPELL_ICON,
            item_type.TOOL:ch.TOOL_ICON,
            item_type.TRAP:ch.TRAP_ICON,
            item_type.UNSET:ch.UNSET_ICON,
            item_type.SPECIAL:ch.FULL_STAR}
        wid = max([len(ing.name.name) for ing in self.ingredients])+2
        ing_print = []
        list_item = ""
        for ing in self.ingredients:
            list_item = "+ "+ing.name.name if ing.alignment>=0 else "- "+ing.name.name
            ing_print.append(list_item)
        s = ch.DOUBLE_LEFT_TOP+ch.DOUBLE_HORIZ_PIPE*7+ch.DOUBLE_RIGHT_TOP+"\n"+ch.DOUBLE_VERTI_PIPE+" "*3+\
            color.PURPLE+iconmap[self.craft_type]+color.END+" "*3+ch.DOUBLE_T_LEFT+ch.DOUBLE_HORIZ_PIPE*2+ch.DOUBLE_RIGHT_TOP+" "
        s+= "+ " if self.alignment>=0 else "- "
        #s+= color.BOLD+color.DARKCYAN+self.text+color.END+" ({:.2f})\n".format(self.alignment) # uncomment to display alignment
        s+= color.BOLD+color.DARKCYAN+self.text+color.END+"\n"                                  # comment to display alignment
        s+= "╚╦══════╝  ║ "+color.RED+self.subtext+color.END+"\n"
        s+= " ║         ╚══════════════╗ \n"
        s+= " ║  {0}STR:{1} {2}{3}{4}CHA:{5} {6}{7}║\n".format(
            color.PURPLE, color.END,
            self.modifiers["str"]," "*(6-len(str(self.modifiers["str"]))), 
            color.PURPLE, color.END,
            self.modifiers["cha"]," "*(6-len(str(self.modifiers["cha"]))))
        s+= " ║  {0}PCT:{1} {2}{3}{4}INT:{5} {6}{7}║ {8}{9}{10}\n".format(
            color.PURPLE, color.END,
            self.modifiers["pct"]," "*(6-len(str(self.modifiers["pct"]))), 
            color.PURPLE, color.END,
            self.modifiers["int"]," "*(6-len(str(self.modifiers["int"]))), color.YELLOW, self.badge, color.END)
        s+= " ║  {0}LCK:{1} {2}{3}{4}HPS:{5} {6}{7}╔══╩{8}\n".format(
            color.PURPLE, color.END,
            self.modifiers["lck"]," "*(6-len(str(self.modifiers["lck"]))), 
            color.PURPLE, color.END,
            self.modifiers["hps"]," "*(3-len(str(self.modifiers["hps"]))),
            "═"*wid+"╗")
        ing = ing_print.pop()
        s+= " ╚═════════════════════╣ "+ing+" "*(wid+2-len(ing))+"║\n"
        while ing_print:
            ing = ing_print.pop()
            s+= "                       ║ "+ing+" "*(wid+2-len(ing))+"║\n"
        s+="                       ╚═══"+"═"*wid+"╝"
        return s

    def __repr__(self):
        iconmap = {
            item_type.WEAPON:ch.WEAPON_ICON,
            item_type.INGREDIENT:ch.CRAFT_ICON,
            item_type.SPELL:ch.SPELL_ICON,
            item_type.TOOL:ch.TOOL_ICON,
            item_type.TRAP:ch.TRAP_ICON,
            item_type.UNSET:ch.UNSET_ICON,
            item_type.SPECIAL:ch.FULL_STAR}
        s = ""


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

class BOOK (_item):
    """
    Increses int when read. Bigger books take longer to read, but grant higher int
    Small books perform a special character buff (new spell, new craft, etc)
    """
    def __init__(self):
        self.craft_type = item_type.BOOK
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
        self.craft_type = item_type.LIGHT
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
        self.craft_type = item_type.ALTAR
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
    def __init__(self, ing_name=None):
        self.craft_type = item_type.INGREDIENT
        self.modifiers = {}
        self.size = compute().RANDOMIZE_SIZE_INGREDIENT()
        self.durability = compute().RANDOMIZE_DURABILITY()
        self.rarity = compute().RANDOMIZE_RARITY()
        self.timestamp = datetime.datetime.now(pytz.utc).isoformat()
        self.alignment = compute().ALIGNMENT()
        self.score = super().get_uses()
        self.name = ing_name if ing_name else compute().RANDOMIZE_INGREDIENT_NAME()
        self.icon = ch.CRAFT_ICON
        self.badge = ""
        self.countdown = 1
    def __str__(self): return super().__str__()
        
if __name__ == "__main__":
    books = []
    lights = []
    altars = []
    ingredients = []
    rardict = {
        rarity.COMMON:0,
        rarity.UNUSUAL:0,
        rarity.STRANGE:0,
        rarity.INCREDIBLE:0,
        rarity.IMMACULATE:0,
        rarity.MYTHOLOGICAL:0}
    durdict = {
        durability.FRAGILE:0,
        durability.RAMSHACKLE:0,
        durability.ADEQUATE:0,
        durability.STURDY:0,
        durability.CHONKY:0,
        durability.YOKED:0}
    count = 0
    maxnum = 1000
    for i in range(0, maxnum):
        x = INGREDIENT()
        rardict[x.rarity]+=1
        durdict[x.durability]+=1
        ingredients.append(x)
    print("\n######## RARITY DISTRIBUTION TEST ########")
    for i, j in rardict.items():
        print("{:15s} : {:.2%}".format(i.name, j/maxnum))
    print("\n######## DURABILITY DISTRIBUTION TEST ########")
    for i, j in durdict.items():
        print("{:15s} : {:.2%}".format(i.name, j/maxnum))

    for i in range(0, 5):
        print(ingredients[i])

    # randomize a weapon from craft_engine