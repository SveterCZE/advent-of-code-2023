from itertools import product

def get_input():
    f = open("input.txt", "r")
    instructions = []
    for line in f:
        split_line = line.strip().split()
        instructions.append((list(split_line[0]), [int(x) for x in split_line[1].split(",")]))
    return instructions

def part1(instructions):
    valid_solutions = 0
    for elem in instructions:
        valid_solutions += calculate_valid_solutions(elem)
    return valid_solutions

def calculate_valid_solutions(checked_data):
    valid_positions = 0
    unknown_positions = []
    records = checked_data[0]
    pattern = checked_data[1]
    for i in range(len(records)):
        if records[i] == "?":
            unknown_positions.append(i)
    possible_permutations = product([".","#"], repeat=len(unknown_positions))
    for checked_permutation in list(possible_permutations):
        for i in range(len(checked_permutation)):
            records[unknown_positions[i]] = checked_permutation[i]
        if is_valid_record(records, pattern) == True:
            valid_positions += 1
    return valid_positions

def is_valid_record(records, pattern):
    broken_elems_freq = []
    broken_counter = 0
    counting_broken = False
    for i in range(len(records)):
        if records[i] == "#":
            counting_broken = True
            broken_counter += 1
        elif records[i] == ".":
            if counting_broken == True:
                counting_broken = False
                broken_elems_freq.append(broken_counter)
                broken_counter = 0
    if counting_broken == True:
        broken_elems_freq.append(broken_counter)
    
    if (len(broken_elems_freq) != len(pattern)):
        return False
    for i in range(len(broken_elems_freq)):
        if broken_elems_freq[i] != pattern[i]:
            return False
    return True

if __name__ == "__main__":
    instructions = get_input()
    print(part1(instructions))
    # print(part2(instructions))