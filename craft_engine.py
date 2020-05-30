## defines the crafting trees and their mechanics
from enum import Enum
if __name__=='__main__':
    # testing
    from _abstr import ingredient_name as ing, SPELLS, TRAPS, WEAPONS, TOOLS, SPECIAL
else:
    from ._abstr import ingredient_name as ing, SPELLS, TRAPS, WEAPONS, TOOLS, SPECIAL

spells = {
    "WISHFORHELP":("Wish for help", 
    "Wish someone would show up to help", [
        ing.CATWHISKER, 
        ing.YELLOWTEALIGHT, 
        ing.MATCHSTICK]),
    "HOUSESALAD":("House Salad", 
    "This is the super salad. Grants 70 health points", [
        ing.SCISSORHALVE, 
        ing.ICEBERGLETTUCE, 
        ing.TOMATO, 
        ing.CROUTONS, 
        ing.OLIVEOIL, 
        ing.VINEGAR]),
    "HEALINGMINOR":("Griffin Potion",
    "Your sweet baby healing potion. Grants 10 health points", [
        ing.BOTTLE,
        ing.MOONWATER,])
    "HEALINGMIDDLE":("Travis Potion",
    "Your middlest healing potion. Grants 30 health points", [
        ing.BOTTLE,
        ing.QUARTZ,
        ing.MOONWATER,])
    "HEALINGMAX":("Justin Potion", 
    "Your oldest healing potion. Grants 50 health points", [
        ing.BOTTLE,
        ing.ROSEMARY, 
        ing.QUARTZ, 
        ing.WHITETEALIGHT, 
        ing.MOONWATER, 
        ing.MATCHSTICK]),
    "FLIGHT":("Flight",
    "The parasypathetic nervous system reacts...", [
        ing.REISHIMUSHROOM,
        ing.MOONWATER,
        ing.ROSEMARY,
        ing.BOTTLE]),
    "FIGHT":("Fight",
    "...and you're in fight or flight mode", [
        ing.BOTTLE,
        ing.BLACKWIDOW,
        ing.OLEANDER,
        ing.NIGHTSHADE]),
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
        TOOLS.MOLLYPOP,
        ing.FLASHBULB,
        ing.CIRCUIT,
        ing.BATTERY]),
    "LOCKPICKINGLAWYER":("The Lockpicking Laywer",
    "This is The Lockpicking Laywer, and today I have something special for you",[
        ing.COPPERWIRE,
        ing.NAIL]),
    "BOSNIANTOOL":("BosnianBill",
    "We're just gonna use the tool that BosnianBill and I made",[
        TOOLS.LOCKPICKINGLAWYER,
        ing.PIPE,
        ing.SPRING]),
}

special = {
    "THEGIFTER":("The Gifter","Cindy Lou sends her best...",[ # Trap, probaby cookies and milk based
        SPECIAL.THEGIFTER,
    ]),
    "MARCUSMUNITIONS":("Marcus Munitions","What, you don't like money?",[ # One shot gun
        SPECIAL.MARCUSMUNITIONS,
    ])
}