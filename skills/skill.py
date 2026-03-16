class Skill:
    C = 7.3803
    MAX_LEVEL = 150

    @classmethod
    def build_xp_table(cls):
        xp_table = {1: 0}
        for level in range(2, cls.MAX_LEVEL + 1):
            xp_table[level] = sum(
                int(i + 300 * 2 ** (i / Skill.C))
                for i in range(1, level)
            ) // 4
        return xp_table

    def __init__(self, name, level=1):
        self.name = name
        self.level = level
        self.xp = Skill.XP_TABLE[level]

    @staticmethod
    def resolve_xp(level):
        return Skill.XP_TABLE.get(level, None)

    @staticmethod
    def resolve_level(xp):
        for level, xp_required in Skill.XP_TABLE.items():
            if xp < xp_required:
                return level - 1
        return Skill.MAX_LEVEL

    def gain_xp(self, xp):
        self.xp += xp
        new_level = Skill.resolve_level(self.xp)
        while self.level < new_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        print(f"{self.name} leveled up to {self.level}!")

    def xp_to_next_level(self):
        next_level_xp = Skill.resolve_xp(self.level + 1)
        if next_level_xp is not None:
            return next_level_xp - self.xp
        return None

    def xp_into_level(self):
        current_level_xp = Skill.resolve_xp(self.level)
        if current_level_xp is not None:
            return self.xp - current_level_xp
        return None

    def skill_summary(self):
        return f"{self.name} - Level: {self.level}, XP: {self.xp}, XP to next level: {self.xp_to_next_level()}, XP into level: {self.xp_into_level()}"

    def __str__(self):
        return f"{self.name} (Level {self.level})"


Skill.XP_TABLE = Skill.build_xp_table()
