import json
from pathlib import Path

# This class represents an item in the game. 
# It has attributes for the item's name, description, ID, value, and whether it is stackable.
class Item:
    def __init__(
        self,
        name,
        description,
        item_id,
        value,
        stackable=False,
        category=None,
        sub_category=None,
        quantity=1,
        max_stack=None,
    ):
        self.name = name
        self.description = description
        self.item_id = item_id
        self.value = value
        self.stackable = stackable

        # Always present
        self.quantity = quantity
        # Default max_stack: 1 for non-stackable, 1000 for stackable (unless overridden)
        if max_stack is None:
            self.max_stack = 1000 if stackable else 1
        else:
            self.max_stack = max_stack

        self.category = category
        self.sub_category = sub_category
    
    def __str__(self):
        return f"{self.name} (ID: {self.item_id}, Value: {self.value}, Quantity: {self.quantity})"
    
    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "value": self.value,
            "stackable": self.stackable,
            "category": self.category.name if self.category else None,
            "sub_category": self.sub_category.name if self.sub_category else None,
            "category_id": self.category.category_id if self.category else None,
            "sub_category_id": (
                self.sub_category.sub_category_id if self.sub_category else None
            ),
        }

    
class Category:
    def __init__(self, name, category_id):
        self.name = name
        self.category_id = category_id
        self.item_id_start = self.resolve_start_id()
        self.item_id_end = self.resolve_end_id()
        self.sub_categories = {}

    def resolve_start_id(self):
        # Category N occupies N*10000 .. (N+1)*10000 - 1
        return self.category_id * 10000

    def resolve_end_id(self):
        return (self.category_id + 1) * 10000 - 1
    
    def add_sub_category(self, sub_category):
        if sub_category.sub_category_id in self.sub_categories:
            print(f"Sub-category with ID {sub_category.sub_category_id} already exists in category '{self.name}'.")
            return
        self.sub_categories[sub_category.sub_category_id] = sub_category
class Sub_Category:
    def __init__(self, name, sub_category_id, parent_category):
        self.name = name
        self.sub_category_id = sub_category_id
        self.parent_category = parent_category
        self.item_id_start = self.resolve_start_id()
        self.item_id_end = self.resolve_end_id()

    def resolve_start_id(self):
        # Sub-category M of category N: N*10000 + M*1000 .. N*10000 + (M+1)*1000 - 1
        return self.parent_category.item_id_start + (self.sub_category_id * 1000)

    def resolve_end_id(self):
        return self.parent_category.item_id_start + ((self.sub_category_id + 1) * 1000) - 1
    
    
