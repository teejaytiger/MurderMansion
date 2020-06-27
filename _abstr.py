from abc import ABC, abstractmethod
from enum import Enum
import random
from math import sqrt, cos, sin, log, pi

class _abstr (ABC):
    def __init__(self):
        self.timestamp = None
        self.modifiers = {}
        """
        = {
            ## character modifier: (effect, duration)
            "str":(1,0) : adds 1 to struggle permanently
            "pct":(-1,3) : adds -1 to perception for 3 action calls
            "lck":0,
            "cha":0,
            "int":0
        }
        """
        ## MECHANIC 
        """
        CURSE AND BLESS:
        cursed and blessed items add factors to the success of spells and attacks
        blessed items have a higher probability of performing critical hits and superior spells
        superior spells last longer and are stronger
        adequate spells last their default amounts and perform nominally
        poor spells perform much worse
        """
        self.alignment = 0.0 ## any curse or bless effects normalized -1 to 1

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    # print(color.BOLD + 'Hello World !' + color.END)

class term:
    SAVECURSOR = '\033[s'
    CURSORHOME = '\033[H'
    RESTORECURSOR = '\033[u'
    CURSORUP = '\033[a'
    CURSORDOWN = '\033[b'
    CURSORRIGHT = '\033[c'
    CURSORLEFT = '\033[d'
    ERASELINE = '\033[1M' # or 2K, unsure
    ERASESOL = '\033[1K'
    ERASEEOL = '\033[K'
    CLS = '\033[2J'
    ERASEUP = '\033[1J'
    ERASEDOWN = '\033[J'
    ESCAPE = b'\x1b'

class item_type(Enum):
    BOOK = 0
    WEAPON = 1
    LIGHT = 2
    ALTAR = 3
    SPELL = 4
    TRAP = 5
    TOOL = 6
    SPECIAL = 7
    INGREDIENT = 8
    UNSET = 9

class chars:
    DOUBLE_LEFT_TOP = u'\u2554' # ╔ 
    DOUBLE_VERTI_PIPE = u'\u2551' # ║ 
    DOUBLE_LEFT_BOTTOM = u'\u255a' # ╚ 
    DOUBLE_RIGHT_TOP = u'\u2557' # ╗ 
    DOUBLE_RIGHT_BOTTOM = u'\u255d' # ╝ 
    DOUBLE_HORIZ_PIPE = u'\u2550' # ═ 
    SINGLE_LEFT_TOP = u'\u250c' # ┌ 
    SINGLE_VERTI_PIPE = u'\u2502' # │ 
    SINGLE_LEFT_BOTTOM = u'\u2514' # └ 
    SINGLE_RIGHT_TOP = u'\u2510' # ┐ 
    SINGLE_RIGHT_BOTTOM = u'\u2518' # ┘ 
    SINGLE_HORIZ_PIPE = u'\u2500' # ─
    DOUBLE_T_RIGHT = u'\u2563' # ╣
    DOUBLE_T_LEFT = u'\u2560' # ╠
    DOUBLE_T_TOP = u'\u2566' # ╦
    DOUBLE_T_BOTTOM = u'\u2569' # ╩
    #TRIANGLELEFT = u'\u25c1' # ◁
    #TRIANGLERIGHT = u'\u25b7' # ▷
    TRIANGLELEFT = "<" # ◁
    TRIANGLERIGHT = ">" # ▷
    TRIANGLEUP = u'\u25b3' # △
    TRIANGLEDOWN = u'\u25bd' # ▽
    BOOK_ICON = chr(10026)
    ALTAR_ICON = chr(9912)
    LIGHT_ICON = chr(9775)
    CRAFT_ICON = chr(9881)
    WEAPON_ICON = chr(9876)
    SPELL_ICON = chr(9708)
    TRAP_ICON = chr(9637)
    INGREDIENT_ICON = chr(9630)
    TOOL_ICON = chr(9655)
    UNSET_ICON = chr(9711)
    EMPTY_STAR = chr(9734) # ☆
    FULL_STAR = chr(9733) # ★
    

class size(Enum):
    """Enumeration of all item sizes (except lamps)"""
    # MUST BE KEPT IN SIZE ORDER, ENUM USED IN CALCULATIONS
    TINY = 0        ## weight 0
    SMALL = 1       ## weight 1
    MEDUIM = 2      ## etc
    LARGE = 3
    HUGE = 4

class lamp_style(Enum): 
    """Enumeration of Lamp types. Affects book reading time. """
    CANDLE = 0      ## 5
    SCONCE = 1      ## 3
    DESKLAMP = 2    ## 1
    FLOORLAMP = 3   ## 1

