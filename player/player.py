from player.inventory import Inventory
from player.gear import GearSlot, GearStats, Gear

class Player:
    def __init__(self, name):
        self.name = name
        self.skills = []
        self.hp = 100
        self.Inventory = Inventory()
        self.gear_slots = {
            "head": GearSlot("head"),
            "body": GearSlot("body"),
            "legs": GearSlot("legs"),
            "boots": GearSlot("boots"),
            "gloves": GearSlot("gloves"),
            "main-hand": GearSlot("main-hand"),
            "off-hand": GearSlot("off-hand"),
            "amulet": GearSlot("amulet"),
            "ring": GearSlot("ring"),
            "cape": GearSlot("cape"),
            "ammo": GearSlot("ammo"),
        }
        self.gear_stats = GearStats()

    #region Skill methods

    def add_skills(self, skills):
        self.skills = skills

        for skill in self.skills:
            print(f"Added skill: {skill}")
    
    def add_skill(self, skill):
        self.skills.append(skill)

        print(f"Added skill: {skill}")

    def list_skills(self):
        print(f"{self.name}'s Skills:")
        for skill in self.skills:
            print(f" - {skill}")
    
    def skill_summary(self):
        for skill in self.skills:
            print(skill.skill_summary())

    #endregion

    #region combat methods
    def take_damage(self, amt_dmg):
        self.hp -= amt_dmg
        print(f"{self.name} took {amt_dmg} damage! HP is now {self.hp}.")

    def heal(self, amt_heal):
        self.hp += amt_heal
        print(f"{self.name} healed {amt_heal}! HP is now {self.hp}")
    #endregion

    #region gear methods
    def equip_gear(self, gear: Gear, slot_name: str):
        if slot_name in self.gear_slots:
            self.gear_slots[slot_name].equip_gear(gear, self)
            self.update_gear_stats()
        else:
            print(f"Invalid gear slot: {slot_name}")
    
    def update_gear_stats(self):
        # Reset gear stats
        self.gear_stats = GearStats()

        # Aggregate stats from equipped gear
        for slot in self.gear_slots.values():
            if slot.equipped_gear is not None:
                self.gear_stats.add_stats_inplace(slot.equipped_gear.stats)
            
        print(f"{self.name}'s current gear stats: {self.gear_stats}")
    def unequip_gear(self, slot_name: str):
        if slot_name in self.gear_slots:
            self.gear_slots[slot_name].unequip_gear(self)
            self.update_gear_stats()
        else:
            print(f"Invalid gear slot: {slot_name}")

    def list_equipped_gear(self):
        print(f"{self.name}'s Equipped Gear:")
        for slot_name, gear_slot in self.gear_slots.items():
            if gear_slot.equipped_gear is not None:
                print(f" - {slot_name}: {gear_slot.equipped_gear.name}")
    

    #endregion