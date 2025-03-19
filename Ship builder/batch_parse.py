import os
import json
from ssstatgrab import parse_ship_screenshot, parse_weapon_screenshot

def read_names(file_path: str) -> list:
    """
    Reads a list of names from a text file.
    Each non-empty, non-comment line is considered a name.
    """
    names = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                names.append(line)
    return names

def process_ship(name: str, mode: str):
    """
    For a given ship/weapon name:
      - Assumes the input image is named '<name>.png'
      - Uses the appropriate parser function
      - Writes the output JSON to '<name>.json'
    """
    image_file = f"ss/{mode}/{name}.png"
    output_file = f"{mode}/{name}.json"

    if not os.path.exists(image_file):
        print(f"Image file not found for '{name}': expected {image_file}")
        return

    data = parse_ship_screenshot(name, mode)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Processed {name}: JSON written to {output_file}")


def process_weapon(name: str, mode: str):
    """
    For a given ship/weapon name:
      - Assumes the input image is named '<name>.png'
      - Uses the appropriate parser function
      - Writes the output JSON to '<name>.json'
    """
    active_file = f"ss/{mode}/active/{name}.png"
    ability_file = f"ss/{mode}/ability/{name}.png"
    output_file = f"{mode}/{name}.json"

    if not os.path.exists(active_file):
        print(f"Image file not found for '{name}': expected {active_file}")
        return
    if not os.path.exists(ability_file):
        print(f"Image file not found for '{name}': expected {ability_file}")
        return

    data = parse_weapon_screenshot(active_file, ability_file)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Processed {name}: JSON written to {output_file}")

def main():
    # Change these as needed:
    names_list_file = "names.txt"  # This file should contain one ship or weapon name per line.
    mode = "weapon"                  # "ship" or "weapon"

    names = read_names(names_list_file)
    if not names:
        print("No valid names found in", names_list_file)
        return

    for name in names:
        if mode.lower() == "ship":
            process_ship(name, mode)
        else:
            process_weapon(name, mode)

if __name__ == "__main__":
    main()
