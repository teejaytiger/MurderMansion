from _item import BOOK, LIGHT, ALTAR, INGREDIENT, _craft, ingredient_name
from _abstr import craft_engine, item_type, chars as ch, WEAPONS, TOOLS, TRAPS, SPELLS, SPECIAL
from _room import DOOR, room
from _character import character
from _crafting import crafting
import random

class MurderMansion:
    def __init__(self):
        self.char = character()
        self.crafter = crafting()

        self.room = room()
        self.room_history = []

    def next_room(self):
        self.room_history.append(self.room)
        self.room = room()
        return self.room

    def struggle(self):
        pass

class specials:
    def __init__(self):
        pass

if __name__ == "__main__":

    def test1():
        m = MurderMansion()
        for i in range(0, 4):
            print(_craft(craft_type=craft_engine().spells))
        print(_craft(craft_type=craft_engine().tools))
        print(_craft(craft_type=craft_engine().traps))
        print(_craft(craft_type=craft_engine().weapons))

        print(_craft(craft_type=craft_engine().spells, craft_name=SPELLS.INTROSPECTION))
        c = _craft(craft_type=craft_engine().spells, craft_name=SPELLS.DUPLICATION)
        print(c)
        for i in c.functions: print(i)
        #print(_craft(craft_type=craft_engine().special, craft_name=SPECIAL.SUCTIONCUPDILDO))

    def test2():
        # create an inventory with an altar and the ingredients needed for a spell
        m = MurderMansion()
        m.char.inventory.put_away(ALTAR())
        for ingredient in m.crafter.ingredients_by_spell(SPELLS.PROTECTION):
            m.char.inventory.put_away(ingredient)
        # this causes the side effect of adding craft names as ingredients, they should be ignored or removed
        # test remove
        for ing in m.char.inventory.ingredients.items:
            # check items against the ingredient list
            if not ing.name in [e for e in ingredient_name]:
                # throw away everything that isn't an ingredient
                m.char.inventory.throw_away(ing)
        # now that everything is cleaned up, craft the spells!
        # hand the sublist of selected ingredients to the craft engine.
        print("Items accounted for? {}".format( m.crafter.check_spell_prerequisites(m.char.inventory, SPELLS.PROTECTION) ))
        prot = _craft(craft_type=craft_engine().spells, craft_name=SPELLS.PROTECTION, 
            ingredients_list=\
                m.char.inventory.ingredients.items+\
                m.char.inventory.spells.items)
        # This is where you would remove the selected item subset, but we're not doing that here
        # instead, we'll just blow away the whole list and replace it with the new subset
        m.char.inventory.ingredients.items = [] # kabloosh now it's empty
        m.char.inventory.spells.items = [] # kabloosh now it's empty
        # next craft, now without any comments:

        for ingredient in m.crafter.ingredients_by_spell(SPELLS.PROTECTION2):
            m.char.inventory.put_away(ingredient)
        for ing in m.char.inventory.ingredients.items:
            if not ing.name in [e for e in ingredient_name]:
                m.char.inventory.throw_away(ing)
        m.char.inventory.put_away(prot) # okay, one comment. This spell requires the craft we made before
        print("Items accounted for? {}".format( m.crafter.check_spell_prerequisites(m.char.inventory, SPELLS.PROTECTION2) ))
        prot2 = _craft(craft_type=craft_engine().spells, craft_name=SPELLS.PROTECTION2, 
            ingredients_list=\
                m.char.inventory.ingredients.items+\
                m.char.inventory.spells.items)
        m.char.inventory.ingredients.items = []
        m.char.inventory.spells.items = []

        # and 3
        for ingredient in m.crafter.ingredients_by_spell(SPELLS.PROTECTION3):
            m.char.inventory.put_away(ingredient)
        for ing in m.char.inventory.ingredients.items:
            if not ing.name in [e for e in ingredient_name]:
                m.char.inventory.throw_away(ing)
        m.char.inventory.put_away(prot2) # same thing as before
        print("Items accounted for? {}".format( m.crafter.check_spell_prerequisites(m.char.inventory, SPELLS.PROTECTION3) ))
        prot3 = _craft(craft_type=craft_engine().spells, craft_name=SPELLS.PROTECTION3, 
            ingredients_list=\
                m.char.inventory.ingredients.items+\
                m.char.inventory.spells.items)

        m.char.inventory.put_away(prot) # need to put this back in because we blew away the inventory containing it
        m.char.inventory.put_away(prot3)

        print(m.char.inventory) # should just contain the list from protection3, since I didn't blow that one away, and the three crafts
        # the existence of protection2 proves it works

        #let's try again, but with the wrong ingredients

    def test3():
        # Same things as test2, but better and closer to a use casew
        m = MurderMansion()
        # Use the crafting classes in this test
        c = crafting()
        # populate inventory with everything you need
        for ingredient in m.crafter.ingredients_by_spell(SPELLS.PROTECTION): c.select(ingredient)
        c.select(ALTAR())
        new_craft = c.craft(craft_engine().spells, SPELLS.PROTECTION)
        if new_craft: 
            c.select(new_craft)
            m.char.inventory.put_away(new_craft)
        for ingredient in m.crafter.ingredients_by_spell(SPELLS.PROTECTION2): c.select(ingredient)
        c.select(ALTAR())
        new_craft = c.craft(craft_engine().spells, SPELLS.PROTECTION2)
        if new_craft: 
            c.select(new_craft)
            m.char.inventory.put_away(new_craft)
        for ingredient in m.crafter.ingredients_by_spell(SPELLS.PROTECTION3): c.select(ingredient)
        c.select(ALTAR())
        new_craft = c.craft(craft_engine().spells, SPELLS.PROTECTION3)
        if new_craft: 
            c.select(new_craft)
            m.char.inventory.put_away(new_craft)
        print(m.char.inventory)


        

    test3()
