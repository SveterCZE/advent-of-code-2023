def get_input():
    f = open("input.txt", "r")
    instructions = []
    for line in f:
        instructions.append(line.strip().split())
    return instructions

def part1(instructions):
    intervals = []
    rows_intervals = set()
    initial_coordinate = (0,0)
    identify_intervals(instructions, initial_coordinate, intervals, rows_intervals)
    intervals = sorted(intervals, key=lambda element: (element[0][1], element[1][1], element[0][0], element[1][0]))
    intervals_DB = create_intervals_DB(intervals)
    return calculate_total_area(intervals_DB, rows_intervals)

def identify_intervals(instructions, initial_coordinate, intervals, rows_intervals):
    for elem in instructions:
        initial_coordinate = add_interval(elem, initial_coordinate, intervals, rows_intervals)
    
def add_interval(checked_instruction, initial_coordinate, intervals, rows_intervals):
    if checked_instruction[0] == "U":
        next_coordinate = (initial_coordinate[0] - int(checked_instruction[1]), initial_coordinate[1])
        intervals.append((next_coordinate, initial_coordinate))
    elif checked_instruction[0] == "D":
        next_coordinate = (initial_coordinate[0] + int(checked_instruction[1]), initial_coordinate[1])
        intervals.append((initial_coordinate, next_coordinate))
    elif checked_instruction[0] == "L":
        next_coordinate = (initial_coordinate[0], initial_coordinate[1] - int(checked_instruction[1]))
        rows_intervals.add((next_coordinate, initial_coordinate))
    elif checked_instruction[0] == "R":
        next_coordinate = (initial_coordinate[0], initial_coordinate[1] + int(checked_instruction[1]))
        rows_intervals.add((initial_coordinate, next_coordinate))
    print(next_coordinate)
    return next_coordinate

def create_intervals_DB(intervals):
    intervals_DB = {}
    for i in range(len(intervals)):
        calculate_individual_interval_area(intervals[i], i, intervals, intervals_DB)
    # print()
    return intervals_DB
    
def calculate_individual_interval_area(checked_interval, position, intervals, intervals_DB):
    for row_no in range(checked_interval[0][0], checked_interval[1][0] + 1):
        if row_no not in intervals_DB:
            intervals_DB[row_no] = set()
        intervals_DB[row_no].add(checked_interval[0][1])
        start_coordinate = (row_no, checked_interval[0][1])
        for other_coordinate_no in range(position + 1, len(intervals)):
            if pair_interval_found(start_coordinate, intervals[other_coordinate_no]) == True:
                intervals_DB[row_no].add(intervals[other_coordinate_no][0][1])
    return 0

def pair_interval_found(checked_coordinate, checked_interval):
    if checked_coordinate[0] >= checked_interval[0][0] and checked_coordinate[0] <= checked_interval[1][0]:
        return True
    else:
        return False

def calculate_total_area(intervals_DB, rows_intervals):
    total_area = 0
    for key, value in intervals_DB.items():
        corrected_intervals = calculate_corrected_intervals(key, list(value), rows_intervals)
        # print("Initital:", corrected_intervals)
        merged_intervals = calculate_merged_intervals(corrected_intervals)
        # print("Merged:", merged_intervals)
        row_area = sum_merged_intervals(merged_intervals)
        # print(row_area)
        total_area += row_area
    return total_area

def calculate_corrected_intervals(current_row, interval_edges, rows_intervals):
    interval_edges.sort()
    pointer = 0
    corrected_intervals = []
    two_columns_encoutered = False
    while True:
        if pointer >= len(interval_edges) - 1:
            break
        potential_row_tuple = ((current_row, interval_edges[pointer]),(current_row, interval_edges[pointer+1]))
        if potential_row_tuple in rows_intervals:
            corrected_intervals.append((interval_edges[pointer], interval_edges[pointer+1]))
            pointer += 1
            two_columns_encoutered = False
        else:
            if two_columns_encoutered == True:
                pointer += 1
                two_columns_encoutered = False
            else:
                corrected_intervals.append((interval_edges[pointer], interval_edges[pointer+1]))
                pointer += 1
                two_columns_encoutered = True
    return corrected_intervals

def calculate_merged_intervals(corrected_intervals):
    if len(corrected_intervals) == 1:
        return corrected_intervals
    merged_intervals = []
    pointer_left = 0
    pointer_right = 1
    while True:
        # # Check if the left pointer points out of the list
        # if pointer_left + 1 >= len(corrected_intervals):
        #     return merged_intervals
        # Check if the left pointer points to the last item in the list. If so, it cannot be merged further
        if pointer_left == len(corrected_intervals) - 1:
            merged_intervals.append(corrected_intervals[pointer_left])
            return merged_intervals
        # Iterate over the remaining items in the list until a non-mergeable interval is found
        for i in range(pointer_right, len(corrected_intervals)):
            # If a pair in which the right pointer point to intervals whcih does not overlap with the previous one, break and move pointers accordingly
            if corrected_intervals[i - 1][1] != corrected_intervals[i][0]:
                # Insert a new interval
                merged_intervals.append((corrected_intervals[pointer_left][0], corrected_intervals[i - 1][1]))
                # Move pointers accordingly and break from the loop
                pointer_left = i
                pointer_right = i + 1
                break
            # Check in case the last item is reached
            if i == len(corrected_intervals) - 1:
                merged_intervals.append((corrected_intervals[pointer_left][0], corrected_intervals[i][1]))
                pointer_left = i
                pointer_right = i + 1
                return merged_intervals

def sum_merged_intervals(merged_intervals):
    row_sum = 0
    for elem in merged_intervals:
        row_sum += ((elem[1] - elem[0]) + 1)
    return row_sum
    

def part2(instructions):
    pass

if __name__ == "__main__":
    instructions = get_input()
    print(part1(instructions))
    # print(part2(instructions))