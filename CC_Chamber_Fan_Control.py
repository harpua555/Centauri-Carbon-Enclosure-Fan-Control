#!/usr/bin/env python3
import sys
import re

def main():
    if len(sys.argv) < 2:
        print("Usage: ControlEnclosureFan.py <gcode_file>")
        sys.exit(1)

    gcode_file = sys.argv[1]

    # Prompt for fan speed
    try:
        percent = int(input("Enter fan speed (0–100%): "))
        if not 0 <= percent <= 100:
            raise ValueError
    except ValueError:
        print("Invalid input. Must be an integer between 0–100.")
        sys.exit(1)

    # Prompt for line interval
    try:
        interval_input = input("Insert every how many lines? (default = 20): ").strip()
        interval = int(interval_input) if interval_input else 20
        if interval < 1:
            raise ValueError
    except ValueError:
        print("Invalid interval. Using default of 20.")
        interval = 20

    fan_value = min(round(percent * 255 / 100), 255)

    with open(gcode_file, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    # Find start at ;LAYER:0
    start_idx = next((i for i, l in enumerate(lines) if ";LAYER:0" in l), None)
    if start_idx is None:
        print("Could not find ;LAYER:0")
        sys.exit(1)
    insert_start = start_idx + 20

    # Find last pair of LAYER:### + SET_PRINT_STATS_INFO CURRENT_LAYER=###
    layer_pattern = re.compile(r";LAYER:(\d+)")
    stats_pattern = re.compile(r"SET_PRINT_STATS_INFO CURRENT_LAYER=(\d+)")
    last_layer_idx = None

    for i in range(len(lines) - 1):
        layer_match = layer_pattern.match(lines[i].strip())
        stats_match = stats_pattern.match(lines[i + 1].strip())
        if layer_match and stats_match and layer_match.group(1) == stats_match.group(1):
            last_layer_idx = i + 1  # line with SET_PRINT_STATS_INFO

    if last_layer_idx is None:
        print("Could not find matching end-layer marker.")
        sys.exit(1)

    # Find next EXCLUDE_OBJECT_END after last_layer_idx
    insert_end = None
    for i in range(last_layer_idx + 1, len(lines)):
        if lines[i].strip().startswith("EXCLUDE_OBJECT_END"):
            insert_end = i
            break

    if insert_end is None:
        print("Could not find EXCLUDE_OBJECT_END after last print layer.")
        sys.exit(1)

    # Insert fan command every N lines between insert_start and insert_end
    modified = []
    for i, line in enumerate(lines):
        modified.append(line)
        if insert_start <= i < insert_end and (i - insert_start) % interval == 0:
            modified.append(f"M106 P3 S{fan_value}\n")

    with open(gcode_file, "w", encoding="utf-8") as f:
        f.writelines(modified)

    print(f"Inserted M106 P3 S{fan_value} every {interval} lines between line {insert_start} and line {insert_end}.")

if __name__ == "__main__":
    main()
