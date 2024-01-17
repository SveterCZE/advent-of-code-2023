from itertools import product
import re

def get_input():
    f = open("input.txt", "r")
    instructions = []
    for line in f:
        split_line = line.strip().split()
        instructions.append((list(split_line[0]), [int(x) for x in split_line[1].split(",")]))
    return instructions

def create_formatted_instructions(instructions, extend_instructions):
    extended_instructions = []
    for checked_instruction in instructions:
        initial_instruction_as_string = ""
        for elem in checked_instruction[0]:
            initial_instruction_as_string += elem
        extended_instruction = ""
        if extend_instructions == True:
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
        
        if extend_instructions == True:    
            extended_instructions.append((extended_instruction, 5 * checked_instruction[1]))
        else:
            extended_instructions.append((extended_instruction, 1 * checked_instruction[1]))
    return extended_instructions

def part1(instructions):
    valid_counter = 0
    for checked_instruction in instructions:
        states_db = {}
        valid_solutions = explore_instruction(checked_instruction, states_db)
        valid_counter += valid_solutions
    return valid_counter

def explore_instruction(checked_instruction, states_db):
    # CREATE VARIABLES FOR CONVENIENCE
    checked_symbol_sequence = checked_instruction[0]
    checked_frequency_sequence = checked_instruction[1]
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
            new_tuple = (tuple(checked_symbol_sequence[checked_frequency_sequence[0] + 1:]), tuple(checked_frequency_sequence[1:]))
            if new_tuple in states_db:
                valid_solutions_found += states_db[new_tuple]
            else:
                new_tuple_solutions = explore_instruction( new_tuple , states_db)
                states_db[new_tuple] = new_tuple_solutions
                valid_solutions_found += new_tuple_solutions
        # ELSE, DO NOT CONTINUE
    
    # CASE 2 START WITH UNKNOWN
    elif checked_symbol_sequence[0] == "?":
        # CASE 2A - CHECK IF DAMAGED SYMBOL CAN BE INSERTED
        if check_if_damaged_can_be_inserted(checked_symbol_sequence, checked_frequency_sequence[0]) == True:
        # IF IT CAN BE INSERTED, CONTINUE TO NEXT ELEMENT
            new_tuple = (tuple(checked_symbol_sequence[checked_frequency_sequence[0] + 1:]), tuple(checked_frequency_sequence[1:]))
            if new_tuple in states_db:
                valid_solutions_found += states_db[new_tuple]
            else:
                new_tuple_solutions = explore_instruction( new_tuple , states_db)
                states_db[new_tuple] = new_tuple_solutions
                valid_solutions_found += new_tuple_solutions
        # ELSE, DO NOT CONTINUE THIS ALTERNATIVE

        # CASE 2B - CHECK IF OPERATIONAL SYMBOL CAN BE INSERTED --- Check that there are enough items left where damaged can be inserted
        # IF LENGTH OF THE REMAINING SEGMENT IS LESS THAN THE NUMBER OF THE BROKEN ONES TO BE INSERTED, OPERATIONAL CANNOT BE INSERTED
        if (len(checked_symbol_sequence) - 1) < sum(checked_frequency_sequence) + (len(checked_frequency_sequence) - 1):
            pass
        else:
            # INSERT EMPTY VALUE AND CONTINUE EXPLORING
            new_tuple = (tuple(checked_symbol_sequence[1:]), tuple(checked_frequency_sequence))
            if new_tuple in states_db:
                valid_solutions_found += states_db[new_tuple]
            else:
                new_tuple_solutions = explore_instruction( new_tuple , states_db)
                states_db[new_tuple] = new_tuple_solutions
                valid_solutions_found += new_tuple_solutions
    # CASE 3 START WITH OPERATIONAL --- CONTINUE MOVING DOWN
    else:
        new_tuple = (tuple(checked_symbol_sequence[1:]), tuple(checked_frequency_sequence))
        if new_tuple in states_db:
            valid_solutions_found += states_db[new_tuple]
        else:
            new_tuple_solutions = explore_instruction( new_tuple , states_db)
            states_db[new_tuple] = new_tuple_solutions
            valid_solutions_found += new_tuple_solutions
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
    formatted_instructions = create_formatted_instructions(instructions, False)
    print(part1(formatted_instructions))
    
    instructions = get_input()
    formatted_instructions = create_formatted_instructions(instructions, True)
    print(part1(formatted_instructions)) 
