"""
Speaking to someone
interacting with an object
analyzing a room
hiding something
performing a spell
wishing
"""
from typing import Text
#from _abstr import ACTION
import random
from functools import partial
from _inventory import inventory
from _character import character
from _abstr import item_type, ingredient_name, TRAPS, ACTION, craft_engine, SPELLS, color
from _mansion import mansion
from _room import room, DOOR
from _item import _craft, ALTAR, LIGHT, BOOK, INGREDIENT
from _crafting import crafting

class action:
    """Implements the ACTION enums in _abstr. Effectively manages game engine mechanics by maintaining the active physical model of the game."""
    def __init__(self, 
        game : mansion = mansion()):
        self.crafter = crafting()
        self.game = game
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
            ACTION.INCREASEATT : self.increase, # for custom increases
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
            ACTION.EXTENDAMBUSH : partial(self.extend_ambush, time=30),
            ACTION.PLACETRAP : partial(self.place_trap, code="000"),
            ACTION.LOCKDOOR : partial(self.neutralize_door),
            ACTION.AMBUSH : self.ambush, 
            # 
        }

    def do(self, action : ACTION, *args, **kwargs):
        """Main API entry point for completing actions. Refer to ACTION class in _abstr for complete registered action enum"""
        return self.map[action](*args, **kwargs)

    def trade_initiation(self):
        pass

    def fuck(self):
        pass

    def murder(self):
        pass

    def free(self, item_t, item_name=None):
        choices = {
            item_type.SPELL:craft_engine().spells,
            item_type.TRAP:craft_engine().traps,
            item_type.TOOL:craft_engine().tools,
            item_type.WEAPON:craft_engine().weapons,
        }
        if not item_name: item_name = random.choice([e for e in choices[item_t] if type(e)!=type("string")])
        for ingredient in self.crafter.ingredients_by_name(choices[item_t], item_name): self.crafter.select(ingredient)
        new_craft = self.crafter.craft(choices[item_t], item_name)
        print("making free {}".format(item_name))
        if new_craft: 
            print("selecting items")
            self.crafter.select(new_craft)
            self.game.char.inventory.put_away(new_craft)
        return new_craft

    def free_level(self, level_type : Text):
        "returns a character with +1 level in crafting or spells"
        if level_type == "craft":
            self.game.char.craft_level+=1
        if level_type == "spell":
            self.game.char.spell_level+=1
    
    def increase(self, attrib : Text, amount : float=1) -> character:
        """increases a character attribute status (string)"""
        self.game.char.attributes[attrib] += amount
        return character

    def init_special(self, special : Text):
        """Multiplexes special actions taken by unique characters"""
        pass

    def neutralize_door(self, code : Text):
        """Uses one-hot encoding string to neutralize a specific door (i.e. "010" would make door two, and only door two, safe)"""
        try:
            assert code.count("0")==2 and len(code) == 3 # ensure one hot encoding by counting 0s
            for i in range(0, 3):
                self.game.room.doors[i].murderous=code[i]
        except:
            print ("improper one-hot door encoding encountered.")
    
    def place_trap(self, trap : _craft, code : Text = "000"):
        """Uses encoding to place trap in a room. Currently, traps default to all doors and trigger on ambush."""
        for i in range(0, 3):
            self.game.room.doors[i].trap = trap if int(code[i]) else None
        self.game.char.inventory.throw_away(trap)

    def impact_next_struggle(self, factor: float=1):
        """Affects the factor used to increase or decrease the difficulty when struggling during an ambush."""
        pass

    def extend_ambush(self, time : float):
        """Increases (or decreases with a negative value) the time in the room until ambush occurs"""
        pass

    def ambush(self):
        """Entry point for ambush mechanic""" 
        print("Ambush placeholder")
        for i in self.game.room.doors:
            m = i.murderous
            s = i.trap.name if i.trap else False
            print("door {} -> murderous: {} | trapped: {}".format(i, m, s))

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

    def title(self):
        print("\n\n\n")
        print(color.RED+\
              "  ███▄ ▄███▓ █    ██  ██▀███  ▓█████▄ ▓█████  ██▀███      ███▄ ▄███▓ ▄▄▄       ███▄    █   ██████  ██▓ ▒█████   ███▄    █ \n"+\
              "  ▓██▒▀█▀ ██▒ ██  ▓██▒▓██ ▒ ██▒▒██▀ ██▌▓█   ▀ ▓██ ▒ ██▒   ▓██▒▀█▀ ██▒▒████▄     ██ ▀█   █ ▒██    ▒ ▓██▒▒██▒  ██▒ ██ ▀█   █ \n"+\
              "  ▓██    ▓██░▓██  ▒██░▓██ ░▄█ ▒░██   █▌▒███   ▓██ ░▄█ ▒   ▓██    ▓██░▒██  ▀█▄  ▓██  ▀█ ██▒░ ▓██▄   ▒██▒▒██░  ██▒▓██  ▀█ ██▒\n"+\
              "  ▒██    ▒██ ▓▓█  ░██░▒██▀▀█▄  ░▓█▄   ▌▒▓█  ▄ ▒██▀▀█▄     ▒██    ▒██ ░██▄▄▄▄██ ▓██▒  ▐▌██▒  ▒   ██▒░██░▒██   ██░▓██▒  ▐▌██▒\n"+\
              "  ▒██▒   ░██▒▒▒█████▓ ░██▓ ▒██▒░▒████▓ ░▒████▒░██▓ ▒██▒   ▒██▒   ░██▒ ▓█   ▓██▒▒██░   ▓██░▒██████▒▒░██░░ ████▓▒░▒██░   ▓██░\n"+\
              "  ░ ▒░   ░  ░░▒▓▒ ▒ ▒ ░ ▒▓ ░▒▓░ ▒▒▓  ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░   ░ ▒░   ░  ░ ▒▒   ▓▒█░░ ▒░   ▒ ▒ ▒ ▒▓▒ ▒ ░░▓  ░ ▒░▒░▒░ ░ ▒░   ▒ ▒ \n"+\
              "  ░  ░      ░░░▒░ ░ ░   ░▒ ░ ▒░ ░ ▒  ▒  ░ ░  ░  ░▒ ░ ▒░   ░  ░      ░  ▒   ▒▒ ░░ ░░   ░ ▒░░ ░▒  ░ ░ ▒ ░  ░ ▒ ▒░ ░ ░░   ░ ▒░\n"+\
              "  ░      ░    ░░░ ░ ░   ░░   ░  ░ ░  ░    ░     ░░   ░    ░      ░     ░   ▒      ░   ░ ░ ░  ░  ░   ▒ ░░ ░ ░ ▒     ░   ░ ░ \n"+\
              "         ░      ░        ░        ░       ░  ░   ░               ░         ░  ░         ░       ░   ░      ░ ░           ░ \n"+\
              "                                ░                                                                                          \n")
        s = random.choice([
            ("We’ve all got the power in our hands to kill, but most people are afraid to use it. The ones who aren’t afraid, control life itself.", "-Richard Ramirez"),
            ("We serial killers are your sons, we are your husbands, we are everywhere. And there will be more of your children dead tomorrow.", "-Ted Bundy"),
            ("I just wanted to see how it felt to shoot Grandma.", "-Edmund Kemper"),
            ("A clown can get away with murder.", "-John Wayne Gacy"),
            ("I’m the most cold-hearted son-of-a-bitch you’ll ever meet.", "-Ted Bundy"),
            ("What’s one less person on the face of the earth, anyway?", "-Ted Bundy"),
            ("I’ve got to start eating at home more.", "-Jeffrey Dahmer"),
            ("The only thing they can get me for is running a funeral parlor without a license.", "-John Wayne Gacy"),
            ("I actually think I may be possessed with demons; I was dropped on my head as a kid.", "-Dennis Rader"),
            ("Even psychopaths have emotions; then again, maybe not.", "-Richard Ramirez"),
            ("I wanted to clear all the lies and let the truth come out. I have hate crawling through my system.", "-Aileen Wuornos"),
            ("I like children, they are tasty.", "-Albert Fish"),
            ("If you’re going to do something, do it well. And leave something witchy.", "-Charles Manson"),
            ("I believe the only way to reform people is to kill them.", "-Carl Panzram"),
            ("That is my ambition, to have killed more people- more helpless people- than any man or woman who has ever lived.", "-Jane Toppan"),
            ("To me, this world is nothing but evil, and my own evil just happened to come out 'cause of the circumstances of what I was doing.", "-Aileen Wuornos"),
            ("Hurry it up, you Hoosier bastard! I could kill a dozen men while you're screwing around!", "-Carl Panzram"),
            ("We do whatever we enjoy doing. Whether it happens to be judged good or evil is a matter for others to decide.", "-Ian Bady"),
            ("It wasn’t as dark and scary as it sounds. I had a lot of fun… killing somebody’s a funny experience.", "Albert DeSalvo")
        ])
        wid = len(s[0])-10
        print("{}\n{}{}\n\n\n".format(s[0], " "*wid, s[1]))
        print(  "A GAME BUILT BY YOUR LOVED ONES\n\n"+color.END+\
                color.RED+"DEVELOPER:"+color.END+" \nJames McKay\n\n"+\
                color.RED+"TECHNICAL CONSULTANTS:"+color.END+"\n"+\
                "Greg Hoople\nJared Enos\n\n"+\
                color.RED+"CREATIVE CONSULTANTS:"+color.END+"\n"+\
                "Elisabeth Enos\nHannah Gonzalez\n"+\
                "Haley Harrison\nEllen Lindsay\nIcy Boi\n"+\
                "Gabbz\nGabby Zermeno\nAlex Zermeno\n"+\
                "Lucy Carroll\nTom Carroll\n"+\
                "Chloe\nMegan Lee"
            )

    def intro(self):
        return [
            " ",0,
            "You wake up in a strange place...", 3,
            "Your head feels fuzzy and your eyes can't see too well...", 1,
            "How did you get here?", 1, "You have a strange feeling.", 1, "Like there's someone else here.", 1, "Someone BAD.", 1,
            "You climb to your feet and try to take in the splendor of this place...", 3, "You're in some sort of intricate room. ", 0, 
            "Everything in here looks really expensive. This must be some kind of mansion...", 2]

if __name__ == "__main__":
    ## make a game
    ## increase character stats 
    ## make a room
    ## lock a door
    ## print character and doors
    game = action()
    game.title()
    game.crafter.select(ALTAR()) # adds an altar to the default character inventory
    new_trap = game.do(ACTION.GETFREETRAP) 
    new_spell = game.do(ACTION.GETFREESPELL)
    new_weapon = game.do(ACTION.GETFREEWEAPON) 
    new_tool = game.do(ACTION.GETFREETOOL) 
    print(game.game.char.inventory) # prints the inventory to show that it is in the trap section
    game.do(ACTION.PLACETRAP, new_trap, code="010") # places the HOMEALONE trap on doors
    game.do(ACTION.AMBUSH) # triggers the ambush (currently just shows door status)
    print(game.game.char.inventory) # print the inventory to show the trap is gone from the inventory
