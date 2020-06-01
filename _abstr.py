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

class item_type(Enum):
    BOOK = 0
    WEAPON = 1
    LIGHT = 2
    ALTAR = 3
    THEGIFTER = 4
    MARCUSMUNITIONS = 5

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
    BOOK_ICON = chr(10026)
    ALTAR_ICON = chr(9912)
    LIGHT_ICON = chr(9775)
    CRAFT_ICON = chr(9881)
    SWORD_ICON = chr(9876)

class size(Enum):
    """Enumeration of all item sizes (except lamps)"""
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
    """Enumeratio of item durabilities"""
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
    """Ingredients are the primary mechanism in crafting. Crafting trees can be found in craf_engine.py"""
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

class SPELLS(Enum):
    """Spells have consumption time"""
    WISHFORHELP = 0
    HOUSESALAD = 1
    HEALINGMAX = 2
    HEALINGMINOR = 3
    HEALINGMIDDLE = 4
    FLIGHT = 5
    FIGHT = 6

class TRAPS(Enum):
    """Traps have setup time"""
    FRONTTOWARDSENEMY = 0
    HOMEALONE = 1
    SNAILPROBLEM = 2
    BANGBANGBANG = 3
    SPILTLEGOS = 4

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
    STARTTRADE = 0
    FUCK = 1
    MURDER = 2
    GETFREETRAP = 10
    GETFREETOOL = 11 
    GETFREESPELL = 12 # gifts crafted spell
    GETFREECRAFT = 13 # unlocks acraft
    GETFREEMAGIC = 14  # unlocks a spell
    GETFREEITEM = 15 # gifts a completed craft
    GETFREEING = 16 # gifts a free ingredient
    GETFREEWEAPON = 15
    # Gen 100->score->pick highest item
    INCREASEINT = 20
    INCREASECHA = 21
    INCREASESTR = 22
    INCREASELCK = 23
    INCREASEPCT = 24
    # Specific Character Actions
    GIVESANTAGIFT = 100 # 

class compute:
    """Class defines how items and attributes are randomized in game. Also creates scores and computes affect."""
    def __init__(self):
        pass
    def RANDOMIZE_DURABILITY(self):
        """Randomizes an item's durability - can be used to affect number of uses or effectiveness in battle"""
        return random.choice(
            [durability.FRAGILE]*5+\
            [durability.RAMSHACKLE]*10+\
            [durability.ADEQUATE]*70+\
            [durability.STURDY]*9+\
            [durability.CHONKY]*5+\
            [durability.YOKED]*1)
    def RANDOMIZE_RARITY(self):
        """Randomizes an item's rarity - can be used to affect the quality of crafts"""
        return random.choice(
            [rarity.COMMON]*25+\
            [rarity.UNUSUAL]*15+\
            [rarity.STRANGE]*5+\
            [rarity.INCREDIBLE]*2+\
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
        

if __name__ == "__main__":
    r = []
    for i in range(0, 100):
        r += [compute().ALIGNMENT()]
    print(sum(r))
    print(sum(r)/len(r))