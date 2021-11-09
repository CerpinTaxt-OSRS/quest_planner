#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from quest import Quest


def parse_quests_json():
    """Reads from the configured json file and returns a dictionary of
    quests.
    """
    with open('quests.json', encoding='utf-8') as quests_f:
        return json.load(quests_f)


def find_recursive_skill_reqs(quest: Quest, all_quests: list, checked=set()):
    """Find the maximum level for each skill required to beat this
    Quest, taking into account each other quest this quest itself requires
    by recursively calling this function on subsequent quests, while avoiding
    infinitely re-checking quests already considered.
    """
    checked.add(quest)  # Add current quest to avoid infinite recursion
    max_skill_reqs = quest.get_skill_req()
    for quest_name in quest.get_quest_req():
        required_quest = all_quests.get(quest_name)
        # Don't recheck an already checked quest.
        if required_quest not in checked:
            required_quest_skill_reqs = find_recursive_skill_reqs(
                required_quest, all_quests)
            for skill, level in required_quest_skill_reqs.items():
                if level > max_skill_reqs.get(skill, 0):
                    max_skill_reqs[skill] = level
    return max_skill_reqs


def find_recursive_quest_reqs(quest: Quest, all_quests: list, checked=set()):
    """Find the total list of quests required to beat this Quest, taking into
    account each other quest this quest itself requires by recursively calling
    this function on subsequent quests, while avoiding infinitely re-checking
    quests already considered.
    """
    checked.add(quest)  # Add current quest to avoid infinite recursion
    required_quests_set = set(quest.get_quest_req())
    for quest_name in quest.get_quest_req():
        required_quest = all_quests.get(quest_name)
        # Don't recheck an already checked quest.
        if required_quest not in checked:
            required_quest_quest_reqs = find_recursive_quest_reqs(
                required_quest, all_quests, checked)
            required_quests_set.update(required_quest_quest_reqs)
    return required_quests_set


if __name__ == "__main__":
    quest_list = {
        name: Quest(name, info) for name, info in parse_quests_json().items()
    }
    jp = quest_list["Jungle Potion"]
