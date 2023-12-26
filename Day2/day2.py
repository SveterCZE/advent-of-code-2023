import re

def main():
    instructions = get_input()
    print(part1(instructions))
    print(part2(instructions))

def get_input():
    instructions = []
    f = open("input.txt", "r")
    for line in f:
        instructions.append(line.strip().split(": ")[1].split("; "))
    return instructions

def part1(instructions):
    sum_of_valid_game_IDs = 0
    rules = generate_rules()
    for i in range(len(instructions)):
        if is_valid_game(instructions[i], rules):
            sum_of_valid_game_IDs += (i + 1)
    return sum_of_valid_game_IDs

def part2(instructions):
    sum_of_game_IDs = 0
    for i in range(len(instructions)):
        sum_of_game_IDs += (determine_min_balls(instructions[i]))
    return sum_of_game_IDs

def determine_min_balls(checked_game):
    min_balls = {}
    min_balls["red"] = 0
    min_balls["green"] = 0
    min_balls["blue"] = 0
    for checked_draw in checked_game:
        determine_mins(checked_draw, min_balls)
    total = 1
    for key, value in min_balls.items():
        total *= value
    return total

def determine_mins(checked_draw, min_balls):
    numeric_values = re.findall(r'\d+', checked_draw)
    word_values = re.findall(r'[a-z]+', checked_draw)
    for i in range(len(numeric_values)):
        if min_balls[word_values[i]] < int(numeric_values[i]):
            min_balls[word_values[i]] = int(numeric_values[i])

def is_valid_game(checked_game, rules):
    for checked_draw in checked_game:
        if is_draw_valid(checked_draw, rules) == False:
            return False
    return True

def is_draw_valid(checked_draw, rules):
    draw_results = {}
    numeric_values = re.findall(r'\d+', checked_draw)
    word_values = re.findall(r'[a-z]+', checked_draw)
    for i in range(len(numeric_values)):
        if word_values[i] not in draw_results:
            draw_results[word_values[i]] = 0
        draw_results[word_values[i]] += int(numeric_values[i])
    for key, value in draw_results.items():
        if value > rules[key]:
            return False
    return True
    
def generate_rules():
    rules = {}
    rules["red"] = 12
    rules["green"] = 13
    rules["blue"] = 14
    return rules

main()