# This class represents the item database. 
# It has methods for populating the database from a JSON file, saving the database to a JSON file, 
# retrieving items by ID, getting the maximum ID, getting the next available ID, checking if an item already exists, 
# sorting items, adding items, listing items, and removing items.
class ItemDB:

    #Constant for the file path of the item database JSON file.
    ITEM_DB_FILE = Path(__file__).parent / "itemdb.json"

    # The constructor initializes the items dictionary and calls the populate method to load items from the JSON file.
    def __init__(self):
        self.categories = {}
        self.populate_categories()

        self.add_sub_categories(2, ["Logs", "Axes"])
        self.items = {}
        self.populate()

    # This method populates the item database by reading from a JSON file.
    def populate(self):
        try:
            with open(self.ITEM_DB_FILE, "r") as f:
                db_load = json.load(f)
        except FileNotFoundError:
            print(f"{self.ITEM_DB_FILE} not found.")
            return

        if not db_load:
            print("Item database is empty.")
            return

        for item_id_str, item_data in db_load.items():
            item_id = int(item_id_str)

            category = None
            sub_category = None

            category_name = item_data.get("category")
            sub_category_name = item_data.get("sub_category")
            category_id = item_data.get("category_id")
            sub_category_id = item_data.get("sub_category_id")

            # Prefer ID-based resolution if present
            if category_id is not None and category_id in self.categories:
                category = self.categories[category_id]
            elif category_name is not None:
                for existing_category in self.categories.values():
                    if existing_category.name == category_name:
                        category = existing_category
                        break

            if category is not None:
                if sub_category_id is not None and sub_category_id in category.sub_categories:
                    sub_category = category.sub_categories[sub_category_id]
                elif sub_category_name is not None:
                    for sc in category.sub_categories.values():
                        if sc.name == sub_category_name:
                            sub_category = sc
                            break

            self.items[item_id] = Item(
                name=item_data["name"],
                description=item_data["description"],
                item_id=item_id,
                value=item_data["value"],
                stackable=item_data.get("stackable", False),
                category=category,
                sub_category=sub_category,
            )
   
    def populate_categories(self):
        self.categories = {
            0: Category("Other", 0),
            1: Category("Quest Items", 1),
            2: Category("Woodcutting", 2),
            3: Category("Firemaking", 3),
            4: Category("Fishing", 4),
            5: Category("Cooking", 5),
            6: Category("Brewing", 6),
            7: Category("Mining", 7),
            8: Category("Smithing", 8),
            25: Category("Weapons", 25),
            26: Category("Armor", 26),
            27: Category("Accessories", 27),
        }

    def add_sub_categories(self, category_id, sub_category_names):
        category = self.categories.get(category_id)
        if category is None:
            print(f"Category with ID {category_id} not found.")
            return
        for sub_category_id, sub_category_name in enumerate(sub_category_names):
            sub_category = Sub_Category(sub_category_name, sub_category_id, category)
            category.add_sub_category(sub_category)

    # This method saves the current state of the item database to a JSON file.
    def save(self):
        # Initialize an empty dictionary to hold the item data 
        data = {}

        # Loop through each item in the items dictionary 
        # convert it to a dictionary format using the to_dict method of the Item class.
        for item_id, item in self.items.items():
            data[str(item_id)] = item.to_dict()
        # Write the data dictionary to the JSON file specified by ITEM_DB_FILE with indentation for readability.
        with open(self.ITEM_DB_FILE, "w") as f:
            json.dump(data, f, indent=4)

    # This method gets an item based on its ID or name.
    def get_item(self, identifier):
        if identifier in self.items:
            print(f"Retrieved item '{self.items[identifier].name}' with ID {identifier} from database.")
            return self.items[identifier]

        if isinstance(identifier, str):
            for item in self.items.values():
                if item.name == identifier:
                    print(f"Retrieved item '{item.name}' with ID {item.item_id} from database.")
                    return item
            print(f"Item named '{identifier}' not found in database.")
            return None

        print(f"Item with ID {identifier} not found in database.")
        return None

    def get_max_id_for_category(self, category):
        return category.item_id_end

    # This method gets the next available ID for a new item.
    def get_next_id_for_category(self, category):
        for item_id in range(category.item_id_start, category.item_id_end + 1):
            if item_id not in self.items:
                return item_id
        print(f"No available IDs in category '{category.name}'.")
        return None
    
    # This method checks if an item with the same name and description already exists in the database.
    # Shows Duplicate entry of the item
    def item_already_exists(self, item):
        for existing_item in self.items.values():
            if existing_item.name == item.name and existing_item.description == item.description:
                return True
        return False
    
    # This function sorts the items in the database by their ID. 
    # It converts the items dictionary into a list of (id, item) pairs, sorts that list, and then converts it back into a dictionary. 
    # This ensures that the items are stored in order of their IDs.
    def sort_items(self):
        pairs = self.items.items()
        sorted_pairs = sorted(pairs) #Returns sorted tuples of (id, item) pairs
        sorted_dict = dict(sorted_pairs) #Converts sorted tuples back into a dictionary
        self.items = sorted_dict

    # This function adds a new item to the database.
    # It first checks if an item with the same name and description already exists in the database using the item_already_exists method. 
    # If it does, it prints a message and returns without adding the item. 
    # If it doesn't, it adds the item to the items dictionary using its ID as the key
    def add_item(self, item):
        if self.item_already_exists(item):
            print(f"Item '{item.name}' already exists in the database.")
            return
        
        self.items[item.item_id] = item
        self.sort_items()
        self.save()
        print(f"Added item '{item.name}' with ID {item.item_id} to database.")

    # This function lists all the items in the database. 
    # It iterates through the items dictionary and prints out the ID, name, description, and value of each item.
    def list_items(self):   
        print("Item Database:")
        for item in self.items.values():
            print(f"ID {item.item_id}: {item.name} - {item.description} (Value: {item.value})")

    # This function removes an item from the database. 
    # It first checks if the item with the given ID exists in the items dictionary.
    # If it doesn't, it prints a message and returns. 
    # If it does, it deletes the item from the items dictionary, saves the updated database
    def remove_item(self, item):
        if item is None:
            print("No item provided for removal.")
            return

        if item.item_id not in self.items:
            print(f"Item '{item.name}' does not exist in the database.")
            return

        del self.items[item.item_id]
        self.save()
        print(f"Removed item with ID {item.item_id} from database.")

    def get_category_by_name(self, name: str):
        for category in self.categories.values():
            if category.name == name:
                return category
        raise ValueError(f"Category '{name}' not found")

    def get_sub_category_by_name(self, category: "Category", name: str):
        for sub_category in category.sub_categories.values():
            if sub_category.name == name:
                return sub_category
        raise ValueError(f"Sub-category '{name}' not found in '{category.name}'")
    def get_next_id_for_sub_category(self, sub_category: "Sub_Category"):
        for item_id in range(sub_category.item_id_start, sub_category.item_id_end + 1):
            if item_id not in self.items:
                return item_id
        print(f"No available IDs in sub-category '{sub_category.name}'.")
        return None
    def create_item(
        self,
        name: str,
        description: str,
        value: int,
        stackable: bool,
        category_name: str,
        sub_category_name: str,
        quantity: int = 1,
        max_stack: int = None,
    ):
        category = self.get_category_by_name(category_name)
        sub_category = self.get_sub_category_by_name(category, sub_category_name)

        item_id = self.get_next_id_for_sub_category(sub_category)
        if item_id is None:
            raise RuntimeError(f"No IDs left in sub-category '{sub_category_name}'")

        item = Item(
            name=name,
            description=description,
            item_id=item_id,
            value=value,
            stackable=stackable,
            category=category,
            sub_category=sub_category,
            quantity=quantity,
            max_stack=max_stack,
        )
        self.add_item(item)
        return item