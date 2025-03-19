import argparse
import json
import re
import pytesseract
from PIL import Image

# If Tesseract is not in your PATH, specify its location:
# pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"  # Linux example
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Windows example


def read_config_from_txt(file_path: str) -> dict:
    """
    Reads a simple key=value config from a .txt file.
    Lines starting with '#' or blank lines are ignored.
    Returns a dictionary of config values.
    """
    config = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Skip comments or empty lines
            if not line or line.startswith('#'):
                continue

            # Split on the first '='
            if '=' in line:
                key, val = line.split('=', 1)
                key = key.strip()
                val = val.strip()
                config[key] = val

    return config


def parse_ship_screenshot(image_path: str, name: str) -> dict:
    """
    Parse a 'ship' screenshot (like Hammerhead, Thulmar) and return a dict
    that matches the structure of the sample JSON (thulmar.json).
    """
    img = Image.open(image_path)
    ocr_text = pytesseract.image_to_string(img)

    ship_name = name

    # Helper: guess class from text like "Battleship M1" or "Corvett" or "Destroyer"
    # Tweak to match your game classes.
    class_match = re.search(r"(Battleship|Corvette|Titan|Destroyer)", ocr_text, re.IGNORECASE)
    ship_class = class_match.group(1).lower() if class_match else "unknown_class"

    # Example function to parse lines like "Shield: 25000 +3500"
    def extract_two_numbers(label):
        pattern = rf"{label}\s*:\s*([\d,\.]+)\s*\+([\d,\.]+)"
        match = re.search(pattern, ocr_text, re.IGNORECASE)
        if match:
            base_str, inc_str = match.groups()
            base_val = int(base_str.replace(",", ""))
            inc_str = inc_str.replace(".", "")
            inc_val = int(inc_str.replace(",", ""))
            return base_val, inc_val
        else:
            # fallback if we only find one number
            single_pattern = rf"{label}\s*:\s*([\d,\.]+)"
            single_match = re.search(single_pattern, ocr_text, re.IGNORECASE)
            if single_match:
                return int(single_match.group(1).replace(",", "")), 0
        return 0, 0

    def extract_single_number(label):
        pattern = rf"{label}\s*:\s*([\d,\.]+)"
        match = re.search(pattern, ocr_text, re.IGNORECASE)
        if match:
            val_str = match.group(1).replace(",", "")
            return float(val_str) if "." in val_str else int(val_str)
        return 0

    def extract_damage(label):
        # e.g. "Impact Damage: 110% +5%"
        pattern = rf"{label}\s*:\s*([\d\.]+)%?\s*\+([\d\.]+)%?"
        match = re.search(pattern, ocr_text, re.IGNORECASE)
        if match:
            base_str, inc_str = match.groups()
            return float(base_str), float(inc_str)
        else:
            single_pattern = rf"{label}\s*:\s*([\d\.]+)%"
            single_match = re.search(single_pattern, ocr_text, re.IGNORECASE)
            if single_match:
                return float(single_match.group(1)), 0.0
        return 0.0, 0.0

    # Extract stats
    base_shield, shield_inc = extract_two_numbers("Shield")
    base_shield_regen, regen_inc = extract_two_numbers("Shield/Sec")
    base_armor, armor_inc = extract_two_numbers("Armor")
    base_cpu, cpu_inc = extract_two_numbers("CPU")
    # Energy might appear as "Energy/Size: 25" => interpret as needed
    energy = extract_single_number("Energy")
    base_energy_regen = extract_single_number("Energy/Sec")  # parse if needed
    base_speed_move = extract_single_number("Speed/Move")
    base_speed_turn = extract_single_number("Speed/Turn")
    base_weapons = extract_single_number("Weapons")
    base_fittings = extract_single_number("Fittings")
    base_riggings = extract_single_number("Rigging")
    base_cells = extract_single_number("Cells")

    imp_base, imp_inc = extract_damage("Impact Damage")
    impr_base, impr_inc = extract_damage("Impact Range")
    eng_base, eng_inc = extract_damage("Energy Damage")
    engr_base, engr_inc = extract_damage("Energy Range")
    exp_base, exp_inc = extract_damage("Explosive Damage")
    expr_base, expr_inc = extract_damage("Explosive Range")
    rep_base, rep_inc = extract_damage("Repair Strength")


    # Construct final dict
    ship_data = {
        "name": ship_name,
        "ship_class": ship_class,
        "base_shield": base_shield,
        "base_shield_regen": base_shield_regen,
        "base_armor": base_armor,
        "base_cpu": base_cpu,
        "base_energy": energy,
        "base_energy_regen": base_energy_regen,
        "base_speed_move": base_speed_move,
        "base_speed_turn": base_speed_turn,
        "base_weapons": base_weapons,
        "base_fittings": base_fittings,
        "base_riggings": base_riggings,
        "base_cells": base_cells,
        "base_bonuses": {
            "Impact Damage": imp_base,
            "Energy Damage": eng_base,
            "Explosive Damage": exp_base,
            "Repair Strength": rep_base,
            "Impact Range": impr_base,
            "Energy Range": engr_base,
            "Explosive Range": expr_base,
        },
        "shield_increment": shield_inc,
        "regen_increment": regen_inc,
        "armor_increment": armor_inc,
        "cpu_increment": cpu_inc,
        "bonus_increment": imp_inc  # or store them separately if they differ
    }
    return ship_data


