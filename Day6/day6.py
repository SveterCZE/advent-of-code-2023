import re

def get_input():
    instructions = []
    f = open("input.txt", "r")
    for line in f:
        instructions.append([int(x) for x in re.findall(r'\d+', line)])
    games_db = []
    for i in range(len(instructions[0])):
        games_db.append((instructions[0][i], instructions[1][i]))
    return games_db


def part1(instructions):
    total_score = 1
    for checked_race in instructions:
        total_score *= calculate_best_race_result(checked_race)
    return total_score

def part2(instructions):
    sum_time = ""
    sum_distance = ""
    for i in range(len(instructions)):
        sum_time += str(instructions[i][0])
        sum_distance += str(instructions[i][1])
    return calculate_best_race_result((int(sum_time), int(sum_distance)))

def calculate_best_race_result(checked_race):
    better_result = 0
    for i in range(1, checked_race[0]):
        score = (checked_race[0] - i) * i
        if score > checked_race[1]:
            better_result += 1
    return better_result

if __name__ == "__main__":
    instructions = get_input()
    print(part1(instructions))
    print(part2(instructions))