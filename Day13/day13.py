import copy

def get_input():
    f = open("input.txt", "r")
    instructions = []
    temp_instruction = []
    for line in f:
        temp_line = list(line.strip())
        if len(temp_line) == 0:
            instructions.append(temp_instruction)
            temp_instruction = 0
            temp_instruction = []
        else:
            temp_instruction.append(temp_line)
    instructions.append(temp_instruction)
    return instructions

def part1(instructions):
    sum = 0
    for elem in instructions:
        sum += check_pattern_for_reflections(elem)
    return sum

def check_pattern_for_reflections(pattern):
    row_db, column_db = create_pattern_dbs(pattern)
    return sum(find_reflection(row_db, 100)) + sum(find_reflection(column_db, 1))

def find_reflection(pattern_db, multiplier):
    reflections = set()
    for i in range(len(pattern_db) - 1):
        if pattern_db[i] == pattern_db[i+1]:
            reflection_found = True
            steps_to_be_checked = min(i, len(pattern_db) - (i + 2))
            for j in range(1, steps_to_be_checked + 1):
                if pattern_db[i-j] != pattern_db[i+j+1]:
                    reflection_found = False
            if reflection_found == True:
                reflections.add((i + 1) * multiplier) 
    return reflections

def create_pattern_dbs(pattern):
    row_db = {}
    column_db = {}
    for i in range(len(pattern)):
        row_db[i] = tuple(pattern[i]) 
    for i in range(len(pattern[0])):
        temp_column = []
        for j in range(len(pattern)):
            temp_column.append(pattern[j][i])
        column_db[i] = tuple(temp_column)
    return row_db, column_db

def part2(instructions):
    sum = 0
    for pattern in instructions:
        sum += find_smudges(pattern)
    return sum

def find_smudges(pattern):
    total = 0
    # initial_reflection = check_pattern_for_reflections(pattern)
    row_db, column_db = create_pattern_dbs(pattern)
    original_row_value = find_reflection(row_db, 100)
    original_column_value = find_reflection(column_db, 1)
    new_row_reflections_found = set()
    new_column_reflections_found = set()
    for i in range(len(pattern)):
        for j in range(len(pattern[0])):
            updated_pattern = copy.deepcopy(pattern)
            if updated_pattern[i][j] == "#":
                updated_pattern[i][j] = "."
            else:
                updated_pattern[i][j] = "#"
            # updated_reflections = check_pattern_for_reflections(updated_pattern)
            # sum += sum(updated_reflections - initial_reflection)
            row_db_updated, column_db_updated = create_pattern_dbs(updated_pattern)
            reflection_value_row = find_reflection(row_db_updated, 100)
            for elem in reflection_value_row:
                new_row_reflections_found.add(elem)
            reflection_value_column = find_reflection(column_db_updated, 1)
            for elem in reflection_value_column:
                new_column_reflections_found.add(elem)
            # if reflection_value_row != original_row_value and reflection_value_row not in new_reflections_found:
            #     sum += reflection_value_row
            #     new_reflections_found.add(reflection_value_row)

            # if reflection_value_column != original_column_value and reflection_value_column not in new_reflections_found:
            #     sum += reflection_value_column
            #     new_reflections_found.add(reflection_value_column)
    # if sum == 0:
    #     print(pattern)
    return sum(new_row_reflections_found - original_row_value) + sum(new_column_reflections_found - original_column_value)

if __name__ == "__main__":
    instructions = get_input()
    print(part1(instructions))
    print(part2(instructions))