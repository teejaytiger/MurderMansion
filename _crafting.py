from _abstr import craft_engine, ingredient_name
from _item import _craft, INGREDIENT, ALTAR

class crafting:
    def __init__(self):
        self.selected = []
        self.ALTARTYPE = type(ALTAR())

    def RANDOMIZE_CRAFT(
        self,
        craft_type = None,
        craft_name = None,
        effect_funcs = [],
        quantity = ""):
        return _craft(craft_type,craft_name,effect_funcs, quantity)

    def ingredients_by_spell(self, spell):
        """Returns a list of constructed ingredients based on the spell requirements"""
        return [INGREDIENT(ing_name=ing) for ing in craft_engine().spells[spell][4] if type(ing)==type(ingredient_name.ADDERSTONE)]

    def ingredients_by_name(self, item_type, item_name):
        """Returns a list of constructed ingredients based on the item_type dict"""
        return [INGREDIENT(ing_name=ing) for ing in item_type[item_name][4] if type(ing)==type(ingredient_name.ADDERSTONE)]

    def select(self, item):
        self.selected.append(item)

    def check_spell_prerequisites(self, item_type, item_name):
        """
        Function returns True if altar + required inventory items present, otherwise returns False

        :param item_type: craft_engine subtype dict
        :param item_name: _abstr enum (e.g. SPELLS.WISHFORHELP)
        """
        # can't craft spells without an altar
        if item_type == craft_engine().spells:
            if not self.ALTARTYPE in [type(i) for i in self.selected]:
                return False
        # altar, but missing ingredients
        return all(x in [e.name for e in self.selected] for x in item_type[item_name][4])

    def craft(self, item_type, item_name):
        """
        Wraps the _craft() constructor with inventory checks

        :param item_type: craft_engine subtype dict
        :param item_name: _abstr enum (e.g. SPELLS.WISHFORHELP)
        """
        # check spell prerequisites and altar existence
        new_craft = None
        if self.check_spell_prerequisites(item_type, item_name):
            new_craft = _craft(craft_type=item_type, craft_name=item_name, ingredients_list=self.selected)
        self.selected = []
        return new_craft