def get_input():
    f = open("input.txt", "r")
    instructions = []
    for line in f:
        instructions.append(line.strip().split())
    return instructions

def part1(instructions):
    coordinates = []
    initial_coordinate = (0,0)
    coordinates.append(initial_coordinate)
    identify_intervals(instructions, initial_coordinate, coordinates)
    circumference = count_circumference(instructions)
    inner_area = count_inner_area(coordinates)
    return int ((circumference / 2) + inner_area + 1) 

def count_circumference(instructions):
    circumference = 0
    for elem in instructions:
        circumference += int(elem[1])
    return circumference

def count_inner_area(coordinates):
    inner_area = 0
    for i in range(len(coordinates) - 1):
        inner_area += count_pair_value(coordinates, i)
    return abs(inner_area) / 2

def count_pair_value(coordinates, i):
    return ((coordinates[i][0]*coordinates[i+1][1]) - (coordinates[i+1][0]*coordinates[i][1]) )

def identify_intervals(instructions, initial_coordinate, coordinates):
    for elem in instructions:
        initial_coordinate = add_interval(elem, initial_coordinate, coordinates)
    
def add_interval(checked_instruction, initial_coordinate, coordinates):
    if checked_instruction[0] == "U":
        next_coordinate = (initial_coordinate[0] - int(checked_instruction[1]), initial_coordinate[1])
        coordinates.append(next_coordinate)
    elif checked_instruction[0] == "D":
        next_coordinate = (initial_coordinate[0] + int(checked_instruction[1]), initial_coordinate[1])
        coordinates.append(next_coordinate)
    elif checked_instruction[0] == "L":
        next_coordinate = (initial_coordinate[0], initial_coordinate[1] - int(checked_instruction[1]))
        coordinates.append(next_coordinate)
    elif checked_instruction[0] == "R":
        next_coordinate = (initial_coordinate[0], initial_coordinate[1] + int(checked_instruction[1]))
        coordinates.append(next_coordinate)
    return next_coordinate

def part2(instructions):
    instructions = decode_part2_instructions(instructions)
    return part1(instructions)

def decode_part2_instructions(instructions):
    modified_instructions = []
    for elem in instructions:
        hex_value = int(elem[2][2:7], 16)
        direction_value = int(elem[2][7])
        if direction_value == 0:
            modified_instructions.append(["R", hex_value])
        elif direction_value == 1:
            modified_instructions.append(["D", hex_value])
        elif direction_value == 2:
            modified_instructions.append(["L", hex_value])
        elif direction_value == 3:
            modified_instructions.append(["U", hex_value])
    return modified_instructions

if __name__ == "__main__":
    instructions = get_input()
    print(part1(instructions))
    print(part2(instructions))