def parse_weapon_screenshot(active_image_path: str, ability_image_path: str) -> dict:
    active_img = Image.open(active_image_path)
    active_text = pytesseract.image_to_string(active_img)
    ability_img = Image.open(ability_image_path)
    ability_text = pytesseract.image_to_string(ability_img)
    print(active_text)
    def extract_stat(label, text):
        pattern = rf"{label}\s*:\s*([\d,\.]+)"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            val_str = match.group(1).replace(",", "")
            return float(val_str) if "." in val_str else int(val_str)
        return 0

    def dmg_type(text):
        targetMatch = re.search(r"(Explosive|Energy|Impact|Repair)", text, re.IGNORECASE)
        target = targetMatch.group(1).lower() if targetMatch else "unknown_target"
        return target

    def extract_damage(text):
        type = dmg_type(text)
        pattern = rf"{type} damage\s*:\s*([\d,\.]+)"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            val_str = match.group(1).replace(",", "")
            return float(val_str) if "." in val_str else int(val_str)
        return 0

    def projectile_count(text):
        type = dmg_type(text)
        pattern = rf"{type} damage\s*:\s*([x,\d,\.]+)"
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            val_str = match.group(1).replace(",", "")
            return int(val_str.split("x")[1]) if len(val_str.split("x")) > 1 else 0
        return 1


    def active_stat():
        targetMatch = re.search(r"(Enemy|Self|Ally)", active_text, re.IGNORECASE)
        target = targetMatch.group(1).lower() if targetMatch else "unknown_target"
        range = extract_stat("Range", active_text)
        aoe = extract_stat("AOE", active_text)
        speed = extract_stat("Speed", active_text)
        armor = extract_stat("Armor", active_text)
        recharge = extract_stat("Recharge", active_text)
        data = {
            "target": target,
            "range": range,
            "aoe": aoe,
            "damage_type": dmg_type(active_text),
            "damage": extract_damage(active_text),
            "projectile_count": projectile_count(active_text),
            "speed": speed,
            "armor": armor,
            "recharge": recharge,
            "armor_damage": extract_stat("Armor Damage", ability_text),
            "shield_damage": extract_stat("Shield Damage", ability_text)
        }
        return data


    def ability_stat():
        targetMatch = re.search(r"(Enemy|Self|Ally)", ability_text, re.IGNORECASE)
        target = targetMatch.group(1).lower() if targetMatch else "unknown_target"
        range = extract_stat("Range", ability_text)
        aoe = extract_stat("AOE", ability_text)
        speed = extract_stat("Speed", ability_text)
        armor = extract_stat("Armor", ability_text)
        energy = extract_stat("Energy", ability_text)
        recharge = extract_stat("Recharge", ability_text)

        data = {
            "target": target,
            "range": range,
            "aoe": aoe,
            "damage_type": dmg_type(ability_text),
            "damage": extract_damage(ability_text),
            "projectile_count": projectile_count(ability_text),
            "speed": speed,
            "armor": armor,
            "energy": energy,
            "recharge": recharge,
            "armor_damage": extract_stat("Armor Damage", ability_text),
            "shield_damage": extract_stat("Shield Damage", ability_text)
        }
        return data



    # Process Active stats screenshot
    active_stats = active_stat()

    # Process Ability stats screenshot
    ability_stats = ability_stat()

    # Construct final dictionary in the attached format
    output_data = {
        "active_stats": active_stats,
        "ability_stats": ability_stats
    }
    return output_data


def main():
    # 1) Read config from a text file (hard-coded to "config.txt" here)
    config = read_config_from_txt("config.txt")

    # 2) Extract needed fields (with defaults)
    image_path = config.get("image_path", "screenshot.png")
    mode = config.get("mode", "ship")      # "ship" or "weapon"
    tab = config.get("tab", "active")      # "active" or "ability" (ignored for ships)
    output = config.get("output", "output.json")

    # 3) Run the appropriate parser
    if mode.lower() == "ship":
        data = parse_ship_screenshot(image_path)
    else:
        data = parse_weapon_screenshot(image_path)

    # 4) Write the JSON to file
    with open(output, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"JSON data written to {output}")


if __name__ == "__main__":
    main()
