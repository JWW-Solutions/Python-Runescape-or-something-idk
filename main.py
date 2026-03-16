from skills.skill import Skill
from item import ItemDB, Item
from player.player import Player
from skills.action import action, nonCombatAction, combatAction
from skills.woodcutting import Woodcutting, Tree
from player.gear import Gear, GearSlot, GearStats

def main():
    # Initialize item database and add some items
    Item_DB = populate_db()
    gear = populate_gear(Item_DB)

    skills = populate_skills()
    player = Player("Jaybiz")

    player.add_skills(skills)

    player.equip_gear(gear[Item_DB.get_item("Bronze Helmet").item_id], "head")

    player.equip_gear(gear[Item_DB.get_item("Steel Platebody").item_id], "body")
    player.equip_gear(gear[Item_DB.get_item("Steel Platelegs").item_id], "legs")
    player.equip_gear(gear[Item_DB.get_item("Steel Boots").item_id], "boots")
    player.equip_gear(gear[Item_DB.get_item("Steel Gloves").item_id], "gloves")

def populate_db():
    Item_DB = ItemDB()
    Item_DB.add_sub_categories(2, ["Logs", "Axes", "Misc", "Gear", "Consumables"])
    Item_DB.add_sub_categories(27, ["Ring", "Amulet", "Cape"])
    Item_DB.add_sub_categories(26, ["Head", "Body", "Legs", "Boots", "Gloves"])
    Item_DB.add_sub_categories(25, ["Main-hand", "Off-hand"])

    # Axes
    Item_DB.create_item("Bronze Axe", "A basic axe for woodcutting.", 10, False, "Woodcutting", "Axes")
    Item_DB.create_item("Iron Axe", "A stronger axe for woodcutting.", 50, False, "Woodcutting", "Axes")
    Item_DB.create_item("Steel Axe", "A durable axe for woodcutting.", 100, False, "Woodcutting", "Axes")
    Item_DB.create_item("Mithril Axe", "A powerful axe for woodcutting.", 200, False, "Woodcutting", "Axes")
    Item_DB.create_item("Adamant Axe", "A strong axe for woodcutting.", 500, False, "Woodcutting", "Axes")
    Item_DB.create_item("Rune Axe", "A top-tier axe for woodcutting.", 1000, False, "Woodcutting", "Axes")

    # Logs
    Item_DB.create_item("Normal Logs", "Logs from regular trees.", 1, True, "Woodcutting", "Logs")
    Item_DB.create_item("Oak Logs", "Logs from oak trees.", 5, True, "Woodcutting", "Logs")
    Item_DB.create_item("Willow Logs", "Logs from willow trees.", 10, True, "Woodcutting", "Logs")
    Item_DB.create_item("Maple Logs", "Logs from maple trees.", 20, True, "Woodcutting", "Logs")
    Item_DB.create_item("Yew Logs", "Logs from yew trees.", 50, True, "Woodcutting", "Logs")
    Item_DB.create_item("Magic Logs", "Logs from magic trees.", 100, True, "Woodcutting", "Logs")

    #region for armor and weapons

    # Helmets
    Item_DB.create_item("Bronze Helmet", "A basic helmet for protection.", 20, False, "Armor", "Head")
    Item_DB.create_item("Iron Helmet", "A stronger helmet for protection.", 100, False, "Armor", "Head")
    Item_DB.create_item("Steel Helmet", "A durable helmet for protection.", 200, False, "Armor", "Head")

    # Body 
    Item_DB.create_item("Bronze Platebody", "A basic platebody for protection.", 30, False, "Armor", "Body")
    Item_DB.create_item("Iron Platebody", "A stronger platebody for protection.", 150, False, "Armor", "Body")
    Item_DB.create_item("Steel Platebody", "A durable platebody for protection.", 300, False, "Armor", "Body")

    # Legs
    Item_DB.create_item("Bronze Platelegs", "A basic pair of platelegs for protection.", 25, False, "Armor", "Legs")
    Item_DB.create_item("Iron Platelegs", "A stronger pair of platelegs for protection.", 125, False, "Armor", "Legs")
    Item_DB.create_item("Steel Platelegs", "A durable pair of platelegs for protection.", 250, False, "Armor", "Legs")

    # Boots
    Item_DB.create_item("Bronze Boots", "A basic pair of boots for protection.", 15, False, "Armor", "Boots")
    Item_DB.create_item("Iron Boots", "A stronger pair of boots for protection.", 75, False, "Armor", "Boots")
    Item_DB.create_item("Steel Boots", "A durable pair of boots for protection.", 150, False, "Armor", "Boots")

    # Gloves
    Item_DB.create_item("Bronze Gloves", "A basic pair of gloves for protection.", 10, False, "Armor", "Gloves")
    Item_DB.create_item("Iron Gloves", "A stronger pair of gloves for protection.", 50, False, "Armor", "Gloves")
    Item_DB.create_item("Steel Gloves", "A durable pair of gloves for protection.", 100, False, "Armor", "Gloves")
    #endregion

    return Item_DB

def populate_skills():
    skills = []
    woodcutting = Skill("Woodcutting", 1)
    fire_making = Skill("Firemaking", 1)
    mining = Skill("Mining", 1)
    hitpoints = Skill("Hitpoints", 10)

    skills.extend([woodcutting, fire_making, mining, hitpoints])
    return skills

