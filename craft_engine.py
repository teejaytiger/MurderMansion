## defines the crafting trees and their mechanics
from enum import Enum
if __name__=='__main__':
    # testing
    from _abstr import ingredient_name as ing
else:
    from ._abstr import ingredient_name as ing


class SPELLS(Enum):
    ## Spells have consumption time
    WISHFORHELP = 0
    HOUSESALAD = 1
    HEALINGMAX = 2

class TRAPS(Enum):
    ## Traps have setup time
    FRONTTOWARDSENEMY = 0
    HOMEALONE = 1
    SNAILPROBLEM = 2
    BANGBANGBANG = 3

class WEAPONS(Enum):
    ## Weapons have a maximum number of uses
    DADDYSLITTLEMONSTER = 0
    THEGREY = 1

class TOOLS(Enum):
    ## Tools have a maximum number of uses, and increase relevant character attribute until used up
    RAVEON = 0
    MOLLYPOP = 1
    LIGHTBRINGER = 2


spells = {
    "WISHFORHELP":("Wish for help", 
    "Wish someone would show up to help", [
        ing.CATWHISKER, 
        ing.YELLOWTEALIGHT, 
        ing.MATCHSTICK]),
    "HOUSESALAD":("House Salad", 
    "This is the super salad. Grants 10 health points", [
        ing.SCISSORHALVE, 
        ing.ICEBERGLETTUCE, 
        ing.TOMATO, 
        ing.CROUTONS, 
        ing.OLIVEOIL, 
        ing.VINEGAR]),
    "HEALINGMAX":("Max Healing Potion", 
    "Grants 70 health points", [
        ing.ROSEMARY, 
        ing.QUARTZ, 
        ing.WHITETEALIGHT, 
        ing.MOONWATER, 
        ing.MATCHSTICK]),
}

traps = {
    "FRONTTOWARDSENEMY": ("Front Towards Enemy", 
    "I regret nothing. The end.", [
        ing.SHOTGUNSHELL, 
        ing.PIPE, 
        ing.NAIL, 
        ing.STRING, 
        ing.SPRING]),
    "HOMEALONE": ("Home Alone", 
    "Keep the change, ya filthy animal", [
        ing.STRING, 
        ing.PAINTCAN]),
    "SNAILPROBLEM": ("Snail Problem", 
    "For problems out in the garden. Stuns enemies", [
        ing.GLASSSHARD, 
        ing.SALT]),
    "BANGBANGBANG": ("Bang Bang Bang", 
    "All smoke, no sizzle. Stuns enemies", [
        ing.FLASHBULB, 
        ing.SMALLBOX, 
        ing.STRING,
        ing.BATTERY]),
}

weapons = {
    "DADDYSLITTLEMONSTER": ("Daddy's Little Monster", 
    "It's nails on a stick, you get it", [
        ing.WOODENDOWEL, 
        ing.NAIL]),
    "THEGREY": ("The Grey", 
    "Don't worry about Mythbusters, this'll work", [
        ing.WOODENDOWEL, 
        ing.NAIL, 
        ing.DUCTTAPE, 
        ing.SHOTGUNSHELL]),
}

tools = {
    "RAVEON": ("Rave On!",
    "Improves perception slightly. Very slightly. Also not for very long",[
        ing.WOODENDOWEL, 
        ing.GLOWSTICK, 
        ing.DUCTTAPE]),
    "MOLLYPOP": ("Mollypop", 
    "Strobe light that improves perception. Not for those who suffer from epilepsy.", [
        ing.FLASHBULB,
        ing.SMALLBOX,
        ing.BATTERY]),
    "LIGHTBRINGER": ("Lightbringer", 
    "Lord of light! Come to us in our darkness... For the night is dark and full of terrors", [
        ing.FLASHBULB,
        ing.CIRCUIT,
        ing.BATTERY,
        ing.SMALLBOX,
        ing.SCREWS])
}