class rarity(Enum):
    """Enumeratio of item rarities"""
    ## MUST BE IN ORDER, ENUM USED IN CALCULATIONS
    COMMON = 0       ## 25
    UNUSUAL = 1      ## 15
    STRANGE = 2      ## 5
    INCREDIBLE = 3   ## 2
    IMMACULATE = 4   ## 2
    MYTHOLOGICAL = 5 ## 1

class durability(Enum):
    """Enumeration of item durabilities"""
    ## MUST BE IN ORDER, ENUM USED IN CALCULATIONS
    FRAGILE = 0     ## 5
    RAMSHACKLE = 1  ## 10
    ADEQUATE = 2    ## 70
    STURDY = 3      ## 9
    CHONKY = 4      ## 5
    YOKED = 5       ## 1
    
class room_type(Enum):
    """Enumeration of all room types"""
    BEDROOM = 0
    SITTINGROOM = 1
    KITCHEN = 2
    HALLWAY = 3
    STUDY = 4
    LIBRARY = 5

class container(Enum):  # contains up to:
    """Enumeration of all room container types"""
    CABINET = 0         # MEDIUM
    DRESSER = 1         # SMALL
    CHEST = 2           # MEDIUM
    BREADBOX = 3        # TINY
    DRAWER = 4          # SMALL
    CLOSET = 5          # HUGE
    DESKDRAWER = 6      # SMALL
    SHELF = 8           # SMALL
    BOOKCASE = 9        # MEDIUM
    DISPLAYCASE = 10    # LARGE
    BED = 11            # HUGE
    DESK = 12           # HUGE
    UNDERBED = 14       # HUGE
    CHESTERFIELD = 15   # SMALL
    PANTRY = 16         # HUGE
    CHIMNEY = 17        # HUGE Elisabeth
    def MAX_SIZE(self):
        """Returns a list of item sizes compatible with a room container"""
        return {
            self.CABINET:   [size.TINY, size.SMALL, size.MEDUIM],
            self.DRESSER:   [size.TINY, size.SMALL],
            self.CHEST:     [size.SMALL, size.MEDUIM],
            self.BREADBOX:  [size.TINY],
            self.DRESSER:   [size.TINY, size.SMALL],
            self.CLOSET:    [size.MEDUIM, size.LARGE, size.HUGE],
            self.PANTRY:    [size.MEDUIM, size.LARGE, size.HUGE],
            self.DESKDRAWER:[size.TINY, size.SMALL],
            self.SHELF:     [size.TINY, size.SMALL],
            self.BOOKCASE:  [size.TINY, size.SMALL, size.MEDUIM],
            self.DISPLAYCASE:[size.TINY,size.SMALL, size.MEDUIM, size.LARGE],
            self.BED:       [size.MEDUIM, size.LARGE, size.HUGE],
            self.DESK:      [size.TINY, size.SMALL, size.HUGE],
            self.CHIMNEY:   [size.SMALL, size.MEDUIM, size.LARGE, size.HUGE],
            self.UNDERBED:  [size.MEDUIM, size.LARGE, size.HUGE],
            self.CHESTERFIELD:[size.TINY, size.SMALL]
        }

class available(Enum):
    """The presence of an item or the ability to craft an item"""
    AVAILABLE = 1
    UNAVAILABLE = 0 

