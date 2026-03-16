from random import random

from skills.skill import Skill
from skills.action import Action


class Tree:
    """Represents a tree that can be chopped."""
    def __init__(self, name, level_required, xp_per_log, reward_item, max_logs=10, chop_delay=2000, fail_weight=0.1):
        self.name = name
        self.level_required = level_required
        self.xp_per_log = xp_per_log
        self.reward_item = reward_item
        self.logs_chopped = 0
        self.max_logs = max_logs
        self.chop_delay = chop_delay
        self.fail_weight = fail_weight
        self.alive = True


    def is_depleted(self):
        return self.logs_chopped >= self.max_logs
    
    def deplete(self):
        self.alive = False


class Woodcutting(Skill):
    """Woodcutting skill that manages trees."""
    def __init__(self, name, level):
        super().__init__(name, level)
        self.trees = {}

    def add_tree(self, tree: Tree):
        self.trees[tree.name] = tree

    def get_tree(self, tree_name):
        return self.trees.get(tree_name)

    def chop_tree(self, player, tree_name: str):
        """Perform a chop action on a tree."""
        tree = self.get_tree(tree_name)
        if not tree:
            print(f"Tree '{tree_name}' not found.")
            return False
        
        if self.level < tree.level_required:
            print(f"{player.name} needs Woodcutting level {tree.level_required} to chop {tree.name}.")
            return False
        
        if tree.is_depleted():
            tree.deplete()
            print(f"The {tree.name} tree has been depleted.")
            return False
        
        # Success roll
        if self._roll_success(self.level, tree.level_required, tree):
            tree.logs_chopped += 1
            self.gain_xp(tree.xp_per_log)
            player.Inventory.add_item(tree.reward_item)
            print(f"{player.name} successfully chopped {tree.reward_item} and gained {tree.xp_per_log} XP!")
            return True
        else:
            print(f"{player.name} failed to chop the {tree.name}.")
            return False


class ChopTree(Action):
    """Action to chop a specific tree."""
    def __init__(self, tree: Tree, woodcutting_skill: Skill):
        super().__init__(
            name=f"Chop {tree.name}",
            description=f"Chopping down a {tree.name} tree.",
            skill=woodcutting_skill,
            delay= tree.chop_delay,
            required_level=tree.level_required,
            xp_reward=tree.xp_per_log,
            reward_item=tree.reward_item
        )
        self.tree = tree

    def perform_action(self, player):
        super().perform_action(player)
        # Use Woodcutting.chop_tree for the actual logic
        self.skill.chop_tree(player, self.tree.name)