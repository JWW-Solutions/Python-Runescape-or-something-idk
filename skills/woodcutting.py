from skills.skill import Skill
class Woodcutting (Skill):
    def __init__(self, name, level):
        super().__init__(name, level)
    

class Tree:
    def __init__(self, name, level_required, xp_per_log):
        self.name = name
        self.level_required = level_required
        self.xp_per_log = xp_per_log

