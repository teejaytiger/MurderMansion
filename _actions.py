"""
Speaking to someone
interacting with an object
analyzing a room
hiding something
performing a spell
wishing
"""

#from _abstr import ACTION
import random
from functools import partial
from _inventory import inventory
from _character import character
from _abstr import item_type, ingredient_name, TRAPS, ACTION, craft_engine

class action:
    def __init__(self, character):
        self.me = character
        self.map = {
            ACTION.STARTTRADE : self.trade_initiation,
            ACTION.FUCK : self.fuck,
            ACTION.MURDER : self.murder,
            ACTION.GETFREETRAP : partial(self.free,item_type.TRAP),
            ACTION.GETFREETOOL : partial(self.free,item_type.TOOL),
            ACTION.GETFREESPELL : partial(self.free,item_type.SPELL),
            ACTION.GETFREECRAFTLEVEL : partial(self.free_level,"craft"),
            ACTION.GETFREESPELLLEVEL : partial(self.free_level,"spell"),
            ACTION.GETFREEITEM : partial(self.free,item_type.UNSET), # free random craft
            ACTION.GETFREEING : partial(self.free,item_type.INGREDIENT), # gifts a free ingredient
            ACTION.GETFREEWEAPON : partial(self.free,item_type.WEAPON),
            # Gen 100->score->pick highest item
            ACTION.INCREASEINT : partial(self.increase,"int"),
            ACTION.INCREASECHA : partial(self.increase,"cha"),
            ACTION.INCREASESTR : partial(self.increase,"str"),
            ACTION.INCREASELCK : partial(self.increase,"lck"),
            ACTION.INCREASEPCT : partial(self.increase,"pct"),
            ACTION.INCREASEUNK : self.increase, # for custom increases
            # Specific Character Actions
            ACTION.SANTAEFFECT : partial(self.init_special,"santa"), # function should have a "code=" keyword to multiplex specific instructions to helpers
            ACTION.DILDOEFFECT : partial(self.init_special,"dildo"),
            ACTION.MARCUSEFFECT : partial(self.init_special,"marcus"),
            ACTION.CUSTOMEFFECT : self.init_special,
            # Specific functions for jokes
            ACTION.GIVESASH : partial(self.free,item_type.INGREDIENT, item_name=ingredient_name.ASH),
            ACTION.HONEYPOT : partial(self.free,item_type.TRAP, item_name=TRAPS.HONEYPOT),
            # MECHANIC FUNCTIONS
            ACTION.SUPPRESSAMBUSHALL : partial(self.neutralize_door,"000"), # all doors don't spawn murderer, one hot code for door danger
            ACTION.STRUGGLE50 : partial(self.impact_next_struggle,factor=50),
            ACTION.STRUGGLE25 : partial(self.impact_next_struggle,factor=25),
            ACTION.STRUGGLE75 : partial(self.impact_next_struggle,factor=75),
            ACTION.STRUGGLE100 : partial(self.impact_next_struggle,factor=100),
        }

    def do(self, action, *args, **kwargs):
        return self.map[action](*args, **kwargs)

    def trade_initiation(self):
        pass

    def fuck(self):
        pass

    def murder(self):
        pass

    def free(self, item_type, item_name=None):
        pass

    def free_level(self, level_type):
        "returns a character with +1 level in crafting or spells"
        if level_type == "craft":
            self.me.craft_level+=1
        if level_type == "spell":
            self.me.spell_level+=1
        return self.me
    
    def increase(self, status, amount=1):
        """increases a character attribute status (string)"""
        pass

    def init_special(self, special):
        pass

    def neutralize_door(self, code):
        pass

    def impact_next_struggle(self, factor=1):
        pass

    def read(self, book):
        pass

    def set_trap(self, trap):
        pass

    def cast(self, spell):
        pass

    def struggle(self):
        pass

    def use_tool(self, tool):
        pass

    def craft(self):
        pass

if __name__ == "__main__":
    a = action(character())
    a.do(ACTION.GETFREESPELLLEVEL)
    print (a.me.spell_level)