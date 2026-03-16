from decimal import Clamped

from player.inventory import Inventory
from player.gear import GearSlot, GearStats, Gear

class Player:
    def __init__(self, name):
        self.name = name
        self.skills = []
        self.hp_level = 10
        self.base_hp = 10 * self.hp_level
        self.hp = self.base_hp
        self.max_hp = self.hp
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
        
        self.update_base_hp_from_hitpoints_skill()
    
    def add_skill(self, skill):
        self.skills.append(skill)

        print(f"Added skill: {skill}")
        self.update_base_hp_from_hitpoints_skill()

    def update_base_hp_from_hitpoints_skill(self):
        for skill in self.skills:
            if skill.name == "Hitpoints":
                old_base_hp = self.base_hp
                self.base_hp = skill.level * 10
                self.hp = self.base_hp
                self.max_hp = self.base_hp
                if self.base_hp != old_base_hp:
                    print(f"{self.name}'s base HP updated to {self.base_hp} (Hitpoints level: {skill.level})")
                return

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

    def update_max_hp(self, new_max_hp):
        self.max_hp = new_max_hp
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        print(f"{self.name}'s max HP is now {self.max_hp}.")
    #endregion

    #region gear methods
    def equip_gear(self, gear: Gear, slot_name: str):
        if slot_name in self.gear_slots:
            self.gear_slots[slot_name].equip_gear(gear, self)
            self.update_gear_stats()
        else:
            print(f"Invalid gear slot: {slot_name}")
    
    def update_gear_stats(self):
        old_max_hp = self.max_hp
        # Reset gear stats
        self.gear_stats = GearStats()
        # Aggregate stats from equipped gear
        for slot in self.gear_slots.values():
            if slot.equipped_gear is not None:
                self.gear_stats.add_stats_inplace(slot.equipped_gear.stats)
        
        # Update max HP based on gear stats and ensure current HP does not exceed new max HP
        self.update_max_hp(round((self.base_hp + self.gear_stats.hitpoints) * self.gear_stats.hitpoints_multiplier))
        self.hp = self.max_hp  # Update current HP to match new max HP after equipping gear
        print(f"{self.name}'s gear stats updated: {self.gear_stats}, Max HP: {self.max_hp}, Current HP: {self.hp}")
        if self.max_hp != old_max_hp:
            print(f"{self.name}'s max HP changed from {old_max_hp} to {self.max_hp}. Current HP: {self.hp}")

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