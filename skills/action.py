from asyncio import timeout

from item import Item
from skills.skill import Skill
from player.gear import Gear
class action:
    def __init__(self, name: str, 
                 description: str, 
                 skill: Skill, 
                 delay: int):
        self.name = name
        self.description = description
        self.skill = skill
        self.delay = delay

    def perform_action(self, player):
        print(f"{player.name} performs {self.name}: {self.description}")
        timeout(self.delay)

class nonCombatAction(action):
    def __init__(self, 
                 name: str, 
                 description: str, 
                 skill: Skill, 
                 delay: int, 
                 gear: Gear = None, 
                 required_level: int = 1, 
                 xp_reward: int = 0, 
                 reward_item: Item = None
                 ):
        
        super().__init__(name, description, skill, delay)
        self.gear = gear
        self.required_level = required_level
        self.xp_reward = xp_reward
        self.reward_item = reward_item
    
    def perform_action(self, player):
        super().perform_action(player)
        print(f"{player.name} gains {self.skill.xp_to_next_level()} XP in {self.skill.name}!")

class combatAction(action):
    def __init__(self, 
                 name: str, 
                 description: str, 
                 skill: Skill, 
                 gear: Gear):
        super().__init__(name, description, skill, delay=1000)  # Default delay for combat actions
        self.gear = gear

    def roll_damage(self):
        # Placeholder for damage calculation logic - Based on player's stats and gear
        self.damage = 10  # Example fixed damage value
        return self.damage
    
    def perform_action(self, player):
        super().perform_action(player)
        damage = self.roll_damage()
        print(f"{player.name} deals {damage} damage!")

class ActionManager:
    def __init__(self):
        self.actions = []

    def add_action(self, action: action):
        self.actions.append(action)

    def get_actions_for_skill(self, skill_name: str):
        return [action for action in self.actions if action.skill.name == skill_name]