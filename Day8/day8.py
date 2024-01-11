import re
from math import lcm

def get_input():
    f = open("input.txt", "r")
    instructions = []
    map = {}
    for line in f:
        if len(instructions) == 0:
            instructions = list(line.strip())
        else:
            temp_line = re.findall(r'[a-zA-Z0-9]+', line)
            if len(temp_line) == 3:
                map[temp_line[0]] = (temp_line[1], temp_line[2])
    return instructions, map

def part1(instructions, map):
    counter = 0
    start = "AAA"
    return take_steps(instructions, map, counter, start)

def take_steps(instructions, map, counter, current_coordinate):
    while True:
        if current_coordinate == "ZZZ":
            return counter
        else:
            if instructions[counter % len(instructions)] == "L":
                current_coordinate = map[current_coordinate][0]
            elif instructions[counter % len(instructions)] == "R":
                current_coordinate = map[current_coordinate][1]
            counter += 1

def part2(instructions, map):
    counter = 0
    starting_coordinates = find_starting_coordinates(map)
    steps_counts = []
    for checked_coordinate in starting_coordinates:
        steps_counts.append(take_ghost_steps(instructions, map, counter, checked_coordinate, checked_coordinate))
    return(lcm(*steps_counts))

def find_starting_coordinates(map):
    staring_coordinates = []
    for key, value in map.items():
        if key[-1] == "A":
            staring_coordinates.append(key)
    return staring_coordinates

def take_ghost_steps(instructions, map, counter, current_coordinate, initial_coordinate):
    while True:
        if current_coordinate[2] == "Z":
            return counter
        if instructions[counter % len(instructions)] == "L":
            current_coordinate = map[current_coordinate][0]
        elif instructions[counter % len(instructions)] == "R":
            current_coordinate = map[current_coordinate][1]
        counter += 1

def ghost_coordinates_reached(current_coordinates):
    for elem in current_coordinates:
        if elem[2] != "Z":
            return False
    return True

if __name__ == "__main__":
    instructions, map = get_input()
    print(part1(instructions, map))
    print(part2(instructions, map))