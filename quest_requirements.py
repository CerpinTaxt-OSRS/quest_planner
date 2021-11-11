#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from quest import Quest
from pprint import pprint


def get_quest_requirements(quest: Quest, all_quests: list):
    """Finds the true and completely detailed quest requirements for a given
    quest. Calls each of the recursive search functions to populate the
    `requirements` section, and returns the dictionary/json representation of
    this quest.
    """
    q = {
        quest.name: {
            "f2p": quest.f2p,
            "requirements": {
                "skills": find_recursive_skill_reqs(quest, quest_list),
                "quests": quest.get_quest_req(),
                "other": find_recursive_other_reqs(quest, quest_list)
            }
        }
    }
    return q


def quest_point_cape(quest_list):
    """Special function to find and return the full requirements of a QPC."""
    info = {
        "f2p": False,
        "requirements": {
            "skills": {},
            "quests": [quest for quest in quest_list.keys()],
            "other": {}
        }
    }
    return Quest("Quest Point Cape", info)


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
        if required_quest and required_quest not in checked:
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
        if required_quest and required_quest not in checked:
            required_quest_quest_reqs = find_recursive_quest_reqs(
                required_quest, all_quests, checked)
            required_quests_set.update(required_quest_quest_reqs)
    return list(required_quests_set)


def find_recursive_other_reqs(quest: Quest, all_quests: list, checked=set()):
    """Find the total list of other miscellaneous requirements needed to beat
    this Quest, taking into account each other quest this quest itself requires
    by recursively calling this function on subsequent quests, while avoiding
    infinitely re-checking quests already considered.
    """
    checked.add(quest)  # Add current quest to avoid infinite recursion
    max_other_reqs = quest.get_other_req()
    for quest_name in quest.get_quest_req():
        required_quest = all_quests.get(quest_name)
        # Don't recheck an already checked quest.
        if required_quest and required_quest not in checked:
            required_quest_other_reqs = find_recursive_other_reqs(
                required_quest, all_quests, checked)
            for task, val in required_quest_other_reqs.items():
                if val > max_other_reqs.get(task, 0):
                    max_other_reqs[task] = val
    return max_other_reqs


if __name__ == "__main__":
    quest_list = {
        name: Quest(name, info) for name, info in parse_quests_json().items()
    }
    qpc = quest_point_cape(quest_list)    
    qpc = get_quest_requirements(qpc, quest_list)
    qpc = Quest(list(qpc.keys())[0], qpc[list(qpc.keys())[0]])
    print(qpc)
