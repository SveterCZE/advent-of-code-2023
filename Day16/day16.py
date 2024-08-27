
def get_input():
    f = open("input.txt", "r")
    instructions = []
    for line in f:
        instructions.append(list(line.strip()))
    return instructions

def part1(instructions, initial_state):
    next_states = []
    next_states.append(initial_state)
    positions_visited = set()
    positions_visited.add(initial_state[0])
    states_db = set()
    states_db.add(initial_state)    

    while True:
        next_states = determine_next_steps(instructions, next_states, positions_visited, states_db)
        if len(next_states) == 0:
            break
    return len(positions_visited)
    
def determine_next_steps(instructions, current_states, positions_visited, states_db):
    next_states = []
    for checked_state in current_states:
        make_steps_from_current_state(instructions, checked_state, positions_visited, states_db, next_states)
    return next_states

def make_steps_from_current_state(instructions, checked_state, positions_visited, states_db, next_states):
    if instructions[checked_state[0][0]][checked_state[0][1]] == ".":
        potential_next_states = make_simple_move(checked_state)

    elif instructions[checked_state[0][0]][checked_state[0][1]] == "\\":
        potential_next_states = []
        if checked_state[1] == "N":
            potential_next_states.append((generate_neighbouring_tile(checked_state[0], "W"), "W"))
        elif checked_state[1] == "E":
            potential_next_states.append((generate_neighbouring_tile(checked_state[0], "S"), "S"))
        elif checked_state[1] == "S":
            potential_next_states.append((generate_neighbouring_tile(checked_state[0], "E"), "E"))
        elif checked_state[1] == "W":
            potential_next_states.append((generate_neighbouring_tile(checked_state[0], "N"), "N"))

    elif instructions[checked_state[0][0]][checked_state[0][1]] == "/":
        potential_next_states = []
        if checked_state[1] == "N":
            potential_next_states.append((generate_neighbouring_tile(checked_state[0], "E"), "E"))
        elif checked_state[1] == "E":
            potential_next_states.append((generate_neighbouring_tile(checked_state[0], "N"), "N"))
        elif checked_state[1] == "S":
            potential_next_states.append((generate_neighbouring_tile(checked_state[0], "W"), "W"))
        elif checked_state[1] == "W":
            potential_next_states.append((generate_neighbouring_tile(checked_state[0], "S"), "S"))

    elif instructions[checked_state[0][0]][checked_state[0][1]] == "-":
        if checked_state[1] == "E" or checked_state[1] == "W":
            potential_next_states = make_simple_move(checked_state)
        elif checked_state[1] == "N" or checked_state[1] == "S":
            potential_next_states = []
            potential_next_states.append((generate_neighbouring_tile(checked_state[0], "E"), "E"))
            potential_next_states.append((generate_neighbouring_tile(checked_state[0], "W"), "W"))

    elif instructions[checked_state[0][0]][checked_state[0][1]] == "|":
        if checked_state[1] == "N" or checked_state[1] == "S":
            potential_next_states = make_simple_move(checked_state)
        elif checked_state[1] == "E" or checked_state[1] == "W":
            potential_next_states = []
            potential_next_states.append((generate_neighbouring_tile(checked_state[0], "N"), "N"))
            potential_next_states.append((generate_neighbouring_tile(checked_state[0], "S"), "S"))
    
    validate_potential_next_step(potential_next_states, positions_visited, states_db, next_states)

def generate_neighbouring_tile(checked_state, move_direction):
    if move_direction == "N":
        return (checked_state[0] - 1, checked_state[1])
    elif move_direction == "E":
        return (checked_state[0], checked_state[1] + 1)
    elif move_direction == "S":
        return (checked_state[0] + 1, checked_state[1])
    elif move_direction == "W":
        return (checked_state[0], checked_state[1] - 1)

def make_simple_move(checked_state):
    return [(generate_neighbouring_tile(checked_state[0], checked_state[1]), checked_state[1])]

def is_valid(instructions, checked_position):
    if checked_position[0] < 0 or checked_position[1] < 0:
        return False
    if checked_position[0] >= len(instructions) or checked_position[1] >= len(instructions[1]):
        return False
    return True

def validate_potential_next_step(potential_next_states, positions_visited, states_db, next_states):
    for potential_next_state in potential_next_states:
        if is_valid(instructions, potential_next_state[0]) and potential_next_state not in states_db:
            positions_visited.add(potential_next_state[0])
            next_states.append(potential_next_state)
            states_db.add(potential_next_state)

def part2(instructions):
    best_score = 0
    # From top heading down
    for i in range(len(instructions[1])):
        test_score = part1(instructions, ((0,i), "S"))
        if test_score > best_score:
            best_score = test_score
    
    # From bottom heading up
    for i in range(len(instructions[1])):
        test_score = part1(instructions, ((len(instructions) - 1,i), "N"))
        if test_score > best_score:
            best_score = test_score

    # From left to right
    for i in range(len(instructions[0])):
        test_score = part1(instructions, ((i,0), "E"))
        if test_score > best_score:
            best_score = test_score
    
    # From right to left
    for i in range(len(instructions[0])):
        test_score = part1(instructions, ((i,len(instructions[0]) - 1), "W"))
        if test_score > best_score:
            best_score = test_score

    return best_score

if __name__ == "__main__":
    instructions = get_input()
    print(part1(instructions, ((0,0), "E")))
    print(part2(instructions))