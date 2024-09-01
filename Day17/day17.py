import queue
import collections
import copy

def get_input():
    f = open("input.txt", "r")
    instructions = []
    for line in f:
        instructions.append([int(x) for x in line.strip()])
    return instructions

def part1(instructions):
    visited_coordinates = set()
    initial_coordinate = (0,0)
    direction = "S"
    direction_stepe_taken = 0
    steps_queue = queue.PriorityQueue()
    steps_queue.put((0, initial_coordinate, direction, direction_stepe_taken))
    heat_loss = run_steps_calculation(instructions, visited_coordinates, steps_queue)
    return heat_loss

def run_steps_calculation(instructions, visited_coordinates, steps_queue):
    while True:
        current_coordinate = steps_queue.get()
        if (current_coordinate[1], current_coordinate[2], current_coordinate[3]) in visited_coordinates:
            pass
        else:
            visited_coordinates.add((current_coordinate[1], current_coordinate[2], current_coordinate[3]))
            # Check if the target had been reached
            if current_coordinate[1] == (len(instructions) - 1, len(instructions[0]) - 1):
                # print(current_coordinate[3])
                return current_coordinate[0]
            # If not, generate next possible steps and add if they are valid, add them to the queue
            generate_potential_next_steps(current_coordinate, instructions, visited_coordinates, steps_queue)

        
def generate_potential_next_steps(current_coordinate, instructions, visited_coordinates, steps_queue):
    if is_move_direction_permissible(current_coordinate[2], current_coordinate[3], "N"):
        N = (current_coordinate[1][0] - 1, current_coordinate[1][1])
        try_adding_step_to_queue(current_coordinate, N, "N", instructions, steps_queue)
    if is_move_direction_permissible(current_coordinate[2], current_coordinate[3], "E"):
        E = (current_coordinate[1][0], current_coordinate[1][1] + 1)
        try_adding_step_to_queue(current_coordinate, E, "E", instructions, steps_queue)
    if is_move_direction_permissible(current_coordinate[2], current_coordinate[3], "S"):
        S = (current_coordinate[1][0] + 1, current_coordinate[1][1])
        try_adding_step_to_queue(current_coordinate, S, "S", instructions, steps_queue)
    if is_move_direction_permissible(current_coordinate[2], current_coordinate[3], "W"):
        W = (current_coordinate[1][0], current_coordinate[1][1] - 1)
        try_adding_step_to_queue(current_coordinate, W, "W", instructions, steps_queue)

def is_move_direction_permissible(current_direction, current_direction_steps, proposed_direction):
    if (current_direction == proposed_direction) and current_direction_steps == 3:
        return False
    if current_direction == "N" and proposed_direction == "S":
        return False
    if current_direction == "S" and proposed_direction == "N":
        return False
    if current_direction == "W" and proposed_direction == "E":
        return False
    if current_direction == "E" and proposed_direction == "W":
        return False
    return True

def try_adding_step_to_queue(current_coordinate, new_coordinate, new_direction, instructions, steps_queue):
    if is_coordinate_valid(new_coordinate, instructions):
        # Moving in the same direction:
        if current_coordinate[2] == new_direction:
            new_coordinate_for_insertion = (current_coordinate[0] + instructions[new_coordinate[0]][new_coordinate[1]], new_coordinate, new_direction, current_coordinate[3] + 1)
        else:
            new_coordinate_for_insertion = (current_coordinate[0] + instructions[new_coordinate[0]][new_coordinate[1]], new_coordinate, new_direction, 1)
        steps_queue.put(new_coordinate_for_insertion)

def is_coordinate_valid(new_coordinate, instructions):
    if new_coordinate[0] < 0 or new_coordinate[1] < 0:
        return False
    if new_coordinate[0] >= len(instructions) or new_coordinate[1] >= len(instructions[1]):
        return False
    return True

def part2(instructions):
    pass

if __name__ == "__main__":
    instructions = get_input()
    print(part1(instructions))
    print(part2(instructions))