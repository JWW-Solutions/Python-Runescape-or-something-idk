from __future__ import annotations

from item import Item


def _normalize_slot_name(slot_name: str | None) -> str | None:
    if slot_name is None:
        return None
    return slot_name.strip().lower()


class Gear:
    def __init__(
        self,
        name: str,
        description: str,
        slot: str | GearSlot | None,
        Item: Item = None,
        stats: GearStats = None,
    ):
        self.name = name
        self.description = description
        self.slot = slot if isinstance(slot, GearSlot) else None
        self.slot_name = slot.slot_name if isinstance(slot, GearSlot) else _normalize_slot_name(slot)
        self.Item = Item
        self.stats = stats if stats is not None else GearStats()

    def equip(self, player, slot: GearSlot | None = None):
        target_slot = slot or self.slot
        if target_slot is None:
            print(f"{self.name} cannot be equipped as it has no designated slot.")
            return False
        if target_slot.equipped_gear is not None and target_slot.equipped_gear is not self:
            print(
                f"{target_slot.equipped_gear.name} is already equipped in the "
                f"{target_slot.slot_name} slot. Please unequip it first."
            )
            return False

        self.slot = target_slot
        self.slot_name = target_slot.slot_name
        target_slot.equipped_gear = self

        print(f"{player.name} equips {self.name} in the {target_slot.slot_name} slot.")
        for stat, bonus in self.stats.items():
            print(f"{player.name}'s {stat} increases by {bonus}!")
        return True

    def unequip(self, player):
        if self.slot is None:
            print(f"{self.name} cannot be unequipped as it has no designated slot.")
            return False
        if self.slot.equipped_gear is not self:
            print(f"{self.name} is not currently equipped in the {self.slot.slot_name} slot.")
            return False

        print(f"{player.name} unequips {self.name} from the {self.slot.slot_name} slot.")
        for stat, bonus in self.stats.items():
            print(f"{player.name}'s {stat} decreases by {bonus}!")

        self.slot.equipped_gear = None
        self.slot = None
        return True


class GearSlot:
    def __init__(self, slot_name: str, equipped_gear: Gear = None, id: int = None):
        self.slot_name = _normalize_slot_name(slot_name)
        self.equipped_gear = equipped_gear
        self.id = id

    def equip_gear(self, gear: Gear, player):
        if gear.slot_name is not None and gear.slot_name != self.slot_name:
            print(f"{gear.name} cannot be equipped in the {self.slot_name} slot.")
            return False
        if self.equipped_gear is not None and self.equipped_gear is not gear:
            self.unequip_gear(player)
        return gear.equip(player, self)

    def unequip_gear(self, player):
        if self.equipped_gear is not None:
            return self.equipped_gear.unequip(player)
        return False


GearSlots = dict[str, GearSlot]


class GearStats:
    def __init__(
        self,
        attack=0,
        defense=0,
        strength=0,
        magic=0,
        ranged=0,
        prayer=0,
        hitpoints=0,
        attack_multiplier=1.0,
        defense_multiplier=1.0,
        strength_multiplier=1.0,
        magic_multiplier=1.0,
        ranged_multiplier=1.0,
        prayer_multiplier=1.0,
        hitpoints_multiplier=1.0,
    ):
        self.attack = attack
        self.defense = defense
        self.strength = strength
        self.magic = magic
        self.ranged = ranged
        self.prayer = prayer
        self.hitpoints = hitpoints
        self.attack_multiplier = attack_multiplier
        self.defense_multiplier = defense_multiplier
        self.strength_multiplier = strength_multiplier
        self.magic_multiplier = magic_multiplier
        self.ranged_multiplier = ranged_multiplier
        self.prayer_multiplier = prayer_multiplier
        self.hitpoints_multiplier = hitpoints_multiplier

    def items(self):
        return {
            "attack": self.attack,
            "defense": self.defense,
            "strength": self.strength,
            "magic": self.magic,
            "ranged": self.ranged,
            "prayer": self.prayer,
            "hitpoints": self.hitpoints,
            "attack_multiplier": self.attack_multiplier,
            "defense_multiplier": self.defense_multiplier,
            "strength_multiplier": self.strength_multiplier,
            "magic_multiplier": self.magic_multiplier,
            "ranged_multiplier": self.ranged_multiplier,
            "prayer_multiplier": self.prayer_multiplier,
            "hitpoints_multiplier": self.hitpoints_multiplier,
        }.items()

    def add_stats_inplace(self, additional_stats):
        self.attack += additional_stats.attack
        self.defense += additional_stats.defense
        self.strength += additional_stats.strength
        self.magic += additional_stats.magic
        self.ranged += additional_stats.ranged
        self.prayer += additional_stats.prayer
        self.hitpoints += additional_stats.hitpoints
        self.attack_multiplier *= additional_stats.attack_multiplier
        self.defense_multiplier *= additional_stats.defense_multiplier
        self.strength_multiplier *= additional_stats.strength_multiplier
        self.magic_multiplier *= additional_stats.magic_multiplier
        self.ranged_multiplier *= additional_stats.ranged_multiplier
        self.prayer_multiplier *= additional_stats.prayer_multiplier
        self.hitpoints_multiplier *= additional_stats.hitpoints_multiplier

    def __str__(self):
        stats_str = ", ".join(f"{stat}: {bonus}" for stat, bonus in self.items() if bonus != 0)
        return f"GearStats({stats_str})" if stats_str else "GearStats()"