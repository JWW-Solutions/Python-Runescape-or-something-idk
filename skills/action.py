import time

from item import Item
from skills.skill import Skill
from player.gear import Gear

class Action:
    """Base action class for both combat and non-combat actions."""
    def __init__(self, name: str, 
                 description: str, 
                 skill: Skill, 
                 delay: int,
                 required_level: int = 1, 
                 xp_reward: int = 0, 
                 reward_item: Item = None,
                 gear: Gear = None):
        self.name = name
        self.description = description
        self.skill = skill
        self.delay = delay
        self.required_level = required_level
        self.xp_reward = xp_reward
        self.reward_item = reward_item
        self.gear = gear

    def perform_action(self, player):
        print(f"{player.name} performs {self.name}: {self.description}")
        time.sleep(self.delay / 1000)

    def _gain_xp(self, player):
        """Helper to award XP for this action."""
        if self.xp_reward > 0:
            self.skill.gain_xp(self.xp_reward)
            print(f"{player.name} gained {self.xp_reward} XP in {self.skill.name}!")

class CombatAction(Action):
    """Action class specifically for combat."""
    def __init__(self, name: str, description: str, skill: Skill, gear: Gear):
        super().__init__(name, description, skill, delay=1000, gear=gear)

    def roll_damage(self):
        """Calculate damage based on player stats and gear."""
        return 10  # Placeholder
    
    def perform_action(self, player):
        super().perform_action(player)
        damage = self.roll_damage()
        print(f"{player.name} deals {damage} damage!")


class ActionManager:
    """Manages a collection of actions."""
    def __init__(self):
        self.actions = []

    def add_action(self, action: Action):
        self.actions.append(action)

    def get_actions_for_skill(self, skill_name: str):
        return [a for a in self.actions if a.skill.name == skill_name]