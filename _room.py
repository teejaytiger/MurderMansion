from _item import BOOK, LIGHT, ALTAR, INGREDIENT
from _abstr import container as c
from _abstr import size, compute, room_type
import random
from enum import Enum

class DOOR:
    """
    Establishes three doors in a room. One leads to the murderer, two don't! 
    Doors can be locked when the lockpicking craft is discovered.
    Players can also set traps on doors to help shelter them. 
    """
    def __init__(self):
        self.murderous = False
        self.locked = False
        self.trap = None

class room:
    """Builds a random room with furnishings and special gameplay items"""
    def __init__(self):
        self.containers = {
            # container:[item,...]
        }
        self.person_container = None # None for no person, otherwise a container
        self.doors = [DOOR(), DOOR(), DOOR()]
        random.choice(self.doors).murderous = True ## makes one of the doors contain a room with the serial killer in it
        self.room_type = compute().RANDOMIZE_ROOM_TYPE()
        self.book = None    # occurs in 30% of rooms
        self.light = None   # occurs in 40% of rooms
        self.altar = None   # occurs in 10% of rooms
        self.time_to_encounter = { # time until attack happens (in seconds)
            room_type.BEDROOM:180,
            room_type.SITTINGROOM:60,
            room_type.KITCHEN:120,
            room_type.HALLWAY:30,
            room_type.STUDY:240,
            room_type.LIBRARY:280
        }[self.room_type]
        self.furnish()

    def __str__(self):
        s = "This is a {}\n".format(self.room_type.name)
        for container, items in self.containers.items():
            s+="container: {0}\n".format(container.name)
            for item in items:
                s+=item.__str__()+"\n"
        return s


    def furnish(self):
        """Populates a room with furniture and ingredients. Needs to be overhauled."""
        #TODO: Overhaul this whole thing
        self.containers = {
            room_type.BEDROOM:{c.CHEST:[], c.CLOSET:[], c.DRESSER:[], c.BED:[], c.UNDERBED:[]},
            room_type.SITTINGROOM:{c.CHEST:[], c.CHESTERFIELD:[], c.SHELF:[], c.DISPLAYCASE:[]},
            room_type.KITCHEN:{c.CABINET:[], c.BREADBOX:[], c.PANTRY:[]},
            room_type.HALLWAY:{c.DISPLAYCASE:[]},
            room_type.STUDY:{c.DESKDRAWER:[], c.DESK:[], c.CABINET:[], c.CHEST:[], c.BOOKCASE:[], c.DISPLAYCASE:[], c.CHESTERFIELD:[]},
            room_type.LIBRARY:{c.BOOKCASE:[], c.DESK:[], c.DESKDRAWER:[]}
        }[self.room_type]
        for container, items in self.containers.items():
            ## populate with ingredients
            # number of ingredients in container
            for i in range(0, random.choice([0]*20+[1]*30+[2]*30+[3]*10+[4]*8+[5]*2)+1):
                items.append(INGREDIENT())
        if random.choice([True]*3+[False]*7): self.book = BOOK()
        if random.choice([True]*4+[False]*6): self.light = LIGHT()
        if random.choice([True]*1+[False]*9): self.altar = ALTAR()

    def test_fit(self):
        """sample code for making sure things fit in places"""
        b = BOOK()
        print("-------made a book-------")
        print("size: {0}\ndblt: {1}\nrare: {2}\ngood: {3}".format(
            b.size.name, b.durability.name, b.rarity.name, b.alignment))
        max = c.MAX_SIZE(c)[c.CABINET]

        print("It fits in a cabinet: {}".format(b.size in max))

if __name__ == "__main__":
    r = room()
    print(r)
    print("SPECIALS")
    if r.book: print(r.book) 
    else: print("No books")
    if r.light: print(r.light) 
    else: print("No lights")
    if r.altar: print(r.altar) 
    else: print("No altars")
    print("Time to encounter: {}".format(r.time_to_encounter))
    for door in r.doors:
        print("Murderous door?: {}".format(door.murderous))