class ingredient_name(Enum):
    """Ingredients are the primary mechanism in crafting"""
    ## predominantly spells
    CATWHISKER = 0      # 
    MUGWORT = 1         # 
    DEADFLESH = 2       # 
    MURDERWEAPON = 3    # 
    QUARTZ = 4          # 
    DRYROT = 5          # 
    BLACKWIDOW = 6      # 
    WHITESAGE = 7       # 
    SILVER = 8          # 
    EPSOMSALT = 9       # 
    GLASSEYE = 10       # 
    TEARS = 11          # 
    COPPERWIRE = 12     # 
    GOLD = 13           # 
    MINT = 14           # 
    ROSEMARY = 15       # 
    ROSEPETALS = 16     # 
    LAVENDER = 17       # 
    SKULL = 18          # 
    ADDERSTONE = 19     # 
    MOONWATER = 20      # 
    GRAVEYARDDIRT = 21  # 
    YELLOWTEALIGHT = 22 # 
    BLACKTEALIGHT = 23  # 
    WHITETEALIGHT = 24  # 
    SALT = 25           # 
    VINEGAR = 26        #
    REISHIMUSHROOM = 27 # Elisabeth
    NIGHTSHADE = 28     # Elisabeth
    OLEANDER = 29       # Elisabeth
    ASH = 30            # Elisabeth
    BOTTLE = 31         # common item
    FLOUR = 32          # 
    HONEY = 33          # 
    ## predominantly crafts
    MATCHSTICK = 51     # 
    PIPE = 52           # 
    SHOTGUNSHELL = 53   # 
    WOODBLOCK = 54      # 
    SCISSORHALVE = 55   # 
    PLASTIC = 56        # 
    WOODENDOWEL = 57    # 
    LENS = 58           # 
    SMALLBOX = 59       # 
    SCREWS = 60         # 
    NAIL = 61           # 
    BOTTLECAP = 62      # 
    GLASSSHARD = 63     # 
    STRING = 64         # 
    ROPE = 65           # 
    PAPER = 66          # 
    PAINTCAN = 67       # 
    DUCTTAPE = 68       # 
    FLASHBULB = 69      # 
    SPRING = 70         # 
    GLOWSTICK = 71      # 
    BATTERY = 72        # 
    CIRCUIT = 73        # 
    CLOTH = 74          # 
    STEELWOOL = 75      # 
    ## Haley's salad
    ICEBERGLETTUCE = 100# 
    TOMATO = 101        # 
    CROUTONS = 102      # 
    OLIVEOIL = 103      # 
    ## family stuff
    DERMESTIDBEETLES=200# 1
    WERTHERSCANDY = 201 # 1
    HONEYMUSTARD = 202  # 1
    VOLLEYBALL = 203    # 1
    AVETTBROTHERSCD=204 # 1
    VPDHAT = 205        # 1
    COFFEE = 206        # 1
    # weed
    OREGANO = 300       # 1
    # special 
    SPECIAL = 400

class SPELLS(Enum):
    """Spells have consumption time"""
    WISHFORHELP = 0
    HOUSESALAD = 1
    HEALINGMAX = 2
    HEALINGMINOR = 3
    HEALINGMIDDLE = 4
    FLIGHT = 5
    FIGHT = 6
    SMOKEBRINGER = 7
    INTROSPECTION = 8
    DUPLICATION = 9
    PROTECTION = 10
    PROTECTION2 = 11
    PROTECTION3 = 12

class TRAPS(Enum):
    """Traps have setup time"""
    FRONTTOWARDSENEMY = 0
    HOMEALONE = 1
    SNAILPROBLEM = 2
    BANGBANGBANG = 3
    SPILTLEGOS = 4
    AUTOSTUBBER = 5
    THETOEANNIHILATOR = 6
    STUBTOSTUB = 7
    HONEYPOT = 8

class SPECIAL(Enum):
    """Weapons have a maximum number of uses"""
    THEGIFTER = 0
    MARCUSMUNITIONS = 1
    SUCTIONCUPDILDO = 2

class WEAPONS(Enum):
    """Weapons have a maximum number of uses"""
    TSHIRTCANNON = 0
    #ROLLOFQUARTERS = 1
    #CANDLESTICK = 3
    SOAPINASOCK = 4
    SHARPPENCIL = 5
    POCKETSAND = 6
    TEDDYSTICK = 7
    REALLYHOTPIZZA = 8
    TSHIRTSNIPER = 9
    # FARTCANNON = 10
    # THROWINGCARDS = 11
    # THICKRUBBERBANDS = 12
    GARROTEFLOSS = 13
    # PLANKY = 14
    SPLINTERPLACER5K = 15 #Haley
    TOEKNIFE = 16
    BROTORCH = 17
    # COKEANDMENTOS = 18
    # POTATOGUN = 19
    # SKILLET = 20
    # CATPEESQUIRTGUN = 22
    ENTRYLEVEL = 23
    THECONSTABLE = 24
    FAGGOT = 25
    DADDYSLITTLEMONSTER = 26
    THEGREY = 27

class TOOLS(Enum):
    """Tools have a maximum number of uses, and increase relevant character attribute until used up"""
    RAVEON = 0
    MOLLYPOP = 1
    LIGHTBRINGER = 2
    LOCKPICKINGLAWYER = 3
    BOSNIANTOOL = 4
    JIMSHAPIRO = 5

