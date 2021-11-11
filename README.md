# quest_planner
Loads all quest requirements from a .json file and allows you to find out what skill, quest, and other requirements are needed to complete some specific quest in Old School RuneScape.

Run from the command line with python3 providing any quests you want to find the requirements of as strings.

## Example
Executing:
`$ python3 quest_requirements.py "One Small Favour"`

Will produce:
```
========================================================
One Small Favour (p2p)

Skill requirements:
        agility         36
        crafting        25
        herblore        18
        smithing        30

Quest requirements:
        Rune Mysteries
        Shilo Village
        Jungle Potion
        Druidic Ritual

Other requirements:
(none)
```

## Extra
Providing "Quest Point Cape" will find the total max requirements of all quests in the game.