def populate_gear(Item_DB):
    gear = {}
    # Head
    bronze_helmet = Gear("Bronze Helmet", "A basic helmet for protection.", "Head", Item_DB.get_item("Bronze Helmet"), GearStats(defense=1, hitpoints=1))
    iron_helmet = Gear("Iron Helmet", "A stronger helmet for protection.", "Head", Item_DB.get_item("Iron Helmet"), GearStats(defense=2, hitpoints=2))
    steel_helmet = Gear("Steel Helmet", "A durable helmet for protection.", "Head", Item_DB.get_item("Steel Helmet"), GearStats(defense=3, hitpoints=3, hitpoints_multiplier=1.01))

    # Body
    bronze_platebody = Gear("Bronze Platebody", "A basic platebody for protection.", "Body", Item_DB.get_item("Bronze Platebody"), GearStats(defense=3, hitpoints=3))
    iron_platebody = Gear("Iron Platebody", "A stronger platebody for protection.", "Body", Item_DB.get_item("Iron Platebody"), GearStats(defense=5, hitpoints=5))
    steel_platebody = Gear("Steel Platebody", "A durable platebody for protection.", "Body", Item_DB.get_item("Steel Platebody"), GearStats(defense=7, hitpoints=7, hitpoints_multiplier=1.01))

    # Legs
    bronze_platelegs = Gear("Bronze Platelegs", "A basic pair of platelegs for protection.", "Legs", Item_DB.get_item("Bronze Platelegs"), GearStats(defense=2, hitpoints=2))
    iron_platelegs = Gear("Iron Platelegs", "A stronger pair of platelegs for protection.", "Legs", Item_DB.get_item("Iron Platelegs"), GearStats(defense=4, hitpoints=4))
    steel_platelegs = Gear("Steel Platelegs", "A durable pair of platelegs for protection.", "Legs", Item_DB.get_item("Steel Platelegs"), GearStats(defense=6, hitpoints=6, hitpoints_multiplier=1.01))

    # Boots
    bronze_boots = Gear("Bronze Boots", "A basic pair of boots for protection.", "Boots", Item_DB.get_item("Bronze Boots"), GearStats(defense=1, 
                                                                                                                                      strength=2, 
                                                                                                                                      hitpoints=1))
    iron_boots = Gear("Iron Boots", "A stronger pair of boots for protection.", "Boots", Item_DB.get_item("Iron Boots"), GearStats(defense=2, 
                                                                                                                                   strength=4, 
                                                                                                                                   hitpoints=2))
    steel_boots = Gear("Steel Boots", "A durable pair of boots for protection.", "Boots", Item_DB.get_item("Steel Boots"), GearStats(defense=3, 
                                                                                                                                     strength=6, 
                                                                                                                                     hitpoints=3))

    # Gloves
    bronze_gloves = Gear("Bronze Gloves", "A basic pair of gloves for protection.", "Gloves", Item_DB.get_item("Bronze Gloves"), GearStats(defense=1, 
                                                                                                                                           strength=1, 
                                                                                                                                           hitpoints=1, 
                                                                                                                                           attack=2,
                                                                                                                                           attack_multiplier=1.01))
    iron_gloves = Gear("Iron Gloves", "A stronger pair of gloves for protection.", "Gloves", Item_DB.get_item("Iron Gloves"), GearStats(defense=2, 
                                                                                                                                        strength=2, 
                                                                                                                                        hitpoints=2, 
                                                                                                                                        attack=4,
                                                                                                                                        attack_multiplier=1.02))
    steel_gloves = Gear("Steel Gloves", "A durable pair of gloves for protection.", "Gloves", Item_DB.get_item("Steel Gloves"), GearStats(defense=3, 
                                                                                                                                          strength=3, 
                                                                                                                                          hitpoints=3, 
                                                                                                                                          attack=6, 
                                                                                                                                          attack_multiplier=1.03, 
                                                                                                                                          hitpoints_multiplier=1.01,
                                                                                                                                          strength_multiplier=1.01))

    gear.update({
        Item_DB.get_item("Bronze Helmet").item_id: bronze_helmet,
        Item_DB.get_item("Iron Helmet").item_id: iron_helmet,
        Item_DB.get_item("Steel Helmet").item_id: steel_helmet,
        Item_DB.get_item("Bronze Platebody").item_id: bronze_platebody,
        Item_DB.get_item("Iron Platebody").item_id: iron_platebody,
        Item_DB.get_item("Steel Platebody").item_id: steel_platebody,
        Item_DB.get_item("Bronze Platelegs").item_id: bronze_platelegs,
        Item_DB.get_item("Iron Platelegs").item_id: iron_platelegs,
        Item_DB.get_item("Steel Platelegs").item_id: steel_platelegs,
        Item_DB.get_item("Bronze Boots").item_id: bronze_boots,
        Item_DB.get_item("Iron Boots").item_id: iron_boots,
        Item_DB.get_item("Steel Boots").item_id: steel_boots,
        Item_DB.get_item("Bronze Gloves").item_id: bronze_gloves,
        Item_DB.get_item("Iron Gloves").item_id: iron_gloves,
        Item_DB.get_item("Steel Gloves").item_id: steel_gloves,
    })
    return gear

if __name__ == "__main__":
    main()
    