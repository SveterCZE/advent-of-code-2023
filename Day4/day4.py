import re

def main():
    instructions = get_input()
    print(part1(instructions))
    print(part2(instructions))

def get_input():
    instructions = []
    f = open("input.txt", "r")
    for line in f:
        temp_line = line.strip().split("|")
        card1 = re.findall(r'\d+', temp_line[0])[1:]
        card2 = re.findall(r'\d+', temp_line[1])
        instructions.append((card1, card2))
    return instructions

def part1(instructions):
    counter = 0
    for checked_cards in instructions:
        counter += count_card_value(checked_cards)
    return counter

def part2(instructions):
    card_db = {}
    for i in range(len(instructions)):
        card_db[i] = 1
    for j in range(len(instructions)):
        winning_numbers = count_winning_numbers(instructions[j])
        if winning_numbers > 0:
            for k in range(winning_numbers):
                card_db[j+k+1] = card_db[j+k+1] + card_db[j]
    counter = 0
    for key, value in card_db.items():
        counter += value
    return counter

def count_winning_numbers(checked_cards):
    counter = 0
    for card in checked_cards[1]:
        if card in checked_cards[0]:
            counter += 1
    return counter

def count_card_value(checked_cards):
    counter = 0
    for card in checked_cards[1]:
        if card in checked_cards[0]:
            counter += 1
    if counter <= 1:
        return counter
    else:
        return multiply_card_value(counter)

def multiply_card_value(counter):
    card_value = 1
    for i in range(counter - 1):
        card_value *= 2
    return card_value

main()