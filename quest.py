#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json


class Quest:
    """Represents all the information needed to understand the requirements of
    a quest. Takes into account all requirements a normal account *must* meet
    to complete the quest. Makes no assessment of the suitability of an ironman
    account or combat levels (unless combat levels are explicitly required to
    recieve and complete the quest). If partial completion is all that is
    required, this will assume you still need all the requirements of that
    quest anyway, even if you don't complete the quest.
    """
    def __init__(self, name, info):
        self.name = name
        self.f2p = info.get('f2p')
        self._skill_req = info.get('requirements').get('skills')
        self._quest_req = info.get('requirements').get('quests')
        self._other_req = info.get('requirements').get('other')

    def __repr__(self):
        """Return a json string representation of this Quest."""
        return json.dumps({
            self.name: {
                "f2p": self.f2p,
                "requirements": {
                    "skills": self.get_skill_req(),
                    "quests": self.get_quest_req(),
                    "other": self.get_other_req()
                }
            }
        })
    
    def __str__(self):
        """Return a nice human-readable representation of this Quest."""
        output = self.name
        output += f"{' (f2p)' if self.f2p else ' (p2p)'}" + '\n\n'
        output += "Skill requirements:\n"
        for skill, level in self.get_skill_req().items():
            output += f"\t{skill:<12}\t{level}\n"
        output += "\nQuest requirements:\n"
        for quest in self.get_quest_req():
            output += f"\t{quest}\n"
        output += "\nOther requirements:\n"
        for task, value in self.get_other_req().items():
            if value == 1:
                output += f"\t{task:<24}\tCompleted\n"
            elif 'favour' in task:
                output += f"\t{task:<24}\t{value}%\n"
            else:
                output += f"\t{task:<24}\t{value}\n"
        return output

    def get_skill_req(self):
        """Get and return all skill requirements of this Quest."""
        return self._skill_req

    def get_quest_req(self):
        """Get and return all quest requirements of this Quest."""
        return self._quest_req

    def get_other_req(self):
        """Get and return all other requirements of this Quest."""
        return self._other_req
