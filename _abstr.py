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

class size(Enum):
    TINY = 0        ## weight 0
    SMALL = 1       ## weight 1
    MEDUIM = 2      ## etc
    LARGE = 3
    HUGE = 4

class lamp_size(Enum): 
    """affects how long a book takes to read"""
    CANDLE = 0      ## 5
    SCONCE = 1      ## 3
    DESKLAMP = 2    ## 1
    FLOORLAMP = 3   ## 1

class rarity(Enum):
    COMMON = 0       ## 25
    UNUSUAL = 1      ## 15
    STRANGE = 2      ## 5
    INCREDIBLE = 3   ## 2
    IMMACULATE = 4   ## 2
    MYTHOLOGICAL = 5 ## 1

class durability(Enum):
    FRAGILE = 0     ## 5
    RAMSHACKLE = 1  ## 10
    ADEQUATE = 2    ## 70
    STURDY = 3      ## 9
    CHUNKY = 4      ## 5
    YOKED = 5       ## 1
    
class room_type(Enum):
    BEDROOM = 0
    SITTINGROOM = 1
    KITCHEN = 2
    HALLWAY = 3
    STUDY = 4
    LIBRARY = 5

class container(Enum):  # contains up to:
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
    def MAX_SIZE(self):
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
            self.DESK:      [size.TINY, size.SMALL, size.MEDUIM, size.LARGE, size.HUGE],
            self.UNDERBED:  [size.MEDUIM, size.LARGE, size.HUGE],
            self.CHESTERFIELD:[size.TINY, size.SMALL]
        }

class available(Enum):
    AVAILABLE = 0
    UNAVAILABLE = 1 

class ingredient_name(Enum):
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
    NEWSPAPER = 66      # 
    PAINTCAN = 67       # 
    DUCTTAPE = 68       # 
    FLASHBULB = 69      # 
    SPRING = 70         # 
    GLOWSTICK = 71      # 
    BATTERY = 72        # 
    CIRCUIT = 73        # 
    ## Haley's salad
    ICEBERGLETTUCE = 100# 
    TOMATO = 101        #
    CROUTONS = 102      # 
    OLIVEOIL = 103      # 

class compute:
    def __init__(self):
        pass
    def RANDOMIZE_DURABILITY(self):
        return random.choice(
            [durability.FRAGILE]*5+\
            [durability.RAMSHACKLE]*10+\
            [durability.ADEQUATE]*70+\
            [durability.STURDY]*9+\
            [durability.CHUNKY]*5+\
            [durability.YOKED]*1)
    def RANDOMIZE_RARITY(self):
        return random.choice(
            [rarity.COMMON]*25+\
            [rarity.UNUSUAL]*15+\
            [rarity.STRANGE]*5+\
            [rarity.INCREDIBLE]*2+\
            [rarity.IMMACULATE]*2+\
            [rarity.MYTHOLOGICAL]*1)
    def RANDOMIZE_SIZE_BOOK(self):
        return random.choice(
            [size.TINY]*1+\
            [size.SMALL]*5+\
            [size.MEDUIM]*3+\
            [size.LARGE]*1)
    def RANDOMIZE_SIZE_LAMP(self):
        return random.choice(
            [lamp_size.CANDLE]*5+\
            [lamp_size.SCONCE]*3+\
            [lamp_size.DESKLAMP]*1+\
            [lamp_size.FLOORLAMP]*1)
    def RANDOMIZE_ROOM_TYPE(self):
        return random.choice(
            [room_type.BEDROOM]*50+\
            [room_type.SITTINGROOM]*20+\
            [room_type.KITCHEN]*5+\
            [room_type.HALLWAY]*10+\
            [room_type.STUDY]*10+\
            [room_type.LIBRARY]*5)
    def RANDOMIZE_INGREDIENT_NAME(self):
        return random.choice([e for e in ingredient_name])
    def ALIGNMENT(self):
        # returns an alignment normalized from -1 to 1
        a = random.uniform(0, 1.0)
        b = random.uniform(0, 1.0)
        x = sqrt(-2*log(a))*(cos(2*pi*b))
        y = (sqrt(-2*log(a))*(sin(2*pi*b)))
        return random.choice([x/4, y/4])
    def RANDOMIZE_SIZE_INGREDIENT(self):
        return size.TINY
    def RANDOMIZE_SIZE_ALTAR(self):
        return size.SMALL
        

if __name__ == "__main__":
    r = []
    for i in range(0, 100):
        r += [compute().ALIGNMENT()]
    print(sum(r))
    print(sum(r)/len(r))