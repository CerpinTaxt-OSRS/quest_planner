#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module to find real quest requirements for OSRS quests."""

import argparse
import json
from quest import Quest


def get_quest_requirements(query_quest: Quest, quest_list: list):
    """Finds the true and completely detailed quest requirements for a given
    quest. Calls each of the recursive search functions to populate the
    `requirements` section, and returns the dictionary/json representation of
    this quest.
    :param query_quest: The quest to find the requirements of.
    :param quest_list: The list of all available quests.
    :rtype: Quest
    """
    quest_info = {
        "f2p": query_quest.f2p,
        "requirements": {
            "skills": find_recursive_skill_reqs(query_quest, quest_list, set()),
            "quests": query_quest.get_quest_req(),
            "other": find_recursive_other_reqs(query_quest, quest_list, set())
        }
    }
    return Quest(query_quest.name, quest_info)


def quest_point_cape(quest_list):
    """Special function to find and return the full requirements of a QPC.
    :param quest_list: The list of all available quests.
    :rtype: Quest
    """
    info = {
        "f2p": False,
        "requirements": {
            "skills": {},
            "quests": list(quest_list.keys()),
            "other": {}
        }
    }
    return Quest("Quest Point Cape", info)


def parse_quests_json():
    """Reads from the configured json file and returns a dictionary of
    quests.
    :rtype: dict
    """
    with open('quests.json', encoding='utf-8') as quests_f:
        return json.load(quests_f)


def find_recursive_skill_reqs(query_quest: Quest, all_quests: list, checked):
    """Find the maximum level for each skill required to beat this
    Quest, taking into account each other quest this quest itself requires
    by recursively calling this function on subsequent quests, while avoiding
    infinitely re-checking quests already considered.
    :param query_quest: The quest to find the requirements of.
    :param quest_list: The list of all available quests.
    :param checked: Set of already considered quest in this lookup.
    :rtype: string
    """
    if not checked:
        checked = set()
    checked.add(query_quest)  # Add current quest to avoid infinite recursion
    max_skill_reqs = query_quest.get_skill_req()
    for quest_name in query_quest.get_quest_req():
        required_quest = all_quests.get(quest_name)
        # Don't recheck an already checked quest.
        if required_quest and required_quest not in checked:
            required_quest_skill_reqs = find_recursive_skill_reqs(
                required_quest, all_quests, set())
            for skill, level in required_quest_skill_reqs.items():
                if level > max_skill_reqs.get(skill, 0):
                    max_skill_reqs[skill] = level
    return max_skill_reqs


def find_recursive_quest_reqs(query_quest: Quest, all_quests: list, checked):
    """Find the total list of quests required to beat this Quest, taking into
    account each other quest this quest itself requires by recursively calling
    this function on subsequent quests, while avoiding infinitely re-checking
    quests already considered.
    :param query_quest: The quest to find the requirements of.
    :param quest_list: The list of all available quests.
    :param checked: Set of already considered quest in this lookup.
    :rtype: list
    """
    if not checked:
        checked = set()
    checked.add(query_quest)  # Add current quest to avoid infinite recursion
    required_quests_set = set(query_quest.get_quest_req())
    for quest_name in query_quest.get_quest_req():
        required_quest = all_quests.get(quest_name)
        # Don't recheck an already checked quest.
        if required_quest and required_quest not in checked:
            required_quest_quest_reqs = find_recursive_quest_reqs(
                required_quest, all_quests, checked)
            required_quests_set.update(required_quest_quest_reqs)
    return list(required_quests_set)


def find_recursive_other_reqs(query_quest: Quest, all_quests: list, checked):
    """Find the total list of other miscellaneous requirements needed to beat
    this Quest, taking into account each other quest this quest itself requires
    by recursively calling this function on subsequent quests, while avoiding
    infinitely re-checking quests already considered.
    :param query_quest: The quest to find the requirements of.
    :param quest_list: The list of all available quests.
    :param checked: Set of already considered quest in this lookup.
    :rtype: string
    """
    if not checked:
        checked = set()
    checked.add(query_quest)  # Add current quest to avoid infinite recursion
    max_other_reqs = query_quest.get_other_req()
    for quest_name in query_quest.get_quest_req():
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
    # Initial data read from json file.
    full_quest_list = {
        name: Quest(name, info) for name, info in parse_quests_json().items()
    }
    parser = argparse.ArgumentParser(
        description="Find requirements for quests."
    )
    parser.add_argument(
        'quest name', metavar='quest', type=str, nargs='+',
        help='the quest(s) you want the requirements for'
    )
    quests_to_check = vars(parser.parse_args()).get('quest name')
    for quest in quests_to_check:
        if quest.lower() == 'quest point cape':
            print(
                get_quest_requirements(quest_point_cape(full_quest_list), full_quest_list)
            )
        else:
            print(get_quest_requirements(full_quest_list[quest], full_quest_list))
