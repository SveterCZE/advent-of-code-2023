def get_input():
    f = open("input.txt", "r")
    instructions = []
    for line in f:
        instructions.append(list(line.strip()))
    return instructions

def part1(instructions):
    starting_coordinate = find_starting_coordinate(instructions)
    visited_coordinates = traverse_map(instructions, starting_coordinate)
    print (len(visited_coordinates) // 2)
    return visited_coordinates

def part2(instructions, visited_coordinates):
    isolated_coordinates = set()
    correct_start_coordinate(instructions, visited_coordinates)
    for column in range(len(instructions[0])):
        intersections = 0
        traversing_edge = False
        entry_item = None
        for row in range(len(instructions)):
            checked_coordinate = (row, column)
            if checked_coordinate in visited_coordinates:
                if instructions[row][column] == "|":
                    continue
                elif instructions[row][column] == "-":
                    intersections += 1
                elif traversing_edge == False:
                    entry_item = instructions[row][column]
                    traversing_edge = True
                elif traversing_edge == True:
                    if entry_item == "7":
                        if instructions[row][column] == "J":
                            pass
                        elif instructions[row][column] == "L":
                            intersections += 1
                    elif entry_item == "F":
                        if instructions[row][column] == "L":
                            pass
                        elif instructions[row][column] == "J":
                            intersections += 1
                    traversing_edge = False
                    entry_item = None
            else:
                if intersections % 2 == 1:
                    isolated_coordinates.add(checked_coordinate)
    return len(isolated_coordinates)

def find_starting_coordinate(instructions):
    for row in range(len(instructions)):
        for column in range(len(instructions[0])):
            if instructions[row][column] == "S":
                return (row, column)

def correct_start_coordinate(instructions, visited_coordinates):
    starting_coordinate = find_starting_coordinate(instructions)
    N = (starting_coordinate[0] - 1, starting_coordinate[1])
    S = (starting_coordinate[0] + 1, starting_coordinate[1])
    E = (starting_coordinate[0], starting_coordinate[1] + 1)
    W = (starting_coordinate[0], starting_coordinate[1] - 1)
    if N in visited_coordinates and E in visited_coordinates:
        instructions[starting_coordinate[0]][starting_coordinate[1]] = "L"
    elif N in visited_coordinates and W in visited_coordinates:
        instructions[starting_coordinate[0]][starting_coordinate[1]] = "J"
    elif S in visited_coordinates and W in visited_coordinates:
        instructions[starting_coordinate[0]][starting_coordinate[1]] = "7"
    elif S in visited_coordinates and E in visited_coordinates:
        instructions[starting_coordinate[0]][starting_coordinate[1]] = "F"

def traverse_map(instructions, starting_coordinate):
    visited_nodes = set()
    direction = determine_initial_direction(instructions, starting_coordinate)
    current_coordinate = starting_coordinate
    while True:
        if starting_coordinate in visited_nodes:
            return visited_nodes
        current_coordinate = determine_next_coordinate(current_coordinate, direction)
        visited_nodes.add(current_coordinate)
        direction = determine_next_direction(instructions, direction, current_coordinate)
        

def determine_initial_direction(instructions, starting_coordinate):
    N = (starting_coordinate[0] - 1, starting_coordinate[1])
    if is_valid_coordinate(N, instructions):
        if instructions[N[0]][N[1]] == "|" or instructions[N[0]][N[1]] == "7" or instructions[N[0]][N[1]] == "F":
            return "N"
    S = (starting_coordinate[0] + 1, starting_coordinate[1])
    if is_valid_coordinate(S, instructions):
        if instructions[S[0]][S[1]] == "|" or instructions[S[0]][S[1]] == "L" or instructions[S[0]][S[1]] == "J":
            return "S"
    E = (starting_coordinate[0], starting_coordinate[1] + 1)
    if is_valid_coordinate(E, instructions):
        if instructions[E[0]][E[1]] == "-" or instructions[E[0]][E[1]] == "7" or instructions[E[0]][E[1]] == "J":
            return "E"
    W = (starting_coordinate[0], starting_coordinate[1] - 1)
    if is_valid_coordinate(W, instructions):
        if instructions[W[0]][W[1]] == "|" or instructions[W[0]][W[1]] == "L" or instructions[W[0]][W[1]] == "F":
            return "W"

def determine_next_coordinate(current_coordinate, direction):
    if direction == "N":
        return (current_coordinate[0] - 1, current_coordinate[1])
    elif direction == "S":
        return (current_coordinate[0] + 1, current_coordinate[1])
    elif direction == "E":
        return (current_coordinate[0], current_coordinate[1] + 1)
    elif direction == "W":
        return (current_coordinate[0], current_coordinate[1] - 1)

def determine_next_direction(instructions, direction, current_coordinate):
    if instructions[current_coordinate[0]][current_coordinate[1]] == "|":
        return direction
    elif instructions[current_coordinate[0]][current_coordinate[1]] == "-":
        return direction
    elif instructions[current_coordinate[0]][current_coordinate[1]] == "L":
        if direction == "S":
            return "E"
        elif direction == "W":
            return "N"
    elif instructions[current_coordinate[0]][current_coordinate[1]] == "J":
        if direction == "S":
            return "W"
        elif direction == "E":
            return "N"
    elif instructions[current_coordinate[0]][current_coordinate[1]] == "7":
        if direction == "E":
            return "S"
        elif direction == "N":
            return "W"
    elif instructions[current_coordinate[0]][current_coordinate[1]] == "F":
        if direction == "W":
            return "S"
        elif direction == "N":
            return "E"

def is_valid_coordinate(checked_coordinate, instructions):
    if checked_coordinate[0] < 0 or checked_coordinate[1] < 0 or checked_coordinate[0] >= len(instructions) or checked_coordinate[1] >= len(instructions[0]):
        return False
    else:
        return True

if __name__ == "__main__":
    instructions = get_input()
    visited_coordinates = part1(instructions)
    print(part2(instructions, visited_coordinates))