class ACTION(Enum):
    # must be implemented by the top level
    STARTTRADE = 0
    FUCK = 1
    MURDER = 2
    GETFREETRAP = 10
    GETFREETOOL = 11 
    GETFREESPELL = 12 # gifts crafted spell
    GETFREECRAFTLEVEL = 13 # unlocks a craft level
    GETFREESPELLLEVEL = 14  # unlocks a spell level
    GETFREEITEM = 15 # gifts a completed craft
    GETFREEING = 16 # gifts a free ingredient
    GETFREEWEAPON = 15
    # Gen 100->score->pick highest item
    INCREASEINT = 20
    INCREASECHA = 21
    INCREASESTR = 22
    INCREASELCK = 23
    INCREASEPCT = 24
    INCREASEATT = 25
    # Specific Character Actions
    SANTAEFFECT = 100 #
    DILDOEFFECT = 101
    MARCUSEFFECT = 102 
    CUSTOMEFFECT = 103
    # Specific functions for jokes
    GIVESASH = 200
    HONEYPOT = 201
    # MECHANIC FUNCTIONS
    SUPPRESSAMBUSHALL = 300 # all doors don't spawn murderer
    STRUGGLE50 = 301
    STRUGGLE25 = 302
    STRUGGLE75 = 303
    STRUGGLE100 = 304
    EXTENDAMBUSH = 305
    PLACETRAP = 306
    LOCKDOOR = 307
    AMBUSH = 308

class compute:
    """Class defines how items and attributes are randomized in game. Also creates scores and computes affect."""
    def __init__(self):
        pass
    def RANDOMIZE_DURABILITY(self):
        """Randomizes an item's durability - can be used to affect number of uses or effectiveness in battle"""
        return random.choice(
            [durability.FRAGILE]*5+\
            [durability.RAMSHACKLE]*10+\
            [durability.ADEQUATE]*60+\
            [durability.STURDY]*12+\
            [durability.CHONKY]*7+\
            [durability.YOKED]*2)
    def RANDOMIZE_RARITY(self):
        """Randomizes an item's rarity - can be used to affect the quality of crafts"""
        return random.choice(
            [rarity.COMMON]*24+\
            [rarity.UNUSUAL]*15+\
            [rarity.STRANGE]*5+\
            [rarity.INCREDIBLE]*3+\
            [rarity.IMMACULATE]*2+\
            [rarity.MYTHOLOGICAL]*1)
    def RANDOMIZE_SIZE_BOOK(self):
        """Randomizes a book's size. Bigger books take longer to read, but have better benefits to int and craft"""
        return random.choice(
            [size.TINY]*1+\
            [size.SMALL]*5+\
            [size.MEDUIM]*3+\
            [size.LARGE]*1)
    def RANDOMIZE_STYLE_LAMP(self):
        """Randomizes the type of lamp in a room. Books must be read in a room with a light. Light brightness affects book reading time."""
        return random.choice(
            [lamp_style.CANDLE]*5+\
            [lamp_style.SCONCE]*3+\
            [lamp_style.DESKLAMP]*1+\
            [lamp_style.FLOORLAMP]*1)
    def RANDOMIZE_ROOM_TYPE(self):
        """Randomizes the style of room. Some rooms have more loot and more slots for people to show up!"""
        return random.choice(
            [room_type.BEDROOM]*50+\
            [room_type.SITTINGROOM]*20+\
            [room_type.KITCHEN]*5+\
            [room_type.HALLWAY]*10+\
            [room_type.STUDY]*10+\
            [room_type.LIBRARY]*5)
    def RANDOMIZE_INGREDIENT_NAME(self):
        """Randomizes the ingredients that appear in room containers."""
        return random.choice([e for e in ingredient_name])
    def RANDOMIZE_WEAPON_NAME(self):
        """Randomizes the weapon names for autogenerated weapons."""
        return random.choice([e for e in WEAPONS])
    def ALIGNMENT(self):
        """Randomizes the alignment of an item. Vaues come from points on a normal distribution centered on 0 between -1 and 1"""
        a = random.uniform(0, 1.0)
        b = random.uniform(0, 1.0)
        x = sqrt(-2*log(a))*(cos(2*pi*b))
        y = (sqrt(-2*log(a))*(sin(2*pi*b)))
        return random.choice([x/4, y/4])
    def RANDOMIZE_SIZE_INGREDIENT(self):
        """Returns the size an ingredient is allowed to be. Currently only returns size.TINY"""
        return size.TINY
    def RANDOMIZE_SIZE_ALTAR(self):
        """Returns the size an altar is allowed to be. Currently only returns size.SMALL"""
        return size.SMALL
    def RANDOMIZE_SIZE_LAMP(self):
        """Returns the size an altar is allowed to be. Currently only returns size.SMALL"""
        return size.MEDUIM
    def RANDOMIZE_WEAPON_DPS(self):
        return random.choice([2]*5+[3]*4+[4]*3+[5]*2)
    def RANDOMIZE_LIGHT_STATUS(self):
        return random.choice([available.AVAILABLE]+[available.UNAVAILABLE])

