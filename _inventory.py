from _abstr import item_type
from _item import _craft, BOOK, LIGHT, ALTAR, INGREDIENT
import random

class inventory:
    def __init__(self):
        self.books = books()
        self.weapons = weapons()
        self.altars = altars()
        self.spells = spells()
        self.traps = traps()
        self.tools = tools()
        self.ingredients = ingredients()

        self.max_weight = 30
        self.current_weight = 0
    
    def categorize(self):
        return {
            item_type.BOOK:self.books,
            item_type.WEAPON:self.weapons,
            item_type.ALTAR:self.altars,
            item_type.SPELL:self.spells,
            item_type.TRAP:self.traps,
            item_type.TOOL:self.tools,
            item_type.INGREDIENT:self.ingredients}

    def put_away(self, item):
        if self.max_weight < item.size.value+self.current_weight:
            return 0
        self.categorize()[item.craft_type].items.append(item)
        self.current_weight+=item.size.value
        return 1

    def throw_away(self, item):
        self.categorize()[item.craft_type].items.remove(item)
        self.current_weight-=item.size.value

    def refresh_weight(self):
        pass #TODO: weigh everything
    
    def show_subinv(self, type):
        print(self.categorize()[type])

    def __str__(self):
        s = ""
        s+= "\n"+self.books.__str__()
        s+= "\n"+self.weapons.__str__()
        s+= "\n"+self.altars.__str__()
        s+= "\n"+self.spells.__str__()
        s+= "\n"+self.traps.__str__()
        s+= "\n"+self.tools.__str__()
        s+= "\n"+self.ingredients.__str__()
        return s

class books:
    def __init__(self): self.items = []
    def __str__(self): return "Books:\n"+"\n".join([e.__str__() for e in self.items])
class weapons:
    def __init__(self): self.items = []
    def __str__(self): return "weapons:\n"+"\n".join([e.__str__() for e in self.items])
class altars:
    def __init__(self): self.items = []
    def __str__(self): return "altars:\n"+"\n".join([e.__str__() for e in self.items])
class spells:
    def __init__(self): self.items = []
    def __str__(self): return "spells:\n"+"\n".join([e.__str__() for e in self.items])
class traps:
    def __init__(self): self.items = []
    def __str__(self): return "traps:\n"+"\n".join([e.__str__() for e in self.items])
class tools:
    def __init__(self): self.items = []
    def __str__(self): return "tools:\n"+"\n".join([e.__str__() for e in self.items])
class ingredients:
    def __init__(self): self.items = []
    def __str__(self): return "ingredients:\n"+"\n".join([e.__str__() for e in self.items])

if __name__ == "__main__":
    inv = inventory()
    for i in range(0, 10):
        c = _craft()
        print(c)
        if not inv.put_away(c):
            print("didn't go in")
    for i in range(0, 10):
        c = random.choice( [BOOK(), ALTAR(), INGREDIENT()] )
        if not inv.put_away(c):
            print("didn't go in")
    print(inv.current_weight)

    inv.show_subinv(item_type.WEAPON)