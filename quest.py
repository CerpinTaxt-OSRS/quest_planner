#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json


class Quest:
    """Represents all the information needed to understand the requirements of
    a quest. Takes into account all requirements a normal account *must* meet
    to complete the quest. Makes no assessment of the suitability of an ironman
    account or combat levels (unless combat levels are explicitly required to
    recieve and complete the quest), nor does it consider obtaining certain
    quest items, for example, you need a ghostspeak amulet to do Nature Spirit,
    but you do not have to complete The Restless Ghost to obtain the amulet.
    This is a concious decision since some players may not wish to gain the
    reward experience from a quest, but they can still partially complete the
    quest to obtain necessary items required for another quest.
    """
    def __init__(self, name, info):
        self.name = name
        self.f2p = info.get('f2p')
        self._skill_req = info.get('requirements').get('skills')
        self._quest_req = info.get('requirements').get('quests')
        self._other_req = info.get('requirements').get('other')

    def __str__(self):
        """Return a human-readable string representation of this Quest."""
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

    def get_skill_req(self):
        """Get and return all skill requirements of this Quest."""
        return self._skill_req

    def get_quest_req(self):
        """Get and return all quest requirements of this Quest."""
        return self._quest_req

    def get_other_req(self):
        """Get and return all other requirements of this Quest."""
        return self._other_req