class craft_engine:
    def __init__(self):
        self.spells = { # CONSUMABLE
            "type":item_type.SPELL,
            # [str, pct, lck, cha, int, hps]
            SPELLS.WISHFORHELP:("Wish for help", 
            "Wish someone would show up to help", [0, 0, .5, .1, 0, 0], 
                [], [
                ingredient_name.CATWHISKER, 
                ingredient_name.YELLOWTEALIGHT, 
                ingredient_name.MATCHSTICK]),
            SPELLS.HOUSESALAD:("House Salad", 
            "This is the super salad. Grants 70 health points", [0, 0, 0, 0, 0, 70], 
                [], [
                ingredient_name.SCISSORHALVE, 
                ingredient_name.ICEBERGLETTUCE, 
                ingredient_name.TOMATO, 
                ingredient_name.CROUTONS, 
                ingredient_name.OLIVEOIL, 
                ingredient_name.VINEGAR]),
            SPELLS.HEALINGMINOR:("Griffin Potion",
            "Your sweet baby healing potion. Grants 10 health points", [0, 0, 0, 0, 0, 10], 
                [], [
                ingredient_name.BOTTLE,
                ingredient_name.MOONWATER]),
            SPELLS.HEALINGMIDDLE:("Travis Potion",
            "Your middlest healing potion. Grants 30 health points", [0, 0, 0, 0, 0, 30], 
                [], [
                ingredient_name.BOTTLE,
                ingredient_name.QUARTZ,
                ingredient_name.MOONWATER]),
            SPELLS.HEALINGMAX:("Justin Potion", 
            "Your oldest healing potion. Grants 50 health points", [0, 0, 0, 0, 0, 50], 
                [], [
                ingredient_name.BOTTLE,
                ingredient_name.ROSEMARY, 
                ingredient_name.QUARTZ, 
                ingredient_name.WHITETEALIGHT, 
                ingredient_name.MOONWATER, 
                ingredient_name.MATCHSTICK]),
            SPELLS.FLIGHT:("Flight",
            "The parasypathetic nervous system reacts...", [0, 0, 0, 0, 0, 0], 
                [ACTION.SUPPRESSAMBUSHALL], [
                ingredient_name.REISHIMUSHROOM,
                ingredient_name.MOONWATER,
                ingredient_name.ROSEMARY,
                ingredient_name.BOTTLE]),
            SPELLS.FIGHT:("Fight",
            "...and you're in fight or flight mode", [0, 0, 0, 0, 0, 0], 
                [ACTION.SUPPRESSAMBUSHALL], [
                ingredient_name.BOTTLE,
                ingredient_name.BLACKWIDOW,
                ingredient_name.OLEANDER,
                ingredient_name.NIGHTSHADE]),
            SPELLS.SMOKEBRINGER:("Smoke Bringer",
            "For the night is dank and full of flowers", [0, 0, 0, 0, -1, 0], 
                [ACTION.GIVESASH, ACTION.SUPPRESSAMBUSHALL], [ # add ash to inventory after this is used
                ingredient_name.OREGANO,
                ingredient_name.PAPER,
                ingredient_name.MATCHSTICK]),
            SPELLS.INTROSPECTION:("Introspection",
            "Prah prah prow proud. I’m proud of Jay.", [0, 0, 0, 0, 0, 0],
                [ACTION.STRUGGLE75], [
                ingredient_name.GLASSSHARD,
                ingredient_name.SILVER,
                ingredient_name.YELLOWTEALIGHT,
                ingredient_name.MATCHSTICK]),
            SPELLS.DUPLICATION:("Duplication",
            "So, lemme guess. You're the real Pinkie Pie.", [0, 0, 0, 0, 0, -10],
                [ACTION.STRUGGLE100],[
                SPELLS.INTROSPECTION,
                ingredient_name.WOODENDOWEL,
                ingredient_name.DEADFLESH]),
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
            "I can take away your pain", [2, 0, 0, 0, 0, 0],
                [ACTION.STRUGGLE50], [
                ingredient_name.MOONWATER,
                ingredient_name.ROSEPETALS,
                ingredient_name.QUARTZ,
                ingredient_name.SALT,
                SPELLS.PROTECTION]),
            SPELLS.PROTECTION3:( "Strongest Protection Spell",
            "I will stand by you forever", [3, 0, 0, 0, 0, 0],
                [ACTION.STRUGGLE100], [
                ingredient_name.ADDERSTONE,
                SPELLS.PROTECTION2]),
        }

        self.traps = { # CONSUMABLE
            "type":item_type.TRAP,
            TRAPS.FRONTTOWARDSENEMY: ("Front Towards Enemy", # level 1
            "I regret nothing. The end.", [3, 0, 0, 0, 0, 0], 
                [], [
                ingredient_name.SHOTGUNSHELL, 
                ingredient_name.PIPE, 
                ingredient_name.NAIL, 
                ingredient_name.STRING, 
                ingredient_name.SPRING]),
            TRAPS.HOMEALONE: ("Home Alone", # level 1
            "Keep the change, ya filthy animal", [1, 0, 0, 0, 0, 0], 
                [], [
                ingredient_name.STRING, 
                ingredient_name.PAINTCAN]),
            TRAPS.SNAILPROBLEM: ("Snail Problem", # level 1
            "For problems out in the garden. Stuns enemies", [1, 0, 0, 0, 0, 0], 
                [], [
                ingredient_name.GLASSSHARD, 
                ingredient_name.SALT]),
            TRAPS.BANGBANGBANG: ("Bang Bang Bang", # level 1
            "All smoke, no sizzle. Stuns enemies", [0, 0, 0, 0, 0, 0], 
                [], [
                ingredient_name.FLASHBULB, 
                ingredient_name.SMALLBOX, 
                ingredient_name.STRING,
                ingredient_name.BATTERY]),
            TRAPS.SPILTLEGOS: ("Spilt Legos", # level 2
            "RIP Feet", [0, 0, 0, 0, 0, 0], 
                [], [
                ingredient_name.PLASTIC,
                TRAPS.SNAILPROBLEM]),
            TRAPS.AUTOSTUBBER: ("The Autostubber", # level 1
            "I hope you're wearing steeltoed boots...", [0, 0, 0, 0, 0, 0], 
                [], [
                ingredient_name.WOODBLOCK,
                ingredient_name.SPRING,
                ingredient_name.STRING]),
            TRAPS.THETOEANNIHILATOR: ("The Toe Annihilator", # level 2
            "Yeah, you read that right", [0, 0, 0, 0, 0, 0], 
                [], [
                TRAPS.AUTOSTUBBER,
                ingredient_name.NAIL,
                ingredient_name.SCISSORHALVE]),
            TRAPS.STUBTOSTUB: ("Stub to Stub", # level 3
            "Ashes to Ashes...", [0, 0, 0, 0, 1, 0], 
                [ACTION.GIVESASH], [
                TRAPS.THETOEANNIHILATOR,
                ingredient_name.SCREWS,
                ingredient_name.SCISSORHALVE]),
            TRAPS.HONEYPOT:("The Honeypot",
            "I have ascertained the target, Sir. And he's actually quite handsome.", [0, 0, 0, 0, 0, 0],
                [ACTION.STRUGGLE50], [
                ingredient_name.HONEY,
                ingredient_name.HONEYMUSTARD,
                ingredient_name.BOTTLE,
                ingredient_name.BOTTLECAP]),
        }

        self.weapons = { # MAX NUM USES
            "type":item_type.WEAPON,
            WEAPONS.DADDYSLITTLEMONSTER: ("Daddy's Little Monster", # level 1
            "It's nails on a stick, you get it", [0, 0, 0, 0, 0, 0], 
                [], [
                ingredient_name.WOODENDOWEL, 
                ingredient_name.NAIL]),
            WEAPONS.THEGREY: ("The Grey", 
            "Don't worry about Mythbusters, this'll work", [0, 0, 0, 0, 0, 0], 
                [], [ # level 1
                ingredient_name.WOODENDOWEL, 
                ingredient_name.NAIL, 
                ingredient_name.DUCTTAPE, 
                ingredient_name.SHOTGUNSHELL]),
            WEAPONS.TSHIRTCANNON: ("T-Shirt Cannon", # level 1
            "But at close range", [0, 0, 0, 0, 0, 0], 
                [], [
                ingredient_name.CLOTH,
                ingredient_name.PIPE,
                ingredient_name.SHOTGUNSHELL,
                ingredient_name.SCISSORHALVE]),
            WEAPONS.TSHIRTSNIPER: ("T-Shirt Sniper", # level 2
            "But at long range", [0, 0, 0, 0, 0, 0], 
                [], [
                WEAPONS.TSHIRTCANNON,
                ingredient_name.CLOTH,
                ingredient_name.PIPE,
                ingredient_name.BATTERY,
                ingredient_name.STEELWOOL,
                ingredient_name.SHOTGUNSHELL]),
            WEAPONS.SOAPINASOCK: ("Soap In A Sock", # level 1
            "Don't be a fuckin' narc", [0, 0, 0, 0, 0, 0], 
                [], [
                ingredient_name.CLOTH,
                ingredient_name.ROSEMARY,
                ingredient_name.EPSOMSALT]),
            WEAPONS.SHARPPENCIL: ("Sharp Pencil", # level 1
            "A FOOKING PEENCIL", [0, 0, 0, 0, 0, 0], 
                [], [
                ingredient_name.WOODENDOWEL,
                ingredient_name.SCISSORHALVE]),
            WEAPONS.POCKETSAND: ("Pocket Sand!",
            "Are you attempting to get to know me?", [0, 0, 0, 0, 0, 0], 
                [], [ # level 2
                ingredient_name.SALT,
                ingredient_name.GLASSSHARD,
                TOOLS.JIMSHAPIRO]),
            WEAPONS.ENTRYLEVEL: ("Entry Level", # level 1
            "It's just a stick with duct tape, man.", [0, 0, 0, 0, 0, 0], 
                [], [
                ingredient_name.WOODENDOWEL,
                ingredient_name.DUCTTAPE]),
            WEAPONS.THECONSTABLE: ("The Constable", # level 2
            "It's two sticks taped together", [0, 0, 0, 0, 0, 0], 
                [], [
                WEAPONS.ENTRYLEVEL,
                ingredient_name.WOODENDOWEL,
                ingredient_name.DUCTTAPE]),
            WEAPONS.FAGGOT: ("Faggot", # level 3
            "It's a bundle of sticks, and also me.", [0, 0, 0, 0, 0, 0], 
                [], [
                WEAPONS.THECONSTABLE,
                ingredient_name.WOODENDOWEL,
                ingredient_name.DUCTTAPE]),
            WEAPONS.TEDDYSTICK: ("The Teddy Stick", # level 4
            "Walk softly, motherfucker", [0, 0, 0, 0, 2, 0], 
                [], [
                WEAPONS.FAGGOT,
                ingredient_name.WOODENDOWEL,
                ingredient_name.DUCTTAPE]),
            WEAPONS.REALLYHOTPIZZA: ("Really Hot Pizza", # level 3
            "RIP roof of the mouth", [0, 0, 0, 0, 1, 0], 
                [], [
                ingredient_name.FLOUR,
                ingredient_name.ROSEMARY,
                ingredient_name.SALT,
                ingredient_name.TOMATO,
                ingredient_name.WHITETEALIGHT,
                ingredient_name.REISHIMUSHROOM,
                ingredient_name.OLIVEOIL]),
            WEAPONS.GARROTEFLOSS: ("Garrote Floss", # level 1
            "and the toothbrush is the detonation device!", [0, 0, 0, 0, 0, 0], 
                [], [
                ingredient_name.STRING,
                ingredient_name.MINT]),
            WEAPONS.SPLINTERPLACER5K: ("Splinter Placer 5k", # level 4
            "Brought to you by Zoom Care", [0, 0, 0, 0, 0, 0], 
                [], [
                WEAPONS.FAGGOT,
                ingredient_name.GLASSSHARD]),
            WEAPONS.TOEKNIFE: ("Toe Knife", # level 2
            "Now if only you had a shoe phone", [0, 0, 0, 0, 0, 0], 
                [], [
                ingredient_name.SCISSORHALVE,
                ingredient_name.SPRING,
                ingredient_name.SCREWS]),
            WEAPONS.BROTORCH: ("Bro Torch", # level 2
            "Bros before Not a Flamethrowers", [0, 0, 0, 0, 0, 0], 
                [], [
                ingredient_name.STEELWOOL,
                ingredient_name.PIPE,
                ingredient_name.MATCHSTICK,
                ingredient_name.OLIVEOIL]),
        }

        self.tools = { # MAX NUM USES
            "type":item_type.TOOL,
            TOOLS.RAVEON: ("Rave On!", # level 1
            "You can't see them, but they can see you.", [0, 0, 0, 0, 0, 0], 
                [], [
                ingredient_name.WOODENDOWEL, 
                ingredient_name.GLOWSTICK, 
                ingredient_name.DUCTTAPE]),
            TOOLS.MOLLYPOP: ("Mollypop", # level 1
            "Not for those who suffer from epilepsy.", [0, 0, 0, 0, 0, 0], 
                [], [
                ingredient_name.FLASHBULB,
                ingredient_name.SMALLBOX,
                ingredient_name.BATTERY]),
            TOOLS.LIGHTBRINGER: ("Lightbringer", # level 2
            "For the night is dark and full of terrors", [0, 0, 0, 0, 0, 0], 
                [], [
                TOOLS.MOLLYPOP,
                ingredient_name.FLASHBULB,
                ingredient_name.CIRCUIT,
                ingredient_name.BATTERY]),
            TOOLS.LOCKPICKINGLAWYER:("The Lockpicking Laywer", # level 1
            "This is The Lockpicking Laywer, and today I have something special", [0, 0, 0, 0, 0, 0], 
                [], [
                ingredient_name.COPPERWIRE,
                ingredient_name.NAIL]),
            TOOLS.BOSNIANTOOL:("BosnianBill", # level 2
            "We're just gonna use the tool that BosnianBill and I made", [0, 0, 0, 0, 0, 0], 
                [], [
                TOOLS.LOCKPICKINGLAWYER,
                ingredient_name.PIPE,
                ingredient_name.SPRING]),
            TOOLS.JIMSHAPIRO: ("Jim Shapiro", # level 1
            "Every single penny", [0, 0, 0, 0, 0, 0], 
                [], [
                ingredient_name.STRING,
                ingredient_name.WOODENDOWEL,
                ingredient_name.WOODBLOCK]),
        }
    
        # specials need to be initalized by the game engine as items and mapped to their enums
        self.special = {
            "type":item_type.SPECIAL,
            SPECIAL.THEGIFTER:("The Gifter",
            "Cindy Lou sends her best...", [0, 0, 0, 0, 0, 0], 
                [ACTION.SANTAEFFECT], [
                ingredient_name.SPECIAL] ),
            SPECIAL.MARCUSMUNITIONS:("Marcus Munitions",
            "What, you don't like money?", [0, 0, 0, 0, 0, 0],
                [ACTION.MARCUSEFFECT], [
                ingredient_name.SPECIAL] ),
            SPECIAL.SUCTIONCUPDILDO: ("Suction Cup Dildo", 
            "Made from 100% medical-grade embarrassment", [0, 0, 0, -1, 0, 0],
                [ACTION.DILDOEFFECT], [
                ingredient_name.SPECIAL] ),
        }

