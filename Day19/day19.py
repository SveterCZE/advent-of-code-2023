import re
import copy

def get_input():
    f = open("input.txt", "r")
    instructions = {}
    parts = []
    inserting_instructions = True
    for line in f:
        if len(line) <= 1:
            inserting_instructions = False
            continue
        if inserting_instructions == True:
            split_line = line.strip().split("{")
            instructions[split_line[0]] = extract_instruction_sequence(split_line[1][:-1])
        else:
            part = {}
            parameters = re.findall(r'[a-zA-Z]+', line)
            numbers = re.findall(r'\d+', line)
            for i in range(len(parameters)):
                part[parameters[i]] = int(numbers[i])
            parts.append(part)
    return instructions, parts

def extract_instruction_sequence(text_segment):
    correctly_split_segment = []
    segment_split = text_segment.split(",")
    for i in range(len(segment_split) -1 ):
        correctly_split_segment.append(extract_individual_instruction(segment_split[i]))
    correctly_split_segment.append(segment_split[-1])
    return correctly_split_segment

def extract_individual_instruction(individual_segment):
    extracted_segment = []
    extracted_segment.append(individual_segment[0])
    extracted_segment.append(individual_segment[1])
    individual_segment = individual_segment[2:].split(":")
    extracted_segment.append(int(individual_segment[0]))
    extracted_segment.append(individual_segment[1])
    return extracted_segment

def part1(instructions, parts):
    accepted = []
    rejected = []
    for elem in parts:
        check_part(elem, instructions, accepted, rejected)
    return count_accepted_value(accepted)

def check_part(checked_part, instructions, accepted, rejected):
    relevant_instruction = instructions["in"]
    iterate_over_instruction(checked_part, instructions, relevant_instruction, accepted, rejected)

def iterate_over_instruction(checked_part, instructions, checked_instruction, accepted, rejected):
    for i in range(len(checked_instruction)):
        # If a final element had been reached, check 
        if i == len(checked_instruction) - 1:
            if checked_instruction[i][0] == "A":
                accepted.append(checked_part)
                return 0
            elif checked_instruction[i][0] == "R":
                rejected.append(checked_part)
                return 0
            else:
                iterate_over_instruction(checked_part, instructions, instructions[checked_instruction[-1]], accepted, rejected)
                return 0
        # Check if the condition was satisfied
        else:
            condition_satisfied = check_condition_satisfaction(checked_part, checked_instruction[i])
            # If condition is satisfied, skip to the next instruction or add to relevant basket
            if condition_satisfied == True:
                if checked_instruction[i][3] == "A":
                    accepted.append(checked_part)
                    return 0
                elif checked_instruction[i][3] == "R":
                    rejected.append(checked_part)
                    return 0
                else:
                    iterate_over_instruction(checked_part, instructions, instructions[checked_instruction[i][3]], accepted, rejected)
                    return 0
            # If condition is not satisfied, iterate over the remaining instructions

def check_condition_satisfaction(checked_part, checked_condition):
    if checked_condition[1] == ">":
        if checked_part[checked_condition[0]] > checked_condition[2]:
            return True
        else:
            return False
    elif checked_condition[1] == "<":
        if checked_part[checked_condition[0]] < checked_condition[2]:
            return True
        else:
            return False

def count_accepted_value(accepted):
    accepted_value = 0
    for elem in accepted:
        for key, value in elem.items():
            accepted_value += value
    return accepted_value

def part2(instructions):
    accepted_intervals = []
    rejected_intervals = []
    inital_intervals = {}
    inital_intervals["x"] = (1,4000)
    inital_intervals["m"] = (1,4000)
    inital_intervals["a"] = (1,4000)
    inital_intervals["s"] = (1,4000)
    iterate_over_instructions_p2(instructions, accepted_intervals, rejected_intervals, inital_intervals, instructions["in"])
    return calculate_passing_intervals_value(accepted_intervals)

def iterate_over_instructions_p2(instructions, accepted_intervals, rejected_intervals, checked_interval, checked_instruction):
    # iterate over individual items in the instruction
    for i in range(len(checked_instruction)):
        if i == len(checked_instruction) - 1:
            if checked_instruction[i][0] == "A":
                accepted_intervals.append(checked_interval)
                return 0
            elif checked_instruction[i][0] == "R":
                rejected_intervals.append(checked_interval)
                return 0
            else:
                iterate_over_instructions_p2(instructions, accepted_intervals, rejected_intervals, checked_interval, instructions[checked_instruction[-1]])
                return 0
        else:
            passing_interval, failing_interval = slice_intervals(checked_interval, checked_instruction[i])
            # If a part of the interval passes, check next interval
            if passing_interval != False:
                if checked_instruction[i][3] == "A":
                    accepted_intervals.append(passing_interval)
                elif checked_instruction[i][3] == "R":
                    rejected_intervals.append(passing_interval)
                else:
                    iterate_over_instructions_p2(instructions, accepted_intervals, rejected_intervals, passing_interval, instructions[checked_instruction[i][3]])
            # If a part of the interval passes, iterate further with this interval further
            if failing_interval != False:
                # The remaining iteration to take place over the limited interval, without the part which was sliced as passing
                checked_interval = failing_interval
            # If there was no failing, there is no need to iterate further and we can return
            if failing_interval == False:
                return 0

def slice_intervals(checked_interval, checked_condition):
    passing_interval = copy.deepcopy(checked_interval)
    failing_interval = copy.deepcopy(checked_interval)
    if checked_condition[1] == ">":
        # If the highest value in the checked interval is lower than the value from the condition, all fail
        if checked_interval[checked_condition[0]][1] < checked_condition[2]:
            return False, failing_interval
        # If the lower value in the checked interval is higher than the value from the condition, all pass
        elif checked_interval[checked_condition[0]][0] > checked_condition[2]:
            return passing_interval, False
        # If the slice is in the middle
        else:
            passing_segment = (checked_condition[2] + 1, checked_interval[checked_condition[0]][1])
            failing_segment = (checked_interval[checked_condition[0]][0], checked_condition[2])
            passing_interval[checked_condition[0]] = passing_segment
            failing_interval[checked_condition[0]] = failing_segment
            return passing_interval, failing_interval
    elif checked_condition[1] == "<":
        # If the highest value in the checked interval is lower than the value from the condition, all pass
        if checked_interval[checked_condition[0]][1] < checked_condition[2]:
            return passing_interval, False
        # If the lowest value in the checked interval is higher than the value from the condition, all fail
        elif checked_interval[checked_condition[0]][0] > checked_condition[2]:
            return False, failing_interval
        # If the slice is in the middle
        else:
            passing_segment = (checked_interval[checked_condition[0]][0], checked_condition[2] - 1)
            failing_segment = (checked_condition[2], checked_interval[checked_condition[0]][1])
            passing_interval[checked_condition[0]] = passing_segment
            failing_interval[checked_condition[0]] = failing_segment
            return passing_interval, failing_interval

def calculate_passing_intervals_value(accepted_intervals):
    total_sum = 0
    for elem in accepted_intervals:
        i = 1
        for key, value in elem.items():
            i *= (value[1] - value[0] + 1)
        total_sum += i
    return total_sum

if __name__ == "__main__":
    instructions, parts = get_input()
    print(part1(instructions, parts))
    print(part2(instructions))