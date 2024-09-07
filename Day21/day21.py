def get_input():
    f = open("input.txt", "r")
    instructions = []
    for line in f:
        instructions.append(list(line.strip()))
    return instructions

def part1(instructions):
    possible_states = set()
    possible_states.add(find_start_coordinate(instructions))
    for i in range(64):
        possible_states = make_step(instructions, possible_states)
    return len(possible_states)

def make_step(instructions, possible_states):
    next_steps_states = set()
    for checked_coordinate in possible_states:
        generate_possible_next_states(instructions, checked_coordinate, next_steps_states)
    return next_steps_states

def generate_possible_next_states(instructions, checked_coordinate, next_steps_states):
    possible_steps = []
    possible_steps.append((checked_coordinate[0] + 1, checked_coordinate[1]))
    possible_steps.append((checked_coordinate[0] - 1, checked_coordinate[1]))
    possible_steps.append((checked_coordinate[0], checked_coordinate[1] + 1))
    possible_steps.append((checked_coordinate[0], checked_coordinate[1] - 1))
    for possible_step in possible_steps:
        if is_valid_coordinate(possible_step, instructions):
            next_steps_states.add(possible_step)
    return next_steps_states

def is_valid_coordinate(possible_step, instructions):
    if possible_step[0] < 0 or possible_step[1] < 0 or possible_step[0] >= len(instructions) or possible_step[1] >= len(instructions[0]):
        return False
    if instructions[possible_step[0]][possible_step[1]] == "#":
        return False
    return True

def find_start_coordinate(instructions):
    for row in range(len(instructions)):
        for column in range(len(instructions[0])):
            if instructions[row][column] == "S":
                instructions[row][column] = "."
                return (row, column)

if __name__ == "__main__":
    instructions = get_input()
    print(part1(instructions))
    # print(part2(instructions))