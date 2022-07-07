# Murder Mansion

Murder mansion is a text-based RPG I'm developing for my wife. It has elements of magic, horror, and fear. 

## I need your help!
Anyone who helps me come up with ideas for characters Alice can encounter, new ideas for spells, and craftable items she can use will end up in the credits! It'll be well worth it for her to experience your influence in this game!

## Gameplay: The Most Dangerous Game
You wake up in a house with a murderer after you, moving from room to room avoiding confrontation as much as possible, while building up your magical abilities by performing spells, crafting weapons, traps, and tools, and by reading books to know your enemy. 

Since you're in a mansion, the room situation almost feels... infinite? No current end state has been determined. 

when you enter a room, you lock the door behind you. You have a certain amount of time before the murderer can make it to the room your in via a different route. Use that time to collect items, craft weapons, place traps, cast spells, and read books. 

When you're finished with your tasks, exit the room through one of three doors, but take caution, and the murderer could be in any of those rooms, waiting for you. 

Some rooms contain victims (alive or dead) that may be able to help you by trading items and providing information. It's best to hear these people out and see what they have to offer you. 

Keep moving! If you stay in any one place too long, the murderer could find his way into the room! If your traps and spells don't get him, you'll have to struggle to escape! Use crafted weapons, potions, or melee attacks to liberate yourself from your captor. Some weapons and potions are particularly potent, and can deftly incapacitate your foe. 

Leave the mansion at all costs! Become a badass in the process! Live life on the edge of your seat as you attempt to escape Murder Mansion. 

## Crafting
The crafting system uses a set of ingredients, scattered all over the mansion in appropriate distributions to simulate rarity. The spells and crafts are collaborative and come from ideas made by family and friends! An incomplete list of ingredients is shown below:

    CATWHISKER      MUGWORT         DEADFLESH       
    MURDERWEAPON    QUARTZ          DRYROT           
    BLACKWIDOW      WHITESAGE       SILVER            
    EPSOMSALT       GLASSEYE        TEARS         
    COPPERWIRE      GOLD            MINT          
    ROSEMARY        ROSEPETALS      LAVENDER        
    SKULL           ADDERSTONE      MOONWATER      
    GRAVEYARDDIRT   YELLOWTEALIGHT  BLACKTEALIGHT   
    WHITETEALIGHT   SALT            VINEGAR      
    MATCHSTICK      PIPE            SHOTGUNSHELL     
    WOODBLOCK       SCISSORHALVE    PLASTIC      
    WOODENDOWEL     LENS            SMALLBOX       
    SCREWS          NAIL            BOTTLECAP      
    GLASSSHARD      STRING          ROPE   
    NEWSPAPER       PAINTCAN        DUCTTAPE    
    FLASHBULB       SPRING          GLOWSTICK     
    BATTERY         CIRCUIT         ICEBERGLETTUCE  
    TOMATO          CROUTONS        OLIVEOIL    

> Crafts are defined in `craft_engine` class and uses the enumerated ingredients listed in `_abstr` to create requirements for spells, traps, weapons, and tools.  
> Check out [this link](https://github.com/teejaytiger/MurderMansion/blob/884054e9763ea0462e044b468d2547a37c3c42b7/_abstr.py#L406) to see some examples of crafts and spells I've already put in the game!  
> You can also see an updated ingredients list in [this file](https://github.com/teejaytiger/MurderMansion/blob/884054e9763ea0462e044b468d2547a37c3c42b7/_abstr.py#L172)

Here is an example spell:  

![example spell](https://raw.githubusercontent.com/teejaytiger/MurderMansion/master/images/spell_example.PNG)
>+/- denotes the blessed/cursed value (`_craft().alignment`), which affects the quality of the craft. Craft quality is dependent on the quality of the ingredients. Taking advantage of this mechanic can help the player to craft powerful items. Alignments of ingredients are rolled on room construction. Badges aren't implemented, but will give useful information in the context of the item (e.g. trap and weapon badges will show damage, books with show reading time, etc)

Spells are enumerated in the `SPELLS` class, traps in `TRAPS`, and so on.

## Code
Murder Mansion uses simple mechanisms to randomize the gameplay and give a higher replay value. Spawns and gamepley elements are selected using a distribution curve, and rooms are made of containers that hold spawns. This is convenient from a coding perspective, because even humans are in containers like closets, as they're hiding from the murderer! 

The crafting system uses a set of ingredients to power a fixed set of craftables that can be easily expanded. The entire system is scalable, even though probabilities aren't the easiest to update without disrupting game balance (when has that ever not been true). A convenient module `_abstr` contains all the named constants and randomization functionality, so it's very easy to expand or "reskin" the game. 

The murderer regens life after every encounter, so it's best to keep moving and avoid the room timeouts. Studies are the best place to craft and read, as their timeouts are extended. Tieouts are set in `_room.py`. 

Item constructors can be found in `_item.py`, and use enums and functions from `abstr` to dynamically generate items on a distribution curve. `_abstr` is the place to make game-wide adjustments to item attribute distributions. 
