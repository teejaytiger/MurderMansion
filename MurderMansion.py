from _item import BOOK, LIGHT, ALTAR, INGREDIENT, _craft
from _abstr import craft_engine, item_type, chars as ch, WEAPONS, TOOLS, TRAPS, SPELLS
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
    print(m.RANDOMIZE_CRAFT())
    print(m.RANDOMIZE_CRAFT(craft_type=craft_engine().spells))
    print(m.RANDOMIZE_CRAFT(craft_type=craft_engine().tools))
    print(m.RANDOMIZE_CRAFT(craft_type=craft_engine().traps))
    print(m.RANDOMIZE_CRAFT(craft_type=craft_engine().weapons))
    print(m.RANDOMIZE_CRAFT(craft_type=craft_engine().weapons, craft_name=WEAPONS.THEGREY))