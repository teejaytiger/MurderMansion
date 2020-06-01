## defines the crafting trees and their mechanics
from enum import Enum
if __name__=='__main__':
    # testing
    from _abstr import ingredient_name as ing, SPELLS, TRAPS, WEAPONS, TOOLS, SPECIAL
else:
    from ._abstr import ingredient_name as ing, SPELLS, TRAPS, WEAPONS, TOOLS, SPECIAL

class crafts:
    def __init__(self):
        self.spells = {
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
                ing.MOONWATER]),
            "HEALINGMIDDLE":("Travis Potion",
            "Your middlest healing potion. Grants 30 health points", [
                ing.BOTTLE,
                ing.QUARTZ,
                ing.MOONWATER]),
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

        self.traps = {
            "FRONTTOWARDSENEMY": ("Front Towards Enemy", # level 1
            "I regret nothing. The end.", [
                ing.SHOTGUNSHELL, 
                ing.PIPE, 
                ing.NAIL, 
                ing.STRING, 
                ing.SPRING]),
            "HOMEALONE": ("Home Alone", # level 1
            "Keep the change, ya filthy animal", [
                ing.STRING, 
                ing.PAINTCAN]),
            "SNAILPROBLEM": ("Snail Problem", # level 1
            "For problems out in the garden. Stuns enemies", [
                ing.GLASSSHARD, 
                ing.SALT]),
            "BANGBANGBANG": ("Bang Bang Bang", # level 1
            "All smoke, no sizzle. Stuns enemies", [
                ing.FLASHBULB, 
                ing.SMALLBOX, 
                ing.STRING,
                ing.BATTERY]),
            "SPILTLEGOS": ("Spilt Legos", # level 2
            "RIP Feet", [
                ing.PLASTIC,
                TRAPS.SNAILPROBLEM]),
            "AUTOSTUBBER": ("The Autostubber", # level 1
            "I hope you're wearing steeltoed boots...", [
                ing.WOODBLOCK,
                ing.SPRING,
                ing.STRING]),
            "THETOEANNIHILATOR": ("The Toe Annihilator", # level 2
            "Yeah, you read that right", [
                TRAPS.AUTOSTUBBER,
                ing.NAIL,
                ing.SCISSORHALVE]),
            "STUBTOSTUB": ("Stub to Stub", # level 3
            "Ashes to Ashes...", [
                TRAPS.THETOEANNIHILATOR,
                ing.SCREWS,
                ing.SCISSORHALVE])
        }

        self.weapons = {
            "DADDYSLITTLEMONSTER": ("Daddy's Little Monster", # level 1
            "It's nails on a stick, you get it", [
                ing.WOODENDOWEL, 
                ing.NAIL]),
            "THEGREY": ("The Grey", 
            "Don't worry about Mythbusters, this'll work", [ # level 1
                ing.WOODENDOWEL, 
                ing.NAIL, 
                ing.DUCTTAPE, 
                ing.SHOTGUNSHELL]),
            "TSHIRTCANNON": ("T-Shirt Cannon", # level 1
            "But at close range", [
                ing.CLOTH,
                ing.PIPE,
                ing.SHOTGUNSHELL,
                ing.SCISSORHALVE]),
            "TSHIRTSNIPER": ("T-Shirt Sniper", # level 2
            "But at long range", [
                WEAPONS.TSHIRTCANNON,
                ing.CLOTH,
                ing.PIPE,
                ing.BATTERY,
                ing.STEELWOOL,
                ing.SHOTGUNSHELL]),
            "SOAPINASOCK": ("Soap In A Sock", # level 1
            "Don't be a fuckin' narc", [
                ing.CLOTH,
                ing.ROSEMARY,
                ing.EPSOMSALT]),
            "SHARPPENCIL": ("Sharp Pencil", # level 1
            "A FOOKING PEENCIL", [
                ing.WOODENDOWEL,
                ing.SCISSORHALVE]),
            "POCKETSAND": ("Pocket Sand!",
            "Are you attempting to get to know me?", [ # level 2
                ing.SALT,
                ing.GLASSSHARD,
                TOOLS.JIMSHAPIRO]),
            "ENTRYLEVEL": ("Entry Level", # level 1
            "It's just a stick with duct tape, man.", [
                ing.WOODENDOWEL,
                ing.DUCTTAPE]),
            "THECONSTABLE": ("The Constable", # level 2
            "It's two sticks taped together", [
                WEAPONS.ENTRYLEVEL,
                ing.WOODENDOWEL,
                ing.DUCTTAPE]),
            "FAGGOT": ("Faggot", # level 3
            "It's a bundle of sticks, and my best friend is gay", [
                WEAPONS.THECONSTABLE,
                ing.WOODENDOWEL,
                ing.DUCTTAPE]),
            "TEDDYSTICK": ("The Teddy Stick", # level 4
            "Walk softly, motherfucker", [
                WEAPONS.FAGGOT,
                ing.WOODENDOWEL,
                ing.DUCTTAPE]),
            "REALLYHOTPIZZA": ("Really Hot Pizza", # level 3
            "RIP roof of the mouth", [
                ing.FLOUR,
                ing.ROSEMARY,
                ing.SALT,
                ing.TOMATO,
                ing.WHITETEALIGHT,
                ing.REISHIMUSHROOM,
                ing.OLIVEOIL]),
            "GARROTEFLOSS": ("Garrote Floss", # level 1
            "and the toothbrush is the detonation device!", [
                ing.STRING,
                ing.MINT]),
            "SPLINTERPLACER5K": ("Splinter Placer 5k", # level 4
            "Brought to you by Zoom Care", [
                WEAPONS.FAGGOT,
                ing.GLASSSHARD]),
            "TOEKNIFE": ("Toe Knife", # level 2
            "Now if only you had a shoe phone", [
                ing.SCISSORHALVE,
                ing.SPRING,
                ing.SCREWS]),
            "BROTORCH": ("Bro Torch", # level 2
            "Bros before Not a Flamethrowers", [
                ing.STEELWOOL,
                ing.PIPE,
                ing.MATCHSTICK,
                ing.OLIVEOIL]),
        }

        self.tools = {
            "RAVEON": ("Rave On!", # level 1
            "Lets you read books anywhere at quarter speed. Try dancing while you do it.",[
                ing.WOODENDOWEL, 
                ing.GLOWSTICK, 
                ing.DUCTTAPE]),
            "MOLLYPOP": ("Mollypop", # level 1
            "Lets you read books anywhere at half speed. Not for those who suffer from epilepsy.", [
                ing.FLASHBULB,
                ing.SMALLBOX,
                ing.BATTERY]),
            "LIGHTBRINGER": ("Lightbringer", # level 2
            "Lord of light! Come to us in our darkness... For the night is dark and full of terrors", [
                TOOLS.MOLLYPOP,
                ing.FLASHBULB,
                ing.CIRCUIT,
                ing.BATTERY]),
            "LOCKPICKINGLAWYER":("The Lockpicking Laywer", # level 1
            "This is The Lockpicking Laywer, and today I have something very special for you",[
                ing.COPPERWIRE,
                ing.NAIL]),
            "BOSNIANTOOL":("BosnianBill", # level 2
            "We're just gonna use the tool that BosnianBill and I made",[
                TOOLS.LOCKPICKINGLAWYER,
                ing.PIPE,
                ing.SPRING]),
            "JIMSHAPIRO": ("Jim Shapiro", # level 1
            "JIM 'THE HAMMER' SHAPIRO", [
                ing.STRING,
                ing.WOODENDOWEL,
                ing.WOODBLOCK]),
        }

        # specials need to be initalized by the game engine as items and mapped to their enums
        self.special = {
            "THEGIFTER":("The Gifter","Cindy Lou sends her best...",[ # Trap, probaby cookies and milk based
                SPECIAL.THEGIFTER,
            ]),
            "MARCUSMUNITIONS":("Marcus Munitions","What, you don't like money?",[ # One shot gun
                SPECIAL.MARCUSMUNITIONS,
            ]),
            "SUCTIONCUPDILDO": ("Suction Cup Dildo", "Why was this in the laundry?", [ # WEAPON, causes embarrassment
                SPECIAL.SUCTIONCUPDILDO,
            ])
        }