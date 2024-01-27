import copy

def get_input():
    f = open("input.txt", "r")
    instructions = []
    for line in f:
        instructions.append(list(line.strip()))
    return instructions

def part1(instructions):
    updated_graph = create_empty_updated_graph(instructions)
    make_items_fall(instructions, updated_graph)
    return calculate_value(updated_graph)

def part2(instructions):
    patterns_DB = calculate_pattern_number(instructions)
    instructions = patterns_DB[-1]
    pivot_first_appearance = patterns_DB.index(instructions)
    frequency_length = len(patterns_DB[pivot_first_appearance + 1:])
    for i in range((1000000000 - (pivot_first_appearance + 1)) % frequency_length):
        instructions = make_circular_rotation(instructions)
    return calculate_value(instructions)

def calculate_pattern_number(instructions):
    patterns_DB = []
    while True:
        instructions = make_circular_rotation(instructions)
        if instructions in patterns_DB:
            patterns_DB.append(instructions)
            return patterns_DB
        else:
            patterns_DB.append(instructions)

def make_circular_rotation(instructions):
    for i in range(4):
        updated_graph = create_empty_updated_graph(instructions)
        make_items_fall(instructions, updated_graph)
        rotated_graph = rotate_graph(updated_graph)
        instructions = rotated_graph
    return instructions

def convert_pattern_to_tuple(pattern):
    temp_list = []
    for elem in pattern:
        temp_list.append(tuple(elem))
    return tuple(temp_list)

def rotate_graph(updated_graph):
    rotated_graph = []
    for i in range(len(updated_graph[0])):
        temp_line = []
        for j in range(len(updated_graph)):
            temp_line.append("x")
        rotated_graph.append(temp_line)
    for i in range(len(updated_graph)):
        for j in range(len(updated_graph[0])):
            rotated_graph[j][len(updated_graph) - 1 - i] = updated_graph[i][j]
    return rotated_graph

def calculate_value(updated_graph):
    sum = 0
    multiplier = len(updated_graph)
    for i in range(len(updated_graph)):
        for elem in updated_graph[i]:
            if elem == "O":
                sum += multiplier
        multiplier = multiplier - 1
    return sum 

def make_items_fall(instructions, updated_graph):
    for row in range(len(instructions)):
        for column in range(len(instructions[0])):
            if instructions[row][column] == "O":
                for i in reversed(range(row + 1)):
                    if i == 0 and updated_graph[i][column] == ".":
                        updated_graph[i][column] = "O"
                    elif updated_graph[i - 1][column] == "#" or updated_graph[i - 1][column] == "O":
                        updated_graph[i][column] = "O"
                        break

def create_empty_updated_graph(instructions):
    updated_graph = []
    for row in instructions:
        temp_line = []
        for elem in row:
            if elem == "#":
                temp_line.append("#")
            else:
                temp_line.append(".")
        updated_graph.append(temp_line)
    return updated_graph
            

if __name__ == "__main__":
    instructions = get_input()
    print(part1(instructions))
    instructions = get_input()
    print(part2(instructions))