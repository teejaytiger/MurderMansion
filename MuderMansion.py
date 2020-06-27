from _actions import action, ACTION
from enum import Enum
import time
import random
from _abstr import color, term, chars, item_type
import sys
from _item import INGREDIENT, ALTAR

def _find_getch():
    try:
        import termios
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return msvcrt.getch

    # POSIX system. Create and return a getch that manipulates the tty.
    import sys, tty
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    return _getch

class MuderMansion:
    """Main entry point for the game. It's basically a glorified state machine."""
    # TODO: Add transitions to the states

    def __init__(self):
        """
        Because of time constraints, Murder Mansion is a glorified state machine
        that uses the actions module like a game model. Hopefully it's just clever
        enough to work. The state map points to local definitions of the state
        functions and next calls. No abstraction here, even though I should. Time.
        """
        self.act = action()
        self.getch = _find_getch()
        # map all the states to their functions
        self.statemap= {
            STATES.TITLE:self.TITLE,
            STATES.INTRO:self.INTRO,
            STATES.TUTORIAL:self.TUTORIAL,
            STATES.OCCUPY:self.OCCUPY,
            STATES.EXPLORE:self.EXPLORE,
            STATES.RUMMAGE:self.RUMMAGE,
            STATES.CHAT:self.CHAT,
            STATES.TRADE:self.TRADE,
            STATES.NEXTROOM:self.NEXTROOM,
            STATES.BROWSEINV:self.BROWSEINV,
            STATES.CRAFTING:self.CRAFTING,
            STATES.CONSUME:self.CONSUME,
            STATES.STRUGGLE:self.STRUGGLE
        }
        self.PREVIOUS_STATE = None
        self.CURRSTATE = None
        self.INVRETURN = STATES.OCCUPY
        self.timer = time.time()+self.act.game.room.time_to_encounter
        print(self.timer)
    
    def getKey(self):
        c1 = self.getch()
        if c1 in (b'\x00', b'\xe0'):
            arrows = {b'H': "up", b'P': "down", b'M': "right", b'K': "left"}
            c2 = self.getch()
            return arrows.get(c2, c1 + c2)
        return c1

    def start(self):
        start_state = STATES.INTRO
        self.CURRSTATE = start_state
        self.NEXTSTATE(start_state)

    def NEXTSTATE(self, next_state:Enum):
        """Uses state info to execute the next state"""
        self.PREVIOUS_STATE = self.CURRSTATE
        self.CURRSTATE = next_state
        # TODO: transitions here
        self.statemap[next_state]()

    def TITLE(self):
        # State code
        print(term.CLS+term.CURSORHOME)
        self.act.title()
        # Next state
        while(True):
            g = self.getKey()
            if g=='right':
                self.NEXTSTATE(STATES.TUTORIAL)

    def INTRO(self):
        print(term.CLS+term.CURSORHOME)
        self.real_type(self.act.intro())
        # Next state
        while(True):
            if self.getKey()=='right':
                self.NEXTSTATE(STATES.TITLE)


    def TUTORIAL(self):
        print(term.CLS+term.CURSORHOME)
        print("rest of the fuckin owl")
        # Next state
        while(True):
            if self.getKey()=='right':
                self.NEXTSTATE(STATES.OCCUPY)

    def OCCUPY(self):
        # option are to open explore shell, go to the next room, or open the inventory shell
        print(term.CLS+term.CURSORHOME)
        print("OPTIONS:\n  1. Exit this room\n  2. Explore this room\n  3. Open inventory\n  4. Quit\n\nWhat is your choice?")
        while(True):
            g = self.getKey()
            if g!='':
                if g==b'1':
                    self.NEXTSTATE(STATES.NEXTROOM)
                elif g==b'2':
                    self.NEXTSTATE(STATES.EXPLORE)
                elif g==b'3':
                    self.NEXTSTATE(STATES.BROWSEINV)
                elif g==b'4':
                    exit(1)

    def EXPLORE(self):
        print(term.CLS+term.CURSORHOME)
        print("OPTIONS:\n  1. Go through this shit\n  2. Open inventory\n  3. Go back\n\nWhat is your choice?")
        while(True):
            g = self.getKey()
            if g!='':
                if g==b'1':
                    self.NEXTSTATE(STATES.RUMMAGE)
                elif g==b'2':
                    self.NEXTSTATE(STATES.BROWSEINV)
                elif g==b'3':
                    self.NEXTSTATE(STATES.OCCUPY)
        print(self.act.game.room)


    def RUMMAGE(self):
        self.rummaging_shell()

    def CHAT(self):
        print("that was enough chatting")
        self.NEXTSTATE(STATES.TRADE)

    def TRADE(self):
        print("whew I'm all traded out")
        self.NEXTSTATE(STATES.RUMMAGE)

    def NEXTROOM(self):
        self.act.game.next_room()
        self.NEXTSTATE(STATES.OCCUPY)

    def BROWSEINV(self):
        print("OPTIONS:\n  1. Craft an Item\n  2. Consume an Item\n  3. Go back\n\nWhat is your choice?")
        # implement good UX "back" mechanics for state loops
        if self.PREVIOUS_STATE==STATES.OCCUPY or self.PREVIOUS_STATE==STATES.EXPLORE:
            self.INVRETURN=self.PREVIOUS_STATE
        self.inventory_shell()

    def CRAFTING(self):
        print("whew that was crafty")
        self.NEXTSTATE(STATES.BROWSEINV)

    def CONSUME(self):
        print("I feel much better now")
        self.NEXTSTATE(STATES.BROWSEINV)

    def STRUGGLE(self):
        print("eh, you lose")

    def inventory_shell(self):
        highlight = 0
        subcat = 0

        while True:
            inventory = [
            (item_type.WEAPON, self.act.game.char.inventory.weapons.items),
            (item_type.BOOK, self.act.game.char.inventory.books.items),
            (item_type.ALTAR, self.act.game.char.inventory.altars.items),
            (item_type.SPELL, self.act.game.char.inventory.spells.items),
            (item_type.TRAP, self.act.game.char.inventory.traps.items),
            (item_type.TOOL, self.act.game.char.inventory.tools.items),
            (item_type.INGREDIENT, self.act.game.char.inventory.ingredients.items),
            (item_type.SPECIAL, self.act.game.char.inventory.specials.items)]
            self.show_container(inventory[subcat], highlight, badge1="Select/Deselect for Craft(s)", badge2="Consume (a)", post_usage="ESC : Go Back\nQ : Enter Craft Menu")
            k = self.getKey()
            if len(inventory[subcat][1]):
                if k == "up": highlight = abs((highlight-1)%len(inventory[subcat][1]))
                if k=="down": highlight = abs((highlight+1)%len(inventory[subcat][1]))
            if len(inventory):
                if k=="left": 
                    subcat = abs((subcat-1)%len(inventory))
                    highlight = 0
                if k=="right":
                    subcat = abs((subcat+1)%len(inventory))
                    highlight = 0
            if k==b'q':
                self.NEXTSTATE(STATES.CRAFTING)
            if k==b'a':
                self.NEXTSTATE(STATES.CONSUME)
            #if k==b's': # select an item for crafting
            #    self.act.game.crafter.select()
            if k==term.ESCAPE:
                self.NEXTSTATE(self.INVRETURN) # "go back"
            else:
                print (k)

    def crafting_shell(self):
        """defines all UI for crafting state"""
        pass

    def spellcrafting_shell(self):
        pass

    def craftcrafting_shell(self):
        pass

    def chatting_shell(self): 
        pass

    def trade_shell(self):
        pass

    def rummaging_shell(self):
        highlight = 0
        container = 0
        containers = []

        for container_type, ingredients_list in self.act.game.room.containers.items():
            containers.append((container_type, ingredients_list))

        while True:
            self.show_container(containers[container], highlight, badge1="Take This (s)", badge2="Take All (a)")
            k = self.getKey()
            if k == "up": highlight = abs((highlight-1)%len(containers[container][1]))
            if k=="down": highlight = abs((highlight+1)%len(containers[container][1]))
            if k=="left": 
                container = abs((container-1)%len(containers))
                highlight = 0
            if k=="right":
                container = abs((container+1)%len(containers))
                highlight = 0
            if k==b's': # selected an item
                index = self.act.game.room.containers[containers[container][0]].index(containers[container][1][highlight])
                collected = self.act.game.room.containers[containers[container][0]].pop(index)
                self.act.game.char.inventory.put_away(collected) # puts the item into the char inventory
                containers = []
                for container_type, ingredients_list in self.act.game.room.containers.items():
                    containers.append((container_type, ingredients_list))
                highlight = 0
            if k==b'a':
                for i in range(len(containers[container][1])):
                    index = self.act.game.room.containers[containers[container][0]].index(containers[container][1][0])
                    collected = self.act.game.room.containers[containers[container][0]].pop(index)
                    self.act.game.char.inventory.put_away(collected) # puts the item into the char inventory
                containers = []
                for container_type, ingredients_list in self.act.game.room.containers.items():
                    containers.append((container_type, ingredients_list))
            if k==term.ESCAPE:
                    self.NEXTSTATE(STATES.EXPLORE) # this is "go back"
            else:
                print (k)

        for i in range(0, 10):
            self.show_container(containers[container], highlight)
            time.sleep(1)
    
    def show_container(self, container, highlight, badge1="", badge2="", post_usage="ESCAPE : Go Back"):
        label, item_list = container
        print(term.CLS+term.CURSORHOME)
        print(
            "".join([" "]*16)+"{} {} {}\n\n".format(chars.TRIANGLELEFT, label.name, chars.TRIANGLERIGHT)
        )
        for i in range(0, len(item_list)):
            if i==highlight:
                if type(item_list[i])==type(INGREDIENT()):
                    sel = item_list[i].__str__().split("\n")
                    s =  color.PURPLE + sel[0] + color.END + "  {}\n".format(chars.TRIANGLEUP)
                    s += color.PURPLE + sel[1] + color.END + " {} \n".format(badge1)
                    s += color.PURPLE + sel[2] + color.END + " {} \n".format(badge2)
                    s += color.PURPLE + sel[3] + color.END + "  {}".format(chars.TRIANGLEDOWN) + color.END
                    print(s)
                else:
                    sel = item_list[i].__str__().split("\n")
                    sel[0] = chars.TRIANGLEUP+"\n"+chars.SINGLE_VERTI_PIPE+" "+sel[0]
                    sel[6] = sel[6]+" {}".format(badge1)
                    sel[7] = sel[7]+" {}".format(badge2)
                    sel = sel + ["\n{}".format(chars.TRIANGLEDOWN)]
                    for i in range(1, len(sel)):
                        sel[i] = chars.SINGLE_VERTI_PIPE+" "+sel[i]
                    print("\n".join(sel))


            else:
                if type(item_list[i])==type(INGREDIENT()): print(self.mini_ingredient(item_list[i])) # works for 4 line cards (ingredients, items, not crafts)
                else: print(self.mini_craft(item_list[i])) # works on craft cards
        print("\n\n{}".format(post_usage))

    def mini_ingredient(self, ingredient):
        # take an ingredient and prints a cute version
        lines = ingredient.__str__().split("\n")
        return lines[1][2:-1].rstrip(" ")

    def mini_craft(self, craft):
        # take an craft and prints a cute version
        lines = craft.__str__().split("\n")
        return lines[1][22:].rstrip(" ")
            
    def exploration_shell(self):
        pass

    def real_type(self, text_list):
        for comp in text_list:
            if type(comp)==type(0):
                time.sleep(comp) 
            else:
                for i in comp:
                    sys.stdout.write(i)
                    sys.stdout.flush()
                    time.sleep(random.uniform(0.03, 0.18))
                print()

class STATES(Enum):
    """Maintains a list of possible states, so I don't forget to implement anything."""
    TITLE = 0
    INTRO = 1
    TUTORIAL = 2
    OCCUPY = 10
    EXPLORE = 20
    RUMMAGE = 21
    CHAT = 22
    TRADE = 23
    NEXTROOM = 30
    BROWSEINV = 40
    CRAFTING = 41
    CONSUME = 42
    STRUGGLE = 100

if __name__ == "__main__":
    game = MuderMansion()
    for i in "     ":
        game.act.do(ACTION.GETFREEWEAPON)
        game.act.do(ACTION.GETFREEITEM)
        game.act.crafter.select(ALTAR())
        game.act.do(ACTION.GETFREESPELL)
        game.act.do(ACTION.GETFREETOOL)
        game.act.do(ACTION.GETFREETRAP)
    game.start()