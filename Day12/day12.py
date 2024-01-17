from itertools import product
import re

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

def create_extended_instructions(instructions):
    extended_instructions = []
    for checked_instruction in instructions:
        initial_instruction_as_string = ""
        for elem in checked_instruction[0]:
            initial_instruction_as_string += elem
        extended_instruction = ""

        for i in range(4):
            extended_instruction += initial_instruction_as_string
            extended_instruction += "?"

        extended_instruction += initial_instruction_as_string
        extended_instruction = re.sub(r'(\.)\1+', r'\1', extended_instruction)
        extended_instruction = list(extended_instruction)
        if extended_instruction[0] == ".":
            extended_instruction.remove(".")
        if extended_instruction[-1] == ".":
            extended_instruction.pop()
            
        extended_instructions.append((extended_instruction, 5 * checked_instruction[1]))
        # extended_instructions.append((extended_instruction, checked_instruction[1]))

    return extended_instructions

def part2(instructions):
    valid_counter = 0
    states_db = {}
    for checked_instruction in instructions:
        valid_solutions = explore_instruction(checked_instruction, states_db)
        # print(valid_solutions, checked_instruction)
        valid_counter += valid_solutions
    return valid_counter

def explore_instruction(checked_instruction, states_db):
    # CREATE VARIABLES FOR CONVENIENCE
    checked_symbol_sequence = checked_instruction[0]
    checked_frequency_sequence = checked_instruction[1]

    # DETERMINE CERTAIN ADDITIONAL CHARACTERISTICS OF THE PUZZLE
    # total_broken_springs = sum(checked_frequency_sequence)
    # total_broken_spings_already_inserted = 0
    # unknown_status_count = 0
    # for elem in checked_symbol_sequence:
    #     if elem == "#":
    #         total_broken_spings_already_inserted += 1
    # broken_springs_to_be_inserted = total_broken_springs - total_broken_spings_already_inserted

    valid_solutions_found = 0

    # BASE CASE --- REACHED END
    # BASE CASE SUCCESS --- NOTHING LEFT TO EXPLORE AND NOTHING LEFT TO INSERT
    if len(checked_symbol_sequence) == 0 or len(checked_frequency_sequence) == 0:
        # SUCCES CASE 1 - NOTHING LEFT TO EXPLORE
        if len(checked_symbol_sequence) == 0 and len(checked_frequency_sequence) == 0:
            return 1
        # SUCCESS CASE 2 - ONLY OPERATIONAL LEFT TO EXPLORE
        elif len(checked_frequency_sequence) == 0 and "#" not in checked_symbol_sequence:
            return 1
        else:
            return 0

    # CASE 1 - STARTS WITH DAMAGED
    if checked_symbol_sequence[0] == "#":
        # CHECK IF ADDITIONAL DAMAGED SYMBOL CAN BE INSERTED ---- Check there are no conflicts with operational elements
        # IF IT CAN BE INSERTED, CONTINUE TO NEXT ELEMENT
        if check_if_damaged_can_be_inserted(checked_symbol_sequence, checked_frequency_sequence[0]) == True:
            valid_solutions_found += explore_instruction( (checked_symbol_sequence[checked_frequency_sequence[0] + 1:], checked_frequency_sequence[1:]) , states_db)
        # ELSE, DO NOT CONTINUE
    
    # CASE 2 START WITH UNKNOWN
    elif checked_symbol_sequence[0] == "?":
        # CASE 2A - CHECK IF DAMAGED SYMBOL CAN BE INSERTED
        if check_if_damaged_can_be_inserted(checked_symbol_sequence, checked_frequency_sequence[0]) == True:
        # IF IT CAN BE INSERTED, CONTINUE TO NEXT ELEMENT
            valid_solutions_found += explore_instruction( (checked_symbol_sequence[checked_frequency_sequence[0] + 1:], checked_frequency_sequence[1:]) , states_db)
        # ELSE, DO NOT CONTINUE THIS ALTERNATIVE

        # CASE 2B - CHECK IF OPERATIONAL SYMBOL CAN BE INSERTED --- Check that there are enough items left where damaged can be inserted
        # IF LENGTH OF THE REMAINING SEGMENT IS LESS THAN THE NUMBER OF THE BROKEN ONES TO BE INSERTED, OPERATIONAL CANNOT BE INSERTED
        if (len(checked_symbol_sequence) - 1) < sum(checked_frequency_sequence) + (len(checked_frequency_sequence) - 1):
            pass
        else:
            # INSERT EMPTY VALUE AND CONTINUE EXPLORING
            valid_solutions_found += explore_instruction( (checked_symbol_sequence[1:], checked_frequency_sequence) , states_db)
    # CASE 3 START WITH OPERATIONAL --- CONTINUE MOVING DOWN
    else:
        valid_solutions_found += explore_instruction( (checked_symbol_sequence[1:], checked_frequency_sequence) , states_db)

    return valid_solutions_found



def check_if_damaged_can_be_inserted(checked_symbol_sequence, next_broken_segment_length):
    # If the length to be inserted is longer than the remaining segment, quit
    if next_broken_segment_length > len(checked_symbol_sequence):
        return False
    
    # Check that there is no conflicting operational item. If ther is, return false
    for i in range(next_broken_segment_length):
        if checked_symbol_sequence[i] == ".":
            return False
    # If this is the last item, confirm that it can be inserted
    if len(checked_symbol_sequence) == next_broken_segment_length:
        return True
    # Check that there is an operational item immediately afer the insertion zone
    if checked_symbol_sequence[next_broken_segment_length] == "#":
        return False
    return True


if __name__ == "__main__":
    instructions = get_input()
    print(part1(instructions))
    instructions = get_input()
    extended_instruction = create_extended_instructions(instructions)
    print(part2(extended_instruction))

    # instructions = get_input()

    # for i in range(len(extended_instruction)):
    #     # print(extended_instruction[i])
    #     p1 = part1([instructions[i]])
    #     p2 = part2([extended_instruction[i]])
    #     if p1 != p2:
    #         print(p1, p2)
    #         print(extended_instruction[i])

    
    
