from _item import BOOK, LIGHT, ALTAR, INGREDIENT, _craft
from _abstr import craft_engine, item_type, chars as ch, WEAPONS, TOOLS, TRAPS, SPELLS
import random

class _:
    def __init__(self):
        pass

    def RANDOMIZE_CRAFT(self, 
    craft_type=craft_engine().spells, 
    craft_name=None):
        # pick an item at random
        s = ""
        gap = 60
        if not craft_name: craft_name = random.choice([e for e in craft_type])
        craft = _craft() # set the craft type
        craft.randomize()
        craft.ingredients = []
        craft.text, craft.subtext, modifiers, inglist = craft_type[craft_name] # assign the text and subtext from the craft prototype
        craft.craft_type = craft_type["type"]
        # print(inglist) # debug

        # set the modifiers
        craft.modifiers["str"] = modifiers[0]
        craft.modifiers["pct"] = modifiers[1]
        craft.modifiers["lck"] = modifiers[2]
        craft.modifiers["cha"] = modifiers[3]
        craft.modifiers["int"] = modifiers[4]
        craft.modifiers["hps"] = modifiers[5]

        # create the ingredients randomized
        for ing in inglist:
            randomized = INGREDIENT()
            randomized.name = ing
            craft.ingredients.append(randomized) # add the ingredients to the craft list
        # print([i.name for i in craft.ingredients]) # debug

        for att, tex in craft.modifiers.items():
            s += "{}: {}\n".format(att, tex)

        # compute the alignment and score from the ingredients
        craft.compute_score()
        craft.compute_alignment()

        for i in craft.ingredients: s += i.__str__()+"\n" # debug ing build
        s = "CRAFT: {}\n{}\n{}\n{}\n{}\n".format(
            craft_name.name, 
            craft.text, 
            craft.subtext,
            craft.score,
            craft.alignment)+s
        # print(s) # debug
        print(craft)

        s2 = ch.DOUBLE_LEFT_TOP+ch.DOUBLE_HORIZ_PIPE*gap+ch.DOUBLE_RIGHT_TOP+"\n"
        for i in s.split("\n"):
            s2+=ch.DOUBLE_VERTI_PIPE+i+" "*(gap-len(i))+ch.DOUBLE_VERTI_PIPE+"\n"
        s2 += ch.DOUBLE_LEFT_BOTTOM+ch.DOUBLE_HORIZ_PIPE*gap+ch.DOUBLE_RIGHT_BOTTOM+"\n"
        # return s2

if __name__ == "__main__":
    m = MurderMansion()
    print(m.RANDOMIZE_CRAFT(craft_type=craft_engine().spells))
    print(m.RANDOMIZE_CRAFT(craft_type=craft_engine().tools))
    print(m.RANDOMIZE_CRAFT(craft_type=craft_engine().traps))
    print(m.RANDOMIZE_CRAFT(craft_type=craft_engine().weapons))
    print(m.RANDOMIZE_CRAFT(craft_type=craft_engine().weapons, craft_name=WEAPONS.THEGREY))