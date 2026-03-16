class Inventory:
    MAX_SLOTS = 32
    def __init__(self):
        self.items = [None] * Inventory.MAX_SLOTS

    def add_item(self, item):
        for i in range(Inventory.MAX_SLOTS):
            if self.items[i] is None:
                self.items[i] = item
                print(f"Added {item} to inventory slot {i}.")
                return True
        print("Inventory is full! Cannot add item.")
        return False
    
    def remove_item(self, item):
        for i in range(Inventory.MAX_SLOTS):
            if self.items[i] == item:
                self.items[i] = None
                print(f"Removed {item} from inventory slot {i}.")
                return True
        print(f"Item {item} not found in inventory.")
        return False
    
    def list_items(self):
        print("Inventory:")
        for i, item in enumerate(self.items):
            if item is not None:
                print(f" Slot {i}: {item}")