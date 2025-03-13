import json
import os

class Ship:
    def __init__(self, name, ship_class, base_shield, base_shield_regen, base_armor, base_cpu, base_energy, base_energy_regen, base_speed_move, base_speed_turn, base_weapons, base_fittings, base_riggings, base_cells, base_bonuses, shield_increment, regen_increment, armor_increment, cpu_increment, bonus_increment):
        self.name = name
        self.ship_class = ship_class
        self.base_shield = base_shield
        self.base_shield_regen = base_shield_regen
        self.base_armor = base_armor
        self.base_cpu = base_cpu
        self.base_energy = base_energy
        self.base_energy_regen = base_energy_regen
        self.base_speed_move = base_speed_move
        self.base_speed_turn = base_speed_turn
        self.base_weapons = base_weapons
        self.base_fittings = base_fittings
        self.base_riggings = base_riggings
        self.base_cells = base_cells
        self.base_bonuses = base_bonuses
        self.shield_increment = shield_increment
        self.regen_increment = regen_increment
        self.armor_increment = armor_increment
        self.cpu_increment = cpu_increment
        self.bonus_increment = bonus_increment
    
    def get_stats(self, tier):
        # Calculate stats based on the tier
        shield = self.base_shield + (tier - 1) * self.shield_increment
        shield_regen = self.base_shield_regen + (tier - 1) * self.regen_increment
        armor = self.base_armor + (tier - 1) * self.armor_increment
        cpu = self.base_cpu + (tier - 1) * self.cpu_increment
        energy = self.base_energy
        energy_regen = self.base_energy_regen
        speed_move = self.base_speed_move
        speed_turn = self.base_speed_turn
        weapons = self.base_weapons
        fittings = self.base_fittings
        riggings = self.base_riggings
        cells = self.base_cells
        
        # Unlock rigging at tier 3 and cells at tier 5
        if tier >= 3:
            riggings = 1
        if tier >= 5:
            cells = 2
        
        bonuses = self.base_bonuses.copy()
        for key in bonuses:
            bonuses[key] += (tier - 1) * self.bonus_increment
        
        return {
            'shield': shield,
            'shield_regen': shield_regen,
            'armor': armor,
            'cpu': cpu,
            'energy': energy,
            'energy_regen': energy_regen,
            'speed_move': speed_move,
            'speed_turn': speed_turn,
            'weapons': weapons,
            'fittings': fittings,
            'riggings': riggings,
            'cells': cells,
            'bonuses': bonuses
        }

    def display_stats(self, tier):
        stats = self.get_stats(tier)
        
        print(f"-----{self.name} ({self.ship_class}) Mark {tier}-----")
        print("~Stats~")
        print(f"CPU: {stats['cpu']}")
        print(f"Shield: {stats['shield']}")
        print(f"Shield Regen: {stats['shield_regen']}/sec")
        print(f"Armor: {stats['armor']}")
        print(f"Energy: {stats['energy']}")
        print(f"Energy Regen: {stats['energy_regen']}/sec")
        print(f"Speed/Move: {stats['speed_move']}")
        print(f"Speed/Turn: {stats['speed_turn']}")
        
        print("~SLOTS~")
        print(f"Weapons: {stats['weapons']}")
        print(f"Fittings: {stats['fittings']}")
        print(f"Riggings: {stats['riggings']}")
        print(f"Cells: {stats['cells']}")
        
        print("~Bonuses~")
        for bonus, value in stats['bonuses'].items():
            print(f"{bonus}: {value}%")


def save_ship_to_file(ship):
    # Get the directory where the script is located
    folder_path = os.path.dirname(os.path.realpath(__file__)) + "/ship"
    
    # Create the 'ship' folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Save ship data to the JSON file inside the 'ship' folder (overwrites if the file exists)
    filename = f"{folder_path}/{ship.name.lower().replace(' ', '_')}.json"

    with open(filename, 'w') as f:
        json.dump(ship.__dict__, f, indent=4)
    print(f"Ship data saved to {filename}")


def load_ship_from_file(ship_name):
    folder_path = os.path.dirname(os.path.realpath(__file__)) + "/ship"
    filename = f"{folder_path}/{ship_name.lower().replace(' ', '_')}.json"
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            ship_data = json.load(f)
        return Ship(**ship_data)
    else:
        print(f"Ship with the name '{ship_name}' not found.")
        return None


def create_ship():
    name = input("Enter ship name: ")
    ship_class = input("Enter the class of the ship (e.g., 'Battleship', 'Carrier', 'Destroyer'): ")

    # Stats input
    base_shield = int(input("Enter base shield: "))
    base_shield_regen = int(input("Enter base shield regen: "))
    base_armor = int(input("Enter base armor: "))
    base_cpu = int(input("Enter base CPU: "))
    base_energy = int(input("Enter base energy: "))
    base_energy_regen = int(input("Enter base energy regen: "))
    base_speed_move = float(input("Enter base speed move: "))
    base_speed_turn = float(input("Enter base speed turn: "))
    
    # Slots input
    base_weapons = int(input("Enter weapons slots: "))
    base_fittings = int(input("Enter fittings slots: "))
    base_riggings = int(input("Enter rigging slots: "))
    base_cells = int(input("Enter cell slots: "))
    
    # Bonuses input
    base_bonuses = {}
    while True:
        bonus_name = input("Enter bonus name (or 'done' to finish): ")
        if bonus_name.lower() == "done":
            break
        bonus_value = int(input(f"Enter value for {bonus_name}: "))
        if bonus_value != 0:
            base_bonuses[bonus_name] = bonus_value

    # Increment values
    shield_increment = int(input("Enter shield increment: "))
    regen_increment = int(input("Enter shield regen increment: "))
    armor_increment = int(input("Enter armor increment: "))
    cpu_increment = int(input("Enter CPU increment: "))
    bonus_increment = int(input("Enter bonus increment: "))

    ship = Ship(
        name, ship_class, base_shield, base_shield_regen, base_armor, base_cpu, base_energy, base_energy_regen,
        base_speed_move, base_speed_turn, base_weapons, base_fittings, base_riggings, base_cells,
        base_bonuses, shield_increment, regen_increment, armor_increment, cpu_increment, bonus_increment
    )
    
    return ship


# Main loop
while True:
    print("1. Create new ship")
    print("2. Load an existing ship")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        ship = create_ship()
        save_ship_to_file(ship)
    elif choice == '2':
        ship_name = input("Enter the name of the ship to load: ")
        ship = load_ship_from_file(ship_name)
        if ship:
            tier = int(input("Enter the tier of the ship (1-6): "))
            if 1 <= tier <= 6:
                ship.display_stats(tier)
            else:
                print("Invalid tier. Please enter a number between 1 and 6.")
    elif choice == '3':
        print("Exiting program.")
        break
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
