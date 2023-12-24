import copy

def main():
    instructions = get_input()
    print(part1(instructions))
    modify_the_map(instructions)
    print(part1(instructions))

def get_input():
    coordinates = set()
    instructions = []
    f = open("input.txt", "r")
    for line in f:
        temp_line = list(line.strip())
        instructions.append(temp_line)
    return instructions

def part1(instructions):
    start_coord, finish_coord = find_start_and_finish(instructions)
    visited_coordinates = set()
    visited_coordinates.add(start_coord)
    finished_journeys_DB = []
    make_steps(start_coord, visited_coordinates, instructions, finished_journeys_DB, finish_coord)
    finished_journeys_DB.sort()
    return finished_journeys_DB[-1]
    
def make_steps(current_coordinate, visited_coordinates, instructions, finished_journeys_DB, finish_coord):
    # BASE CASE --- Reached the final coordinate
    if is_finish_found(visited_coordinates, finish_coord):
        finished_journeys_DB.append(len(visited_coordinates) - 1)
        return
    # RECURSIVE CASE --- Find other possible steps
    # ALTERNATIVE 1 - Just one step possible. Move iteratively.
    while True:
        possible_next_steps = find_possible_next_steps(current_coordinate, instructions, visited_coordinates)
        if len(possible_next_steps) == 1:
            current_coordinate = possible_next_steps[0]
            visited_coordinates.add(current_coordinate)
            if is_finish_found(visited_coordinates, finish_coord):
                finished_journeys_DB.append(len(visited_coordinates) - 1)
                return
        else:
            break
    # ALTERNATIVE 2 - More steps possible. Move recursively.
    for possible_step in possible_next_steps:
        new_visited_coord_DB = copy.deepcopy(visited_coordinates)
        new_visited_coord_DB.add(possible_step)
        make_steps(possible_step, new_visited_coord_DB, instructions, finished_journeys_DB, finish_coord)

def is_finish_found(visited_coordinates, finish_coord):
    if finish_coord in visited_coordinates:
        return True
    else:
        return False

def find_possible_next_steps(current_coordinate, instructions, visited_coordinates):
    possible_next_steps = []
    N = (current_coordinate[0] - 1, current_coordinate[1])
    if is_valid_coordinate(N, instructions, "^", visited_coordinates):
        possible_next_steps.append(N)
    S = (current_coordinate[0] + 1, current_coordinate[1])
    if is_valid_coordinate(S, instructions, "v", visited_coordinates):
        possible_next_steps.append(S)
    E = (current_coordinate[0], current_coordinate[1] + 1)
    if is_valid_coordinate(E, instructions, ">", visited_coordinates):
        possible_next_steps.append(E)
    W = (current_coordinate[0], current_coordinate[1] - 1)
    if is_valid_coordinate(W, instructions, "<", visited_coordinates):
        possible_next_steps.append(W)
    return possible_next_steps

def is_valid_coordinate(checked_coordinate, instructions, special_char, visited_coordinates):
    if checked_coordinate in visited_coordinates:
        return False
    if checked_coordinate[0] < 0 or checked_coordinate[1] < 0:
        return False
    if instructions[checked_coordinate[0]][checked_coordinate[1]] == "." or instructions[checked_coordinate[0]][checked_coordinate[1]] == special_char:
        return True
    if instructions[checked_coordinate[0]][checked_coordinate[1]] == "#":
        return False
    else:
        return False

def find_start_and_finish(instructions):
    start_coord = None
    most_recent_coord = None
    for row in range(len(instructions)):
        for column in range(len(instructions[0])):
            if instructions[row][column] == ".":
                most_recent_coord = (row, column)
                if start_coord == None:
                    start_coord = (row, column)
    return start_coord, most_recent_coord

def modify_the_map(instructions):
    special_chars = ["^", "v", ">", "<"]
    for row in range(len(instructions)):
        for column in range(len(instructions[0])):
            if instructions[row][column] in special_chars:
                instructions[row][column] = "."

main()