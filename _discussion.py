from _abstr import container, ACTION
from enum import Enum

"""
Characters:
MIB - Noisy Cricket (weapon)
SANTA - The Cindy Lou (trap, cookies based)
CLOSET_PERSON - 
BIG_RICHARD

"""

class DIA(Enum):
    SANTA1 = 0
    SANTAALICE1 = 1
    SANTAALICE2 = 2
    SANTAALICE3 = 3
    SANTA21 = 21
    SANTA22 = 22
    SANTA23 = 23
    SANTAALICE211 = 211
    SANTAALICE212 = 212
    SANTAALICE221 = 221
    SANTAALICE222 = 222
    SANTAALICE223 = 223
    SANTAALICE231 = 231
    SANTAALICE232 = 232
    SANTA312


class SANTADIA:
    spawn_in = container.CHIMNEY
    SANTADIA = {
        DIA.SANTA1:("HI HI HI","Joyous",[0], 
            [DIA.SANTAALICE1, DIA.SANTAALICE2, DIA.SANTAALICE3]),
        DIA.SANTAALICE1:("Who the fuck are you supposed to be?","Rude",[1], 
            [DIA.SANTA21]),
        DIA.SANTAALICE2:("Hi hi hi?","Confused",[0], 
            [DIA.SANTA22]),
        DIA.SANTAALICE3:("AAAAAHHHHHH","Startled",[0], 
            [DIA.SANTA23]),
        DIA.SANTA21:("That language isn't very nice! I might have to put you on the naughty list!","Finger wag",[0],
            [DIA.SANTAALICE211, DIA.SANTAALICE212]),
        DIA.SANTA22:("Merry Christmas!","Jolly",[0],
            [DIA.SANTAALICE221, DIA.SANTAALICE222, DIA.SANTAALICE223]),
        DIA.SANTA23:("Oh sorry, you looked like my wife! Would you happen to have any cookies?","Horny", [0], 
            [DIA.SANTAALICE231, DIA.SANTAALICE232]),
        DIA.SANTAALICE211:("Fuck you","annoyed",[1],
            []),#TODO: Not Done
        DIA.SANTAALICE212:("Sorry, you caught me off guard. Why are you in the Chimney?","remorseful",[0],
            [])
        DIA.SANTAALICE221:("...Merry Christmas?","Extra confused",[0],
            []),
        DIA.SANTAALICE222:("Oh, you're Santa. Wait, why are you Santa?","Piqued",[0],
            []),
        DIA.SANTAALICE223:("I don't have time to play your mind games, old man. What's in the sack?","Assertive",[1],
            []),
        DIA.SANTAALICE231:("No, you got me, I'm Mrs. Claus, daddy. You show me your North Pole and you can have all the cookies you want.","Aroused",[2],
            []),
        DIA.SANTAALICE232:("I don't have any cookies, but I'll trade if you cut the fireplace creep act.","Irked",[],
            []),



    }