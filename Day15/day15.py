import re

def get_input():
    f = open("input.txt", "r")
    for line in f:
        return line.strip().split(",")

def part1(instructions):
    sum_of_hashes = 0
    for elem in instructions:
        sum_of_hashes += calculate_hash(list(elem))
    return sum_of_hashes

def calculate_hash(checked_input):
    curr_value = 0
    for elem in checked_input:
        curr_value += ord(elem)
        curr_value *= 17
        curr_value = (curr_value%256)
    return(curr_value)

def part2(instructions):
    lens_db = []
    for i in range(256):
        lens_db.append([])
    for elem in instructions:
        split_list = re.split('-|=', elem)
        if "=" in elem:
            do_insertion(lens_db[calculate_hash(split_list[0])], split_list[0], split_list[1])
        else:
            do_deletion(lens_db[calculate_hash(split_list[0])], split_list[0])
    return(calculate_power(lens_db))

def calculate_power(lens_db):
    total_power = 0
    for i in range(len(lens_db)):
        box_no = i + 1
        for j in range(len(lens_db[i])):
            total_power += (box_no * (j + 1) * int(lens_db[i][j][1]))
    return total_power

def is_label_in_box(box, label):
    for i in range(len(box)):
        if box[i][0] == label:
            return [True, i]
    return [False, 0]

def do_insertion(box, label, focal_length):
    search_box = is_label_in_box(box, label)
    if search_box[0] == True:
        box[search_box[1]] = [label, focal_length]
    else:
        box.append([label, focal_length])

def do_deletion(box, label):
    search_box = is_label_in_box(box, label)
    if search_box[0] == True:
        box.pop(search_box[1])

if __name__ == "__main__":
    instructions = get_input()
    print(part1(instructions))
    print(part2(instructions))