if __name__ == "__main__":
    # craft validation
    c = craft_engine()
    INGREDIENTS = [e for e in ingredient_name]
    CRAFTABLE = [e for e in SPELLS]+[e for e in TOOLS]+[e for e in TRAPS]+[e for e in WEAPONS]+[e for e in SPECIAL]
    DEFINED_CRAFTS = {}
    DEFINED_INGRED = {}
    used_ingredients = []
    model = tuple([type("str")]*2+[type([])]*3)
    print("\nValidating craft_engine")
    for i in [c.spells, c.tools, c.traps, c.weapons, c.special]:
        t = i.pop("type")
        assert t in item_type # Missing type enum entry
        for k, v in i.items():
            print("   {:10s} -> {}...".format(t.name, k.name))
            # check types
            assert k in CRAFTABLE # Missing craft enum entry
            DEFINED_CRAFTS[k]=""
            for u in range(0, len(model)):
                assert type(v[u]) == model[u] # Type mismatch between craft prototype and craft implementation
            assert len(v[2]) == 6 # Incomplete character list
            for act in v[3]:
                assert act in ACTION # Missing action enum entry
            for ing in v[4]:
                assert ing in CRAFTABLE+INGREDIENTS # Component enum not found (Ingredient or craft)
                DEFINED_INGRED[ing]=""
                used_ingredients.append(ing)
    # now the other way!
    print("\nensuring craftable enum entries are defined")
    for i in CRAFTABLE:
        assert i in DEFINED_CRAFTS # Craft enum is missing definition
    print("\n#### ALL TESTS PASSED ####")
    print("\n#### UNUSED INGREDIENTS ####")
    for i in (set(INGREDIENTS)-set(DEFINED_INGRED)):
        print(i.name)
    print("\n#### CRAFT INGREDIENT RARITY ####")
    for i in set(DEFINED_INGRED):
        c = used_ingredients.count(i)
        print("{}:{}".format(i.name, c))
