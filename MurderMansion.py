from _item import BOOK, LIGHT, ALTAR, INGREDIENT, _craft, ingredient_name
from _abstr import craft_engine, item_type, chars as ch, WEAPONS, TOOLS, TRAPS, SPELLS, SPECIAL
from _room import DOOR, room
from _character import character
import random

class MurderMansion:
    def __init__(self):
        self.char = character()

    def RANDOMIZE_CRAFT(
    self,
    craft_type = None,
    craft_name = None,
    effect_funcs = [],
    quantity = ""):
        return _craft(craft_type,craft_name,effect_funcs, quantity)

    def ingredients_by_spell(self, spell):
        return [INGREDIENT(ing_name=ing) for ing in craft_engine().spells[spell][4]]
    def check_spell_prerequisites(self, spell):
        return all(x in [e.name for e in self.char.inventory.ingredients.items+\
                                        self.char.inventory.spells.items+\
                                        self.char.inventory.tools.items+\
                                        self.char.inventory.traps.items] for x in craft_engine().spells[spell][4])

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
        """
            SPELLS.PROTECTION:( "Simple Protection Spell",
            "I can be your hero, baybeh", [1, 0, 0, 0, 0, 0],
                [ACTION.STRUGGLE25], [
                ingredient_name.BOTTLE,
                ingredient_name.LAVENDER,
                ingredient_name.WHITESAGE,
                ingredient_name.SALT,
                ingredient_name.QUARTZ,
                ingredient_name.ROSEPETALS]),
            SPELLS.PROTECTION2:( "Stronger Protection Spell",
            "I can be your hero, baybeh", [2, 0, 0, 0, 0, 0],
                [ACTION.STRUGGLE50], [
                ingredient_name.MOONWATER,
                ingredient_name.ROSEPETALS,
                ingredient_name.QUARTZ,
                ingredient_name.SALT,
                SPELLS.PROTECTION]),
            SPELLS.PROTECTION3:( "Strongest Protection Spell",
            "I can be your hero, baybeh", [3, 0, 0, 0, 0, 0],
                [ACTION.STRUGGLE100], [
                ingredient_name.ADDERSTONE,
                SPELLS.PROTECTION2]),
                """
        # create an inventory with an altar and the ingredients needed for a spell
        m = MurderMansion()
        m.char.inventory.put_away(ALTAR())
        for ingredient in m.ingredients_by_spell(SPELLS.PROTECTION):
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
        print("Items accounted for? {}".format( m.check_spell_prerequisites(SPELLS.PROTECTION) ))
        prot = _craft(craft_type=craft_engine().spells, craft_name=SPELLS.PROTECTION, ingredients_list=m.char.inventory.ingredients.items)
        # This is where you would remove the selected item subset, but we're not doing that here
        # instead, we'll just blow away the whole list and replace it with the new subset
        m.char.inventory.ingredients.items = [] # kabloosh now it's empty
        m.char.inventory.spells.items = [] # kabloosh now it's empty
        # next craft, now without any comments:

        for ingredient in m.ingredients_by_spell(SPELLS.PROTECTION2):
            m.char.inventory.put_away(ingredient)
        for ing in m.char.inventory.ingredients.items:
            if not ing.name in [e for e in ingredient_name]:
                m.char.inventory.throw_away(ing)
        m.char.inventory.put_away(prot) # okay, one comment. This spell requires the craft we made before
        print("Items accounted for? {}".format( m.check_spell_prerequisites(SPELLS.PROTECTION2) ))
        prot2 = _craft(craft_type=craft_engine().spells, craft_name=SPELLS.PROTECTION2, ingredients_list=m.char.inventory.ingredients.items+m.char.inventory.spells.items)
        m.char.inventory.ingredients.items = []
        m.char.inventory.spells.items = []

        # and 3
        for ingredient in m.ingredients_by_spell(SPELLS.PROTECTION2):
            m.char.inventory.put_away(ingredient)
        for ing in m.char.inventory.ingredients.items:
            if not ing.name in [e for e in ingredient_name]:
                m.char.inventory.throw_away(ing)
        m.char.inventory.put_away(prot2) # same thing as before
        print("Items accounted for? {}".format( m.check_spell_prerequisites(SPELLS.PROTECTION3) ))
        prot3 = _craft(craft_type=craft_engine().spells, craft_name=SPELLS.PROTECTION3, ingredients_list=m.char.inventory.ingredients.items+m.char.inventory.spells.items)

        m.char.inventory.put_away(prot) # need to put this back in because we blew away the inventory containing it
        m.char.inventory.put_away(prot3)

        print(m.char.inventory) # should just contain the list from protection3, since I didn't blow that one away, and the three crafts
        # the existence of protection2 proves it works

        #let's try again, but with the wrong ingredients


    test2()
