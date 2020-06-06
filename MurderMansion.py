from _item import BOOK, LIGHT, ALTAR, INGREDIENT, _craft
from _abstr import craft_engine, item_type, chars as ch, WEAPONS, TOOLS, TRAPS, SPELLS, SPECIAL
from _room import DOOR, room
import random

class MurderMansion:
    def __init__(self):
        pass

    def RANDOMIZE_CRAFT(
    self,
    craft_type = None,
    craft_name = None,
    effect_funcs = [],
    quantity = ""):
        return _craft(craft_type,craft_name,effect_funcs, quantity)

if __name__ == "__main__":
    m = MurderMansion()
    for i in range(0, 4):
        print(_craft(craft_type=craft_engine().spells))
    print(_craft(craft_type=craft_engine().tools))
    print(_craft(craft_type=craft_engine().traps))
    print(_craft(craft_type=craft_engine().weapons))

    #print(_craft(craft_type=craft_engine().spells, craft_name=SPELLS.SMOKEBRINGER))
    #print(_craft(craft_type=craft_engine().special, craft_name=SPECIAL.SUCTIONCUPDILDO))